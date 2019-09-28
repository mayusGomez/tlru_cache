import asyncio
import json
import logging
import websockets
from datetime import datetime

from trlu_cache_server.serializers.cache_serialize import CacheRespToClientJsonEncoder
from trlu_cache_server.use_cases.tlru_interact_master import TLRU_MasterInteraction 
from trlu_cache_server.serializers import cache_serialize
from trlu_cache_server.repository import file_repo

_app_settings = None


slaves = {}


async def register(websocket):
    """
    Register slave websocket to a dictionary, for broadcast when receive data from clients
    """
    logging.info("Slave registered")
    slaves[websocket] = None

async def unregister(websocket):
    """
    Remove slave from dict when the slave disconected
    """
    try:
        del slaves[websocket] 
    except Exception:
        logging.info("Slave unregistered")


async def clients_server(websocket, path):
    logging.info("Server for clients started")
    server_tlru_interact = TLRU_MasterInteraction(file_repo)
    try:
        async for message in websocket:
            logging.debug(f"Message received: {message}")
            message = json.loads(message, cls=cache_serialize.CacheJsonDecoder)
            logging.debug(f"Message json.loads: {message}")

            date_now = datetime.now()

            if message['type'] == 'set_node':
                node = await server_tlru_interact.set_node_from_client(message['data'], date_now, slaves)
                resp = {
                    'type': 'confirm_set_node',
                    'result': True,
                    'data': {
                        'key': node.key,
                        'value': node.value,
                        'date_stamp': node.date_stamp,
                        'due_date': node.due_date,
                        'state': node.state
                    }
                }
                await websocket.send( json.dumps( resp ))
            
            if message['type'] == 'get_node':
                node = await server_tlru_interact.get_node_from_client(message['data'], date_now, slaves)
                if node:
                    resp = {
                        'type': 'confirm_get_node',
                        'result': True,
                        'data': {
                            'key': node.key,
                            'value': node.value,
                            'date_stamp': node.date_stamp,
                            'due_date': node.due_date,
                            'state': node.state
                        }
                    }
                    await websocket.send( json.dumps( resp  ))
                else:
                    resp = {
                        'type': 'confirm_get_node',
                        'result': False
                    }
                    await websocket.send( json.dumps( resp  ))

            else:
                resp = {
                    'type': 'unsuported',
                    'result': False
                }
                await websocket.send( json.dumps( resp ))

    finally:
        logging.debug(f"Client unregister")


async def slaves_server(websocket, path):
    await register(websocket)
    server_tlru_interact = TLRU_MasterInteraction(file_repo)
        try:
            async for message in websocket:
                message = json.loads(message)
                if message['type'] == 'get_slice_state':
                    resp = await server_tlru_interact.get_slice_state(message['data'])
                    await websocket.send( json.dumps( resp ))
                    
                elif message['type'] == 'set_state_slave':
                    resp = await server_tlru_interact.get_slice_state(message['data'])
                    await websocket.send( json.dumps( resp ))

                elif message['type'] == 'set_node':
                    resp = await server_tlru_interact.set_node_from_slave(message['data'], date_now, slaves)
                    await websocket.send( json.dumps( resp ))

                elif message['type'] == 'get_node':
                    resp = await server_tlru_interact.get_node_from_slave(message['data'], date_now, slaves)
                    await websocket.send( json.dumps( resp ))

                else:
                    await websocket.send("unsupported event:")
                    logging.error("unsupported event:")
    finally:
        await unregister(websocket)


def execute(settings):
    global _app_settings
    _app_settings = settings

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(clients_server, _app_settings['SERVER']['address'] , 
        _app_settings['SERVER']['port_to_clients'])
    )

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(slaves_server, _app_settings['SERVER']['address'] , 
        _app_settings['SERVER']['port_to_slaves'])
    )

    asyncio.get_event_loop().run_forever()
