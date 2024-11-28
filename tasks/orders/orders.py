from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List


@dataclass(frozen=True)
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self):
        # 初期化後に検証
        assert self.title != "", "Title cannot be empty"
        assert self.cost > 0, "Cost must be a positive integer"

    def __lt__(self, other: 'Item') -> bool:
        if self.cost == other.cost:
            return self.title < other.title
        return self.cost < other.cost

    def __le__(self, other: 'Item') -> bool:
        if self.cost == other.cost:
            return self.title <= other.title
        return self.cost <= other.cost

    def __gt__(self, other: 'Item') -> bool:
        if self.cost == other.cost:
            return self.title > other.title
        return self.cost > other.cost

    def __ge__(self, other: 'Item') -> bool:
        if self.cost == other.cost:
            return self.title >= other.title
        return self.cost >= other.cost


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
    positions: List[Position]
    have_promo: bool = False

    @property
    def order_cost(self) -> int:
        total_cost = sum(position.cost for position in self.positions)
        if self.have_promo:
            total_cost *= 0.85  # 15% discount if promo is applied
        return int(total_cost)  # Integer part of the total cost
