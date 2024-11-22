from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List


# 1. Item Class Definition
@dataclass
class Item:
    item_id: int
    title: str
    cost: int

    def __lt__(self, other: 'Item'):
        # Sorting items by cost
        return self.cost < other.cost


# 2. Position Abstract Class and Its Subclasses
class Position(ABC):
    @abstractmethod
    def cost(self) -> int:
        pass

    @property
    @abstractmethod
    def item(self) -> Item:
        pass


class CountedPosition(Position):
    def __init__(self, item: Item, count: int):
        self._item = item
        self.count = count

    @property
    def item(self) -> Item:
        return self._item

    def cost(self) -> int:
        return self._item.cost * self.count


class WeightedPosition(Position):
    def __init__(self, item: Item, weight: int):
        self._item = item
        self.weight = weight

    @property
    def item(self) -> Item:
        return self._item

    def cost(self) -> int:
        return self._item.cost * self.weight


# 3. Order Class Definition
@dataclass
class Order:
    order_id: int
    positions: List[Position] = field(default_factory=list)
    is_promo: bool = False

    @property
    def order_cost(self) -> int:
        # Calculate the total cost by summing the costs of all positions
        return sum(position.cost() for position in self.positions)

    @property
    def have_promo(self) -> bool:
        # Check if there is a promo, based on item_id
        return any(position.item.item_id == 0 for position in self.positions)