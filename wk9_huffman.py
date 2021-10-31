"""
This program defines a Huffman_encoding_maker object. The object is initialised with the string that is to be encoded.

Subfunctions in the class then work to encode the string as follows:

1) _count_of_characters() counts how many times each character in the string appears
2) _list_of_nodes_from_counts() uses that count to make a list of node objects, one for each unique character. These will be the 'leaves' of the Huffman binary tree.
3) _place_nodes_in_tree() then works backwards from those leaves to make the rest of the binary tree.
4) _get_codes_from_tree() then traverses that tree to generate the Huffman codes for each character in the original message.
5) encode() takes the message and encodes it into a binary string using the codes just generated.
6 _get_decoding_function() returns a decoding function that already knows then unique encoding for this message.
7) decode() decodes the encoded message.

I have also included test functions in the 'if __name__ == "main"' section of the file, to test out functionality.
"""

# imports
from sys import getsizeof #used for size comparison when testing the function


class Huffman_encoding_maker:
    """
    This class works as a container for all the different functions that are required to encode using the Huffman schema.
    It takes the string to be encoded as its only argument, and gennerate two final objects; the encoded string, and a function for decoding that string.

    I chose to use a class based implementation to make it easier to reuse this code in other programs. I've also tried to keep my individual functions as short as possible, which could lead to a confusing number of names in the top-level namespace if not contained within a class. 
    """

    class Huffman_Node:
        def __init__(
            self, character, count, left=None, right=None, code=None):
            """
            This is the foundational structure for this encoding. It sets up a binary tree node. 
            """

            # the character(s) to be encoded
            self.character = character
            
            # how often that character(s) appears in the message
            self.count = count

            # define child nodes (None, by default)
            self.left = left
            self.right = right

            # code to use for encoding
            self.code = code


    def __count_of_characters_in_(self, string):
        """This function runs through a string and makes a dictionary with a count of how often each character appears within it.

        The function makes one comparrison for every character in the string. In terms of comparsion, this is a complexity of O(n).

        Each comparison involves reference to two different structures. If (n = length of input) and (u = unique characters in input), the worst case complexity for lookup is O(nu), because for each character in the string it must be checked against each unique character in the character count dictionary."""

        character_dict = {}
        for character in string:
            if character_dict.get(character) != None:
                character_dict[character] += 1
            else:
                character_dict[character] = 1
        return character_dict

    def __list_of_nodes_from_counts(self):
        """
        Takes the dictionary of character counts and transforms it into a list of Node objects ordered by the count value of each character
        
        Complexity is O(u), where u = total unique characters, as one node is made for each.
        """
        
        nodes = []
        
        # get dictionary keys 
        keys = self.counts.keys()
        
        for character in keys:
            
            # make a new node and add it to the list of nodes
            new_node = self.Huffman_Node(character, self.counts.get(character))
            nodes.append(new_node)
        
        #returns complete list of nodes
        return nodes

    def __place_nodes_in_tree(self):
        """
        Organises the list of nodes into a binary tree structure according to principles of Huffman encoding. 
        
        This function will be called 2u-1 times, because a binary tree with u leaf nodes has (by definition) at most 2u-1 nodes total.
        
        Each call to the function involves calling sorted(). Sorted() uses the Timsort algorithm, which has a worst case O(u log u).

        This means complexity for this function exceeds O(n^2). This isn't ideal. But as huffman encoding requires both a binary tree, and re-sort of the originating list before each node is made, there is little scope for improvement.

        Again, as the maximum value of u in this encoding is 127, this was considered adequate.

        """
        
        while len(self.nodes) > 1:
            
            # sort nodes by count of occurences in original message
            self.nodes = sorted(self.nodes, key=lambda x:x.count)

            # code two least frequent letter nodes to 0 and 1
            self.nodes[0].code = 0
            self.nodes[1].code = 1
        
            # create a parent node to represent the two nodes combined
            combined_node = self.Huffman_Node(
                
                # combine details of child nodes to create parent node
                self.nodes[0].character + self.nodes[1].character,
                self.nodes[0].count + self.nodes[1].count,
                
                # point parent node to two child nodes
                self.nodes[0],
                self.nodes[1],
            )        
            
            # remove two smallest nodes from list structure
            self.nodes.pop(1)
            self.nodes.pop(0)

            # add combined node in their place
            self.nodes.append(combined_node)
        
        # when only the root node remains in the list, replace list with root node
        self.nodes = self.nodes[0]
        
        #root node is coded as 1 because Python strips leading 0s in binary
        self.nodes.code = "1"

    def get_codes_from_tree(self, node=None, code=""):
        """
        This module is called recursively to generate codes by traversing the tree that's been made.
        It stores the codes generated in the class' "encoding table" attribute, which is a Python dictionary.
        
        I chose to represent the encoding table as a dictionary, rather than a tree, because built in types will be more familiar to anyone else who needs to maintain this code. The syntax for travering and reordering dictionaries is also simpler.
        
        Using a dictionary also gives benefits in terms of complexity, though these will be discussed in the decoding part of this program.

        Though using a tree to encode, and a table to decode does increase memory needs of the program, I decided this was worth it to make the code more maintainable. Also, as the maximum size of this table is 127 this felt like a small ask of most modern processors.

        This function has a complexity of O(2u-1), because that is how many nodes it will have to check in total.
        """

        # if no Node is specified, start from the root node
        if node == None:
            node = self.nodes
        
        # if this isn't the root node, combine the code of this node with its ancestor nodes' codes
        else:
            node.code = code + str(node.code)

        #if this is a 'combined' node, representing several characters, go further along the branch
        if len(node.character) != 1:
            if node.left != None:
                self.get_codes_from_tree(node.left, node.code)
            if node.right != None:
                self.get_codes_from_tree(node.right, node.code)
        
        #if this is a single character node, set the characters code
        else:
            self.encoding_table[node.character] = node.code
    
    def encode(self, string):
        """
        Uses the encoding table to translate the original string into a Huffman encoded string

        The endoding table is a dict, Python's implementation of a hash table. Look-up in hash tables has constant time, or O(1).

        Doing this same look-up in a tree would have a complexity equal to the height of the tree. If u is the number of unique characters in the tree, the height of the tree will be between log(u) and u-1. 

        Using a hash table means the complexity of encoding the entire length of the input string (n) is only O(n).
        If I had used a binary tree, complexity would be between O(log(u) * n) and O(un).

        int() is used to cast the generated string into binary, as without this the generated string would actually be several times larger than the message it was intended to compress. The syntax int(string, 2) just means 'read this string as if it was a binary code'.
        """
        # Change each character into the encoded version of itself.
        for character in self.encoding_table:
            string = string.replace(character, self.encoding_table[character])
        
        # Transform encoded string into actual binary
        string = int(string, 2)
        
        return string
    
    def get_decoding_function(self):
        """
        Returns a encoding function designed specifically for the message being sent.
        This means that the decoding function can be sent as a part of the message being sent.
        It also means that the recipient doesn't have to have the full code of the encoding function.

        Complexity is O(1), as the same objects are referenced and returned no matter what the input string was.
        """
        
        # declare encoding table within parent scope of nested "decoding_function"
        # keys/values are swapped so we can take advantage of the constant time of a dictionary lookup in decoding too
        encoding_table = {value:key for key, value in self.encoding_table.items()}
        
        def decoding_function(encoded):
            """Decodes a message using the table in the enclosing scope of the "get" method. Calls its subfunction once for every letter of the original message. Complexity is O(n)"""
            
            # turn integer representation of binary back into actual binary
            string = bin(encoded)
            
            # remove leading "0b" of Python's binary representation
            string = string[2:]
            
            # create empty string to hold decoded message
            decoded_string = ""

            def decode_next_letter(string):
                """
                Finds the shortest sequence from the begining of the string that matches an entry in the encoding table.

                Because I have used a hash table, not a tree, each look-up is in constant time, ie O(1). Complexity for this entire function is O(e), (where e is the length of the encoded string) because for every position in the encoded string, the algorithm searches the dictionary of keys and codes. Using a tree, complexity would have altered depending on how many unique letters were in the message (u). Best case scenario with a tree would have been O(e log(u)).

                The combined complexity of this function and its enclosing function is also O(e), as each position in the encoded string is considered only once. 

                """
                
                # Works through possible lengths for first character code
                for i in range(len(string)+1):
                    
                    # defines code as 'first i letters' of string
                    code = string[0:i]
                    
                    # check if that code is in the encoding table
                    if code in encoding_table:
                        return code, encoding_table[code]
                    else:
                        pass
            

            # decode the letters of the string until there are no more letters
            while len(string) > 0:
                
                #call decode function
                code, key = decode_next_letter(string)
                
                # add decoded character to decoded string
                decoded_string = decoded_string + key

                # remove decoded code from string
                string = string.replace(code, "", 1)
            
            return decoded_string

        # return unique decoding function 
        return decoding_function


    def __init__(self, string):

        # count the occurences of each character in the string
        self.counts = self.__count_of_characters_in_(string)
        
        # create a list of nodes using the counts just done
        self.nodes = self.__list_of_nodes_from_counts()
        
        # reorganise list into a tree structure
        self.__place_nodes_in_tree()

        # Create empty dictionary to hold character/code information
        self.encoding_table = {}

        # Traverse tree to get codes, place them into the empty dictionary 
        self.get_codes_from_tree()

        # encode string using those codes
        self.encoded_string = self.encode(string)

        # get decoding function unique to the encoding message
        self.decoding_function = self.get_decoding_function()
    
# I've written the above class with the assumption that it would be used as a module as a part of larger projects. 
# However, if the file is ran on its own, the program will run tests.
# These tests are explained below:
       
if __name__ == "__main__":

  samples = (
      "There is a spectre haunting europe, the spectre of communism.",
      "The worker must have bread, but she must have roses, too.",
      "The history of all hitherto existing society is the history of class struggles. Freeman and slave, patrician and plebeian, lord and serf, guildmaster and journeyman, in a word, oppressor and oppressed, stood in constant opposition to one another, carried on an uninterrupted, now hidden, now open fight, that each time ended, either in the revolutionary reconstitution of society at large, or in the common ruin of the contending classes.",
      "sphynx of black quartz judge my vow",
      )
  for sample in samples:
        
        # initiate Huffman Encoding object
        h = Huffman_encoding_maker(sample)

        # get encoded string from object
        encoded = h.encoded_string

        # get decoding function from object
        decoder = h.decoding_function

        # decode encoded string
        decoded = decoder(encoded)

        # get size of encoded and unencoded messages, for comparisson.
        size_of_sample = getsizeof(sample)
        size_of_encoded = getsizeof(encoded)
        
        # print information to CLI
        print("\n-----------------------------------------")
        print("\nThe original sample reads:")
        print(sample)
        print(f"\n The encoding table looks like:")
        for key, value in h.encoding_table.items():
            print(key + " : " + value)
        print("\nThe encoded binary (read as an int, to save space on the terminal) reads:")
        print(encoded)
        print("\nAfter decoding it reads:")
        print(decoded)
        print(
            f"\nThe size of the original message was {size_of_sample} bytes," \
            f"after encoding it is {size_of_encoded} bytes.")
        print(
            "The ratio of original:encoded is " \
            f"1:{round(size_of_encoded/size_of_sample, 2)}\n")
