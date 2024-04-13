# The MIT License (MIT)
# Copyright © 2021 Yuma Rao
# Copyright © 2023 Opentensor Foundation
# Copyright © 2023 Opentensor Technologies Inc
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

import torch
import random
from typing import List, Optional, Union, Iterable
import cybertensor as ct


async def ping_uids(
        dendrite: ct.dendrite,
        metagraph: ct.metagraph,
        uids: Iterable[int],
        timeout: Optional[int] = 3
) -> [List[int], List[int]]:
    """
    Pings a list of UIDs to check their availability on the cybertensor network.
    Args:
        dendrite (cybertensor.dendrite): The dendrite instance to use for pinging nodes.
        metagraph (cybertensor.metagraph): The metagraph instance containing network information.
        uids (list[int]): A list of UIDs (unique identifiers) to ping.
        timeout (int, optional): The timeout in seconds for each ping. Defaults to 3.
    Returns:
        tuple: A tuple containing two lists:
            - The first list contains UIDs that were successfully pinged.
            - The second list contains UIDs that failed to respond.
    """
    axons = [metagraph.axons[uid] for uid in uids]
    try:
        responses = await dendrite(
            axons,
            ct.Synapse(),  # TODO: potentially get the synapses available back?
            deserialize=False,
            timeout=timeout,
        )
        successful_uids = [
            uid
            for uid, response in zip(uids, responses)
            if response.dendrite.status_code == 200
        ]
        failed_uids = [
            uid
            for uid, response in zip(uids, responses)
            if response.dendrite.status_code != 200
        ]
    except Exception as e:
        ct.logging.error(f"Dendrite ping failed: {e}")
        successful_uids = []
        failed_uids = uids
    ct.logging.debug("ping() successful uids:", successful_uids)
    ct.logging.debug("ping() failed uids    :", failed_uids)
    return successful_uids, failed_uids


async def get_query_api_nodes(
        dendrite: ct.dendrite,
        metagraph: ct.metagraph,
        n: Optional[float] = 0.1,
        timeout: Optional[int] = 3
) -> List[int]:
    """
    Fetches the available API nodes to query for the particular subnet.
    Args:
        dendrite (cybertensor.dendrite): the dendrite
        metagraph (cybertensor.metagraph): The metagraph instance containing network information.
        n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
        timeout (int, optional): The timeout in seconds for pinging nodes. Defaults to 3.
    Returns:
        list: A list of UIDs representing the available API nodes.
    """
    ct.logging.debug(
        f"Fetching available API nodes for subnet {metagraph.netuid}"
    )
    vtrust_uids = [
        uid.item()
        for uid in metagraph.uids
        if metagraph.validator_trust[uid] > 0
    ]
    top_uids = torch.where(metagraph.S > torch.quantile(metagraph.S, 1 - n))
    top_uids = top_uids[0].tolist()
    init_query_uids = set(top_uids).intersection(set(vtrust_uids))
    query_uids, _ = await ping_uids(
        dendrite=dendrite, metagraph=metagraph, uids=init_query_uids, timeout=timeout
    )
    ct.logging.debug(
        f"Available API node UIDs for subnet {metagraph.netuid}: {query_uids}"
    )
    if len(query_uids) > 3:
        query_uids = random.sample(query_uids, 3)
    return query_uids


async def get_query_api_axons(
        wallet: ct.Wallet,
        metagraph: Optional[ct.metagraph] = None,
        netuid: int = 1,
        n: float = 0.1,
        timeout: int = 3,
        uids: Optional[Union[List[int], int]] = None
) -> List[ct.AxonInfo]:
    """
    Retrieves the axons of query API nodes based on their availability and stake.
    Args:
        wallet (cybertensor.Wallet): The wallet instance to use for querying nodes.
        metagraph (cybertensor.metagraph, optional): The metagraph instance containing network information.
        netuid (int, optional): The network ID to get the nodes APIs. Defaults to 1.
        n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
        timeout (int, optional): The timeout in seconds for pinging nodes. Defaults to 3.
        uids (Union[List[int], int], optional): The specific UID(s) of the API node(s) to query. Defaults to None.
    Returns:
        list: A list of axon objects for the available API nodes.
    """
    dendrite = ct.dendrite(wallet=wallet)

    if metagraph is None:
        metagraph = ct.metagraph(netuid=netuid, network="space-pussy")

    if uids is not None:
        query_uids = [uids] if isinstance(uids, int) else uids
    else:
        query_uids = await get_query_api_nodes(
            dendrite, metagraph, n=n, timeout=timeout
        )
    return [metagraph.axons[uid] for uid in query_uids]
