import copy
from DataStructure import DataStructure
from DataStructures.InfiniteList import InfiniteList
from Helpers import MyExceptions

__author__ = 'Phaina'

"""LinkedList is a data structure that consists of nodes pointing to each other (only to the right)."""


class LinkedListNode():
    """
    A node for class LinkedList. Has a token and a pointer (pointing to next node to the right).
    """
    def __init__(self, token, pointing_to=None):
        self.token = token
        self.pointing_to = pointing_to

    def __str__(self):
        return str(self.token)


class LinkedList(DataStructure):
    def __init__(self, parsed_line, insert_type, merge_type, difficulty, content=None):
        """
        :param parsed_line: The current line as parsed by Parser, i.e. first_token, relation, second_token
        :param content: Optional: Content to be used to fill LinkedList object.
        :param insert_type: Currently used insert type, i.e. ff/fff
        :param merge_type: Currently used merge type, i.e. integrate/annotate/supermodels
        :param difficulty: Difficulty singleton handed down by Central Executive for measuring focus operations
        """
        super(LinkedList, self).__init__()

        self.difficulty = difficulty
        self.insert_type = insert_type
        self.merge_type = merge_type
        self.focus = None
        self.focus_change_direction = None
        self.annotations = dict()
        self.supermodel_index = 0
        self.supermodels = []

        if content is None:
            self.content = []
            self.create_from_parsed_line(parsed_line)
        else:
            # Content is a tuple: (content of list, focus of content)
            self.content = content[0]
            self.focus = content[1]

    def __str__(self):
        string_representation = "LinkedList content: "
        # Iterate through above/below layers
        for node in self.content:
            if self.content.index(node) > 0:
                string_representation += "; "
            string_representation += "Layer " + str(self.content.index(node)) + " "
            # And then within these layers, follow one node to the next, going through all links
            string_representation += " " + node.token
            while node.pointing_to:
                string_representation += " -> " + node.pointing_to.token
                node = node.pointing_to
        return string_representation

    def __len__(self):
        length = 0
        # Iterate through above/below layers
        for node in self.content:
            length += 1
            # And then within these layers, follow one node to the next, going through all links
            while node.pointing_to:
                length += 1
                node = node.pointing_to
        return length

    def length_of_linked_list(self, node):
        """
        Given a starting node, return the amount of nodes still left to the right of that node.

        :param node: The node of which the length to terminal node should be calculated
        :return: Length of linked list
        """
        i = 0
        while node.pointing_to:
            i += 1
            node = node.pointing_to
        return i

    def find(self, token):
        """
        Given a token, find the node that has that token.

        :param token: The token that is to be found.

        :return Node or None
        """
        for node in self.content:
            if node.token == token:
                return node
            while node.pointing_to:
                if node.pointing_to.token == token:
                    return node.pointing_to
                self.difficulty.linked_list_followed_pointing_to += 1
                node = node.pointing_to
        return None

    def find_node_pointing_to(self, node_to_be_found):
        """
        Given a node, find the node's predecessor.

        :param node: The token whose predecessor is to be found.
        :return: Predecessor node or None
        """
        for node in self.content:
            if node == node_to_be_found:
                # Because then this node does not have a predecessor
                return None
            while node.pointing_to:
                if node.pointing_to == node_to_be_found:
                    return node
                self.difficulty.linked_list_followed_pointing_to += 1
                node = node.pointing_to
        return None

    def find_node_parent_and_index(self, node_to_be_found):
        """
        Given a node, find the node's parent (i.e. first node in a linked list) and index in the pointers.

        :param node: The node whose parent and index is to be found.
        :return: Parent and index or None
        """
        for node in self.content:
            if node.token == node_to_be_found.token:
                return node, 0
            i = 0
            parent_node = node
            while node.pointing_to:
                i += 1
                if node.pointing_to.token == node_to_be_found.token:
                    return parent_node, i
                self.difficulty.linked_list_followed_pointing_to += 1
                node = node.pointing_to
        return None, None

    def find_linked_list_index(self, parent_node):
        """
        Given a parent node (i.e. first node in a linked list), give the index that the linked list starting with that
        node has in self.content.

        :param parent_node: The parent node of the linked list
        :return: Index or None
        """
        for linked_list in self.content:
            if linked_list.token == parent_node.token:
                return self.content.index(linked_list)
        return None

    def delete_node(self, node):
        """
        Given a node, delete the corresponding linked list. (This should be a parent node, i.e. first in the linked
        list.)

        :param node: The node that is to be deleted.
        """
        for parent_node in self.content:
            if parent_node == node:
                self.content.remove(parent_node)

    def create_from_parsed_line(self, parsed_line):
        """
        Given a parsed line, create initial content for LinkedList.

        :param parsed_line: The parsed line that describes the initial content of LinkedList.
        """
        if parsed_line.relation == "left":
            first_node = LinkedListNode(parsed_line.first_token)
            second_node = LinkedListNode(parsed_line.second_token)
            first_node.pointing_to = second_node
            self.content.append(first_node)
        if parsed_line.relation == "right":
            first_node = LinkedListNode(parsed_line.second_token)
            second_node = LinkedListNode(parsed_line.first_token)
            first_node.pointing_to = second_node
            self.content.append(first_node)
        if parsed_line.relation == "above":
            first_node = LinkedListNode(parsed_line.first_token)
            second_node = LinkedListNode(parsed_line.second_token)
            self.content.append(first_node)
            self.content.append(second_node)
        if parsed_line.relation == "below":
            first_node = LinkedListNode(parsed_line.second_token)
            second_node = LinkedListNode(parsed_line.first_token)
            self.content.append(first_node)
            self.content.append(second_node)

        # Set initial focus to that of the parsed line
        if parsed_line.focus:
            if len(parsed_line.focus) == 1:
                if parsed_line.focus == parsed_line.first_token:
                    self.focus = self.find(parsed_line.second_token)
                else:
                    self.focus = self.find(parsed_line.first_token)
                if self.focus is None:
                    raise MyExceptions.FocusError("LinkedList.create_from_parsed_line focus went to None")
                # Save first direction taken for measuring direction changes
                if parsed_line.relation == "left":
                    self.focus_change_direction = "right"
                if parsed_line.relation == "right":
                    self.focus_change_direction = "left"
                if parsed_line.relation == "above":
                    self.focus_change_direction = "down"
                if parsed_line.relation == "below":
                    self.focus_change_direction = "up"
            else:
                raise MyExceptions.FocusError("Parsed_line.focus had more than one element! Called from"
                                              "LinkedList.create_from_parsed_line()")

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

    def forget(self, token):
        """
        Forget a given token, i.e. replace this token with string 'forgotten'.

        :param token: The token that should be forgotten.
        """
        node_of_token = self.find(token)
        node_of_token.token = 'forgotten'

    def new_node(self, node, index=None):
        """
        Insert a new parent_node into list of linked lists.

        :param node: New parent node
        :param index: Optional: The index of where to insert that new parent node into list of linked lists.
        """
        if index is not None:
            self.content.insert(index, node)
        else:
            self.content.append(node)

    def insert(self, parsed_line):
        """
        Given a parsed object (first_token, relation, second_token), insert it into this data structure.

        Fill free space with x's for possible gaps, so that situations such as:
        ['A' ->  x ->  'B',
         'C' -> 'D' -> 'E']
        are accounted for.

        :param: parsed_line: A parsed line (premise or conclusion)

        :return: True if insert worked
        """
        if self.find(parsed_line.first_token):
            parsed_line.invert()
            located_object = self.find(parsed_line.first_token)
            before_located_object = self.find_node_pointing_to(located_object)
            located_object_parent, located_object_index = self.find_node_parent_and_index(located_object)
            reference_object = parsed_line.second_token
        if self.find(parsed_line.second_token):
            located_object = self.find(parsed_line.second_token)
            before_located_object = self.find_node_pointing_to(located_object)
            located_object_parent, located_object_index = self.find_node_parent_and_index(located_object)
            reference_object = parsed_line.first_token

        # Focus operations
        if self.focus != located_object:
            self.difficulty.focus_move_ops += 1
            focus_parent, focus_index = self.find_node_parent_and_index(self.focus)
            moved_focus_by = abs(focus_index - located_object_index)\
                             + abs(self.find_linked_list_index(focus_parent) -
                                   self.find_linked_list_index(located_object_parent))
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(located_object_parent) and \
               focus_index < located_object_index:
                focus_direction = "right"
            if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(located_object_parent) and \
               focus_index > located_object_index:
                focus_direction = "left"
            if self.find_linked_list_index(focus_parent) > self.find_linked_list_index(located_object_parent) and \
               focus_index == located_object_index:
                focus_direction = "up"
            if self.find_linked_list_index(focus_parent) < self.find_linked_list_index(located_object_parent) and \
               focus_index == located_object_index:
                focus_direction = "down"
            if self.find_linked_list_index(focus_parent) != self.find_linked_list_index(located_object_parent) and \
               focus_index != located_object_index:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = located_object

        # If the LO is itself ambiguous in position, it might need to be moved in the MVP.
        # Therefore it'll be annotated with new information so that it doesn't get moved/switched wrongly.
        if located_object.token in self.annotations:
            parsed_line.invert()
            self.annotations[located_object.token].append((parsed_line.relation, reference_object))
            parsed_line.invert()

        if parsed_line.relation == "left":
            # If there's a node pointing to located object, this insert is ambiguous
            if before_located_object and before_located_object.token != 'x':
                parsed_line.invert()
                self.annotate(located_object.token, parsed_line.relation, reference_object)
                parsed_line.invert()

            new_node = LinkedListNode(reference_object)
            if self.insert_type == "ff":
                if located_object_index == 0:
                    new_node.pointing_to = located_object
                    self.new_node(new_node)
                    self.delete_node(located_object)
                    # If there are other layers, start them with an 'x' as well
                    list_index = self.find_linked_list_index(new_node)
                    for i in range(len(self.content)):
                        if i != list_index:
                            new_x_node = LinkedListNode('x')
                            new_x_node.pointing_to = self.content[i]
                            self.delete_node(self.content[i])
                else:
                    if before_located_object.token != 'x':
                        before_located_object.pointing_to = new_node
                        new_node.pointing_to = located_object
                        # If there are other layers, insert an 'x' into them at the same position (one before located
                        # object)
                        list_index = self.find_linked_list_index(located_object_parent)
                        x_node = LinkedListNode('x')
                        for i in range(len(self.content)):
                            if i != list_index:
                                node = self.content[i]
                                for j in range(located_object_index - 2):
                                    self.difficulty.linked_list_followed_pointing_to += 1
                                    node = node.pointing_to
                                tmp = node.pointing_to
                                node.pointing_to = x_node
                                x_node.pointing_to = tmp
                    else:
                        before_located_object.token = new_node.token
            if self.insert_type == "fff":
                # First see if there's a node before this node whose token is an 'x', so we can place the new token
                # there.
                inserted = False
                while before_located_object:
                    if before_located_object.token == 'x':
                        before_located_object.token = new_node.token
                        inserted = True
                    if self.find_node_parent_and_index(before_located_object)[1] != 0:
                        node_parent, node_index = self.find_node_parent_and_index(before_located_object)
                        before_located_object = node_parent
                        for j in range(node_index - 1):
                            self.difficulty.linked_list_followed_pointing_to += 1
                            before_located_object = before_located_object.pointing_to
                    else:
                        break
                # If there wasn't, insert new node at the beginning
                if not inserted:
                    new_node.pointing_to = located_object_parent
                    # Start all other layers with an 'x'
                    list_index = self.find_linked_list_index(located_object_parent)
                    for i in range(len(self.content)):
                        if i != list_index:
                            new_x_node = LinkedListNode('x')
                            new_x_node.pointing_to = self.content[i]
                            self.delete_node(self.content[i])
                    self.new_node(new_node)
                    self.delete_node(located_object_parent)

        if parsed_line.relation == "right":
            # If the located object is pointing somewhere, this insert is ambiguous.
            if located_object.pointing_to and located_object.pointing_to.token != 'x':
                parsed_line.invert()
                self.annotate(located_object.token, parsed_line.relation, reference_object)
                parsed_line.invert()

            new_node = LinkedListNode(reference_object)
            if self.insert_type == "ff":
                if located_object.pointing_to and located_object.pointing_to.token == 'x':
                    located_object.pointing_to.token = new_node.token
                else:
                    if located_object.pointing_to:
                        tmp = located_object.pointing_to
                        located_object.pointing_to = new_node
                        new_node.pointing_to = tmp
                    else:
                        located_object.pointing_to = new_node
                    # Pad all other layers with 'x's. In this case, insert them at same index place as it was
                    # inserted here.
                    list_index = self.find_linked_list_index(located_object_parent)
                    x_node = LinkedListNode('x')
                    for i in range(len(self.content)):
                        if i != list_index:
                            node = self.content[i]
                            j = located_object_index
                            for k in range(j):
                                self.difficulty.linked_list_followed_pointing_to += 1
                                node = node.pointing_to
                            tmp = node.pointing_to
                            node.pointing_to = x_node
                            x_node.pointing_to = tmp
            if self.insert_type == "fff":
                # First see if there's a node after this node whose token is an 'x', so we can place the new token
                # there.
                rightmost_node = located_object
                inserted = False
                while rightmost_node.pointing_to:
                    if rightmost_node.pointing_to.token == 'x':
                        rightmost_node.pointing_to.token = new_node.token
                        inserted = True
                    else:
                        self.difficulty.linked_list_followed_pointing_to += 1
                        rightmost_node = rightmost_node.pointing_to
                # If there wasn't, node needs to be appended at the very end of linked list.
                if not inserted:
                    rightmost_node.pointing_to = new_node
                    # Make sure that all other layers are padded with x's, in this case just append one because insert
                    # is fff and was therefore at the very right position
                    list_index = self.find_linked_list_index(located_object_parent)
                    x_node = LinkedListNode('x')
                    for i in range(len(self.content)):
                        if i != list_index:
                            node = self.content[i]
                            while node.pointing_to:
                                self.difficulty.linked_list_followed_pointing_to += 1
                                node = node.pointing_to
                            node.pointing_to = x_node

        if parsed_line.relation == "above":
            # If there's another layer above the one which was located, this insert is ambiguous.
            if self.find_linked_list_index(located_object_parent) != 0:
                parsed_line.invert()
                self.annotate(located_object.token, parsed_line.relation, reference_object)
                parsed_line.invert()

            new_node = LinkedListNode(reference_object)
            # The node above which we are is a parent node, so we need to pad this node to the end of linked list
            # with 'x's
            if not before_located_object:
                inserted_node = new_node
                for i in range(self.length_of_linked_list(located_object)):
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    new_node.pointing_to = new_x_node
                    new_node = new_x_node
                new_node = inserted_node
            else:
                # Located node is not a parent node, we need to pad before reference object with 'x's
                new_parent_node = LinkedListNode('x')
                old_x_node = new_parent_node
                for i in range(located_object_index - 1):
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    old_x_node.pointing_to = new_x_node
                    old_x_node = new_x_node
                old_x_node.pointing_to = new_node
                # And also after
                for i in range(self.length_of_linked_list(located_object)):
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    new_node.pointing_to = new_x_node
                    new_node = new_x_node
                new_node = new_parent_node
            list_index = self.find_linked_list_index(located_object_parent)
            if self.insert_type == "ff":
                self.new_node(new_node, list_index)
            if self.insert_type == "fff":
                self.new_node(new_node, 0)

        if parsed_line.relation == "below":
            # If the located object is not on the deepest layer, this insert is ambiguous.
            if self.find_linked_list_index(located_object_parent) != len(self.content):
                parsed_line.invert()
                self.annotate(located_object.token, parsed_line.relation, reference_object)
                parsed_line.invert()

            new_node = LinkedListNode(reference_object)
            # The node below which we are is a parent node, so we need to pad this node to the end of linked list
            # with 'x's
            if not before_located_object:
                inserted_node = new_node
                for i in range(self.length_of_linked_list(located_object)):
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    new_node.pointing_to = new_x_node
                    new_node = new_x_node
                new_node = inserted_node
            else:
                # Located node is not a parent node, we need to pad before reference object with 'x's
                new_parent_node = LinkedListNode('x')
                old_x_node = new_parent_node
                for i in range(located_object_index - 1):
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    old_x_node.pointing_to = new_x_node
                    old_x_node = new_x_node
                old_x_node.pointing_to = new_node
                # And after
                for i in range(self.length_of_linked_list(located_object)):
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    new_node.pointing_to = new_x_node
                    new_node = new_x_node
                new_node = new_parent_node
            list_index = self.find_linked_list_index(located_object_parent)
            if self.insert_type == "ff":
                self.new_node(new_node, list_index + 1)
            if self.insert_type == "fff":
                self.new_node(new_node)

        # Focus operations
        reference_node = self.find(reference_object)
        reference_node_parent, reference_node_index = self.find_node_parent_and_index(reference_node)
        if self.focus != reference_node:
            self.difficulty.focus_move_ops += 1
            focus_parent, focus_index = self.find_node_parent_and_index(self.focus)
            moved_focus_by = abs(focus_index - reference_node_index)\
                             + abs(self.find_linked_list_index(focus_parent) -
                                   self.find_linked_list_index(reference_node_parent))
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(reference_node_parent) and \
               focus_index < reference_node_index:
                focus_direction = "right"
            if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(reference_node_parent) and \
               focus_index > reference_node_index:
                focus_direction = "left"
            if self.find_linked_list_index(focus_parent) > self.find_linked_list_index(reference_node_parent) and \
               focus_index == reference_node_index:
                focus_direction = "up"
            if self.find_linked_list_index(focus_parent) < self.find_linked_list_index(reference_node_parent) and \
               focus_index == reference_node_index:
                focus_direction = "down"
            if self.find_linked_list_index(focus_parent) != self.find_linked_list_index(reference_node_parent) and \
               focus_index != reference_node_index:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = reference_node

        # Returns true because nothing can go wrong here
        return True

    def merge(self, data_structure, parsed_line):
        """
        Merge this linked list with another linked list object on the basis of parsed line (gives the relation
        between two tokens, which are part of different models).
        Uses strategy integrate, i.e. returns a list of merged content.

        E.g. Merge:
        ['A' -> 'B', 'C' -> 'D'] with ['Y' -> 'E', 'F' -> 'G']
        on basis 'B left Y' yields
        ['A' -> 'B' -> 'Y' -> 'E', 'C' -> 'D' -> 'F' -> 'G'].

        :param: data_structure: The other linked list object which with this one should be merged.
        :param: parsed_line: The parsed line that describes the relation between two models.

        :return new_content, self.focus: New content of linked lists
        """
        self_content = copy.deepcopy(self)
        other_content = copy.deepcopy(data_structure)

        if self.find(parsed_line.first_token):
            node_in_this_model = self.find(parsed_line.first_token)
            node_in_this_model_parent, node_in_this_model_index = self.find_node_parent_and_index(node_in_this_model)
            reference_object = parsed_line.second_token
            node_in_other_model = other_content.find(reference_object)
            node_in_other_model_parent, node_in_other_model_index = other_content.find_node_parent_and_index(node_in_other_model)
        if self.find(parsed_line.second_token):
            node_in_this_model = self.find(parsed_line.second_token)
            node_in_this_model_parent, node_in_this_model_index = self.find_node_parent_and_index(node_in_this_model)
            reference_object = parsed_line.first_token
            node_in_other_model = other_content.find(reference_object)
            node_in_other_model_parent, node_in_other_model_index = other_content.find_node_parent_and_index(node_in_other_model)

        if parsed_line.relation == "left":
            if self.find_linked_list_index(node_in_this_model_parent) == other_content.find_linked_list_index(node_in_other_model_parent):
                # Tokens are on the same height
                if len(self_content.content) == len(other_content.content):
                    # Can simply paste the two linked lists together
                    pass
                elif len(self_content.content) > len(other_content.content):
                    # Append empty lines to linked list so it's long enough.
                    # Create an empty line.
                    old_x_node = LinkedListNode('x')
                    start_node = old_x_node
                    node = other_content[0]
                    while node.pointing_to:
                        self.difficulty.linked_list_followed_pointing_to += 1
                        new_x_node = LinkedListNode('x')
                        old_x_node.pointing_to = new_x_node
                        old_x_node = new_x_node
                        node = node.pointing_to
                    # Append it
                    for i in range(len(self_content.content) - len(other_content.content)):
                        other_content.new_node(start_node)
                elif len(other_content.content) > len(self_content.content):
                    # Append empty lines to linked list so it's long enough.
                    # Create an empty line.
                    old_x_node = LinkedListNode('x')
                    start_node = old_x_node
                    node = other_content[0]
                    while node.pointing_to:
                        self.difficulty.linked_list_followed_pointing_to += 1
                        new_x_node = LinkedListNode('x')
                        old_x_node.pointing_to = new_x_node
                        old_x_node = new_x_node
                        node = node.pointing_to
                    # Append it
                    for i in range(len(other_content.content) - len(self_content.content)):
                        other_content.new_node(start_node)
            else:
                # Tokens are on different heights. The height difference has to be padded.
                # Create an empty line in this model.
                old_x_node = LinkedListNode('x')
                start_node = old_x_node
                node = self_content.content[0]
                while node.pointing_to:
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    old_x_node.pointing_to = new_x_node
                    old_x_node = new_x_node
                    node = node.pointing_to
                # Create an empty line in other model.
                old_x_node = LinkedListNode('x')
                start_node = old_x_node
                node = other_content.content[0]
                while node.pointing_to:
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    old_x_node.pointing_to = new_x_node
                    old_x_node = new_x_node
                    node = node.pointing_to
                if node_in_this_model_index > node_in_other_model_index:
                    for i in range(node_in_this_model_index - node_in_other_model_index):
                        # Append it
                        self_content.new_node(start_node)
                        # Insert it
                        other_content.new_node(start_node, 0)
                if node_in_this_model_index < node_in_other_model_index:
                    for i in range(node_in_other_model_index - node_in_this_model_index):
                        # Insert it
                        self_content.new_node(start_node, 0)
                        # Append it
                        other_content.new_node(start_node)
            # The two sides should be prepared, now merge them
            for i, node in enumerate(self_content.content):
                # Go to the rightmost node on a layer, so it can point to the leftmost node on the other side
                while node.pointing_to:
                    self.difficulty.linked_list_followed_pointing_to += 1
                    node = node.pointing_to
                node.pointing_to = other_content.content[i]
            merged_content = self_content.content

        if parsed_line.relation == "right":
            if self.find_linked_list_index(node_in_this_model_parent) == other_content.find_linked_list_index(node_in_other_model_parent):
                # Tokens are on the same height
                if len(self_content.content) == len(other_content.content):
                    # Can simply paste the two linked lists together
                    pass
                elif len(self_content.content) > len(other_content.content):
                    # Append empty lines to linked list so it's long enough.
                    # Create an empty line.
                    old_x_node = LinkedListNode('x')
                    start_node = old_x_node
                    node = other_content[0]
                    while node.pointing_to:
                        self.difficulty.linked_list_followed_pointing_to += 1
                        new_x_node = LinkedListNode('x')
                        old_x_node.pointing_to = new_x_node
                        old_x_node = new_x_node
                        node = node.pointing_to
                    # Append it
                    for i in range(len(self_content.content) - len(other_content.content)):
                        other_content.new_node(start_node)
                elif len(other_content.content) > len(self_content.content):
                    # Append empty lines to linked list so it's long enough.
                    # Create an empty line.
                    old_x_node = LinkedListNode('x')
                    start_node = old_x_node
                    node = other_content[0]
                    while node.pointing_to:
                        self.difficulty.linked_list_followed_pointing_to += 1
                        new_x_node = LinkedListNode('x')
                        old_x_node.pointing_to = new_x_node
                        old_x_node = new_x_node
                        node = node.pointing_to
                    # Append it
                    for i in range(len(other_content.content) - len(self_content.content)):
                        other_content.new_node(start_node)
            else:
                # Tokens are on different heights. The height difference has to be padded.
                # Create an empty line in this model.
                old_x_node = LinkedListNode('x')
                start_node_this_model = old_x_node
                node = self_content.content[0]
                while node.pointing_to:
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    old_x_node.pointing_to = new_x_node
                    old_x_node = new_x_node
                    node = node.pointing_to
                # Create an empty line in other model.
                old_x_node = LinkedListNode('x')
                start_node_other_model = old_x_node
                node = other_content.content[0]
                while node.pointing_to:
                    self.difficulty.linked_list_followed_pointing_to += 1
                    new_x_node = LinkedListNode('x')
                    old_x_node.pointing_to = new_x_node
                    old_x_node = new_x_node
                    node = node.pointing_to
                if node_in_this_model_index > node_in_other_model_index:
                    for i in range(node_in_this_model_index - node_in_other_model_index):
                        # Append it
                        self_content.new_node(start_node_this_model)
                        # Insert it
                        other_content.new_node(start_node_other_model, 0)
                if node_in_this_model_index < node_in_other_model_index:
                    for i in range(node_in_other_model_index - node_in_this_model_index):
                        # Insert it
                        self_content.new_node(start_node_this_model, 0)
                        # Append it
                        other_content.new_node(start_node_other_model)
            # The two sides should be prepared, now merge them
            for i, node in enumerate(other_content.content):
                # Go to the rightmost node on a layer, so it can point to the leftmost node on the other side
                while node.pointing_to:
                    self.difficulty.linked_list_followed_pointing_to += 1
                    node = node.pointing_to
                node.pointing_to = self_content.content[i]
            merged_content = other_content.content

        if parsed_line.relation == "above":
            if node_in_this_model_index == node_in_other_model_index:
                # Tokens are at the same vertical position
                pass
            elif node_in_this_model_index > node_in_other_model_index:
                # Token is further to the right in this model than in other model. Both have to be padded.
                for i in range(node_in_this_model_index - node_in_other_model_index):
                    # The vertical difference that has to be padded.
                    for i in range(len(self_content.content)):
                        # Padded in every layer (i.e. row)
                        node = self_content.content[i]
                        while node.pointing_to:
                            self.difficulty.linked_list_followed_pointing_to += 1
                            node = node.pointing_to
                        node.pointing_to = LinkedListNode('x')
                    for i in range(len(other_content.content)):
                        self.difficulty.linked_list_followed_pointing_to += 1
                        tmp = other_content.content[i]
                        new_x_node = LinkedListNode('x')
                        new_x_node.pointing_to = tmp
                        other_content.delete_node(other_content.content[i])
                        other_content.new_node(new_x_node, 0)
            elif node_in_this_model_index < node_in_other_model_index:
                # Token is further to the left in this model than in other model. Both have to be padded.
                for i in range(node_in_other_model_index - node_in_this_model_index):
                    # The vertical difference that has to be padded
                    for i in range(len(self_content.content)):
                        self.difficulty.linked_list_followed_pointing_to += 1
                        tmp = self_content.content[i]
                        new_x_node = LinkedListNode('x')
                        new_x_node.pointing_to = tmp
                        self_content.delete_node(self_content.content[i])
                        self_content.new_node(new_x_node, 0)
                    for i in range(len(other_content.content)):
                        self.difficulty.linked_list_followed_pointing_to += 1
                        other_content.content[i].pointing_to = LinkedListNode('x')
            merged_content = [x for x in self_content.content]
            for element in other_content.content:
                merged_content.append(element)

        if parsed_line.relation == "below":
            if node_in_this_model_index == node_in_other_model_index:
                # Tokens are at the same vertical position
                pass
            elif node_in_this_model_index > node_in_other_model_index:
                # Token is further to the right in this model than in other model. Both have to be padded.
                for i in range(node_in_this_model_index - node_in_other_model_index):
                    # The vertical difference that has to be padded.
                    for i in range(len(self_content.content)):
                        # Padded in every layer (i.e. row)
                        node = self_content.content[i]
                        while node.pointing_to:
                            self.difficulty.linked_list_followed_pointing_to += 1
                            node = node.pointing_to
                        node.pointing_to = LinkedListNode('x')
                    for i in range(len(other_content.content)):
                        self.difficulty.linked_list_followed_pointing_to += 1
                        tmp = other_content.content[i]
                        new_x_node = LinkedListNode('x')
                        new_x_node.pointing_to = tmp
                        other_content.delete_node(other_content.content[i])
                        other_content.new_node(new_x_node, 0)
            elif node_in_this_model_index < node_in_other_model_index:
                # Token is further to the left in this model than in other model. Both have to be padded.
                for i in range(node_in_other_model_index - node_in_this_model_index):
                    # The vertical difference that has to be padded
                    for i in range(len(self_content.content)):
                        self.difficulty.linked_list_followed_pointing_to += 1
                        tmp = self_content.content[i]
                        new_x_node = LinkedListNode('x')
                        new_x_node.pointing_to = tmp
                        self_content.delete_node(self_content.content[i])
                        self_content.new_node(new_x_node, 0)
                    for i in range(len(other_content.content)):
                        self.difficulty.linked_list_followed_pointing_to += 1
                        other_content.content[i].pointing_to = LinkedListNode('x')
            merged_content = [x for x in other_content.content]
            for element in self_content.content:
                merged_content.append(element)

        node_in_this_model_parent, node_in_this_model_index = self.find_node_parent_and_index(node_in_this_model)
        node_in_other_model_parent, node_in_other_model_index = other_content.find_node_parent_and_index(node_in_other_model)
        focus_this_model_parent, focus_this_model_index = self_content.find_node_parent_and_index(self_content.focus)
        focus_other_model_parent, focus_other_model_index = other_content.find_node_parent_and_index(other_content.focus)
        moved_focus_this_model = abs(focus_this_model_index - node_in_this_model_index)\
                                 + abs(self_content.find_linked_list_index(focus_this_model_parent) -
                                       self_content.find_linked_list_index(node_in_this_model_parent))
        moved_focus_other_model = abs(focus_other_model_index - node_in_other_model_index)\
                                 + abs(other_content.find_linked_list_index(focus_other_model_parent) -
                                       other_content.find_linked_list_index(node_in_other_model_parent))
        if moved_focus_this_model:
            self.difficulty.focus_move_ops += 1
            focus_direction = None
            if self.find_linked_list_index(focus_this_model_parent) == self.find_linked_list_index(node_in_this_model_parent) and \
               focus_this_model_index < node_in_this_model_index:
                focus_direction = "right"
            if self.find_linked_list_index(focus_this_model_parent) == self.find_linked_list_index(node_in_this_model_parent) and \
               focus_this_model_index > node_in_this_model_index:
                focus_direction = "left"
            if self.find_linked_list_index(focus_this_model_parent) > self.find_linked_list_index(node_in_this_model_parent) and \
               focus_this_model_index == node_in_this_model_index:
                focus_direction = "up"
            if self.find_linked_list_index(focus_this_model_parent) < self.find_linked_list_index(node_in_this_model_parent) and \
               focus_this_model_index == node_in_this_model_index:
                focus_direction = "down"
            if self.find_linked_list_index(focus_this_model_parent) != self.find_linked_list_index(node_in_this_model_parent) and \
               focus_this_model_index != node_in_this_model_index:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
        if moved_focus_other_model:
            other_content.difficulty.focus_move_ops += 1
            focus_direction = None
            if self.find_linked_list_index(focus_other_model_parent) == self.find_linked_list_index(node_in_other_model_parent) and \
               focus_other_model_index < node_in_other_model_index:
                focus_direction = "right"
            if self.find_linked_list_index(focus_other_model_parent) == self.find_linked_list_index(node_in_other_model_parent) and \
               focus_other_model_index > node_in_other_model_index:
                focus_direction = "left"
            if self.find_linked_list_index(focus_other_model_parent) > self.find_linked_list_index(node_in_other_model_parent) and \
               focus_other_model_index == node_in_other_model_index:
                focus_direction = "up"
            if self.find_linked_list_index(focus_other_model_parent) < self.find_linked_list_index(node_in_other_model_parent) and \
               focus_other_model_index == node_in_other_model_index:
                focus_direction = "down"
            if self.find_linked_list_index(focus_other_model_parent) != self.find_linked_list_index(node_in_other_model_parent) and \
               focus_other_model_index != node_in_other_model_index:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or other_content.focus_change_direction != focus_direction:
                other_content.focus_change_direction = focus_direction
                other_content.difficulty.focus_direction_changes += 1
        # Difficulty measure difficulty.moved_focus_by is moved by the distance that focus has to travel to mentioned
        # token in the merge premise
        moved_focus_by = moved_focus_this_model + moved_focus_other_model
        if moved_focus_by != 0:
            self.difficulty.focus_move_distance += moved_focus_by
            self.focus = node_in_this_model
            other_content.focus = node_in_other_model
            if self.focus is None or other_content.focus is None:
                raise MyExceptions.FocusError("Merge focus went to None")

        # Return new merged linked list with entries from both
        return merged_content, self.focus

    def to_infinite_list(self):
        """
        Because implementing combine supermodels was really difficult and it works for InfiniteLists, due to ease,
        I'll convert this LinkedList to a list so the combination can take place in InfiniteList.

        :return: A list object with the same content as this BST, formatted as in InfiniteList
        """
        as_list = []
        for node in self.content:
            layer_list = [node.token]
            while node.pointing_to:
                layer_list.append(node.pointing_to.token)
                node = node.pointing_to
            as_list.append(layer_list)
        return as_list

    def variate_model(self, parsed_conclusion, how_far_removed=0):
        """
        Generate alternative model(s) based on annotations and how far removed on the neighborhood graph an
        alternative model is (based on how many swap operations are necessary to gain it from original model).

        :param parsed_conclusion: The conclusion that is to be verified.
        :param how_far_removed: How far on the neighborhood graph the returned alternative models may be.
        :return: bool: If within how_far_removed a model is found that holds under parsed_conclusion, True.
                       Otherwise, False.
        """
        content_as_list = self.to_infinite_list(), (0, 0)
        inf_list = InfiniteList('', self.insert_type, self.merge_type, self.difficulty, content_as_list)
        inf_list.annotations = self.annotations
        if inf_list.variate_model(parsed_conclusion, how_far_removed):
            return True
        else:
            return False

    def evaluate_conclusion(self, parsed_conclusion):
        """
        Evaluate the truth of a given conclusion.

        :param parsed_conclusion: The conclusion to be checked
        :return: Boolean True/False
        """
        # Do the focus stuff
        if self.find(parsed_conclusion.first_token) and self.find(parsed_conclusion.second_token):
            first_token_node = self.find(parsed_conclusion.first_token)
            first_token_parent, first_token_index = self.find_node_parent_and_index(first_token_node)
            second_token_node = self.find(parsed_conclusion.second_token)
            second_token_parent, second_token_index = self.find_node_parent_and_index(second_token_node)

            if self.focus != first_token_node:
                self.difficulty.focus_move_ops += 1
                focus_parent, focus_index = self.find_node_parent_and_index(self.focus)
                moved_focus_by = abs(focus_index - first_token_index)\
                                 + abs(self.find_linked_list_index(focus_parent) -
                                       self.find_linked_list_index(first_token_parent))
                self.difficulty.focus_move_distance += moved_focus_by
                focus_direction = None
                if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(first_token_parent) and \
                   focus_index < first_token_index:
                    focus_direction = "right"
                if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(first_token_parent) and \
                   focus_index > first_token_index:
                    focus_direction = "left"
                if self.find_linked_list_index(focus_parent) > self.find_linked_list_index(first_token_parent) and \
                   focus_index == first_token_index:
                    focus_direction = "up"
                if self.find_linked_list_index(focus_parent) < self.find_linked_list_index(first_token_parent) and \
                   focus_index == first_token_index:
                    focus_direction = "down"
                if self.find_linked_list_index(focus_parent) != self.find_linked_list_index(first_token_parent) and \
                   focus_index != first_token_index:
                    focus_direction = "various_directions"
                if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                    self.focus_change_direction = focus_direction
                    self.difficulty.focus_direction_changes += 1
                self.focus = first_token_node

            if self.focus != second_token_node:
                self.difficulty.focus_move_ops += 1
                focus_parent, focus_index = self.find_node_parent_and_index(self.focus)
                moved_focus_by = abs(focus_index - second_token_index)\
                                 + abs(self.find_linked_list_index(focus_parent) -
                                       self.find_linked_list_index(second_token_parent))
                self.difficulty.focus_move_distance += moved_focus_by
                focus_direction = None
                if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(second_token_parent) and \
                   focus_index < second_token_index:
                    focus_direction = "right"
                if self.find_linked_list_index(focus_parent) == self.find_linked_list_index(second_token_parent) and \
                   focus_index > second_token_index:
                    focus_direction = "left"
                if self.find_linked_list_index(focus_parent) > self.find_linked_list_index(second_token_parent) and \
                   focus_index == second_token_index:
                    focus_direction = "up"
                if self.find_linked_list_index(focus_parent) < self.find_linked_list_index(second_token_parent) and \
                   focus_index == second_token_index:
                    focus_direction = "down"
                if self.find_linked_list_index(focus_parent) != self.find_linked_list_index(second_token_parent) and \
                   focus_index != second_token_index:
                    focus_direction = "various_directions"
                if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                    self.focus_change_direction = focus_direction
                    self.difficulty.focus_direction_changes += 1
                self.focus = second_token_node

        evaluation = False
        if parsed_conclusion.relation == "left":
            if self.find(parsed_conclusion.first_token) and self.find(parsed_conclusion.second_token):
                first_object_parent, first_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.first_token))
                second_object_parent, second_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.second_token))
                if first_object_index is not None and first_object_parent and \
                                second_object_index is not None and second_object_parent:
                    if first_object_index < second_object_index and first_object_parent == second_object_parent:
                        evaluation = True
        if parsed_conclusion.relation == "right":
            if self.find(parsed_conclusion.first_token) and self.find(parsed_conclusion.second_token):
                first_object_parent, first_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.first_token))
                second_object_parent, second_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.second_token))
                if first_object_index is not None and first_object_parent and \
                                second_object_index is not None and second_object_parent:
                    if first_object_index > second_object_index and first_object_parent == second_object_parent:
                        evaluation = True
        if parsed_conclusion.relation == "above":
            if self.find(parsed_conclusion.first_token) and self.find(parsed_conclusion.second_token):
                first_object_parent, first_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.first_token))
                second_object_parent, second_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.second_token))
                first_object_layer = self.find_linked_list_index(first_object_parent)
                second_object_layer = self.find_linked_list_index(second_object_parent)
                if first_object_index is not None and first_object_parent and \
                                second_object_index is not None and second_object_parent:
                    if first_object_index == second_object_index and first_object_layer < second_object_layer:
                        evaluation = True
        if parsed_conclusion.relation == "below":
            if self.find(parsed_conclusion.first_token) and self.find(parsed_conclusion.second_token):
                first_object_parent, first_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.first_token))
                second_object_parent, second_object_index = self.find_node_parent_and_index(self.find(parsed_conclusion.second_token))
                first_object_layer = self.find_linked_list_index(first_object_parent)
                second_object_layer = self.find_linked_list_index(second_object_parent)
                if first_object_index is not None and first_object_parent and \
                                second_object_index is not None and second_object_parent:
                    if first_object_index == second_object_index and first_object_layer > second_object_layer:
                        evaluation = True
        if evaluation:
            return True
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
        first_object_parent, first_object_index = self.find_node_parent_and_index(self.find(first_token))
        second_object_parent, second_object_index = self.find_node_parent_and_index(self.find(second_token))
        if first_object_parent == second_object_parent:
            if first_object_index < second_object_index:
                return "left"
            if first_object_index > second_object_index:
                return "right"
        elif first_object_index == second_object_index:
            if self.find_linked_list_index(first_object_parent) < self.find_linked_list_index(second_object_parent):
                return "above"
            if self.find_linked_list_index(first_object_parent) > self.find_linked_list_index(second_object_parent):
                return "below"
        else:
            return "no_rel"
