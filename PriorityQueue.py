from __future__ import annotations

import heapq
import random
import names

class EmptyError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
#################
class Entry[K,V]:
    __slots__ = ('key', 'value')

    def __init__(self, priority: K, data: V) -> None:
        self.key  : K = priority
        self.value: V = data

    def __str__(self) -> str:
        return f"({self.key},{self.value})"

    def __eq__(self, other: Entry[K,V]) -> bool:
        return self.key == other.key and self.value == other.value

    def __lt__(self, other: Entry[K,V]) -> bool:
        return self.key < other.key

    # not the Pythonic way to use __repr__ but allows us to print a list of Entry
    def __repr__(self) -> str: 
        return f"({repr(self.key)},{'∅' if self.value is None else repr(self.value)})"

#######################
class PriorityQueue[K,V]:
    __slots__ = ('_container')

    def __init__(self) -> None:
        self._container: list[Entry[K,V]] = list()

    def __len__(self)  -> int:  return len(self._container)
    def isEmpty(self) -> bool:  return len(self._container) == 0

    def insert(self, key: K, item: V) -> None: 
        """_summary_ inserts a new item in the proper position for the priority q. Follows min heap rules

        Args:
            key (K): value of item we are inserting
            item (V): item we are inserting
        """
        # create a new Entry having key, item
		# insert into the heap (self._container) using heapq.heappush
        entryPushed = Entry(key, item)
        heapq.heappush(self._container, entryPushed)

    def removeMin(self) -> Entry[K,V]:
        """_summary_ removes the min item of the priority q. in a heap it is the first item of the list

        Raises:
            EmptyError: if the list is empty is can't remove anything and raises an empty error

        Returns:
            Entry[K,V]: returns the entry at the min position
        """
        # remove from the heap (self._container) using heapq.heappop
        if self.isEmpty():
            raise EmptyError("The queue is empty we cannot remove anything")
        else: 
            return heapq.heappop(self._container)

    def min(self) -> Entry[K,V]:
        """_summary_ returns the min item of the priority q without removing it

        Raises:
            EmptyError: raises error if the list is empty

        Returns:
            Entry[K,V]: the min item
        """
        if self.isEmpty():
            raise EmptyError("The queue is empty we cannot remove anything")
        else: return self._container[0]

    def __str__(self) -> str:
        return str(self._container)

##########################
def main() -> None:
    pq = PriorityQueue()
    print(f"len of pq = {len(pq)}")
    # provide more tests below
    l = PriorityQueue()
    i = 0
    while i<5: #tests to see if insert heap works correctly with a list of 5
        key = random.randint(0,100)
        name = names.get_full_name()
        l.insert(key, name)
        print(l.min())
        print(l)
        print("\n")
        i+=1
    


    while not l.isEmpty(): #tests to see if remove works correctly until list is empty
        print(l.removeMin())
        print(l)




if __name__ == "__main__":
    main()
