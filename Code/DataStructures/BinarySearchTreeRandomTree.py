import random
from BinarySearchTree import BinarySearchTree
from InfiniteList import InfiniteList

__author__ = 'Phaina'

"""BinarySearchTreeRandomTree is a data structure that emulates a random BST."""


class BinarySearchTreeRandomTree(BinarySearchTree):
    def __init__(self, key, parsed_line, insert_type, merge_type, difficulty, parent=None, token=None, root=None,
                 base_list_content=None):
        """
        Emulate a random search tree. Make an InfiniteList object that holds all the tokens.
        Iterate through the layers, give each token a key and then insert the tokens with those keys into a BST.
        """
        if base_list_content:
            self.base_list = base_list_content
        else:
            self.base_list = InfiniteList(parsed_line, insert_type, merge_type, difficulty)
        super(BinarySearchTreeRandomTree, self).__init__(0, '', insert_type, merge_type, difficulty, token="yo", root=self)
        self.construct_tree()

    def clear(self):
        """
        Delete all attributes that exist, so that the BSTRT is completely clean.
        """
        self.left = None
        self.right = None
        self.above = None
        self.below = None
        self.depth = 0
        self.key = None
        self.token = None
        self.root = self
        self.parent = None
        self.length = 0
        tree_repr = []
        self.content = self.print_tree(tree_repr)
        self.focus = None
        self.annotations = {}
        self.supermodels = []

    def list_to_key_dict(self, layer):
        """
        Given an infinite list layer (2D), give each token a key and return that dict.

        :return: Dictionary with keys for every token
        """
        dct = {}
        for i, token in enumerate(layer):
            dct[token] = i
        return dct

    def construct_tree(self):
        """
        From base_list and the dict of keys, construct a random BST for every layer.
        """
        self.clear()
        for i, layer in enumerate(self.base_list.content):
            node = self.root
            if i > 0:
                for j in range(i):
                    node = node.below
            dct_keys = self.list_to_key_dict(layer)
            seen_tokens = []
            while dct_keys:
                next_token = random.choice(dct_keys.keys())
                if next_token not in seen_tokens:
                    self.insert_node(dct_keys[next_token], next_token)
                    self.focus = self.find_node(next_token)
                    seen_tokens.append(next_token)
                    dct_keys.pop(next_token)

    def insert(self, parsed_line):
        """
        Every time an insert comes, insert it into InfiniteList object, then construct a new random_tree

        :param parsed_line: The parsed line that is to be inserted.
        :return: True/False depending on whether insert worked
        """
        self.base_list.insert(parsed_line)
        self.construct_tree()
        return True

    def merge(self, data_structure, parsed_line):
        """
        Merge with another BSTRT on basis of parsed line. Merging the base_lists, then constructing a new BSTRT.

        :param data_structure: The other BSTRT
        :param parsed_line: The parsed line on which basis merge happens
        :return: merged object, if it worked
        """
        new_base_list = InfiniteList('', self.insert_type, self.merge_type, self.difficulty,
                                      self.base_list.merge(data_structure.base_list, parsed_line))
        new_random_tree = BinarySearchTreeRandomTree(0, '', self.insert_type, self.merge_type, self.difficulty,
                                                     base_list_content=new_base_list)
        return new_random_tree, new_random_tree.focus
