import copy
from BinarySearchTree import BinarySearchTree

__author__ = 'Phaina'

"""BinarySearchTreeLimitedDepth is a binary search tree with limited depth."""


class BinarySearchTreeLimitedDepth(BinarySearchTree):
    def __init__(self, key, parsed_line, insert_type, merge_type, difficulty, limit, parent=None, token=None, root=None):
        self.limit = limit
        super(BinarySearchTreeLimitedDepth, self).__init__(key, parsed_line, insert_type, merge_type, difficulty,
                                                           parent, token, root)

    def insert(self, parsed_line):
        """
        Given a parsed line, insert it into the BST, but only if depth limit is not surpassed.

        :param parsed_line: The parsed line to insert into BST.
        :return: True/False depending on whether insert worked
        """
        deepcopy_of_self = copy.deepcopy(self)
        super(BinarySearchTreeLimitedDepth, deepcopy_of_self).insert(parsed_line)
        depth_after_insert = deepcopy_of_self.root.depth
        if depth_after_insert <= self.limit:
            super(BinarySearchTreeLimitedDepth, self).insert(parsed_line)
            return True
        else:
            return False

    def merge(self, data_structure, parsed_line):
        """
        Merge this BST of limited depth with another BST of limited depth, but only if their collective depth doesn't
        surpass depth limit.

        :param data_structure: The other BSTLD to merge with.
        :param parsed_line: The parsed line that is the basis for the merge
        :return: merged_object if merge worked
        """
        merged_object = super(BinarySearchTreeLimitedDepth, self).merge(data_structure, parsed_line)
        if merged_object[0].root.depth <= self.limit:
            return merged_object
        else:
            pass
