from dataclasses import dataclass, field, FrozenInstanceError
from abc import ABC, abstractmethod
from typing import List


DISCOUNT_PERCENTS = 15  # 割引率（パーセンテージ）

# Item クラス：商品の基本情報
@dataclass(frozen=True)
class Item:
    item_id: int
    title: str
    cost: int

    def __post_init__(self):
        # 商品のタイトルは空であってはならない、cost は正の整数でなければならない
        assert self.title, "Title cannot be empty"
        assert self.cost > 0, "Cost must be a positive integer"

    def __lt__(self, other):
        # 比較順序: cost が同じならタイトルで比較
        if self.cost == other.cost:
            return self.title < other.title
        return self.cost < other.cost


# 抽象クラス Position：CountedPosition と WeightedPosition の基底クラス
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self):
        """Costは具象クラスで実装されるべき"""
        pass


# CountedPosition クラス：数量ベースの価格
@dataclass
class CountedPosition(Position):
    item: Item
    count: int = 1  # 初期値は1

    @property
    def cost(self) -> float:
        return self.item.cost * self.count


# WeightedPosition クラス：重量ベースの価格
@dataclass
class WeightedPosition(Position):
    item: Item
    weight: float = 1.0  # 初期値は1

    @property
    def cost(self) -> float:
        return self.item.cost * self.weight


# Order クラス：注文情報を保持する
@dataclass
class Order:
    order_id: int
    positions: List[Position] = field(default_factory=list)
    cost: int = 0
    have_promo: bool = False  # プロモーションがあるかどうか

    def __post_init__(self):
        # 注文の総コストを計算
        self.cost = int(sum(position.cost for position in self.positions))
        if self.have_promo:
            self.cost = int(self.cost * (1 - DISCOUNT_PERCENTS / 100))  # 割引適用
        # プロモーションはフィールドとして持たない
        object.__setattr__(self, 'have_promo', False)
