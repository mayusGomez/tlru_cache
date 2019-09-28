import asyncio
import json
import logging
import websockets
from datetime import datetime

from trlu_cache_server.serializers.cache_serialize import CacheRespToClientJsonEncoder
from trlu_cache_server.use_cases.tlru_interact_slave import TLRU_SlaveInteraction
from trlu_cache_server.serializers import cache_serialize
from trlu_cache_server.repository import file_repo

_app_settings = None

master_socker = None

async def clients_server(websocket, path):
    """
    Accept request from clients, and send the data to Master
    """
    try:
        slave_tlru_interact = TLRU_SlaveInteraction(file_repo)
        async for message in websocket:
            message = json.loads(message)
            if message['type'] == 'set_node':
                node = await slave_tlru_interact.set_node_from_client(message['data'], date_now, slaves)
                await websocket.send( json.dumps( resp ))

            if message['type'] == 'get_node':
                node = await slave_tlru_interact.get_node_from_client(message['data'], date_now, slaves)

            else:
                await websocket.send("unsupported event:")
                logging.error("unsupported event:")
    finally:
        print('unregister')


async def socket_to_master(settings):
    """
    Open connection with master, to receive updated and states
    """
    global _app_settings
    _app_settings = settings
    async with websockets.connect(
            'ws://{}:{}'.format(clients_server, _app_settings['SERVER']['address'], _app_settings['SERVER']['port_to_clients'])) as websocket:
        while True:
            msg_master = await websocket.recv()

