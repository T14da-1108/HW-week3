## ORDERS

`class` `dataclass` `abc`

### Task

You need to implement a simple system for storing online store orders 
using [dataclasses](https://docs.python.org/3/library/dataclasses.html), which were introduced in Python 3.7.

You need to implement dataclasses with the following requirements:
* **Item**:
  * `title` is a non-empty string, and `cost` is a positive integer. Check this with `assert` immediately **after** initialization
  * It is forbidden to change the fields of the created object.
  * Items should be compared by price and then (in case the price is the same) by title
    (`item1 > item2` when `(cost1, title1) > (cost2, title2)`)
* **Position**:
  * Super class for `CountedPosition` and `WeightedPosition`. Cannot be created on its own 
  * Stores `item` 
  * Implements an abstract `cost` property that can return a non-integer value
* **CountedPosition**:
  * `Item.cost` - price per unit of goods.
  * By default, the number of goods is equal to one.
* **WeightedPosition**:
  * `Item.cost`- price per unit of goods' weight.
  * By default, the weight of the product is equal to one.
* **Order**:
  * Upon creation, it receives a set of positions. Based on this data, the `cost` field is filled
  * The final cost is always an integer (we keep only the integer part)

In case if you don't pass the tests, try to read
the documentation on [dataclasses](https://docs.python.org/3/library/dataclasses.html) first.