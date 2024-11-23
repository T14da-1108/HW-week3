from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List


@dataclass(frozen=True)
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self):
        assert self.title != '', "Title must not be empty"
        assert self.cost > 0, "Cost must be a positive number"

    def __lt__(self, other: 'Item') -> bool:
        return (self.cost, self.title) < (other.cost, other.title)


class Position(ABC):
    item: Item

    def __init__(self, item: Item) -> None:
        self.item = item

    @property
    @abstractmethod
    def cost(self) -> float:  # 型アノテーションを追加
        pass


@dataclass
class CountedPosition(Position):
    item: Item
    count: int = 1

    @property
    def cost(self) -> float:  # 型アノテーションを追加
        return self.item.cost * self.count


@dataclass
class WeightedPosition(Position):
    item: Item
    weight: float = 1

    @property
    def cost(self) -> float:  # 型アノテーションを追加
        return self.item.cost * self.weight


@dataclass
class Order:
    order_id: int
    positions: List[Position] = field(default_factory=list)
    have_promo: bool = False

    @property
    def order_cost(self) -> int:
        total_cost = sum(position.cost for position in self.positions)
        if self.have_promo:
            total_cost *= 0.9
        return int(total_cost)
