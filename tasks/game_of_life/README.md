## LIFE GAME

`class` `game-of-life`

In this task, you need to implement a version of the classic [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

### Preface

The ocean is represented as a two-dimensional array of cells. 

At each moment of time each cell contains only one of the following:
* nothing, e.g. empty cell
* a rock
* a fish
* a shrimp

Two cells are considered *adjacent* if they have at least one common point
(so, a cell in the middle of the field has eight adjacent cells).
All cells beyond the game field are considered empty. 

How cells are updated with each iteration:
* cells with rocks do not change over time;
* if it is too crowded for a fish (four or more adjacent cells with fish), the fish dies;
* if a fish is too lonely (no or only one adjacent cell(s) containing fish), the fish dies;
* if a fish is surrounded by two or three neighboring fish, it stays itself;
* neighboring rocks and shrimps do not affect the life of fish;
* shrimps exist change over time using the same above rules (counting neighboring shrimps instead of fish);
* if a certain ocean cell was empty and had exactly 3 fish neighbors, then a fish is born in it at the next moment;
otherwise, if the cell had exactly three shrimp neighbors, a shrimp is born in it;
* all ocean cells are updated simultaneously, taking into account only the states of cells at the previous moment in time;

### Task

You need to implement the `GameOfLife` class in the `game_of_life.py` file.

Requirements for the class:
* The class is initialized with the initial state of the ocean - 
a two-dimensional list (list of lists), each element of which is a number. 
0 - if the cell is empty, 1 - cell with a rock, 2 - cell with a fish, 3 - cell with a shrimp.
* Contains the `get_next_generation` method, which updates the state of the ocean and returns its contents
* `get_next_generation` should be the only public method in the class
* You need to think about how to split functionality into small methods, which, 
unlike `get_next_generation`, are marked “private”, that is, their name 
is prefixed with an underscore `_`. 

For example, if you were to create a method that returns all the neighboring cells, you would write the following 
method signature:
```python3
class GameOfLife(object):
    ...
    def _get_neighbours(self, i: int, j: int):
        pass
```

Note that naming a method in such a way does not actually ”hide it” from calling outside of the class (unlike
other OOP languages such as Kotlin, which won't even let you compile source code that accesses private methods).
Just like docstrings that we discussed in the chat, this is merely a *convention* to notify the user that this
method is internal and it is at their own risk to actually call it.

## Example

```python3
>>> game_of_life = GameOfLife([[1, 1], [1, 1]])
>>> game_of_life.get_next_generation()
[[1, 1], [1, 1]]
```