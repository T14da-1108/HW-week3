from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List

@dataclass
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self):
        if self.item_id < 0:
            raise AssertionError("item_id must be non-negative")
        if not self.title:
            raise AssertionError("title must be a non-empty string")
        if self.cost <= 0:
            raise AssertionError("cost must be a positive integer")

    def __lt__(self, other: "Item") -> bool:
        if self.cost == other.cost:
            return self.title < other.title  # If the cost is the same, compare by title
        return self.cost < other.cost  # Compare by cost first

    def __gt__(self, other: "Item") -> bool:
        if self.cost == other.cost:
            return self.title > other.title  # If the cost is the same, compare by title
        return self.cost > other.cost  # Compare by cost first


@dataclass
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> int:
        pass


@dataclass
class CountedPosition(Position):
    count: int = field(default=1)

    def __post_init__(self):
        if self.count < 1:
            raise ValueError("Count must be at least 1")

    @property
    def cost(self) -> int:
        return self.item.cost * self.count


@dataclass
class WeightedPosition(Position):
    weight: float = field(default=1.0)


    @property
    def cost(self) -> int:
        return round(self.item.cost * self.weight)


@dataclass
class Order:
    order_id: int
    positions: List[Position] = field(default_factory=list)
    have_promo: bool = field(default=False)

    @property
    def order_cost(self) -> int:
        """Calculate the total cost of the order, applying promo if eligible."""
        total_cost = sum(position.cost for position in self.positions)
        if self.have_promo:
            total_cost = round(total_cost * 0.85)
        return total_cost