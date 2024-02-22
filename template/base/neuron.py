# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2024 cyber~Congress

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import copy
import typing

import cybertensor as ct

from abc import ABC, abstractmethod

# Sync calls set weights and also resyncs the metagraph.
from template.utils.config import check_config, add_args, config
from template.utils.misc import ttl_get_block
from template import __spec_version__ as spec_version
from template.mock import MockSubtensor, MockMetagraph
# from cybertensor.mock.wallet_mock import MockWallet


class BaseNeuron(ABC):
    """
    Base class for cybertensor miners. This class is abstract and should be inherited by a subclass. It contains
    the core logic for all neurons; validators and miners.

    In addition to creating a wallet, cwtensor, and metagraph, this class also handles the synchronization
    of the network state via a basic checkpointing mechanism based on epoch length.
    """

    @classmethod
    def check_config(cls, config: "ct.Config"):
        check_config(cls, config)

    @classmethod
    def add_args(cls, parser):
        add_args(cls, parser)

    @classmethod
    def config(cls):
        return config(cls)

    cwtensor: "ct.cwtensor"
    wallet: "ct.Wallet"
    metagraph: "ct.metagraph"
    spec_version: int = spec_version

    @property
    def block(self):
        return ttl_get_block(self)

    def __init__(self, config=None):
        base_config = copy.deepcopy(config or BaseNeuron.config())
        self.config = self.config()
        self.config.merge(base_config)
        self.check_config(self.config)

        # Set up logging with the provided configuration and directory.
        ct.logging(config=self.config, logging_dir=self.config.full_path, trace=True, debug=True)

        # If a gpu is required, set the device to cuda:N (e.g. cuda:0)
        self.device = self.config.neuron.device

        # Log the configuration for reference.
        ct.logging.info(self.config)

        # Build cybertensor objects
        # These are core cybertensor classes to interact with the network.
        ct.logging.info("Setting up cybertensor objects.")

        # The wallet holds the cryptographic key pairs for the miner.
        if self.config.mock:
            self.wallet = ct.MockWallet(config=self.config)
            self.cwtensor = MockSubtensor(
                self.config.netuid, wallet=self.wallet
            )
            self.metagraph = MockMetagraph(
                self.config.netuid, subtensor=self.cwtensor
            )
        else:
            self.wallet = ct.Wallet(config=self.config)
            self.cwtensor = ct.cwtensor(config=self.config)
            self.metagraph = self.cwtensor.metagraph(self.config.netuid)

        ct.logging.info(f"Wallet: {self.wallet}")
        ct.logging.info(f"Cwtensor: {self.cwtensor}")
        ct.logging.info(f"Metagraph: {self.metagraph}")

        # Check if the miner is registered on the cybertensor network before proceeding further.
        self.check_registered()

        # Each miner gets a unique identity (UID) in the network for differentiation.
        self.uid = self.metagraph.hotkeys.index(
            self.wallet.hotkey.address
        )
        ct.logging.info(
            f"Running neuron on subnet: {self.config.netuid} with uid {self.uid} using network: {self.cwtensor.network}"
        )
        self.step = 0

    @abstractmethod
    async def forward(self, synapse: ct.Synapse) -> ct.Synapse: ...

    @abstractmethod
    def run(self): ...

    def sync(self):
        """
        Wrapper for synchronizing the state of the network for the given miner or validator.
        """
        # Ensure miner or validator hotkey is still registered on the network.
        self.check_registered()

        if self.should_sync_metagraph():
            self.resync_metagraph()

        if self.should_set_weights():
            self.set_weights()

        # Always save state.
        self.save_state()

    def check_registered(self):
        # --- Check for registration.
        if not self.cwtensor.is_hotkey_registered(
            netuid=self.config.netuid,
            hotkey=self.wallet.hotkey.address,
        ):
            ct.logging.error(
                f"Wallet: {self.wallet} is not registered on netuid {self.config.netuid}."
                f" Please register the hotkey using `btcli subnets register` before trying again"
            )
            exit()

    def should_sync_metagraph(self):
        """
        Check if enough epoch blocks have elapsed since the last checkpoint to sync.
        """
        return (
            self.block - self.metagraph.last_update[self.uid]
        ) > self.config.neuron.epoch_length

    def should_set_weights(self) -> bool:
        # Don't set weights on initialization.
        if self.step == 0:
            return False

        # Check if enough epoch blocks have elapsed since the last epoch.
        if self.config.neuron.disable_set_weights:
            return False

        # Define appropriate logic for when set weights.
        return (
            self.block - self.metagraph.last_update[self.uid]
        ) > self.config.neuron.epoch_length

    def save_state(self):
        ct.logging.warning(
            "save_state() not implemented for this neuron. You can implement this function to save model checkpoints "
            "or other useful data."
        )

    def load_state(self):
        ct.logging.warning(
            "load_state() not implemented for this neuron. You can implement this function to load model checkpoints "
            "or other useful data."
        )
