from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List
from functools import total_ordering

DISCOUNT_PERCENTS = 15


@total_ordering
@dataclass(frozen=True)
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self) -> None:
        assert self.title, "Title cannot be empty"
        assert self.cost > 0, "Cost must be a positive integer"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return (self.cost, self.title) == (other.cost, other.title)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return (self.cost, self.title) < (other.cost, other.title)


class Position(ABC):
    item: 'Item'

    @property
    @abstractmethod
    def cost(self) -> float:
        pass


@dataclass
class CountedPosition(Position):
    item: Item
    count: int = 1

    @property
    def cost(self) -> float:
        return self.item.cost * self.count


@dataclass
class WeightedPosition(Position):
    item: Item
    weight: float = 1.0

    @property
    def cost(self) -> float:
        return self.item.cost * self.weight


@dataclass
class Order:
    order_id: int
    positions: List[Position] = field(default_factory=list)
    cost: int = 0
    _have_promo: bool = False  # Internal field

    def __post_init__(self) -> None:
        self.cost = int(sum(position.cost for position in self.positions))
        if self._have_promo:
            self.cost = int(self.cost * (1 - DISCOUNT_PERCENTS / 100))
        object.__setattr__(self, '_have_promo', False)

    @property
    def have_promo(self) -> bool:
        return self._have_promo

    @have_promo.setter
    def have_promo(self, value: bool) -> None:
        if value:
            self.cost = int(self.cost * (1 - DISCOUNT_PERCENTS / 100))
        object.__setattr__(self, '_have_promo', value)
