from collections import UserList
import typing as tp
from typing import Any


class ListTwist(UserList[tp.Any]):
    """
    List-like class with additional attributes:
        * reversed - return reversed list
        * first - insert or retrieve first element;
                     Undefined for empty list
        * size -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """

    def __getattr__(self, name: str) -> Any:
        if name == "reversed":
            # Return the reversed list
            return list(reversed(self.data))
        elif name == "first":
            # Get the first element
            if not self.data:
                raise ValueError("Cannot access 'first' in an empty list.")
            return self.data[0]
        elif name == "size":
            # Get the size of the list
            return len(self.data)
        else:
            raise AttributeError(f"'ListTwist' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "first":
            # Set the first element
            if not self.data:
                raise ValueError("Cannot set 'first' in an empty list.")
            self.data[0] = value
        elif name == "size":
            # Adjust the size of the list
            if value < 0:
                raise ValueError("Size cannot be negative.")
            current_size = len(self.data)
            if value < current_size:
                del self.data[value:]  # Truncate
            elif value > current_size:
                self.data.extend([None] * (value - current_size))  # Pad with None
        else:
            super().__setattr__(name, value)  # Use default behavior for other attributes
