"""
Why put things into a class?
- cleaner name space
- can be deleted after the fact
- makes it easy to import from this module to use inside another program, which is more likely use case -DRY etc



On binary
- The string of 1s and 0s generated by this function is of the 'string' type.
    -this is built on an array (ie, you can index into a string)
    -and the contents are assumed to be alpha-numeric characters. ie, not the binary positions 0 or 1, but the Asci encoded characters for 0 or 1.
    -the process of translating each individual character into a string of 0 and 1s, and then translating each of those 0s and 1s into an ascii character, and then storing all of those in a larger array, actually inflates rather than compresses the size of the message in memory.
    - the quickest way to convert this string representation of binary into actual binary is to cast the string to an integer and specify base 2 (ie binary) as the conversion system.
    - added benefit that a integer rendering of the binary information takes up much less room in the terminal.

"""

# imports
from sys import getsizeof #used for size comparison when testing the function


class huffman_encoding_maker:
    """
    This class works as a container for all the different functions that are required to encode using the Huffman schema.
    It takes the string to be encoded as its only argument, and returns two objects; the encoded string, and a function for decoding that string.
    Overall complexity is XXXXXXX, which is calculated by summing the complexities outlined for each subfunction within the class.
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

        Each comparison involves reference to two different structures, which means that in terms of look-up, the complexity is O(2n)"""

        character_dict = {}
        for character in string:
            if character_dict.get(character) != None:
                character_dict[character] += 1
            else:
                character_dict[character] = 1
        return character_dict

    def __list_of_nodes_from_counts(self):
        """Takes the dictionary of character counts and transforms it into a list of Node objects ordered by the count value of each character"""
        
        nodes = []
        
        # sort dictionary of character counts  
        sorted_keys = sorted(self.counts)
        
        for character in sorted_keys:
            
            # make a new node and add it to the list of nodes
            new_node = self.Huffman_Node(character, self.counts.get(character))
            nodes.append(new_node)
        
        #returns complete list of nodes
        return nodes

    def __place_nodes_in_tree(self):
        """Organises the list of nodes into a binary tree structure according to principles of Huffman encoding."""
        
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
        """This module is called recursively to generate codes by traversing the tree that's been made.
        It stores the codes generated in the class' "encoding table" attribute, which is a Python dictionary.
        I chose to represent the encoding table as a dictionary, rather than a tree, because built in types will be more familiar to anyone else who needs to maintain this code. The syntax for travering and reordering dictionaries is also simpler.
        Though using a tree to encode, and a table to decode does increase memory needs of the program, I decided this was worth it to make the code more maintainable. Also, as the maximum size of this table is 127 (this being the number of ASCII characters) this felt like a small ask of most modern processors.

        talk about left vs right, depth first
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
        """
        
        # declare encoding table within parent scope of "decoding_function"
        encoding_table = self.encoding_table
        
        def decoding_function(encoded):
            
            # turn integer representation of binary back into actual binary
            string = bin(encoded)
            
            # remove leading "0b" of Python's binary representation
            string = string[2:]
            
            # create empty string to hold decoded message
            decoded_string = ""

            def decode_next_letter(string):
                """
                Finds the shortest sequence from the begining of the string that matches an entry in the encoding table.
                """
                
                # Works through possible lengths for first character code
                for i in range(len(string)+1):
                    
                    # defines code as 'first i letters' of string
                    code = string[0:i]
                    
                    # checks prospective code against encoding table defined in enclosing scope 
                    for key, value in encoding_table.items():
                        
                        # if the code is in the table, return 
                        if code == value:
                            return code, key
                        else:
                            pass
            

            while len(string) > 0:
                code, key = decode_next_letter(string)
                decoded_string = decoded_string + key
                string = string.replace(code, "", 1)
            
            return decoded_string

        return decoding_function


    def __init__(self, string):

        self.counts = self.__count_of_characters_in_(string)
        self.nodes = self.__list_of_nodes_from_counts()
        self.__place_nodes_in_tree()

        self.encoding_table = {}
        self.get_codes_from_tree()

        
        self.encoded_string = self.encode(string)
        self.decoding_function = self.get_decoding_function()
    
        
if __name__ == "__main__":

  samples = (
      "There is a spectre haunting europe, the spectre of communism.",
      "The worker must have bread, but she must have roses, too.",
      "The history of all hitherto existing society is the history of class struggles. Freeman and slave, patrician and plebeian, lord and serf, guildmaster and journeyman, in a word, oppressor and oppressed, stood in constant opposition to one another, carried on an uninterrupted, now hidden, now open fight, that each time ended, either in the revolutionary reconstitution of society at large, or in the common ruin of the contending classes.",
      "sphynx of black quartz judge my vow",
      )
  for sample in samples:
        h = huffman_encoding_maker(sample)
        size_of_sample = getsizeof(sample)
        encoded = h.encoded_string
        size_of_encoded = getsizeof(encoded)
        decoded = h.decoding_function(encoded)
        print("\n-----------------------------------------")
        print("\nThe original sample reads:")
        print(sample)
        print(f"\n The encoding table looks like:")
        print(h.encoding_table)
        print("\nThe encoded version reads:")
        print(encoded)
        print("\nAfter decoding it reads:")
        print(decoded)
        print(
            f"\nThe size of the original message was {size_of_sample} bytes," \
            f"after encoding it is {size_of_encoded} bytes.")
        print(
            "The ratio of original:encoded is " \
            f"1:{round(size_of_encoded/size_of_sample, 2)}")
    
    


