

class TLRU_Cache:

    def __init__(self, setters=None, priority_structure=None, server_status=True, data_state=None):
        self.setters = {}  # Data dict of nodes, for access O(1)
        self.priority_structure = priority_structure  # Data structure of nodes with priority
        self.server_status = server_status  # True or False to accept or reject request
        self.data_state = data_state  # Data structure to save the server state 
                                      # (each "set" or "get" is a new state), for pop() either ends

