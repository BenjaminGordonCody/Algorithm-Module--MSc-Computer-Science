"""
Why put things into a class?
- clearner name space
- can be deleted after the fact

Why return a function?
- 

"""


class huffman_encoding_maker:
    """
    This class works as a container for all the different functions that are required to encode using the Huffman schema.
    It takes the string to be encoded as its only argument, and returns two objects; the encoded string, and a function for decoding that string.
    Overall complexity is XXXXXXX, which is calculated by summing the complexities outlined for each subfunction within the class.
    """

    class Huffman_Node:
        def __init__(
            self, character, count, left=None, right=None, code=None):

            self.character = character
            self.count = count

            self.left = left
            self.right = right

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
        sorted_keys = sorted(self.counts)
        for character in sorted_keys:
            new_node = self.Huffman_Node(character, self.counts.get(character))
            nodes.append(new_node)
        return nodes

    def __place_nodes_in_tree(self):
        while len(self.nodes) > 1:
            self.nodes = sorted(self.nodes, key=lambda x:x.count)

            self.nodes[0].code = 0
            self.nodes[1].code = 1
        
            combined_node = self.Huffman_Node(
                self.nodes[0].character + self.nodes[1].character,
                self.nodes[0].count + self.nodes[1].count,
                self.nodes[0],
                self.nodes[1],
            )        
            
            self.nodes.pop(1)
            self.nodes.pop(0)
            self.nodes.append(combined_node)
        
        self.nodes = self.nodes[0]
        self.nodes.code = ""

    def get_codes_from_tree(self, node=None, code=""):
        if node == None:
            node = self.nodes
        else:
            node.code = code + str(node.code)

        if len(node.character) != 1:
            if node.left != None:
                self.get_codes_from_tree(node.left, node.code)
            if node.right != None:
                self.get_codes_from_tree(node.right, node.code)
        else:
            self.encoding_table[node.character] = node.code
    
    def encode(self, string):
        for character in self.encoding_table:
            string = string.replace(character, self.encoding_table[character])
        return string
    
    def get_decoding_function(self):
        encoding_table = self.encoding_table
        
        def decoding_function(string):
            decoded_string = ""

            def decode_next_letter(string):
                for i in range(len(string)+1):
                    code = string[0:i]
                    
                    for key, value in encoding_table.items():
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
        # return encoded_string, decoding_function
    
        
if __name__ == "__main__":

    sample = "there is a spectre haunting europe, the spectre of communism"
    h = huffman_encoding_maker(sample)
    encoded = h.encoded_string
    decoded = h.decoding_function(encoded)
    print(sample + "\n" + encoded + "\n" +  decoded)
    
    


