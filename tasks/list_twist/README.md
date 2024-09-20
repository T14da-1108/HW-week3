## LIST TWIST

`UserList` `inheritance`

### Task

You need to implement a class with a list interface, in which to add attributes:
* **reversed**:
  * When accessed, it returns a list with elements in reverse order.
* **first**
  * When accessed, the first element of the list is returned.
  * There should be the ability to change this attribute. Along with it, the list itself should change
  * When trying to get or set **first** in an empty list, behavior is undefined
* **size**
  * When accessed, the size of the list is returned.

**Important**: All the functionality of the list should be preserved.

In python, there is a [built-in decorator](https://docs.python.org/3/library/functions.html#property) `@property`,
which allows you to create aliases and getters/setters. But we ask you to go a level down and
play around with `__getattr__` and `__setattr__` directly.


## Example

```python
>>> list_twist = ListTwist([1, 2, 3])
>>> print(list_twist.reversed)
[3, 2, 1]
>>> print(list_twist.first)
1
>>> list_twist.first = 0
>>> print(list_twist)
[0, 2, 3]
>>> list_twist[:2]
[0, 2]
>>> for i in list_twist:
...     print(i)
0
2
3
```

### Remarks

* All listed attributes are not methods (see example)
* You need to compute them on the fly and modify the state
* It is important not to break the basic functionality of the list

---