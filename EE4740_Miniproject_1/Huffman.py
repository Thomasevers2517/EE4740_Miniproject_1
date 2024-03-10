import numpy as np
class Huffman:
    def __init__(self, distribution):
        # distribution is a dictionary of values and their probabilities
        self.distribution = distribution
        self.huff_tree = self.build_tree()
        self.codes = self.build_codes()


    def build_tree(self):
        nodes = []
        for value in self.distribution:
            nodes.append((self.distribution[value], value))
        nodes.sort(key=lambda x: x[0])
        while len(nodes) > 1:
            left = nodes.pop(0)
            right = nodes.pop(0)
            nodes.append((left[0] + right[0], left, right))
            nodes.sort(key=lambda x: x[0])
        return nodes[0]

    def build_codes(self):
        codes = {}
        def build_codes_rec(tree, code):
            if len(tree) == 2:
                codes[tree[1]] = code
            else:
                build_codes_rec(tree[1], code + '0')
                build_codes_rec(tree[2], code + '1')
                
        build_codes_rec(self.huff_tree, '')
        return codes

    def encode(self, data):
        encoded = ''
        for value in data:
            encoded += self.codes[value]
        bits_per_symbol = len(encoded) / len(data)
        return encoded, bits_per_symbol

    def decode(self, encoded):
        decoded = []
        tree = self.huff_tree
        for bit in encoded:
            if bit == '0':
                tree = tree[1]
            else:
                tree = tree[2]
            if len(tree) == 2:
                decoded.append(tree[1])
                tree = self.huff_tree
        decoded = np.array(decoded) 
        return decoded