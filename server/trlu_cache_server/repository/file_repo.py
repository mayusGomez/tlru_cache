"""
Cache in file, slow access but recovery data
Only for small data
"""
import logging
from collections import deque
import itertools
import pickle

from ..model.node import Node
from ..model.tlru_cache import TLRU_Cache
from ..data_structures import cache_nodes  # Intialli is a heap, this is a wrap to change if it's necessary

file_name = 'cache_data.pickle'

# State of cache, start at 0, and increment by 1
counter = None


def init_master():
    """ 
    Initialize the cache.
    try to load from disk
    """
    global nodes_deleted

    nodes_deleted = 0 
    _load_cache_from_disk()
    _conf_master_server_cache()


def init_slave():
    """ 
    Initialize the cache.
    try to load from disk
    """
    _load_cache_from_disk()
    _conf_slave_server_cache()


def _load_cache_from_disk():
    """
    Load from file to cache
    """
    global _cache

    _cache = TLRU_Cache(server_status=False)

    try:
        with open(file_name, "rb") as file_in:
            _cache.setters = pickle.load(file_in)
            logging.debug(f"Cache Pickle , len _cache,{ len(_cache.setters)}" )

    except Exception:
        logging.error(f'Not file to load data')
        _cache.setters = {}
    

def get_tlru_cache():
    """
    Return cache loaded
    """
    global _cache

    return  _cache


def save_tlru_cache():
    """
    Save to a file the data
    """
    global _cache

    try:
        with open(file_name, "wb") as file_out:
            logging.debug(f"Save cache to file, len:{ len(_cache.setters)}")
            pickle.dump(_cache.setters, file_out, protocol=-1)
    except Exception as e:
        logging.error(f"Cache didn't save to file {e}")


def _conf_master_server_cache():
    """
    Load data structures for master server:
    - priority_structure: Python heapq for priority, only the server manage this structure
    - data_state (double link list) to sync data with other servers
    """
    global _cache
    global counter

    # Not load removed nodes
    initial_list_structure = [node for k, node in _cache.setters.items()]
    _cache.data_state = deque()

    if len(initial_list_structure):
        cache_nodes.set_priority(initial_list_structure)
        _cache.priority_structure = initial_list_structure
        _cache.data_state.append(_cache.priority_structure[0])
        counter = itertools.count( cache_nodes.get_n_largest(1, _cache.priority_structure)[0].state + 1)
    else:
        _cache.priority_structure = cache_nodes.initial_structure()
        counter = itertools.count()


def _conf_slave_server_cache():
    """
    Load data structures for slave server:
    - data_state (double link list) to sync data with other servers
    """
    global _cache
    global counter

    initial_list_structure = [node for node in _cache.setters.items()]
    _cache.data_state = deque()

    if len(initial_list_structure):
        cache_nodes.set_priority(initial_list_structure)
        _cache.data_state.append(initial_list_structure[0])
        counter = itertools.count(initial_list_structure[0].state + 1)
    else:
        counter = itertools.count()

def get_next_state():
    """
    Return the next state
    """
    global counter

    if counter:
        logging.debug(f"Counter assigned before")
        return next(counter) 
    else:
        counter = itertools.count()
        logging.debug(f"Counter not assigned before")
        return next(counter)
