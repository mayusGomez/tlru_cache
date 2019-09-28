"""
This implimentations is a wrap of Python heapq, for the moment is the selected structure 
for admin the cache priority
This is a detail
"""

import heapq
import logging

REMOVED = '<removed-task>'

# Node are not deleted from memory, only marked. This Count the deleted nodes, to substract from len(cache_node)
_nodes_deleted = 0  


def initial_structure():
    """
    Empty initial structure
    """ 
    return []


def set_priority(list_=None):
    """
    Inplace,  set the priority structure from a list
    """
    heapq.heapify(list_)


def append_data(priority_structure=None, node=None):
    """
    Add a node to the heapq
    """
    try:
        heapq.heappush(priority_structure, node)
    except Exception:
        logging.error('Error when try to insert node to prior structure')


def get_len(priority_structure=None):
    """
    Return the priority_structure's length 
    """
    try:
        return len(priority_structure)
    except Exception:
        logging.error('Error, when try to return priority_structure length')
        return 0


def get_structure_len(priority_structure):
    """
    Return the true cache's length
    """
    global _nodes_deleted

    return cache_nodes.get_len(priority_structure) - _nodes_deleted


def remove_node(priority_structure, node):
    """
    Mark the node as '<removed-task>'
    """
    global _nodes_deleted
    _nodes_deleted += 1
    node.key = REMOVED


def pop_node(priority_structure):
    """
    Remove the first element in heap
    """
    return heapq.heappop(priority_structure)


def push_node(priority_structure, node):
    """
    Add a node to the structure
    """
    heapq.heappush(priority_structure, node)

def get_n_largest(n , iterable, key=None):
    """
    heapq nlargest
    """
    return heapq.nlargest(n, iterable, key)
