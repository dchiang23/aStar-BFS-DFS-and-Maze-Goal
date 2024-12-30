from __future__ import annotations
from typing import TypeVar
T = TypeVar("T")
from collections import deque

class Stack[T]:
    __slots__ = ("_data")
    def __init__(self):
        """_summary_ initialize the class
        """
        self._data: deque[T] = deque()

    def __len__(self) -> int:
        """_summary_

        Returns:
            int: returns the length of the stack
        """
        return len(self._data)

    def push(self, element: T) -> None:
        """_summary_ pushes an element into the stack

        Args:
            element (T): what we want to push in

        Raises:
            TypeError: type we are trying to push in doesn't match type of stack
        """
        if len(self._data) > 0 and type(element) != type(self._data[0]):
            raise TypeError(f"New Item must be {type(self._data[0])}")
        self._data.append(element)

    def pop(self) -> T:
        """_summary_ remove the item from top of stack

        Returns:
            T: returns the removed item
        """
        if self.is_empty():
            raise IndexError("cannot pop from empty stack")
        else:
            return self._data.pop()
    
    def top(self) -> T:
        """_summary_ gives us the item at the top of the stack

        Returns:
            T: the item at the top of the stack
        """
        if self.is_empty():
            raise IndexError("cannot return from empty stack")
        else: return self._data[-1]

    def is_empty(self) -> bool:
        """_summary_ checks whether the stack is empty or not

        Returns:
            bool: returns true if it is empty, returns false if it isn't
        """
        return len(self._data) == 0

    def __str__(self) -> str:
        """_summary_ prints out the data in the stack

        Returns:
            str: everything in the stack represented as a string
        """
        result = "-- top --\n"
        for i in range(len(self._data) - 1, -1, -1):
            result += f"{str(self._data[i])}\n"
        result += "-- bot --"
        return result


def main()->None:
    s = Stack()
    print(f"type of s: {type(s)}")
    for i in range(10):
        s.push(i)
    print(s)
    s.pop()
    print(s)
    print(s.top())
    

if __name__ == "__main__":
    main()