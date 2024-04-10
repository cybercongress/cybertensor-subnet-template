# Writing your own subnet API
To leverage the abstract `SubnetsAPI` in cybertensor, you can implement a standardized interface. This interface is used 
to interact with the cybertensor network and can is used by a client to interact with the subnet through its exposed axons.

What does cybertensor communication entail? Typically, two processes, (1) preparing data for transit (creating and 
filling `synapse`s) and (2), processing the responses received from the `axon`(s).

This protocol uses a handler registry system to associate bespoke interfaces for subnets by implementing two simple 
abstract functions:
- `prepare_synapse`
- `process_responses`

These can be implemented as extensions of the generic `SubnetsAPI` interface.  E.g.:


This is abstract, generic, and takes(`*args`, `**kwargs`) for flexibility. See the extremely simple base class:
```python
import cybertensor as ct


class SubnetsAPI(ABC):
    def __init__(self, wallet: "ct.Wallet"):
        self.wallet = wallet
        self.dendrite = ct.dendrite(wallet=wallet)

    async def __call__(self, *args, **kwargs):
        return await self.query_api(*args, **kwargs)

    @abstractmethod
    def prepare_synapse(self, *args, **kwargs) -> Any:
        """
        Prepare the synapse-specific payload.
        """
        ...

    @abstractmethod
    def process_responses(self, responses: List[Union["ct.Synapse", Any]]) -> Any:
        """
        Process the responses from the network.
        """
        ...

```


Here is a toy example:

```python
from cybertensor.subnets import SubnetsAPI
from MySubnet import MySynapse

class MySynapseAPI(SubnetsAPI):
    def __init__(self, wallet: "ct.Wallet"):
        super().__init__(wallet)
        self.netuid = 99

    def prepare_synapse(self, prompt: str) -> MySynapse:
        # Do any preparatory work to fill the synapse
        data = do_prompt_injection(prompt)

        # Fill the synapse for transit
        synapse = StoreUser(
            messages=[data],
        )
        # Send it along
        return synapse

    def process_responses(self, responses: List[Union["ct.Synapse", Any]]) -> str:
        # Look through the responses for information required by your application
        for response in responses:
            if response.dendrite.status_code != 200:
                continue
            # potentially apply post processing
            result_data = postprocess_data_from_response(response)
        # return data to the client
        return result_data
```

You can use a subnet API to the registry by doing the following:
1. Download and install the specific repo you want
2. Import the appropriate API handler from bespoke subnets
3. Make the query given the subnet specific API


See a simplified example for subnet 21 (`FileTao` storage) below. See `examples/subnet21.py` file for a full 
implementation example to follow:

```python
# Subnet 21 Interface Example

class StoreUserAPI(SubnetsAPI):
    def __init__(self, wallet: "ct.Wallet"):
        super().__init__(wallet)
        self.netuid = 21

    def prepare_synapse(
        self,
        data: bytes,
        encrypt=False,
        ttl=60 * 60 * 24 * 30,
        encoding="utf-8",
    ) -> StoreUser:
        data = bytes(data, encoding) if isinstance(data, str) else data
        encrypted_data, encryption_payload = (
            encrypt_data(data, self.wallet) if encrypt else (data, "{}")
        )
        expected_cid = generate_cid_string(encrypted_data)
        encoded_data = base64.b64encode(encrypted_data)

        synapse = StoreUser(
            encrypted_data=encoded_data,
            encryption_payload=encryption_payload,
            ttl=ttl,
        )

        return synapse

    def process_responses(
        self, responses: List[Union["ct.Synapse", Any]]
    ) -> str:
        for response in responses:
            if response.dendrite.status_code != 200:
                continue
            stored_cid = (
                response.data_hash.decode("utf-8")
                if isinstance(response.data_hash, bytes)
                else response.data_hash
            )
            ct.logging.debug("received data CID: {}".format(stored_cid))
            break

        return stored_cid


class RetrieveUserAPI(SubnetsAPI):
    def __init__(self, wallet: "ct.Wallet"):
        super().__init__(wallet)
        self.netuid = 21

    def prepare_synapse(self, cid: str) -> RetrieveUser:
        synapse = RetrieveUser(data_hash=cid)
        return synapse

    def process_responses(self, responses: List[Union["ct.Synapse", Any]]) -> bytes:
        success = False
        decrypted_data = b""
        for response in responses:
            if response.dendrite.status_code != 200:
                continue
            decrypted_data = decrypt_data_with_private_key(
                encrypted_data,
                response.encryption_payload,
                bytes(self.wallet.coldkey.private_key.hex(), "utf-8"),
            )
        return data
```

Example usage of the `FileTao` interface, which can serve as an example for other subnets.

```python
# import the bespoke subnet API
from storage import StoreUserAPI, RetrieveUserAPI

wallet = ct.Wallet(wallet="default", hotkey="default") # the wallet used for querying
metagraph = ct.metagraph(netuid=21)  # metagraph of the subnet desired
query_axons = metagraph.axons... # define custom logic to retrieve desired axons (e.g. validator set, specific miners, etc)

# Store the data on subnet 21
ct.logging.info(f"Initiating store_handler: {store_handler}")
cid = await StoreUserAPI(
      axons=query_axons, # the axons you wish to query
      # Below: Parameters passed to `prepare_synapse` for this API subclass
      data=b"Hello cybertensor!",
      encrypt=False,
      ttl=60 * 60 * 24 * 30, 
      encoding="utf-8",
      uid=None,
)
# The Content Identifier that corresponds to the stored data
print(cid)
> "bafkreifv6hp4o6bllj2nkdtzbq6uh7iia6bgqgd3aallvfhagym2s757v4"

# Now retrieve data from SN21 (storage)
data = await RetrieveUserAPI(
  axons=query_axons, # axons desired to query
  cid=cid, # the content identifier to fetch the data
)
print(data)
> b"Hello cybertensor!"
```