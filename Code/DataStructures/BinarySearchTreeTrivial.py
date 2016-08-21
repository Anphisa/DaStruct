# pylint: disable=line-too-long, fix-me

from BinarySearchTree import BinarySearchTree

__author__ = 'Phaina'

"""BinarySearchTreeTrivial is a data structure that consists of a binary search tree that is in insert trivial,
i.e. it will insert without rotation, and therefore have certain problems when evaluating conclusions."""


class BinarySearchTreeTrivial(BinarySearchTree):
    """
    Only differs from "normal" BinarySearchTree in insert procedure.
    """
    def __init__(self, key, parsed_line, insert_type, merge_type, difficulty, parent=None, token=None, root=None):
        super(BinarySearchTreeTrivial, self).__init__(key, parsed_line, insert_type, merge_type, difficulty,
                                                      parent, token, root)

    def insert_node(self, key, token, above=False, below=False):
        """
        Insert a new node into BST.

        :param key: The key with which to insert
        :param token: The token to insert
        """
        if self.token:
            # Left
            if key < self.key:
                if self.left:
                    self.left.insert_node(key, token)
                else:
                    self.left = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                 parent=self, token=token, root=self.root)
                    self.root.length += 1
            # Right
            elif key > self.key:
                if self.right:
                    self.right.insert_node(key, token)
                else:
                    self.right = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                  parent=self, token=token, root=self.root)
                    self.root.length += 1
            elif key == self.key:
                if above and self.above:
                    self.above.insert_node(key, token)
                else:
                    self.above = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                  token=token, root=self.root)
                if below and self.below:
                    self.below.insert_node(key, token)
                else:
                    self.below = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                  token=token, root=self.root)
        # This is the root node
        else:
            self.token = token
            self.key = key
            self.root = self
            self.root.length = 1

    def insert(self, parsed_line):
        """
        Insert a parsed line into this BST.

        :param parsed_line: The parsed line to be inserted into BST

        :return True/False depending on whether insert worked
        """
        if self.find(parsed_line.first_token) or self.find(parsed_line.second_token):
            if self.find(parsed_line.first_token):
                # In this case the relation has to be inverted, because it's always LO rel RO.
                parsed_line.invert()
                located_object = self.find_node(parsed_line.first_token)
                reference_object = parsed_line.second_token
            elif self.find(parsed_line.second_token):
                located_object = self.find_node(parsed_line.second_token)
                reference_object = parsed_line.first_token
            if parsed_line.relation == "left" or parsed_line.relation == "right":
                key = located_object.choose_key(self.insert_type, reference_object, parsed_line.relation,
                                                located_object.key)
                above_or_below = self.above_or_below(located_object)
                if above_or_below:
                    level = self.root
                    # Current level is above the level where insert should take place
                    if above_or_below.startswith("a"):
                        for i in range(len(above_or_below)):
                            level = level.below
                    # Current level is below the level where insert should take place
                    elif above_or_below.startswith("b"):
                        for i in range(len(above_or_below)):
                            level = level.above
                    level.insert_node(key, reference_object)
                else:
                    self.insert_node(key, reference_object)
            elif parsed_line.relation == "above":
                if self.insert_type == "fff":
                    node = located_object
                    while node.above:
                        node = node.above
                    new_layer = BinarySearchTreeTrivial(node.key, "", self.insert_type, self.merge_type, self.difficulty,
                                                 token=reference_object, root=located_object.root)
                    nodes_to_give_above_to = [located_object.root]
                    for node in nodes_to_give_above_to:
                        if node.right:
                            nodes_to_give_above_to.append(node.right)
                        if node.left:
                            nodes_to_give_above_to.append(node.left)
                        node.above = new_layer
                if self.insert_type == "ff":
                    new_layer = BinarySearchTreeTrivial(located_object.key, "", self.insert_type, self.merge_type,
                                                 self.difficulty, token=reference_object, root=located_object.root)
                    if located_object.above:
                        prev_above = located_object.above
                        new_layer.above = prev_above
                        nodes_to_give_above_to = [located_object.root]
                        for node in nodes_to_give_above_to:
                            if node.right:
                                nodes_to_give_above_to.append(node.right)
                            if node.left:
                                nodes_to_give_above_to.append(node.left)
                            node.above = new_layer
                    else:
                        located_object.above = new_layer
                        nodes_to_give_above_to = [located_object.root]
                        for node in nodes_to_give_above_to:
                            if node.right:
                                nodes_to_give_above_to.append(node.right)
                            if node.left:
                                nodes_to_give_above_to.append(node.left)
                            node.above = new_layer
            elif parsed_line.relation == "below":
                if self.insert_type == "fff":
                    node = located_object
                    while node.below:
                        node = node.below
                    new_layer = BinarySearchTreeTrivial(node.key, "", self.insert_type, self.merge_type, self.difficulty,
                                                 token=reference_object, root=located_object.root)
                    nodes_to_give_below_to = [located_object.root]
                    for node in nodes_to_give_below_to:
                        if node.right:
                            nodes_to_give_below_to.append(node.right)
                        if node.left:
                            nodes_to_give_below_to.append(node.left)
                        node.below = new_layer
                if self.insert_type == "ff":
                    new_layer = BinarySearchTreeTrivial(located_object.key, "", self.insert_type, self.merge_type,
                                                 self.difficulty, token=reference_object, root=located_object.root)
                    if located_object.below:
                        prev_below = located_object.below
                        new_layer.below = prev_below
                        nodes_to_give_below_to = [located_object.root]
                        for node in nodes_to_give_below_to:
                            if node.right:
                                nodes_to_give_below_to.append(node.right)
                            if node.left:
                                nodes_to_give_below_to.append(node.left)
                            node.below = new_layer
                    else:
                        located_object.below = new_layer
                        nodes_to_give_below_to = [located_object.root]
                        for node in nodes_to_give_below_to:
                            if node.right:
                                nodes_to_give_below_to.append(node.right)
                            if node.left:
                                nodes_to_give_below_to.append(node.left)
                            node.below = new_layer
        else:
            # No token was found, first token will be the root node
            self.insert_node(0, parsed_line.first_token)
            self.root = self
            parsed_line.invert()
            key = self.choose_key(self.insert_type, parsed_line.second_token, parsed_line.relation, 0)
            self.insert_node(key, parsed_line.second_token)
        return True