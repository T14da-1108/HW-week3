from collections import UserList
import typing as tp


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
