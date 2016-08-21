import copy
from Helpers import MyExceptions
from DataStructure import DataStructure
from InfiniteList import InfiniteList

__author__ = 'Phaina'

"""BinarySearchTree is a data structure that consists of a binary search tree."""


class BinarySearchTree(DataStructure):
    def __init__(self, key, parsed_line, insert_type, merge_type, difficulty, parent=None, token=None, root=None):
        """ Root node constructor

        :param key: The key with which this token should be saved
        :param parsed_line: The parsed_line to be saved from this node
        :param token: The token to be saved (instead of parsed_line)
        :param parent: The parent of this BST (the initiator, so to say)
        :param root: The total root of BST, the very first node

        :var self.left: Left subtree
        :var self.right: Right subtree
        :var self.above: Above subtree
        :var self.below: Below subtree
        :var self.depth: The depth of the tree
        """
        super(BinarySearchTree, self).__init__()

        self.left = None
        self.right = None
        self.above = None
        self.below = None
        self.depth = 0
        self.key = key
        self.token = None
        self.root = root
        self.parent = parent
        self.length = 0
        tree_repr = []
        self.content = self.print_tree(tree_repr)
        self.difficulty = difficulty
        self.insert_type = insert_type
        self.merge_type = merge_type
        self.focus = self.root
        self.focus_change_direction = None
        self.annotations = {}
        self.supermodels = []
        if not parsed_line and token:
            self.token = token
        elif parsed_line:
            self.token = None
            self.insert(parsed_line)
            if parsed_line.focus:
                if len(parsed_line.focus) == 1:
                    if parsed_line.focus == parsed_line.first_token:
                        self.focus = self.find_node(parsed_line.second_token)
                        self.difficulty.focus_key_distance = abs(self.focus.key - self.find_node(parsed_line.first_token).key)
                    else:
                        self.focus = self.find_node(parsed_line.first_token)
                        self.difficulty.focus_key_distance = abs(self.focus.key - self.find_node(parsed_line.second_token).key)
                    if self.focus is None:
                        raise MyExceptions.FocusError("InfiniteList.create_from_parsed_line focus went to None")
                    # Save first direction taken for measuring direction changes
                    if parsed_line.relation == "left":
                        self.focus_change_direction = "left"
                    if parsed_line.relation == "right":
                        self.focus_change_direction = "right"
                    if parsed_line.relation == "above":
                        self.focus_change_direction = "down"
                    if parsed_line.relation == "below":
                        self.focus_change_direction = "up"
                else:
                    raise MyExceptions.FocusError("Parsed_line.focus had more than one element!")

    def __len__(self):
        return self.root.length

    def print_tree(self, tree_repr):
        if self.above:
            tree_repr.append(self.above.print_tree(tree_repr))
        if self.left:
            tree_repr.append(self.left.print_tree(tree_repr))
        tree_repr.append(self.token)
        if self.right:
            tree_repr.append(self.right.print_tree(tree_repr))
        if self.below:
            tree_repr.append(self.below.print_tree(tree_repr))
        return tree_repr

    def __str__(self):
        return str(self.print_tree([]))

    def forget(self, token):
        """
        Forget a given token, i.e. replace this token with string 'forgotten'.

        :param token: The token that should be forgotten.
        """
        node_of_token = self.find_node(token)
        node_of_token.token = 'forgotten'

    def insert_node(self, key, token, above=False, below=False):
        """
        Insert a new node into BST.

        :param key: The key with which to insert
        :param token: The token to insert
        """
        if self.token:
            # fff goes as far to the left/to the right as required (where there is no subtree yet) and opens a
            # new subtree there.
            if self.insert_type == "fff":
                # Left
                if key < self.key:
                    if self.left:
                        self.left.insert_node(key, token)
                    else:
                        self.left = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                     parent=self, token=token, root=self.root)
                        self.root.length += 1
                        if len(self.left.path_start_to_node()) > self.root.depth:
                            self.root.depth += len(self.left.path_start_to_node()) - self.root.depth
                            self.difficulty.BST_depth = self.root.depth
                # Right
                elif key > self.key:
                    if self.right:
                        self.right.insert_node(key, token)
                    else:
                        self.right = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                      parent=self, token=token, root=self.root)
                        self.root.length += 1
                        if len(self.right.path_start_to_node()) > self.root.depth:
                            self.root.depth += len(self.right.path_start_to_node()) - self.root.depth
                            self.difficulty.BST_depth = self.root.depth

            # ff replaces subtrees (if something "comes in the middle", e.g. "A left B", "A left C", then the right
            # subtree of A is first B, then replaced by C) if necessary, if the place is not yet taken,
            # opens a new subtree at that position
            if self.insert_type == "ff":
                # Left
                if key < self.key:
                    if self.left:
                        if key > self.left.key:
                            tmp_left = self.left
                            self.left = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                         token=token, root=self.root, parent=self)
                            self.left.left = tmp_left
                            self.root.length += 1
                            if len(self.left.left.path_start_to_node()) > self.root.depth:
                                self.root.depth += len(self.left.left.path_start_to_node()) - self.root.depth
                                self.difficulty.BST_depth = self.root.depth
                        else:
                            self.left.insert_node(key, token)
                    else:
                        self.left = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                     parent=self, token=token, root=self.root)
                        self.root.length += 1
                        if len(self.left.path_start_to_node()) > self.root.depth:
                            self.root.depth += len(self.left.path_start_to_node()) - self.root.depth
                            self.difficulty.BST_depth = self.root.depth
                # Right
                elif key > self.key:
                    if self.right:
                        if key < self.right.key:
                            tmp_right = self.right
                            self.right = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                          token=token, root=self.root, parent=self)
                            self.right.right = tmp_right
                            self.root.length += 1
                            if len(self.right.right.path_start_to_node()) > self.root.depth:
                                self.root.depth += len(self.right.right.path_start_to_node()) - self.root.depth
                                self.difficulty.BST_depth = self.root.depth
                        else:
                            self.right.insert_node(key, token)
                    else:
                        self.right = BinarySearchTree(key, '', self.insert_type, self.merge_type, self.difficulty,
                                                      parent=self, token=token, root=self.root)
                        self.root.length += 1
                        if len(self.right.path_start_to_node()) > self.root.depth:
                            self.root.depth += len(self.right.path_start_to_node()) - self.root.depth
                            self.difficulty.BST_depth = self.root.depth
        # This is the root node, this tree has no token yet
        else:
            self.token = token
            self.key = key
            self.root = self
            self.root.length = 1
            self.depth = 1
            self.difficulty.BST_depth = self.depth

    def insert(self, parsed_line):
        """
        Insert a parsed line into this BST.

        :param parsed_line: The parsed line to be inserted into BST

        :return True/False depending on whether insert worked
        """
        if self.find(parsed_line.first_token) or self.find(parsed_line.second_token):
            if self.find(parsed_line.first_token):
                # In this case the relation has to be inverted, because it's always LO rel RO. (In the tree, LO is
                # inserted first, then RO accordingly. E.g. "A left B" will become A -> B)
                parsed_line.invert()
                located_object = self.find_node(parsed_line.first_token)
                reference_object = parsed_line.second_token
            elif self.find(parsed_line.second_token):
                located_object = self.find_node(parsed_line.second_token)
                reference_object = parsed_line.first_token

            # Focus changes
            if self.focus != located_object:
                self.difficulty.focus_move_ops += 1
                # Now we need to see if the node currently in focus is a parent node of located object
                if self.find_node(self.focus.token).find_node_right_and_left_only(located_object.token):
                    # Focus node is a parent node, so its path will be shorter than that of located object node,
                    # the focus distance is the difference in path length.
                    moved_focus_by = len(located_object.path_start_to_node()) - len(self.focus.path_start_to_node())
                # Or, the other way round, whether located object is a parent node of the node currently in focus
                elif self.find_node(located_object.token).find_node_right_and_left_only(self.focus.token):
                    moved_focus_by = len(self.focus.path_start_to_node()) - len(located_object.path_start_to_node())
                # No node is a parent node of the other, they need to move "over root node", i.e. the path has to be
                # travelled back to root node (which is the len of path) for both, the sum of which is their distance
                else:
                    moved_focus_by = len(self.focus.path_start_to_node()) + len(located_object.path_start_to_node()) \
                                     + len(self.focus.above_or_below(located_object))
                self.difficulty.focus_move_distance += moved_focus_by
                self.difficulty.focus_key_distance += abs(self.focus.key - located_object.key)
                above_or_below = located_object.above_or_below(self.focus)
                if not above_or_below and self.focus.key < located_object.key:
                    focus_direction = "right"
                elif not above_or_below and self.focus.key > located_object.key:
                    focus_direction = "left"
                elif self.focus.path_start_to_node() == located_object.path_start_to_node() and above_or_below.startswith("a"):
                    focus_direction = "above"
                elif self.focus.path_start_to_node() == located_object.path_start_to_node() and above_or_below.startswith("b"):
                    focus_direction = "below"
                else:
                    focus_direction = "various_directions"
                if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                    self.focus_change_direction = focus_direction
                    self.difficulty.focus_direction_changes += 1
                self.focus = located_object

            # Annotate not absolutely obviously inserted tokens (where the position is just free, it's obvious,
            # otherwise it's a question of ff/fff, which is not strictly obvious), so they can be variated in MVP
            indeterminate = False
            if parsed_line.relation == "left":
                # Either the position to the left of the located object is taken or the located object is the right
                # child of its parent (and thereby the position "above it" that would also fulfill requirements
                # is taken)
                if located_object.parent and located_object.parent.right == located_object or located_object.left:
                    indeterminate = True
            if parsed_line.relation == "right":
                if located_object.parent and located_object.parent.left == located_object or located_object.right:
                    indeterminate = True
            if parsed_line.relation == "below":
                if located_object.below:
                    indeterminate = True
            if parsed_line.relation == "above":
                if located_object.above:
                    indeterminate = True
            if indeterminate:
                if located_object.token == parsed_line.second_token:
                    self.annotate(located_object.token, parsed_line.relation, reference_object)
                else:
                    # Because we inverted the relationship above for the ones were we knew the first token
                    parsed_line.invert()
                    self.annotate(located_object.token, parsed_line.relation, reference_object)
                    parsed_line.invert()
            # If the LO is itself ambiguous in position, it might need to be moved in the MVP.
            # Therefore it'll be annotated with new information so that it doesn't get moved/switched wrongly.
            if located_object.token in self.annotations:
                if located_object.token == parsed_line.second_token:
                    parsed_line.invert()
                    self.annotations[located_object.token].append((parsed_line.relation, reference_object))
                    parsed_line.invert()
                else:
                    self.annotations[located_object.token].append((parsed_line.relation, reference_object))

            if parsed_line.relation == "left" or parsed_line.relation == "right":
                key = located_object.choose_key(self.insert_type, reference_object, parsed_line.relation,
                                                located_object.key)
                # Move to the layer were insert should take place (not necessarily on base level, maybe above/below
                # root node)
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
                    # Move to the very above, then make a new node "at the abovest"
                    while node.above:
                        node = node.above
                    new_layer = BinarySearchTree(node.key, "", self.insert_type, self.merge_type, self.difficulty,
                                                 token=reference_object, root=located_object.root)
                    # Move to the layer where we just inserted a node, but there to the node immediately above/below
                    # root node
                    removed_from_root = node.above_or_below(located_object.root)
                    root = located_object.root
                    for removal in removed_from_root:
                        if removal == "a":
                            root = root.above
                        if removal == "b":
                            root = root.below
                    # And then give the new above to all right/left nodes on this layer
                    nodes_to_give_above_to = [root]
                    for node in nodes_to_give_above_to:
                        if node.right:
                            nodes_to_give_above_to.append(node.right)
                        if node.left:
                            nodes_to_give_above_to.append(node.left)
                        node.above = new_layer
                    located_object.root.length += 1
                if self.insert_type == "ff":
                    new_layer = BinarySearchTree(located_object.key, "", self.insert_type, self.merge_type,
                                                 self.difficulty, token=reference_object, root=located_object.root)
                    if located_object.above:
                        # Here, again, move new layer between this and already existing above layer
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
                    located_object.root.length += 1
            elif parsed_line.relation == "below":
                if self.insert_type == "fff":
                    node = located_object
                    # Move the the very below, add new layer below that
                    while node.below:
                        node = node.below
                    new_layer = BinarySearchTree(node.key, "", self.insert_type, self.merge_type, self.difficulty,
                                                 token=reference_object, root=located_object.root)
                    removed_from_root = node.above_or_below(located_object.root)
                    root = located_object.root
                    for removal in removed_from_root:
                        if removal == "a":
                            root = root.above
                        if removal == "b":
                            root = root.below
                    # Then give all nodes on that layer the "below" link
                    nodes_to_give_below_to = [root]
                    for node in nodes_to_give_below_to:
                        if node.right:
                            nodes_to_give_below_to.append(node.right)
                        if node.left:
                            nodes_to_give_below_to.append(node.left)
                        node.below = new_layer
                    located_object.root.length += 1
                if self.insert_type == "ff":
                    new_layer = BinarySearchTree(located_object.key, "", self.insert_type, self.merge_type,
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
                    located_object.root.length += 1

            # Difficulty measure difficulty.focus_move_distance is updated by the distance that focus had to move
            # self.focus is also updated to new focus object
            reference_node = self.find_node(reference_object)
            if self.focus != reference_node:
                self.difficulty.focus_move_ops += 1
                # Now we need to see if the node currently in focus is a parent node of located object
                if self.find_node(self.focus.token).find_node_right_and_left_only(reference_node.token):
                    # Focus node is a parent node, so its path will be shorter than that of located object node,
                    # the focus distance is the difference in path length.
                    moved_focus_by = len(reference_node.path_start_to_node()) - len(self.focus.path_start_to_node())
                # Or, the other way round, whether located object is a parent node of the node currently in focus
                elif self.find_node(reference_node.token).find_node_right_and_left_only(self.focus.token):
                    moved_focus_by = len(self.focus.path_start_to_node()) - len(reference_node.path_start_to_node())
                # No node is a parent node of the other, they need to move "over root node", i.e. the path has to be
                # travelled back to root node (which is the len of path) for both, the sum of which is their distance
                else:
                    moved_focus_by = len(self.focus.path_start_to_node()) + len(reference_node.path_start_to_node()) \
                                     + len(self.focus.above_or_below(located_object))
                self.difficulty.focus_move_distance += moved_focus_by
                self.difficulty.focus_key_distance += abs(self.focus.key - reference_node.key)
                above_or_below = reference_node.above_or_below(self.focus)
                if not above_or_below and self.focus.key < reference_node.key:
                    focus_direction = "right"
                elif not above_or_below and self.focus.key > reference_node.key:
                    focus_direction = "left"
                elif self.focus.path_start_to_node() == reference_node.path_start_to_node() and above_or_below.startswith("a"):
                    focus_direction = "above"
                elif self.focus.path_start_to_node() == reference_node.path_start_to_node() and above_or_below.startswith("b"):
                    focus_direction = "below"
                else:
                    focus_direction = "various_directions"
                if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                    self.focus_change_direction = focus_direction
                    self.difficulty.focus_direction_changes += 1
                self.focus = reference_node
        else:
            # No token was found (i.e. none of those tokens is already present in BST),
            # first token will be the root node
            self.insert_node(0, parsed_line.first_token)
            self.root = self
            # Inverting because we already inserted first token, the other one is now differently related.
            # E.g. "A left B", we inserted A, so now B has to go to the right of A
            parsed_line.invert()
            if parsed_line.relation == "left" or parsed_line.relation == "right":
                key = self.choose_key(self.insert_type, parsed_line.second_token, parsed_line.relation, 0)
                self.insert_node(key, parsed_line.second_token)
            elif parsed_line.relation == "above":
                self.above = BinarySearchTree(0, "", self.insert_type, self.merge_type,
                                              self.difficulty, token=parsed_line.second_token, root=self.root)
                self.focus_change_direction = "down"
                self.focus = self.above
            elif parsed_line.relation == "below":
                self.below = BinarySearchTree(0, "", self.insert_type, self.merge_type,
                                              self.difficulty, token=parsed_line.second_token, root=self.root)
                self.focus_change_direction = "up"
                self.focus = self.below

        # So supermodels are up to date as well
        if self.supermodels:
            for model in self.supermodels:
                model.insert(parsed_line)
        # Returns true because nothing can really go wrong here, no bounds
        return True

    def choose_key(self, insert_type, token_to_be_inserted, relation, existing_key):
        """
        For a token to be inserted into BST, determine its correct key.

        :param insert_type: The insert type (relevant for determining key)
        :param token_to_be_inserted: The token to be inserted into BST
        :param relation: The relation to a node which already is in the BST
        :param existing_key: The key to the node that is already in the BST and related to the token
        :return: key value to be used
        """
        if relation == "left":
            if insert_type == "fff":
                node = self.root
                while node.left:
                    node = node.left
                # Because in fff, we want the leftmost possible position & key
                return node.key - 1
            elif insert_type == "ff":
                if self.left:
                    # So the key is in between this key and former left key
                    return (self.key + self.left.key) / 2.
                elif self.parent:
                    # So it's in between this key and parent's key
                    return (self.key + self.parent.key) / 2. + .1
                else:
                    return self.key - 1
        if relation == "right":
            if insert_type == "fff":
                node = self.root
                while node.right:
                    node = node.right
                # Because in fff, we want the rightmost possible position & key
                return node.key + 1
            elif insert_type == "ff":
                if self.right:
                    return (self.key + self.right.key) / 2.
                elif self.parent:
                    return (self.key + self.parent.key) / 2. + 1
                else:
                    return self.key + 1

    def find_key(self, token):
        """
        Find a token in this BST and return its key. (DFS)

        :param token: The token to be found
        :return: Key of a token or None
        """
        if self.token == token:
            return self.key
        if self.right and not self.left and not self.below and not self.above:
            return self.right.find_key(token)
        if self.left and not self.right and not self.below and not self.above:
            return self.left.find_key(token)
        if self.left and self.right and not self.below and not self.above:
            return self.left.find_key(token) or self.right.find_key(token)
        if self.below and not self.above and not self.left and not self.right:
            return self.below.find_key(token)
        if self.below and self.right and not self.above and not self.left:
            return self.below.find_key(token) or self.right.find_key(token)
        if self.below and self.left and not self.above and not self.right:
            return self.below.find_key(token) or self.left.find_key(token)
        if self.below and self.left and self.right and not self.above:
            return self.below.find_key(token) or self.left.find_key(token) or self.right.find_key(token)
        if self.above and not self.below and not self.left and not self.right:
            return self.above.find_key(token)
        if self.above and self.right and not self.below and not self.left:
            return self.above.find_key(token) or self.right.find_key(token)
        if self.above and self.left and not self.below and not self.right:
            return self.above.find_key(token) or self.left.find_key(token)
        if self.above and self.left and self.right and not self.below:
            return self.above.find_key(token) or self.left.find_key(token) or self.right.find_key(token)
        if self.above and self.below and not self.left and not self.right:
            return self.above.find_key(token) or self.below.find_key(token)
        if self.above and self.below and self.left and not self.right:
            return self.above.find_key(token) or self.below.find_key(token) or self.left.find_key(token)
        if self.above and self.below and self.right and not self.left:
            return self.above.find_key(token) or self.below.find_key(token) or self.right.find_key(token)
        if self.above and self.below and self.right and self.left:
            return self.above.find_key(token) or self.below.find_key(token) or self.left.find_key(token) or self.right.find_key(token)

    def is_key_taken(self, key):
        """
        Find a key in this BST and return node value.

        :param key: The key to be found
        :return: Node or None
        """
        if self.key == key:
            return self
        elif key < self.key:
            if self.left:
                return self.left.is_key_taken(key)
            else:
                return None
        elif key > self.key:
            if self.right:
                return self.right.is_key_taken(key)
            else:
                return None
        return None

    def find_node(self, token):
        """
        Find a node in this BST by given token.

        :param token: The token of the node
        :return: Node or None
        """
        if self.token == token:
            return self
        if self.right and not self.left and not self.below and not self.above:
            return self.right.find_node(token)
        if self.left and not self.right and not self.below and not self.above:
            return self.left.find_node(token)
        if self.left and self.right and not self.below and not self.above:
            return self.left.find_node(token) or self.right.find_node(token)
        if self.below and not self.above and not self.left and not self.right:
            return self.below.find_node(token)
        if self.below and self.right and not self.above and not self.left:
            return self.below.find_node(token) or self.right.find_node(token)
        if self.below and self.left and not self.above and not self.right:
            return self.below.find_node(token) or self.left.find_node(token)
        if self.below and self.left and self.right and not self.above:
            return self.below.find_node(token) or self.left.find_node(token) or self.right.find_node(token)
        if self.above and not self.below and not self.left and not self.right:
            return self.above.find_node(token)
        if self.above and self.right and not self.below and not self.left:
            return self.above.find_node(token) or self.right.find_node(token)
        if self.above and self.left and not self.below and not self.right:
            return self.above.find_node(token) or self.left.find_node(token)
        if self.above and self.left and self.right and not self.below:
            return self.above.find_node(token) or self.left.find_node(token) or self.right.find_node(token)
        if self.above and self.below and not self.left and not self.right:
            return self.above.find_node(token) or self.below.find_node(token)
        if self.above and self.below and self.left and not self.right:
            return self.above.find_node(token) or self.below.find_node(token) or self.left.find_node(token)
        if self.above and self.below and self.right and not self.left:
            return self.above.find_node(token) or self.below.find_node(token) or self.right.find_node(token)
        if self.above and self.below and self.right and self.left:
            return self.above.find_node(token) or self.below.find_node(token) or self.left.find_node(token) or self.right.find_node(token)

    def find_node_right_and_left_only(self, token):
        """
        Find a node in this BST by given token, but only take left and right (not above and below) turns.

        :param token: The token that is to be found
        :return: Node or None
        """
        if self.token == token:
            return self
        if self.left and self.right:
            return self.left.find_node_right_and_left_only(token) or self.right.find_node_right_and_left_only(token)
        if self.right:
            return self.right.find_node_right_and_left_only(token)
        if self.left:
            return self.left.find_node_right_and_left_only(token)

    def above_or_below(self, other_node):
        """
        Determine whether a node is above or below the level of provided node. Return level.

        :param node: The node to which the relative level should be determined
        :param token: The token whose level should be determined
        :return: The amount of above/below levels that the node is removed or ""
        """
        # First, determine the layer that the other node is on, as determined by difference to root node.
        # E.g. in "A above D", "A above C" (fff), C is below, below A, i.e. "bb". D is below A, i.e. "b". The relative
        # difference in height between C and D is "b", the relative difference between D and C is "a".
        # Only root node knows above/below levels. In this example, D would know that C is below it, but C doesn't know
        # that D is above it. (Otherwise there are recursion problems when looking for nodes, jumping between above &
        # below). So the search always has to start at root level.

        # Other_node_level describes the relationship of the given (other) node to root level.
        found_other_node = False
        other_node_level = ""
        node = self.root
        while node.above:
            node = node.above
            other_node_level += "a"
            if node.find_node_right_and_left_only(other_node.token):
                found_other_node = True
                break
        if not other_node_level:
            other_node_level = ""
        node = self.root
        while node.below:
            node = node.below
            other_node_level += "b"
            if node.find_node_right_and_left_only(other_node.token):
                found_other_node = True
                break
        if not found_other_node:
            other_node_level = ""

        # This_node_level now describes the relationship of this node to root level.
        found_this_node = False
        this_node_level = ""
        node = self.root
        while node.above:
            node = node.above
            this_node_level += "a"
            if node.find_node_right_and_left_only(self.token):
                found_this_node = True
                break
        if not this_node_level:
            this_node_level = ""
        node = self.root
        while node.below:
            node = node.below
            this_node_level += "b"
            if node.find_node_right_and_left_only(self.token):
                found_this_node = True
                break
        if not found_this_node:
            this_node_level = ""

        # In case of equality of levels, return now
        if this_node_level == other_node_level:
            return ""

        # Compare the two absolute level distances to root level and return the relative distance between the two
        # nodes.
        relative_level = ""
        if this_node_level.startswith("a") or (not this_node_level and other_node_level.startswith("b")):
            relative_level = this_node_level
            for layer in other_node_level:
                relative_level += "a"
        if not relative_level:
            relative_level = ""
        if this_node_level.startswith("b") or (not this_node_level and other_node_level.startswith("a")):
            relative_level = this_node_level
            for layer in other_node_level:
                relative_level += "b"
        return relative_level

    def find(self, token=None, key=None):
        """
        Find a token in this BST.

        :param token: The token to be found
        :param key: Optional argument of key, if it is known.
        :return: True/False
        """
        if token:
            if self.find_node(token):
                return True
            else:
                return False
        elif key:
            if self.is_key_taken(key):
                return True
            else:
                return False

    def annotate(self, token, relation, indeterminately_inserted_token):
        """
        If a new token is to be inserted and its position is not determinate, it needs to be
        annotated with that information.

        :param token: The token that is already in the model
        :param relation: The relation with which the new token is to be indeterminately inserted
        :param indeterminately_inserted_token: The new token that is to be indeterminately inserted
        and will be annotated
        """
        if indeterminately_inserted_token in self.annotations:
            self.annotations[indeterminately_inserted_token].append((relation, token))
        else:
            self.annotations[indeterminately_inserted_token] = [(relation, token)]
        self.difficulty.annotation_ops += 1

    def merge(self, data_structure, parsed_line):
        """
        Merge this BST with another BST.

        :param data_structure: The other BST to merge with
        :param parsed_line: The parsed line which is the basis for the merge
        :return: New BST with content from both base BSTs
        """
        if self.find(parsed_line.first_token):
            located_object_node = self.find_node(parsed_line.first_token)
            reference_object = parsed_line.second_token
            this_model = copy.deepcopy(self)
            other_model = copy.deepcopy(data_structure)
        elif self.find(parsed_line.second_token):
            located_object_node = self.find_node(parsed_line.second_token)
            reference_object = parsed_line.first_token
            this_model = copy.deepcopy(data_structure)
            other_model = copy.deepcopy(self)

        if parsed_line.relation == "left":
            # Find the highest index in this model (on the left side of the merge)
            node = this_model.root
            while node.right:
                node = node.right
            highest_index_this_model = node.key

            # Now iterate through all nodes in the model on the right side of the merge, increase them and insert them
            # into the left-side model
            node = other_model.root
            key = node.key + highest_index_this_model + len(other_model)
            this_model.insert_node(key, node.token)
            nodes_to_insert = [node]
            while nodes_to_insert:
                node = nodes_to_insert.pop()
                if node.left:
                    key = node.left.key + highest_index_this_model + len(other_model)
                    this_model.insert_node(key, node.left.token)
                    nodes_to_insert.append(node.left)
                if node.right:
                    key = node.right.key + highest_index_this_model + len(other_model)
                    this_model.insert_node(key, node.right.token)
                    nodes_to_insert.append(node.right)
                if node.above:
                    this_model.find_node(node.token).above = node.above
                    this_model.find_node(node.token).above.key = node.key
                if node.below:
                    this_model.find_node(node.token).below = node.below
                    this_model.find_node(node.token).below.key = node.key
            merged_model = this_model
            merged_model.root.length += len(other_model)

        if parsed_line.relation == "right":
            # Find the highest index in this model (on the left side of the merge)
            node = other_model.root
            while node.right:
                node = node.right
            highest_index_other_model = node.key

            # Now iterate through all nodes in the model on the right side of the merge, increase them and insert them
            # into the left-side model
            node = this_model.root
            key = node.key + highest_index_other_model + len(this_model)
            other_model.insert_node(key, node.token)
            nodes_to_insert = [node]
            while nodes_to_insert:
                node = nodes_to_insert.pop()
                if node.left:
                    key = node.left.key + highest_index_other_model + len(this_model)
                    other_model.insert_node(key, node.left.token)
                    nodes_to_insert.append(node.left)
                if node.right:
                    key = node.right.key + highest_index_other_model + len(this_model)
                    other_model.insert_node(key, node.right.token)
                    nodes_to_insert.append(node.right)
                if node.above:
                    this_model.find_node(node.token).above = node.above
                    this_model.find_node(node.token).above.key = node.key
                if node.below:
                    this_model.find_node(node.token).below = node.below
                    this_model.find_node(node.token).below.key = node.key
            merged_model = other_model
            merged_model.root.length += len(this_model)

        if parsed_line.relation == "above":
            located_object_node = this_model.find_node(located_object_node.token)
            node = located_object_node
            # Go as far below as possible to append other model at the very bottom (we are above)
            while node.below:
                node = node.below
            other_node = other_model.root

            above_or_below = located_object_node.above_or_below(located_object_node.root)
            # Insert new below layer for all nodes of one level, to achieve this, go to node that is
            # directly above or below root node
            node = located_object_node.root
            for layer in above_or_below:
                if layer == "a":
                    node = node.above
                if layer == "b":
                    node = node.below
            nodes_to_give_below_to = [node]
            for node in nodes_to_give_below_to:
                if node.right:
                    nodes_to_give_below_to.append(node.right)
                if node.left:
                    nodes_to_give_below_to.append(node.left)
                node.below = other_node
            merged_model = this_model
            merged_model.root.length += len(other_model)

        if parsed_line.relation == "below":
            node = other_model.find_node(reference_object)
            # Go as far below as possible
            while node.below:
                node = node.below
            other_node = this_model.root

            above_or_below = node.above_or_below(other_model.root)
            # Insert new below layer for all nodes of one level, to achieve this, go to node that is
            # directly above or below root node
            node = other_model.root
            for layer in above_or_below:
                if layer == "a":
                    node = node.above
                if layer == "b":
                    node = node.below
            nodes_to_give_below_to = [node]
            for node in nodes_to_give_below_to:
                if node.right:
                    nodes_to_give_below_to.append(node.right)
                if node.left:
                    nodes_to_give_below_to.append(node.left)
                node.below = other_node
            merged_model = other_model
            merged_model.root.length += len(this_model)

        # Difficulty measure difficulty.focus_move_ops is determined by whether the focus needed to be changed in one
        # or both models.
        # First, in this model.
        if this_model.find_node(located_object_node.token):
            node_in_this_model = located_object_node
            node_in_other_model = other_model.find_node(reference_object)
        else:
            node_in_this_model = this_model.find_node(reference_object)
            node_in_other_model = located_object_node

        if this_model.focus != node_in_this_model:
            this_model.difficulty.focus_move_ops += 1
            # Now we need to see if the node currently in focus is a parent node of located object
            if this_model.find_node(this_model.focus.token).find_node_right_and_left_only(node_in_this_model.token):
                # Focus node is a parent node, so its path will be shorter than that of located object node,
                # the focus distance is the difference in path length.
                moved_focus_by_this_model = len(node_in_this_model.path_start_to_node()) - len(this_model.focus.path_start_to_node())
            # Or, the other way round, whether located object is a parent node of the node currently in focus
            elif this_model.find_node(node_in_this_model.token).find_node_right_and_left_only(this_model.focus.token):
                moved_focus_by_this_model = len(this_model.focus.path_start_to_node()) - len(node_in_this_model.path_start_to_node())
            # No node is a parent node of the other, they need to move "over root node", i.e. the path has to be
            # travelled back to root node (which is the len of path) for both, the sum of which is their distance
            else:
                moved_focus_by_this_model = len(this_model.focus.path_start_to_node()) + len(node_in_this_model.path_start_to_node())
            this_model.difficulty.focus_move_distance += moved_focus_by_this_model
            this_model.difficulty.focus_key_distance += abs(this_model.focus.key - node_in_this_model.key)
            above_or_below = node_in_this_model.above_or_below(this_model.focus)
            if not above_or_below and this_model.focus.key < node_in_this_model.key:
                focus_direction = "right"
            elif not above_or_below and this_model.focus.key > node_in_this_model.key:
                focus_direction = "left"
            elif this_model.focus.path_start_to_node() == node_in_this_model.path_start_to_node() and above_or_below.startswith("a"):
                focus_direction = "above"
            elif this_model.focus.path_start_to_node() == node_in_this_model.path_start_to_node() and above_or_below.startswith("b"):
                focus_direction = "below"
            else:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or this_model.focus_change_direction != focus_direction:
                this_model.focus_change_direction = focus_direction
                this_model.difficulty.focus_direction_changes += 1
            this_model.focus = node_in_this_model

        # Now in other model.
        if other_model.focus != node_in_other_model:
            other_model.difficulty.focus_move_ops += 1
            # Now we need to see if the node currently in focus is a parent node of located object
            if other_model.find_node(other_model.focus.token).find_node_right_and_left_only(node_in_other_model.token):
                # Focus node is a parent node, so its path will be shorter than that of located object node,
                # the focus distance is the difference in path length.
                moved_focus_by_other_model = len(node_in_other_model.path_start_to_node()) - len(other_model.focus.path_start_to_node())
            # Or, the other way round, whether located object is a parent node of the node currently in focus
            elif other_model.find_node(node_in_other_model.token).find_node_right_and_left_only(other_model.focus.token):
                moved_focus_by_other_model = len(other_model.focus.path_start_to_node()) - len(node_in_other_model.path_start_to_node())
            # No node is a parent node of the other, they need to move "over root node", i.e. the path has to be
            # travelled back to root node (which is the len of path) for both, the sum of which is their distance
            else:
                moved_focus_by_other_model = len(other_model.focus.path_start_to_node()) + len(node_in_other_model.path_start_to_node())
            other_model.difficulty.focus_move_distance += moved_focus_by_other_model
            other_model.difficulty.focus_key_distance += abs(other_model.focus.key - node_in_other_model.key)
            above_or_below = node_in_other_model.above_or_below(other_model.focus)
            if not above_or_below and other_model.focus.key < node_in_other_model.key:
                focus_direction = "right"
            elif not above_or_below and other_model.focus.key > node_in_other_model.key:
                focus_direction = "left"
            elif other_model.focus.path_start_to_node() == node_in_other_model.path_start_to_node() and above_or_below.startswith("a"):
                focus_direction = "above"
            elif other_model.focus.path_start_to_node() == node_in_other_model.path_start_to_node() and above_or_below.startswith("b"):
                focus_direction = "below"
            else:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or other_model.focus_change_direction != focus_direction:
                other_model.focus_change_direction = focus_direction
                other_model.difficulty.focus_direction_changes += 1
            other_model.focus = node_in_other_model
        return merged_model, this_model.focus

    def variate_model(self, parsed_conclusion, how_far_removed=0):
        """
        Generate alternative model(s) based on annotations and how far removed on the neighborhood graph an
        alternative model is (based on how many swap operations are necessary to gain it from original model).

        :param parsed_conclusion: The conclusion that is to be verified.
        :param how_far_removed: How far on the neighborhood graph the returned alternative models may be.
        :return: bool: If within how_far_removed a model is found that holds under parsed_conclusion, True.
                       Otherwise, False.
        """
        # This procedure works well with InfiniteLists. I don't currently see a necessity to implement it in
        # BSTs themselves. Would be possible, but would require a lot of node rotating etc.
        content = self.to_infinite_list(), (0, 0)
        inf_list = InfiniteList('', self.insert_type, self.merge_type, self.difficulty, content)
        inf_list.annotations = self.annotations
        if inf_list.variate_model(parsed_conclusion, how_far_removed):
            return True
        else:
            return False

    def layer_to_infinite_list(self, layer, layer_list):
        """
        Convert one layer (only left and right) to a list

        :return: List of format analogous to InfiniteList
        """
        if layer.left:
            self.layer_to_infinite_list(layer.left, layer_list)
        layer_list.append(layer.token)
        if layer.right:
            self.layer_to_infinite_list(layer.right, layer_list)

    def to_infinite_list(self):
        """
        Because implementing combine supermodels was really difficult and it works for InfiniteLists, due to ease,
        I'll convert this BST to a list so the combination can take place in InfiniteList.

        :return: A list object with the same content as this BST, formatted as in InfiniteList
        """
        infi_list = []
        layers = []
        node = self
        while node.above:
            layers.insert(0, node.above)
            node = node.above
        layers.append(self)
        node = self
        while node.below:
            layers.append(node.below)
            node = node.below
        # For every above/below, make a layer into a list
        for layer in layers:
            layer_list = []
            # Every layer makes itself into a list by going left and right only.
            self.layer_to_infinite_list(layer, layer_list)
            infi_list.append(layer_list)

        # Now add the 'x's for empty space above/below a token. This is easy to do since in BSTs the root nodes "hang
        # together", therefore any too short list will have to have 'x's added to the end to pad it.
        max_len = 0
        for layer_list in infi_list:
            if len(layer_list) > max_len:
                max_len = len(layer_list)
        for layer_list in infi_list:
            if len(layer_list) < max_len:
                for i in range(max_len - len(layer_list)):
                    layer_list.append('x')
        return infi_list

    def path_start_to_node(self):
        """
        From the root node (or a node above/below root node, but not laterally removed), return the path taken to a
        child node.
        E.g. in "A left B", the path from root to B is "left", i.e. "l".

        :return: path
        """
        path = ""
        vertically_removed_from_root = self.above_or_below(self.root)
        layer = self.root
        for removal in vertically_removed_from_root:
            if removal == "a":
                layer = layer.above
            if removal == "b":
                layer = layer.below
        node = layer
        while True:
            if node.token == self.token:
                break
            if node.right:
                if node.right.find_node_right_and_left_only(self.token):
                    path += "r"
                    node = node.right
                    continue
            if node.left:
                if node.left.find_node_right_and_left_only(self.token):
                    path += "l"
                    node = node.left
            if not node.right and not node.left:
                break
        return path

    def evaluate_conclusion(self, parsed_conclusion):
        """
        Evaluate the truth of a parsed conclusion.

        :param parsed_conclusion: The conclusion
        :return: True/False depending on whether it's true.
        """
        evaluation = False
        first_token_key = self.find_key(parsed_conclusion.first_token)
        second_token_key = self.find_key(parsed_conclusion.second_token)
        first_token_node = self.find_node(parsed_conclusion.first_token)
        second_token_node = self.find_node(parsed_conclusion.second_token)

        if first_token_node and second_token_node:
            # Change focus to first node
            if self.focus != first_token_node:
                # Now we need to see if the node currently in focus is a parent node of located object
                if self.find_node(self.focus.token).find_node_right_and_left_only(first_token_node.token):
                    # Focus node is a parent node, so its path will be shorter than that of located object node,
                    # the focus distance is the difference in path length.
                    moved_focus_by = len(first_token_node.path_start_to_node()) - len(self.focus.path_start_to_node())
                # Or, the other way round, whether located object is a parent node of the node currently in focus
                elif self.find_node(first_token_node.token).find_node_right_and_left_only(self.focus.token):
                    moved_focus_by = len(self.focus.path_start_to_node()) - len(first_token_node.path_start_to_node())
                # No node is a parent node of the other, they need to move "over root node", i.e. the path has to be
                # travelled back to root node (which is the len of path) for both, the sum of which is their distance
                else:
                    moved_focus_by = len(self.focus.path_start_to_node()) + len(first_token_node.path_start_to_node()) \
                                        + len(self.focus.above_or_below(first_token_node))
                self.difficulty.focus_move_distance += moved_focus_by
                self.difficulty.focus_key_distance += abs(self.focus.key - first_token_node.key)
                above_or_below = first_token_node.above_or_below(self.focus)
                if not above_or_below and self.focus.key < first_token_node.key:
                    focus_direction = "right"
                elif not above_or_below and self.focus.key > first_token_node.key:
                    focus_direction = "left"
                elif self.focus.path_start_to_node() == first_token_node.path_start_to_node() and above_or_below.startswith("a"):
                    focus_direction = "above"
                elif self.focus.path_start_to_node() == first_token_node.path_start_to_node() and above_or_below.startswith("b"):
                    focus_direction = "below"
                else:
                    focus_direction = "various_directions"
                if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                    self.focus_change_direction = focus_direction
                    self.difficulty.focus_direction_changes += 1
                self.focus = first_token_node
            # Now to second node
            if self.focus != second_token_node:
                # Now we need to see if the node currently in focus is a parent node of located object
                if self.find_node(self.focus.token).find_node_right_and_left_only(second_token_node.token):
                    # Focus node is a parent node, so its path will be shorter than that of located object node,
                    # the focus distance is the difference in path length.
                    moved_focus_by = len(second_token_node.path_start_to_node()) - len(self.focus.path_start_to_node())
                # Or, the other way round, whether located object is a parent node of the node currently in focus
                elif self.find_node(second_token_node.token).find_node_right_and_left_only(self.focus.token):
                    moved_focus_by = len(self.focus.path_start_to_node()) - len(second_token_node.path_start_to_node())
                # No node is a parent node of the other, they need to move "over root node", i.e. the path has to be
                # travelled back to root node (which is the len of path) for both, the sum of which is their distance
                else:
                    moved_focus_by = len(self.focus.path_start_to_node()) + len(second_token_node.path_start_to_node()) \
                                        + len(self.focus.above_or_below(second_token_node))
                self.difficulty.focus_move_distance += moved_focus_by
                self.difficulty.focus_key_distance += abs(self.focus.key - second_token_node.key)
                above_or_below = second_token_node.above_or_below(self.focus)
                if not above_or_below and self.focus.key < second_token_node.key:
                    focus_direction = "right"
                elif not above_or_below and self.focus.key > second_token_node.key:
                    focus_direction = "left"
                elif self.focus.path_start_to_node() == second_token_node.path_start_to_node() and above_or_below.startswith("a"):
                    focus_direction = "above"
                elif self.focus.path_start_to_node() == second_token_node.path_start_to_node() and above_or_below.startswith("b"):
                    focus_direction = "below"
                else:
                    focus_direction = "various_directions"
                if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                    self.focus_change_direction = focus_direction
                    self.difficulty.focus_direction_changes += 1
                self.focus = second_token_node

        if parsed_conclusion.relation == "left" and first_token_node and second_token_node:
            evaluation = first_token_key < second_token_key and not first_token_node.above_or_below(second_token_node)
        if parsed_conclusion.relation == "right" and first_token_node and second_token_node:
            evaluation = first_token_key > second_token_key and not first_token_node.above_or_below(second_token_node)
        # In above/below, make sure that the path from root node to asked node is identical (because in some examples,
        # keys might vary, e.g. in ff insertion, nodes above another may have different keys, but the path from the root
        # node to them is identical) & that their relative level is either all "a"s or all "b"s. Startswith suffices
        # since mixed levels may not occur.
        if parsed_conclusion.relation == "above":
            evaluation = first_token_node.path_start_to_node() == second_token_node.path_start_to_node() and \
                         first_token_node.above_or_below(second_token_node).startswith("a")
        if parsed_conclusion.relation == "below":
            evaluation = first_token_node.path_start_to_node() == second_token_node.path_start_to_node() and \
                         first_token_node.above_or_below(second_token_node).startswith("b")
        if evaluation:
            return evaluation
        else:
            if self.supermodels:
                for supermodel in self.supermodels:
                    self.difficulty.supermodels_accessed += 1
                    return supermodel.evaluate_conclusion(parsed_conclusion)
            return False

    def generate(self, first_token, second_token):
        """
        Given two tokens, return the relationship between them as represented in the model.

        :param first_token: First token
        :param second_token: Second token
        :return: Relationship between the two tokens
        """
        key_first_token = self.find_key(first_token)
        key_second_token = self.find_key(second_token)
        node_first_token = self.find_node(first_token)
        node_second_token = self.find_node(second_token)

        if key_first_token < key_second_token and not node_first_token.above_or_below(node_second_token):
            return "left"
        if key_first_token > key_second_token and not node_first_token.above_or_below(node_second_token):
            return "right"
        if node_first_token.path_start_to_node() == node_second_token.path_start_to_node() and \
                node_first_token.above_or_below(node_second_token).startswith("a"):
            return "above"
        if node_first_token.path_start_to_node() == node_second_token.path_start_to_node() and \
                node_first_token.above_or_below(node_second_token).startswith("b"):
            return "below"
        else:
            return "no_rel"
