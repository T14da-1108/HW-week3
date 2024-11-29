from dataclasses import dataclass, field, FrozenInstanceError
from abc import ABC, abstractmethod
from typing import List


DISCOUNT_PERCENTS = 15


@dataclass(frozen=False)
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self) -> None:
        assert self.title, "Title cannot be empty"
        assert self.cost > 0, "Cost must be a positive integer"

    def __lt__(self, other: 'Item') -> bool:
        if self.cost == other.cost:
            return self.title < other.title
        return self.cost < other.cost


class Position(ABC):
    item: Item

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
    have_promo: bool = False

    def __post_init__(self) -> None:
        self.cost = int(sum(position.cost for position in self.positions))
        if self.have_promo:
            self.cost = int(self.cost * (1 - DISCOUNT_PERCENTS / 100))
        object.__setattr__(self, 'have_promo', False)
