'''
This is an implemenation of linked lists using Python.

In a project of my own I would probably implement this as a basic python list.
Head and tail could be reached by simple indexing (ie list[0], list[-1]) and all
the other functions required by this assignment are already built in functions 
of the list type. This didn't feel like the spirit of the assignment. Instead I 
used a two class solution with LinkedLists and Nodes.

The example code given this week included getters and setter methods in its
classes. As none of the variables in my classes are hidden, I felt a more
pythonic approach to the problem was to directly reference variables (self.next
as opposed to self.get_next()). I have left the get/set functions below, 
commented out, just to demonstrate the possibility.

For clarity, I have used the words 'head' and 'tail' to refer only to the ends 
of the entire list. The head/tail of individual nodes are described as the
node's 'item' and 'next'.

The four functions we were asked to add (here named add(), remove(), size() and
search()) all rely on traversal of the list. For this reason, add, size and
search have an worst-case complexity of O(n). The remove function has to 
traverse the list up to 3 times (to select nodes either side of the target, so
they can be linked) and so has a worst case scenario approaching O(3n). Removing
the head node works in constant time, as only the head of the list is 
referenced. Removing the tail node only recquires traversing the list twice, so
has a complexity of O(2n). 

Traversal in these functions is realised either by placing a series of 
if -statements inside a while-true loop, or else by calling to another function 
(ie self.final_node, self.at_location) that implements its own traversal based 
on the same principle. Size is implemented as a recursive function that passes 
the current count of nodes onto another version of itself via argument. 

As traversal is so central to the methods, I considered implementing an __iter__
method for the LinkedList class. However, I decided that the extra processing 
power needed for a method call wasn't adequately made up for by the ability to
use "list.iter()" instead of "node = node.next". 


'''


class Node:
    def __init__(self, item=None):
        self.item = item
        self.next = None

    def is_tail(self):
        if self.next == None:
            return True
        else:
            return False

    def __str__(self):
        return self.item

    # def get_next(self):
    #     return self.next

    # def set_item(self, item):
    #     self.item = item

    # def set_next(self, next):
    #     self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def final_node(self):
        node = self.head
        while True:
            if node == None:
                return node
            if node.is_tail():
                return node
            else:
                node = node.next

    def is_empty(self):
        if self.head == None:
            return True
        else:
            return False

    def at_location(self, int, node="not specified", count=0):
        if self.is_empty():
            print("list is empty")
            return False
        if node == "not specified":
            node = self.head
        while True:
            if count == int:
                return node
            else:
                count += 1
                node = node.next
                if node == None:
                    print("no node at this location")
                    return False

    def add(self, item):
        new_node = Node(item)
        if self.head == None:
            self.head = new_node
        else:
            tail = self.final_node()
            tail.next = new_node

    def remove(self, position):
        if position == 0:   # removes head node
            node = self.head
            post_node = self.at_location(1)
            self.head = post_node
            del(node)

        elif position == self.size() - 1:  # removes tail node
            node = self.at_location(position)
            pre_node = self.at_location(position-1)
            pre_node.next = None
            del(node)

        else:  # removes other nodes
            node = self.at_location(position)
            pre_node = self.at_location(position-1)
            post_node = self.at_location(position+1)

            pre_node.next = post_node
            del(node)

    def size(self, node="not specified", count=0,):
        """returns size of list"""
        if node == "not specified":
            node = self.head
        if node == None:
            return count
        elif node.is_tail():
            count += 1
            return count
        else:
            count += 1
            node = node.next
            count = self.size(node, count)
            return count

    def search(self, item, node="not specified", place=0):
        "returns index of node containing searched for item"
        while True:
            if node == "not specified":
                node = self.head
            elif node == None:
                print("item not found")
                return None
            elif node.item == item:
                return place
            else:
                node = node.next
                place += 1


if __name__ == "__main__":
    ''' These are tests to check class functionality'''

    def shape(list, num):
        '''returns basic details about list'''
        print("\n")
        num = str(num)
        print("test number: " + num)
        if list.is_empty():
            print("list is empty")
            return 0
        else:
            print("list head: " + list.head.item)
            print("list tail: " + list.final_node().item)
            print("length is: " + str(list.size()))

    # init
    list = LinkedList()

    shape(list, 0)

    # add first item

    list.add("first string")
    shape(list, 1)

    # add 2nd item
    list.add("second string")
    shape(list, 2)

    # add 3rd and fourth item (needed for later tests)
    list.add("third string")
    list.add("fourth string")
    shape(list, 3)

    # find search term
    shape(list, 4)
    location = list.search("second string")
    print("search term is at position " + str(location))

    # find node at location (used to simplify deletion)
    shape(list, 5)
    node = list.at_location(2)
    print("item at position 2 is " + node.item)

    # delete  inner node
    list.remove(1)
    shape(list, 6)

    # delete head node
    list.remove(0)
    shape(list, 7)

    # delete tail node
    tail = list.final_node()
    location = list.search(tail.item)
    list.remove(location)
    shape(list, 7)
