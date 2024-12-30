from __future__ import annotations

# https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
# Want to define our own custom Exception class...
class EmptyError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class Node[T]:
    ''' class to implement a single node object in a doubly-linked
        linked list '''
    def __init__(self, data: T):
        self.data: T       = data
        self.next: Node[T] = None  # points to another Node object
        self.prev: Node[T] = None  # points to the previous Node object

class LinkedList[T]:
    ''' class to implement a doubly-linked linked list '''
    __slots__ = ('_head', '_tail', '_size')

    def __init__(self) -> None:
        self._head: Node[T] = None   # the head pointer in the linked list
        self._tail: Node[T] = None   # the tail pointer in the linked list
        self._size: int     = 0

    def __len__(self) -> int:
        """_summary_ returns the size of the list

        Returns:
            int: size of list
        """
        return self._size
    
    def front(self)-> T:
        ''' method to return the data item at the front of the list without
            removing that node
        Returns:
            the T-valued item at the front of the list
        Raises:
            EmptyError if the list is empty
        '''
        if self._size == 0:
            raise EmptyError("List is empty no front")
        else: return self._head.data

    def back(self)-> T:
        ''' method to return the data item at the end of the list without
            removing that node
        Returns:
            the T-valued item at the end of the list
        Raises:
            EmptyError if the list is empty
        '''
        if self._size == 0:
            raise EmptyError("List is empty no front")
        else: return self._tail.data


    def addLeft(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the left
            side of the linked list... remember to reset the head pointer, and,
            when appropriate, the tail pointer
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        if self._head is None:  # empty list
            self._head = self._tail = new_node
            self._size += 1
        else:
            if type(item) != type((self._head.data)):
                raise TypeError("Data is not right type")
            else:
                new_node.next = self._head
                self._head.prev = new_node 
                self._head = new_node
                self._size += 1

    def addRight(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the right 
            of the linked list... remember to reset the tail pointer, and, when
            appropriate, the head pointer
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        if self._head is None:  # empty list
            self._head = self._tail = new_node
            self._size += 1

        else:
            if type(item) != type((self._head.data)):
                raise TypeError("Data is not right type")
            else:
                new_node.prev = self._tail
                self._tail.next = new_node   #(b)
                self._tail = new_node        #(c)
                self._size += 1
   
    def removeLeft(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node...  Remember to handle the special case of an 
            empty list (what should the head and tail pointers be in that case?)
            and remember to update the head & tail pointer(s) when appropriate.
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        if self._size == 0: #empty list
            raise EmptyError("Cannot remove a node from an empty list")
        else:
            value = self._head.data
            if self._head == self._tail:
                self._head = self._tail = None
            else:
                self._head = self._head.next
                self._head.prev = None
            self._size-=1
        return value

    def removeRight(self) -> T:
        ''' removes the last Node in the linked list, returning the data item
            inside that Node...  Remember to handle the special case of an 
            empty list (what should the head and tail pointers be in that case?)

            Note: This one is trickier because you always have to walk (almost)
            all the way through the list in order to know what the new tail
            should be.

            Remember to update the head & tail pointer(s) when appropriate.

        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        if self._size == 0:  # or self._head is None
            raise EmptyError("cannot remove from an empty list")

        # special case: list size 1
        if self._head == self._tail:   # or if self.size == 1
            value = self._head.data
            self._head = self._tail = None
            self._size -= 1
            return value
        else: 
            value = self._tail.data
            self._tail = self._tail.prev
            self._tail.next = None
            self._size -=1

        return value

    def __str__(self):
        ''' returns a str representation of the linked list data
        Returns:
            an str representation of the linked list, showing head pointer
                and data tiems
        '''
        str_ = "head->"

        # start out at the head Node, and walk through Node by Node until we
        # reach the end of the linked list (i.e., the ._next entry is None)
        ptr_ = self._head
        while ptr_ is not None:
            if isinstance(ptr_.data, str):
                str_ += "['" + ptr_.data + "']"
            else: str_ += "[" + str(ptr_.data) + "]" 
            if ptr_.next is not None:
                str_+="<->"
            ptr_ = ptr_.next  # move ptr_ to the next Node in the linked list

        str_ += "<-tail"
        return str_

        
def main() -> None:
    # create a LinkedList and try out some various adds and removes
    ll = LinkedList()

    #tests for front and back are within add right and add left


    #tests for add right
    ll.addRight(8)
    value = ll.front() #test for front
    value2 = ll.back()
    print(f"ll: {ll}")
    print(f"Front of list is: {value}")
    print(f"Back of list is: {value2}")
    ll.addRight(7)
    ll.addRight(6)
    ll.addRight(5)
    print(f"size of ll: {len(ll)}")
    print(f"ll: {ll} \n")

    #tests for add left
    ll.addLeft(9)
    ll.addLeft(10)
    value = ll.front() #test for front
    value2 = ll.back()
    print(f"ll: {ll}")
    print(f"Front of list is: {value}")
    print(f"Back of list is: {value2}")
    ll.addLeft(11)
    ll.addLeft(12)
    print(f"size of ll: {len(ll)}")
    print(f"ll: {ll}\n")

    #tests for remove right
    ll.removeRight()
    ll.removeRight()
    value = ll.front() #test for front
    value2 = ll.back()
    print(f"ll: {ll}")
    print(f"Front of list is: {value}")
    print(f"Back of list is: {value2}")
    ll.removeRight()
    ll.removeRight()
    print(f"size of ll: {len(ll)}")
    print(f"ll: {ll}\n")

    #tests for remove left
    ll.removeLeft()
    ll.removeLeft()
    value = ll.front() #test for front
    value2 = ll.back()
    print(f"ll: {ll}")
    print(f"Front of list is: {value}")
    print(f"Back of list is: {value2}")
    ll.removeLeft()
    ll.removeLeft()
    print(f"size of ll: {len(ll)}")
    print(f"ll: {ll}")



if __name__ == "__main__":
    main()
