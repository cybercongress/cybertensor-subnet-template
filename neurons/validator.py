# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2024 cyber~Congress
# TODO(developer): Set your name
# Copyright © 2024 <your name>

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


import time
from typing import Optional

import cybertensor as ct

from template.base.validator import BaseValidatorNeuron
from template.validator import forward


class Validator(BaseValidatorNeuron):
    """
    Your validator neuron class. You should use this class to define your validator's behavior. In particular, you
    should replace the forward function with your own logic.

    This class inherits from the BaseValidatorNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class
    takes care of routine tasks such as setting up wallet, cwtensor, metagraph, logging directory, parsing config, etc.
    You can override any of the methods in BaseNeuron if you need to customize the behavior.

    This class provides reasonable default behavior for a validator such as keeping a moving average of the scores of
    the miners and using them to set weights at the end of each epoch. Additionally, the scores are reset for new
    hotkeys at the end of each epoch.
    """

    def __init__(self, config: Optional[ct.Config] = None):
        super(Validator, self).__init__(config=config)

        # TODO(developer): Anything specific to your use case you can do here

    async def forward(self):
        """
        Validator forward pass. Consists of:
        - Generating the query
        - Querying the miners
        - Getting the responses
        - Rewarding the miners
        - Updating the scores
        """
        # TODO(developer): Rewrite this function based on your protocol definition.
        return await forward(self)


# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            validator.metagraph.sync(cwtensor=validator.cwtensor)
            ct.logging.info(
                f"Validator {'is up and running' if validator.thread and validator.thread.is_alive() else 'is running and not working'}\t"
                f"step {validator.step if validator.step else '-'}\t"
                f"block {validator.block if validator.block else None:>,}\t\t"
                f"blocks until sync {validator.config.neuron.epoch_length - validator.block + validator.metagraph.last_update[validator.uid]}"
            )
            if validator.thread is None or not validator.thread.is_alive():
                ct.logging.debug("Stopped")
                validator.is_running = False
                time.sleep(60)
                validator.run_in_background_thread()

            time.sleep(15)
