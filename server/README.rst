==============================================================
Problem definition: Time aware least recently used Cache(TLRU)
==============================================================

TLRU definition :
-----------------
**source**: `Wikipedia <https://en.wikipedia.org/wiki/Cache_replacement_policies#Time_aware_least_recently_used_(TLRU)>`_

    The Time aware Least Recently Used (TLRU) is a variant of LRU designed for the situation where the stored contents in cache have a valid life time. The algorithm is suitable in network cache applications, such as Information-centric networking (ICN), Content Delivery Networks (CDNs) and distributed networks in general. TLRU introduces a new term: TTU (Time to Use). TTU is a time stamp of a content/page which stipulates the usability time for the content based on the locality of the content and the content publisher announcement. Owing to this locality based time stamp, TTU provides more control to the 
    local administrator to regulate in network storage. In the TLRU algorithm, when a piece of content arrives, a cache node calculates the local TTU value based on the TTU value assigned by the content publisher. The local TTU value is calculated by using a locally defined function. Once the local TTU value is calculated the replacement of content is performed on a subset of the total content stored in cache node. The TLRU ensures that less popular and small life content should be replaced with the incoming content.

Attributes:
-------------------

1. Simplicity. 
2. Resilient to network failures or crashes
3. Near real time replication of data across Geolocation. Writes need to be in real time
4. Data consistency across regions
5. Locality of reference, data should almost always be available from the closest region: In the client 
implementation is necessary to put a priority to connect when some server is not available
6. Flexible Schema
7. Cache can expire

******************************
Libraries to built
******************************

1. Server Library: This Software allow to run the cache servers and wait for client requests, and interact between slaves and master
2. Client Library: This python software will allow to connect to the server(s) and interact with the cache. (not implemented yet)


==============================================================
Server Design
==============================================================

CORE Implementation
--------------------

1. Model.node: Class to implement the Node structure, it have the next attributes to define the data of a node:

* key: cache's key
* date_stamp: Datetime in isoformat,  this info is defined by the master server
* due_date: Due date in isoformat defined by Master server, when the client not send timeout, then the server put a big due date
* due_date_stamp: timestamp of due_date
* value: cache's value
* state: The master server put a consecutive for each node, this is the state and allow to sync with slaves, each operation (SET, GET) make a new state. This is a second criteria to give order to the nodes

2. Model.tlru_cache: Class to implement the Cache principal structure, it have the next attributes:

* setters: Dictionary (Map) to retrieve a node with O(1). 
* server_status: Boolean value to define the availability of a server
* data_state: Doubly linked list for each GET or SET in any server, the master define the new state (consecutive), add the node to this structure and inform to all slaves. This structure allow to an slave identify if it is syncronized, when detect a problem the slave request to the server for and update to restore his data. A doubly linked list is for clean the structure (remove from left) and add new state to the end.
* priority_structure: In this implementation a Python heapq structure is used. The implementation is by a Wrap in case of replace in a new version. This structure allow to remove the next node quickly and add a new node. The priority to remove is determined by the due date and state. When a SET operation will remove an existing node, the structure not remove the node, intead of this the logic mark the node with a "REMOVED" label, this is beacause a heap structure is optimized to remove the first node.

3. use_cases.constants: 

* DAYS_TO_ADD_NODE_WITHOUT_DUE_DATE: When a client in a SET request not send the timeout (minutes), the master server assign a due date with datetime_now + this value
* NODES_LIMIT_CUANTITY: cache's Size


Details Implementations
------------------------

1. data_structure.cache_nodes: This is a Wrap for the node.priority_structure, implements a Python Heapq.

2. repository.file_repo: This implement the storage to file the cache data, only save de Dictionary. Make the possibility to start from file data and recover from failure. Implement a not efficient pickle structure, not recommended for big data. Every new node or remove node from node.setters make a disk write.

3. web_socket.server_master: This logic execute two servers for Master. 

* Web Socket serve 01: Listen for client requests (this connection only live while the operation)
* Web Socket serve 02: Listen for slaves connection. This is an open channel to broadcast the state to all slaves.

4. web_socket.server_slave: This logic execute one server for cliente, and make a new connection to the master for receive the messages to update the cache's state. Only the master is responsible for add or remove a node from the cache. Is the master the responsible to manage the priority of the nodes and inform to all slaves.

4. app: This file allow to start the server instance from the settings configuration.


Server execution
------------------------

To start a server only is necessary to write a file that import the library's CacheApplibrary and run the app like this:

.. code-block:: python

    from trlu_cache_server.app import CacheApp
    settings = {
        'LOGGING': logging.DEBUG,
        'SERVER': {
            'type': 'master',
            'address': 'localhost',
            'port_to_slaves': 8765,
            'port_to_clients': 8766
        }
    }
    def main():
        app = CacheApp(settings)
        app.run()
    if __name__ == "__main__":
        main()


Servers interaction
--------------------

1. When a client make a SET operation to MASTER:

* The master server search for the node in the cache
* Update the node or add the new node, update the state
* Clean the cache removing expired nodes 
* respond to the client and asyncronously broadcast to slaves the info

2. When a client make a GET operation to MASTER:

* The master search if the key exists in the cache
* Update the node priority, update the state, 
* Clean the cache removing expired nodes 
* Respond to the client and asyncronously broadcast to slaves the info

3. When client make a SET operation to an SLAVE:

* The slave save a dirty data (without time_stamp, nor priority) and respond to the client
* The slave send to Master the new node, the slave put the time_stamp, due_date and state.
* The master broadcats the info to all slaves and the cache is update.

4. When a client make a GET operation to an SLAVE:

* The slave search for the node and return to the client.
* The slave send the operation to server.
* The server make a new state, improve the node position if it is necessary, and broadcast to slaves the new state

5. When and slave detect a different state from the server

* Request to the master for update


********************************************
Client Library Design 
********************************************

This software allow to import and define a configuration with:

* List of servers cluster
* Server assigned to connect

With this information the software can to manage the connection to the cache and select the best option (or available) to connect. To use the software only it's necessary the next:

.. code-block:: python

    from tlru_cache_client import cache
    settings = {
        'main_connection': 'server_b',
        'servers': {
            'server_a': {
                'address': address_01,
                'port': port_01
            },
            'server_b': {
                'address': address_02,
                'port': port_02
            }
        }
    }
    # Define configuration
    cache.set_conf(settings)
    # In another part in the software, implement this to set a new data cache
    cache_data = cache.set_cache(key=key, value=data, minutes_timeout=120)
    # To get the data:
    cache_data = cache.get_cache(key=key)

