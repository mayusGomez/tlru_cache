"""
Cache in memory, fast access but not recovery data
"""

from ..model.tlru_cache import TLRU_Cache


def init():
    """ 
    Initialize the cache.
    """
    _load_cache()


def _load_cache():
    """
    load into memory the cache
    """
    # TODO: Load from file, recovery
    global _cache

    _cache = TLRU_Cache()
    

def get_tlru_cache():
    global _cache
    return  _cache


def save_tlru_cache():
    pass
