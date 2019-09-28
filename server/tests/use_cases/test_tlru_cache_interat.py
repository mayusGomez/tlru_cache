import pytest
from unittest import mock

from datetime import datetime, timedelta

from ...trlu_cache_server.model.tlru_cache import TLRU_Cache
from ...trlu_cache_server.model.node import Node
# from ...trlu_cache_server.use_cases.tlru_interact import TLRU_Interaction
from ...trlu_cache_server.use_cases.response import Response
from ...trlu_cache_server.use_cases.constants import DAYS_TO_ADD_NODE_WITHOUT_DUE_DATE

@pytest.fixture
def load_cache_same_due_date():
    tlru = TLRU_Cache()

    node_3 = Node(
        key='z',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=1, 
        next_node=None, 
        previous_node=None
    )

    node_2 = Node(
        key='y',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=1, 
        next_node=None, 
        previous_node=None
    )

    node_1 = Node(
        key='x',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=1, 
        next_node=None, 
        previous_node=None
    )

    node_0 = Node(
        key='w',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=8, 
        next_node=None, 
        previous_node=None
    )

    node = Node(
        key='v',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=8, 
        next_node=None, 
        previous_node=None
    )

    node.next_node = node_0
    node_0.previous_node = node
    node_0.next_node = node_1
    node_1.previous_node = node_0
    node_1.next_node = node_2
    node_2.previous_node = node_1
    node_2.next_node = node_3
    node_3.previous_node = node_2

    tlru.setters = {
        node.key: node,
        node_0.key: node_0,
        node_1.key: node_1,
        node_2.key: node_2,
        node_3.key: node_3
    }

    tlru.head = node
    tlru.tail = node_3

    return tlru



@pytest.fixture
def load_cache():
    tlru = TLRU_Cache()

    node_3 = Node(
        key='z',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=1, 
        next_node=None, 
        previous_node=None
    )

    node_2 = Node(
        key='y',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=1, 
        next_node=None, 
        previous_node=None
    )

    node_1 = Node(
        key='x',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,7,30,0,00000), 
        value=1, 
        next_node=None, 
        previous_node=None
    )

    node_0 = Node(
        key='w',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,7,30,0,00000), 
        value=8, 
        next_node=None, 
        previous_node=None
    )

    node_0.next_node = node_1
    node_1.previous_node = node_0
    node_1.next_node = node_2
    node_2.previous_node = node_1
    node_2.next_node = node_3
    node_3.previous_node = node_2

    tlru.setters = {
        node_0.key: node_0,
        node_1.key: node_1,
        node_2.key: node_2,
        node_3.key: node_3
    }

    tlru.head = node_0
    tlru.tail = node_3

    return tlru





"""
def test_insert_new_node_1(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)

    node_x = Node(
        key='u',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,30,0,00000), 
        value=8, 
        next_node=None, 
        previous_node=None
    )
    tlru_use_case._insert_new_node(node_x)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    assert list_keys == ['u', 'v', 'w','x','y', 'z']


def test_insert_new_node_2(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)

    node_x = Node(
        key='u',
        time_stamp= datetime.now(), 
        due_date= datetime(2019,1,1,0,29,0,00000), 
        value=8, 
        next_node=None, 
        previous_node=None
    )
    tlru_use_case._insert_new_node(node_x)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    assert list_keys == ['v', 'w','x','y', 'z', 'u']


def test_insert_new_node_3(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)

    node_x = Node(
        key='u',
        time_stamp= datetime.now(), 
        due_date= datetime.now() + timedelta(days=DAYS_TO_ADD_NODE_WITHOUT_DUE_DATE),
        value=8, 
        next_node=None, 
        previous_node=None
    )
    tlru_use_case._insert_new_node(node_x)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    assert list_keys == ['u', 'v', 'w','x','y', 'z']


def test_insert_new_node_4(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)

    for i in range(6):
        node_x = Node(
            key=i,
            time_stamp= datetime.now(), 
            due_date= datetime.now() + timedelta(days=DAYS_TO_ADD_NODE_WITHOUT_DUE_DATE),
            value=8, 
            next_node=None, 
            previous_node=None
        )
        tlru_use_case._insert_new_node(node_x)

    list_keys = tlru_use_case.list_keys(max_iter=10)
    assert list_keys == [5, 4, 3, 2, 1, 0, 'v', 'w','x','y']


def test_set_node_exists_6(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)

    tlru_use_case.set_node(key='x', time_now=datetime.now(), due_date=datetime(2019,1,1,0,40,0,00000), value=8)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    assert list_keys == ['x', 'v', 'w','y', 'z']


def test_move_node_to_rigth_tail_same_due_date(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_to_rigth(load_cache_same_due_date.tail)

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['v', 'w','x','y', 'z']


def test_move_node_to_rigth_head_same_due_date(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_to_rigth(load_cache_same_due_date.head)

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['v', 'w','x','y', 'z']


def test_move_node_to_rigth_head_same_due_date(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)

    load_cache_same_due_date.head.due_date = datetime(2019,1,1,0,0,0,00000)

    response = tlru_use_case._move_to_rigth(load_cache_same_due_date.head)

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['w','x','y','z','v']


def test_move_node_to_left_tail_same_due_date(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache_same_due_date.tail)

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['z', 'v', 'w','x','y']


def test_move_node_to_left_tail_same_due_date_2(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache_same_due_date.setters['y'])

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['y', 'v', 'w','x','z']


def test_move_node_to_left_tail_same_due_date_3(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache_same_due_date.setters['w'])

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['w', 'v', 'x','y', 'z']


def test_move_node_to_left_tail_same_due_date_4(load_cache_same_due_date):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache_same_due_date

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache_same_due_date.setters['v'])

    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['v', 'w', 'x','y', 'z']


def test_move_node_to_left_tail(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache.tail)

    # tlru_use_case = TLRU_Interaction(data)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['w','x','z','y']


def test_move_node_to_left_head(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache.head)

    # tlru_use_case = TLRU_Interaction(data)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['w','x','y','z']


def test_move_node_to_left_inside(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case._move_node_to_left(load_cache.setters['y'])

    # tlru_use_case = TLRU_Interaction(data)
    list_keys = tlru_use_case.list_keys(max_iter=10)
    
    assert list_keys == ['w','x','y','z']


def test_get_item_with_re_order_data_success(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case.get_node('z')

    # tlru_use_case = TLRU_Interaction(data)
    list_keys = tlru_use_case.list_keys(max_iter=10)

    assert response.type_response == Response.SUCCESS
    assert response.value.value == 1
    assert list_keys == ['w','x','z','y']


def test_get_item_with_re_order_data_success_to_head(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case.get_node('x')

    # tlru_use_case = TLRU_Interaction(data)
    list_keys = tlru_use_case.list_keys(max_iter=10)

    assert response.type_response == Response.SUCCESS
    assert list_keys == ['x','w','y','z']


def test_get_item_with_re_order_data_success_head(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case.get_node('w')

    # tlru_use_case = TLRU_Interaction(data)
    list_keys = tlru_use_case.list_keys(max_iter=10)

    assert response.type_response == Response.SUCCESS
    assert list_keys == ['w','x','y','z']


def test_get_item_with_re_order_data_fail(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache

    tlru_use_case = TLRU_Interaction(data)
    response = tlru_use_case.get_node('m')

    assert response.type_response == Response.FAIL




def test_set_items(load_cache):
    data = mock.Mock()
    data.get_tlru_cache.return_value = load_cache
    tlru_use_case = TLRU_Interaction(data)
    now = datetime.now()
    response = tlru_use_case.set_node(
        key='a', 
        time_stamp=now, 
        due_date=datetime(2019,1,1,7,30,0,00000), 
        value=45
    )
"""

