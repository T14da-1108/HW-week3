from dataclasses import is_dataclass, FrozenInstanceError, asdict
from typing import Any
from pathlib import Path
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "orders"))
import pytest
from orders import Item, Position, CountedPosition, WeightedPosition, Order


@pytest.mark.parametrize('class_type', [
    Item, Position, CountedPosition, WeightedPosition, Order
])
def test_class_type(class_type: Any) -> None:
    assert is_dataclass(class_type)


def test_no_init_implemented() -> None:
    solution_file = Path(__file__).parent / 'orders.py'
    assert solution_file.exists()
    with open(solution_file) as f:
        for line in f:
            assert not re.match(r'.*def __init__.*', line)


def test_no_compare_implemented() -> None:
    solution_file = Path(__file__).parent / 'orders.py'
    assert solution_file.exists()
    with open(solution_file) as f:
        for line in f:
            for method in ['__eq__', '__ne__', '__lt__', '__gt__', '__le__', '__ge__']:
                assert not re.match(fr'.*def {method}.*', line)


def test_item_params_check() -> None:
    Item(item_id=1, title='Spoon', cost=25)

    with pytest.raises(AssertionError):
        Item(item_id=100, title='', cost=25)
    with pytest.raises(AssertionError):
        Item(item_id=10, title='Pen', cost=-25)
    with pytest.raises(AssertionError):
        Item(item_id=10, title='Another Pen', cost=0)


def test_item_frozen() -> None:
    item = Item(item_id=0, title="Sub-Zero", cost=500)

    with pytest.raises(FrozenInstanceError):
        item.item_id = 10


def test_items_ordering() -> None:
    assert Item(item_id=0, title='Pop-it', cost=200) < Item(item_id=1, title='Simple Dimple', cost=200)
    assert Item(item_id=0, title='Jacket', cost=15000) > Item(item_id=1, title='Jacket', cost=400)


def test_items_sort() -> None:
    items = [
        Item(item_id=9, title='Thing', cost=44),
        Item(item_id=0, title='Note', cost=8),
        Item(item_id=1, title='Things', cost=100),
        Item(item_id=8, title='Unity', cost=5),
        Item(item_id=11, title='Things', cost=44),
        Item(item_id=15, title='Note', cost=64),
    ]
    sorted_items = sorted(items, key=lambda item: item.cost)
    assert [i.item_id for i in sorted_items] == [0, 15, 9, 11, 1, 8]


@pytest.mark.parametrize('class_type', [CountedPosition, WeightedPosition])
def test_position_inheritance(class_type: Any) -> None:
    assert issubclass(class_type, Position)


def test_position_is_abstract() -> None:
    """Ensure Position class cannot be instantiated directly."""
    with pytest.raises(TypeError):
        _ = Position(item=Item(item_id=0, title='Spoon', cost=25))  # Should raise TypeError

@pytest.mark.parametrize('class_, input_, expected_cost', [
    (CountedPosition, dict(item=Item(0, 'USB cable', 256)), 256),
    (CountedPosition, dict(item=Item(0, 'USB cable', 256), count=4), 1024),
    (CountedPosition, dict(item=Item(0, 'USB plug', 256), count=2), 512),
    (CountedPosition, dict(item=Item(0, 'Book', 4), count=20), 80),
    (WeightedPosition, dict(item=Item(0, 'Book', 40), weight=1), 40),
    (WeightedPosition, dict(item=Item(0, 'Book', 4), weight=20), 80),
    (WeightedPosition, dict(item=Item(0, 'Sugar', 256), weight=0.5), 128),
    (WeightedPosition, dict(item=Item(0, 'Melon', 40), weight=8.3), 332),
])


def test_position_cost(class_, input_, expected_cost):
    position = class_(**input_)
    assert position.cost == expected_cost


@pytest.mark.parametrize('input_, expected_cost', [
    (dict(positions=[CountedPosition(Item(0, 'USB cable', 256), count=4)]), 1024),
    (dict(positions=[CountedPosition(Item(0, 'USB cable', 256), count=2)], have_promo=True), 435),
    (dict(positions=[CountedPosition(Item(i, 'Book', i * 100), count=i) for i in range(5, 8)]), 11000),
    (dict(positions=[CountedPosition(Item(i, 'Book', i * 50), count=i) for i in range(1, 3)], have_promo=True), 127),
    (dict(positions=[WeightedPosition(Item(0, 'Melon', 40), weight=8.3)]), 332),
    (dict(positions=[WeightedPosition(Item(0, 'Melon', 40), weight=8.3), CountedPosition(Item(0, 'Box', 90), count=5)]), 422),
])


def test_order_cost(input_, expected_cost):
    input_['order_id'] = 0
    order = Order(**input_)
    assert order.order_cost == expected_cost


def test_order_have_promo_is_not_field() -> None:
    order = Order(order_id=0)
    assert 'have_promo' not in order.__dict__


def test_order_no_positions() -> None:
    order_first = Order(order_id=0)
    order_first.positions.append(CountedPosition(Item(0, "USB cable", 256), count=5))

    order_second = Order(order_id=1)
    assert order_first.positions != order_second.positions
    assert len(order_first.positions) == 1
    assert len(order_second.positions) == 0
