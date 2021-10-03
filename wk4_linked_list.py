'''
This is an implemenation of linked lists using Python.

In a project of my own I would probably implement this as a basic python list.
Head and tail could be reached by simple indexing (ie list[0], list[-1]) and all
the other functions required by this assignment are already built in functions 
of the list type. This didn't feel like the spirit of the assignment.

The example code given this week included getters and setter methods in its
classes. As none of the variables in my classes are hidden, I felt a more
pythonic approach to the problem was to directly reference variables (self.next
as opposed to self.get_next()). If I was writing in another language, or had a 
need for stronger encapsulation, I would reimplement the get/set functions.

For clarity, I have used the words 'head' and 'tail' to refer only to the ends 
of the entire list. The head/tail of individual nodes are described as the
node's 'item' and 'next'.
'''


class Node:
    def __init__(self, item=None):
        self.item = item
        self.next = None

    def get_next(self):
        return self.next

    def set_item(self, item):
        self.item = item

    def set_next(self, next):
        self.next = next

    def is_tail(self):
        if self.next == None:
            return True
        else:
            return False

    def __str__(self):
        return self.item


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
                node = node.get_next()

    def is_empty(self):
        if self.head == None:
            return True
        else:
            return False

    def location(self, int, node="default", count=0):
        if self.is_empty():
            print("list is empty")
            return False
        if node == "default":
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
            tail.set_next(new_node)

    def remove(self, position):
        if position == 0:   # removes head node
            node = self.head
            post_node = self.location(1)
            self.head = post_node
            del(node)

        elif position == self.size() - 1:  # removes tail node
            node = self.location(position)
            pre_node = self.location(position-1)
            pre_node.next = None
            del(node)

        else:  # removes other nodes
            node = self.location(position)
            pre_node = self.location(position-1)
            post_node = self.location(position+1)

            pre_node.next = post_node
            del(node)

    def size(self, node="default", count=0,):
        while True:
            if node == "default":
                node = self.head
            if node == None:
                return count
            elif node.is_tail():
                count += 1
                return count
            else:
                count += 1
                node = node.get_next()
                count = self.size(node, count)
                return count

    def search(self, item, node="default", place=0):
        while True:
            if node == "default":
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
    node = list.location(2)
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
