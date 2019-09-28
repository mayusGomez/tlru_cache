from collections import deque
import pytest
from datetime import datetime, timedelta
import logging


from ...trlu_cache_server.data_structures.cache_nodes import REMOVED
from ...trlu_cache_server.repository import file_repo
from ...trlu_cache_server.data_structures import cache_nodes

from ...trlu_cache_server.model.tlru_cache import TLRU_Cache
from ...trlu_cache_server.model.node import Node

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture
def load_cache():
    tlru_ = TLRU_Cache(
        setters=None,
        priority_structure=[],
        server_status = False,
        data_state = deque()
    )

    node_01 = Node(
        key='a', 
        date_stamp=datetime.now(), 
        due_date=datetime(2019,1,1,0,30,0,1000), 
        due_date_stamp=datetime.timestamp(datetime(2019,1,1,0,30,0,1000)) , 
        value=234, 
        state=1
    )

    node_02 = Node(
        key='b', 
        date_stamp=datetime.now(), 
        due_date=datetime(2019,1,1,0,35,0,1000), 
        due_date_stamp=datetime.timestamp(datetime(2019,1,1,0,35,0,1000)) , 
        value=233, 
        state=2
    )

    node_03 = Node(
        key='c', 
        date_stamp=datetime.now(), 
        due_date=datetime(2019,1,1,0,40,0,1000), 
        due_date_stamp=datetime.timestamp(datetime(2019,1,1,0,40,0,1000)) , 
        value=890, 
        state=3
    )

    node_04 = Node(
        key='d', 
        date_stamp=datetime.now(), 
        due_date=datetime(2019,1,1,0,45,0,1000), 
        due_date_stamp=datetime.timestamp(datetime(2019,1,1,0,45,0,1000)) , 
        value=429, 
        state=4
    )

    node_05 = Node(
        key='e', 
        date_stamp=datetime.now(), 
        due_date=datetime(2019,1,1,0,50,0,1000), 
        due_date_stamp=datetime.timestamp(datetime(2019,1,1,0,50,0,1000)) , 
        value=870, 
        state=5
    )

    tlru_.setters = {
        'a': node_01,
        'b': node_02,
        'c': node_03,
        'd': node_04,
        'e': node_05
    }

    node_list = [node_01, node_02, node_03, node_04, node_05]
    tlru_.priority_structure = node_list
    tlru_.data_state = deque(node_list)

    return tlru_

"""
def test_init_master_without_data():

    tlru_ = TLRU_Cache(
        setters=None,
        priority_structure=[],
        server_status = False,
        data_state = deque()
    )

    file_repo.init_master()
    cache = file_repo.get_tlru_cache()

    assert cache.data_state == tlru_.data_state
    assert cache.priority_structure == tlru_.priority_structure
    assert cache.server_status == tlru_.server_status
    assert cache.data_state == tlru_.data_state


def test_init_slave_without_data():
    tlru_ = TLRU_Cache(
        setters=None,
        priority_structure=None,
        server_status = False,
        data_state = deque()
    )

    file_repo.init_slave()
    cache = file_repo.get_tlru_cache()

    assert cache.data_state == tlru_.data_state
    assert cache.priority_structure == tlru_.priority_structure
    assert cache.server_status == tlru_.server_status
    assert cache.data_state == tlru_.data_state
"""

def test_save_data_to_file_and_load(load_cache):
    file_repo.init_master()
    cache = file_repo.get_tlru_cache()

    cache.setters = load_cache.setters
    logging.debug(f"build cache, the len is: { len(cache.setters)}")

    # Save to file
    file_repo.save_tlru_cache()
    # Clean _cache
    _cache = TLRU_Cache(server_status=False)

    # load from file and process
    file_repo.init_master()
    cache = file_repo.get_tlru_cache()

    for k, v in cache.setters.items():
        assert cache.setters[k].value == load_cache.setters[k].value
    # assert cache.priority_structure == load_cache.priority_structure

    logging.debug(f"priority_structure len: { len(cache.priority_structure)}")

    """while cache.priority_structure:
        logging.debug(f"order is { cache_nodes.pop_node(cache.priority_structure) }")"""

    assert file_repo.get_next_state() == 6
