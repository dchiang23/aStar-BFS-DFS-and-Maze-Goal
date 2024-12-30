from __future__ import annotations
from typing import TypeVar
from collections import deque

T = TypeVar("T")

class Queue[T]:
    __slots__ = ("_data")

    def __init__(self):
        """_summary_ initilize our queue
        """
        self._data: deque[T] = deque()

    def __len__(self)->int:
        """_summary_ gives length of our queue

        Returns:
            int: returns the length of our queue
        """
        return len(self._data)

    def push(self, element: T) -> None:
        """_summary_ pushes a element of type T to the back of the queue

        Args:
            element (T): what we want to push in

        Raises:
            TypeError: element not same type as queue
        """
        if len(self._data) > 0 and type(element) != type(self._data[0]):
            raise TypeError(f"New Item must be {type(self._data[0])}")
        self._data.append(element)

    def pop(self) -> T:
        """_summary_ removes and returms the item at the front of the queue 

        Returns:
            T: element T at the front of the queue
        
        Raises: EmptyError if the queue is empty
        """
        if self.isEmpty():
            raise IndexError("nothing to pop since queue is empty")
        else:
            return self._data.popleft()
    
    def top(self) -> T:
        """_summary_ returns what is at the front of the queue without removing it

        Returns:
            T: element T at the front of the queue
        Raises: EmptytError if queue is empty

        """
        if self.isEmpty():
            raise IndexError("queue is empty nothing in it")
        else: return self._data[0]

    def isEmpty(self) -> bool:
        """_summary_ checks whether the queue is empty or not

        Returns:
            bool: True if empty false if not
        """
        return len(self._data) == 0

    def __str__(self) -> str:
        """_summary_ prints out the str of our queue

        Returns:
            str: str visual of our queue
        """
        result = "| front | "
        result+= "-->".join(str(item) for item in self._data)
        result += " | back | "
        return result

def main():
    q = Queue()
    print(f"testing for empty queue: {q.isEmpty()}")
    
    print("\n")
    try:
        print(f"testing pop on empty queue: {q.pop()}")
        print(f"testing pop on empty queue: {q.top()}")
    except:
        print(f"indexError")

    print("\n")
    for i in range(10):
        q.push(i)
    print(q)

    print("\n")
    print(f"testing pop. Expected return 0, actual return {q.pop()}\n {q}")

    print("\n")
    print(f"testing top. Except to print 1 without removing: {q.top()} \n {q}")

    

if __name__ == "__main__":
    main()