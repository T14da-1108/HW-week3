from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List

DISCOUNT_PERCENTS = 15

@dataclass(frozen=True)
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self) -> None:
        assert self.title, "Title cannot be empty"
        assert self.cost > 0, "Cost must be a positive integer"

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

class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> float:
        pass

@dataclass
class Order:
    order_id: int
    positions: List[Position] = field(default_factory=list)
    cost: int = 0

    def __post_init__(self) -> None:
        self.cost = int(sum(position.cost for position in self.positions))
        object.__setattr__(self, 'have_promo', False)
