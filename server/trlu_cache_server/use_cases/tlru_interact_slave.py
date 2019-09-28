import logging
from datetime import datetime, timedelta
import asyncio

from trlu_cache_server.model.node import Node
from trlu_cache_server.data_structures import cache_nodes
from .constants import DAYS_TO_ADD_NODE_WITHOUT_DUE_DATE, NODES_LIMIT_CUANTITY


class TLRU_SlaveInteraction:

    def __init__(self, data):
        self.data = data

    async def send_opetarion_to_master():
        """
        Send to master the set and get operations
        Master is in charge to set the time_stamp and due date, and return to all slaves the new state
        """
        pass

    async def set_node_from_client():
        """
        receive SET request from client and send info to master to the new state
        """
        pass

    async def get_node_from_client():
        """
        Receive GET request from client and inform to master for the new state
        """
        pass

    