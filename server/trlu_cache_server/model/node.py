
class Node:
    def __init__(self, key=None, date_stamp=None, due_date=None, due_date_stamp=None, value=None, state=None):
        self.key = key  # Cache's key
        self.date_stamp = date_stamp  # Datetime now() of Master server
        self.due_date = due_date  # Due date defined by Master server
        self.due_date_stamp = due_date_stamp   # timestamp .now() for have priority in nodes
        self.value = value   # Cache's data
        self.state = state   # State of the data (counter), give another priority when due_date is equal

    def __lt__(self, other_node):
        """
        To have and order for every node
        The due_date_stamp is the principal priority, and second is state
        """
        return self.due_date_stamp < other_node.due_date_stamp \
            or (self.due_date_stamp == other_node.due_date_stamp and self.state < other_node.state)
