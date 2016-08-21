import copy
from Helpers import MyExceptions
from DataStructure import DataStructure

__author__ = 'Phaina'

"""Graph is a data structure that consists of a graph, represented as an adjacency matrix encoding relationships."""


class Graph(DataStructure):
    def __init__(self, parsed_line, insert_type, merge_type, difficulty, content=None):
        """
        :param parsed_line: The current line as parsed by Parser, i.e. first_token, relation, second_token
        :param content: Optional: Content to be used to fill InfiniteList object.
        :param insert_type: Currently used insert type, i.e. ff/fff
        :param merge_type: Currently used merge type, i.e. integrate/annotate/supermodels
        :param difficulty: Difficulty singleton handed down by Central Executive for measuring focus operations

        :var self.focus: Index of token currently in focus
        :var self.focus_change_direction: The last direction that focus was changed to.
        :var self.annotations: Annotations for indeterminate relationships between tokens
        :var self.supermodel: The supermodel that this model is contained in (in case of merge type supermodel)
        :var self.supermodel_index: The how-manyest supermodel this is from base models (for nesting parameter)
        """
        super(Graph, self).__init__()

        self.difficulty = difficulty
        self.insert_type = insert_type
        self.merge_type = merge_type
        self.focus = 1
        self.focus_change_direction = None
        self.token_indices = dict()
        self.annotations = dict()
        self.supermodel_index = 0
        self.supermodels = []

        if content is None:
            self.content = [['x']]
            self.create_from_parsed_line(parsed_line)
        else:
            # Content is a tuple: (content of list, focus of content)
            self.content = content[0]
            self.focus = content[1]
            for i, token in enumerate(self.content[0][1:]):
                self.token_indices[token] = i
            self.difficulty.graph_amount_relationships = self.amount_of_relationships()

    def __str__(self):
        return "Graph content: " + str(self.content)

    def __len__(self):
        return len(self.content)

    def amount_of_relationships(self):
        """
        Returns the amount of recorded relationships.

        :return: Amount of recorded relationships.
        """
        amount = 0
        for row in self.content[1:]:
            for column in row[1:]:
                if column != 'x':
                    amount += 1
        # Divided by two because the graph is undirected and therefore mirrored, every relationships is recorded twice.
        return amount/2

    def give_token_index(self, token):
        """
        Given a token, give that token an index (the next free one) and enter it into the dictionary mapping tokens
        to their indices in graph matrix.

        :param token: The token that should get inserted into token_indices dictionary
        """
        index = len(self)
        self.token_indices[token] = index

    def find(self, token):
        """
        Given a token, return its position. This is 1-dimensional since this graph is not directed and therefore
        mirrored. An index is the same column- as row-wise.

        :param token: The given token whose index should be returned
        :return: Index of that token or None if it's not in the graph
        """
        if token in self.content[0]:
            return self.content[0].index(token)
        else:
            return False

    def find_token_by_index(self, index):
        """
        Given an index, return the token name of that index.

        :param index: Index #
        :return: Token name at that index
        """
        for token in self.token_indices:
            if self.token_indices[token] == index:
                return token

    def forget(self, token):
        """
        Forget a given token, i.e. replace this token with string 'forgotten'.

        :param token: The token that should be forgotten.
        """
        index_of_token = self.find(token)
        self.content[0][index_of_token] = 'forgotten'
        self.content[index_of_token][0] = 'forgotten'

    def insert_token_into_graph(self, token):
        """
        Given a token that already has an index in token_indices, add it to the graph (both rows & cols).
        (No relationships yet, just give it a line and a column)

        :param token: The token that should be present in the graph
        """
        # Assert that this token already has an index. This index has to be the highest that was ever given out.
        # New nodes are never inserted in the middle since all ff/fff differences can be determined by giving
        # relationships in matrix instead of actually moving the tokens in the matrix.
        assert self.token_indices[token]
        # Give new token a new line
        self.content.append([token] + ['x' for x in self.content[0][1:]])
        # And a new column
        self.content[0].append(token)
        for row in self.content[1:]:
            row.append('x')

    def insert_relationship_into_graph(self, first_token, relationship, second_token):
        """
        Given two tokens, insert their relationship into the graph.

        :param first_token: The first token
        :param relationship: The relationship
        :param second_token: The second token
        """
        index_first_token = self.find(first_token)
        index_second_token = self.find(second_token)

        # From first token to second token insert relationship as is, e.g. 'A' left 'B'
        self.content[index_first_token][index_second_token] = relationship

        # From second token to first token insert relationship mirrored, e.g. 'B' right 'A'
        if relationship == "left":
            self.content[index_second_token][index_first_token] = "right"
        if relationship == "right":
            self.content[index_second_token][index_first_token] = "left"
        if relationship == "above":
            self.content[index_second_token][index_first_token] = "below"
        if relationship == "below":
            self.content[index_second_token][index_first_token] = "above"
        if relationship == "x":
            self.content[index_second_token][index_first_token] = "x"

    def insert(self, parsed_line):
        """
        Given two tokens, insert a relationship between them into the graph.

        :return True/False depending on whether insert worked
        """
        first_token = parsed_line.first_token
        second_token = parsed_line.second_token
        relationship = parsed_line.relation

        index_first_token = self.find(first_token)
        index_second_token = self.find(second_token)
        if not index_first_token:
            self.give_token_index(first_token)
            self.insert_token_into_graph(first_token)
            index_first_token = self.find(first_token)
        if not index_second_token:
            self.give_token_index(second_token)
            self.insert_token_into_graph(second_token)
            index_second_token = self.find(second_token)
        self.insert_relationship_into_graph(first_token, relationship, second_token)

        # Focus operations
        if self.focus != index_first_token:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus - index_first_token)
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus < index_first_token:
                focus_direction = "right"
            if self.focus > index_first_token:
                focus_direction = "left"
            # In a graph, there's no above/below, all tokens are "on the same layer"...
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = index_first_token

        # Propagate existing relationships of first token
        other_relationships_of_first_token = []
        for i, relation in enumerate(self.content[index_first_token][1:]):
            if i + 1 != index_second_token and relation != 'x':
                other_relationships_of_first_token.append((i + 1, relation))
        if relationship == "left":
            # FT left ST
            if second_token in self.annotations:
                self.annotate(second_token, "left", first_token)
            for other_relationship_of_first_token in other_relationships_of_first_token:
                if other_relationship_of_first_token[1] == "right":
                    self.insert_relationship_into_graph(second_token, "right",
                                                        self.find_token_by_index(other_relationship_of_first_token[0]))
                if other_relationship_of_first_token[1] == "left":
                    # This insert is indeterminate, because there's another thing that FT is right of.
                    self.annotate(first_token, "right", second_token)
                    if self.insert_type == "fff":
                        self.insert_relationship_into_graph(second_token, "right",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                    if self.insert_type == "ff":
                        self.insert_relationship_into_graph(second_token, "left",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                if other_relationship_of_first_token[1] == "above":
                    other_layer_index = other_relationship_of_first_token[0]
                    left_nodes = []
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "left":
                            left_nodes.append(j)
                    if len(left_nodes) == 1:
                        # It's obvious which node is to the right of the node above first node
                        self.insert_relationship_into_graph(self.find_token_by_index(left_nodes[0]), "below",
                                                            second_token)
                    else:
                        # Basically, what happens here is that we find the node that the above node is to the left to,
                        # but to the right of all other nodes that the above node is to the left to. So that node is
                        # the one above the one we just inserted
                        for left_node in left_nodes:
                            this_left_nodes_relationship = []
                            for j, relationship in enumerate(self.content[left_node][1:]):
                                if j in left_nodes and relationship == "right":
                                    this_left_nodes_relationship.append(j)
                            if len(this_left_nodes_relationship) == len(left_nodes) - 1:
                                self.insert_relationship_into_graph(left_node, "below", second_token)
                if other_relationship_of_first_token[1] == "below":
                    other_layer_index = other_relationship_of_first_token[0]
                    left_nodes = []
                    # The node below LO: Which nodes is it to the left to? (Because we're to the right of LO and trying
                    # to find out which node is above us)
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "left":
                            left_nodes.append(j + 1)
                    if len(left_nodes) == 1:
                        # It's obvious which node is to the right of the node below first node
                        self.insert_relationship_into_graph(self.find_token_by_index(left_nodes[0]), "above",
                                                            second_token)
                    else:
                        # Basically, what happens here is that we find the node that the below node is to the left to,
                        # but to the right of all other nodes that the below node is to the left to. So that node is
                        # the one below the one we just inserted
                        for left_node in left_nodes:
                            this_left_nodes_relationship = []
                            for j, relationship in enumerate(self.content[left_node][1:]):
                                if j + 1 in left_nodes and relationship == "left":
                                    this_left_nodes_relationship.append(j + 1)
                            if len(this_left_nodes_relationship) == len(left_nodes) - 1:
                                self.insert_relationship_into_graph(self.find_token_by_index(left_node), "above",
                                                                    second_token)
        if relationship == "right":
            # FT right ST
            if second_token in self.annotations:
                self.annotate(first_token, "right", second_token)
            for other_relationship_of_first_token in other_relationships_of_first_token:
                if other_relationship_of_first_token[1] == "left":
                    # Insert is indeterminate
                    self.annotate(first_token, "left", second_token)
                    self.insert_relationship_into_graph(second_token, "left",
                                                        self.find_token_by_index(other_relationship_of_first_token[0]))
                if other_relationship_of_first_token[1] == "right":
                    if self.insert_type == "fff":
                        self.insert_relationship_into_graph(second_token, "left",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                    if self.insert_type == "ff":
                        self.insert_relationship_into_graph(second_token, "right",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                if other_relationship_of_first_token[1] == "above":
                    if self.insert_type == "ff" and len(['x' for x in
                                                         other_relationships_of_first_token if x[1] == "right"]) > 0:
                        self.insert_relationship_into_graph(second_token, "above",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                        self.insert_relationship_into_graph(first_token, "x",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                    other_layer_index = other_relationship_of_first_token[0]
                    right_nodes = []
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "right":
                            right_nodes.append(j)
                    if len(right_nodes) == 1:
                        # It's obvious which node is to the left of the node above first node
                        self.insert_relationship_into_graph(self.find_token_by_index(right_nodes[0]), "below",
                                                            second_token)
                    else:
                        # Basically, what happens here is that we find the node that the above node is to the right to,
                        # but to the left of all other nodes that the above node is to the right to. So that node is
                        # the one above the one we just inserted
                        for right_node in right_nodes:
                            this_right_nodes_relationships = []
                            for j, relationship in enumerate(self.content[right_node][1:]):
                                if j in right_nodes and relationship == "left":
                                    this_right_nodes_relationships.append(j)
                            if len(this_right_nodes_relationships) == len(right_nodes) - 1:
                                self.insert_relationship_into_graph(right_node, "below", second_token)
                if other_relationship_of_first_token[1] == "below":
                    if self.insert_type == "ff" and len(['x' for x in
                                                         other_relationships_of_first_token if x[1] == "right"]) > 0:
                        self.insert_relationship_into_graph(second_token, "below",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                        self.insert_relationship_into_graph(first_token, "x",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                    other_layer_index = other_relationship_of_first_token[0]
                    right_nodes = []
                    # The node below LO: Which nodes is it to the left to? (Because we're to the right of LO and trying
                    # to find out which node is above us)
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "right":
                            right_nodes.append(j + 1)
                    if len(right_nodes) == 1:
                        # It's obvious which node is to the right of the node below first node
                        self.insert_relationship_into_graph(self.find_token_by_index(right_nodes[0]), "above",
                                                            second_token)
                    else:
                        # Basically, what happens here is that we find the node that the below node is to the left to,
                        # but to the right of all other nodes that the below node is to the left to. So that node is
                        # the one below the one we just inserted
                        for right_node in right_nodes:
                            this_right_nodes_relationships = []
                            for j, relationship in enumerate(self.content[right_node][1:]):
                                if j + 1 in right_nodes and relationship == "left":
                                    this_right_nodes_relationships.append(j + 1)
                            if len(this_right_nodes_relationships) == len(right_nodes) - 1:
                                self.insert_relationship_into_graph(self.find_token_by_index(right_node), "above",
                                                                    second_token)

        # Propagate existing relationships of second token
        other_relationships_of_second_token = []
        for i, relation in enumerate(self.content[index_second_token][1:]):
            if i + 1 != index_first_token and relation != 'x' and not \
                            [x for x in other_relationships_of_first_token if x[0] == i + 1]:
                other_relationships_of_second_token.append((i + 1, relation))
        if relationship == "left":
            # FT left ST
            if first_token in self.annotations:
                self.annotate(second_token, "left", first_token)
            for other_relationship_of_second_token in other_relationships_of_second_token:
                if other_relationship_of_second_token[1] == "left":
                    self.insert_relationship_into_graph(first_token, "left",
                                                        self.find_token_by_index(other_relationship_of_second_token[0]))
                if other_relationship_of_second_token[1] == "right":
                    # This insert is indeterminate, because there's another thing that FT is right of.
                    self.annotate(first_token, "right", second_token)
                    if self.insert_type == "fff":
                        self.insert_relationship_into_graph(first_token, "left",
                                                            self.find_token_by_index(other_relationship_of_second_token[0]))
                    if self.insert_type == "ff":
                        self.insert_relationship_into_graph(first_token, "right",
                                                            self.find_token_by_index(other_relationship_of_second_token[0]))
                if other_relationship_of_second_token[1] == "above":
                    if self.insert_type == "ff" and len(['x' for x in
                                                         other_relationships_of_first_token if x[1] == "left"]) > 0:
                        self.insert_relationship_into_graph(second_token, "above",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                        self.insert_relationship_into_graph(first_token, "x",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                    other_layer_index = other_relationship_of_second_token[0]
                    right_nodes = []
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "right":
                            right_nodes.append(j)
                    if len(right_nodes) == 1:
                        # It's obvious which node is to the left of the node above first node
                        self.insert_relationship_into_graph(self.find_token_by_index(right_nodes[0]), "below",
                                                            first_token)
                    else:
                        # Basically, what happens here is that we find the node that the above node is to the right to,
                        # but to the left of all other nodes that the above node is to the right to. So that node is
                        # the one above the one we just inserted
                        for right_node in right_nodes:
                            this_right_nodes_relationships = []
                            for j, relationship in enumerate(self.content[right_node][1:]):
                                if j in right_nodes and relationship == "left":
                                    this_right_nodes_relationships.append(j)
                            if len(this_right_nodes_relationships) == len(right_nodes) - 1:
                                self.insert_relationship_into_graph(right_node, "below", first_token)
                if other_relationship_of_second_token[1] == "below":
                    if self.insert_type == "ff" and len(['x' for x in
                                                         other_relationships_of_first_token if x[1] == "left"]) > 0:
                        self.insert_relationship_into_graph(second_token, "below",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                        self.insert_relationship_into_graph(first_token, "x",
                                                            self.find_token_by_index(other_relationship_of_first_token[0]))
                    other_layer_index = other_relationship_of_second_token[0]
                    right_nodes = []
                    # The node below LO: Which nodes is it to the left to? (Because we're to the right of LO and trying
                    # to find out which node is above us)
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "right":
                            right_nodes.append(j + 1)
                    if len(right_nodes) == 1:
                        # It's obvious which node is to the right of the node below first node
                        self.insert_relationship_into_graph(self.find_token_by_index(right_nodes[0]), "above",
                                                            first_token)
                    else:
                        # Basically, what happens here is that we find the node that the below node is to the left to,
                        # but to the right of all other nodes that the below node is to the left to. So that node is
                        # the one below the one we just inserted
                        for right_node in right_nodes:
                            this_right_nodes_relationships = []
                            for j, relationship in enumerate(self.content[right_node][1:]):
                                if j + 1 in right_nodes and relationship == "left":
                                    this_right_nodes_relationships.append(j + 1)
                            if len(this_right_nodes_relationships) == len(right_nodes) - 1:
                                self.insert_relationship_into_graph(self.find_token_by_index(right_node), "above",
                                                                    first_token)
        if relationship == "right":
            # FT right ST
            if first_token in self.annotations:
                self.annotate(second_token, "left", first_token)
            for other_relationship_of_second_token in other_relationships_of_second_token:
                if other_relationship_of_second_token[1] == "right":
                    # Insert is indeterminate
                    self.annotate(second_token, "right", first_token)
                    self.insert_relationship_into_graph(first_token, "right",
                                                        self.find_token_by_index(other_relationship_of_second_token[0]))
                if other_relationship_of_second_token[1] == "left":
                    if self.insert_type == "fff":
                        self.insert_relationship_into_graph(first_token, "right",
                                                            self.find_token_by_index(other_relationship_of_second_token[0]))
                    if self.insert_type == "fff":
                        self.insert_relationship_into_graph(first_token, "left",
                                                            self.find_token_by_index(other_relationship_of_second_token[0]))
                if other_relationship_of_second_token[1] == "above":
                    other_layer_index = other_relationship_of_second_token[0]
                    left_nodes = []
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "left":
                            left_nodes.append(j)
                    if len(left_nodes) == 1:
                        # It's obvious which node is to the right of the node above first node
                        self.insert_relationship_into_graph(self.find_token_by_index(left_nodes[0]), "below",
                                                            first_token)
                    else:
                        # Basically, what happens here is that we find the node that the above node is to the left to,
                        # but to the right of all other nodes that the above node is to the left to. So that node is
                        # the one above the one we just inserted
                        for left_node in left_nodes:
                            this_left_nodes_relationship = []
                            for j, relationship in enumerate(self.content[left_node][1:]):
                                if j in left_nodes and relationship == "right":
                                    this_left_nodes_relationship.append(j)
                            if len(this_left_nodes_relationship) == len(left_nodes) - 1:
                                self.insert_relationship_into_graph(left_node, "below", first_token)
                if other_relationship_of_second_token[1] == "below":
                    other_layer_index = other_relationship_of_second_token[0]
                    left_nodes = []
                    # The node below LO: Which nodes is it to the left to? (Because we're to the right of LO and trying
                    # to find out which node is above us)
                    for j, relationship in enumerate(self.content[other_layer_index][1:]):
                        if relationship == "left":
                            left_nodes.append(j + 1)
                    if len(left_nodes) == 1:
                        # It's obvious which node is to the right of the node below first node
                        self.insert_relationship_into_graph(self.find_token_by_index(left_nodes[0]), "above",
                                                            first_token)
                    else:
                        # Basically, what happens here is that we find the node that the below node is to the left to,
                        # but to the right of all other nodes that the below node is to the left to. So that node is
                        # the one below the one we just inserted
                        for left_node in left_nodes:
                            this_left_nodes_relationship = []
                            for j, relationship in enumerate(self.content[left_node][1:]):
                                if j + 1 in left_nodes and relationship == "left":
                                    this_left_nodes_relationship.append(j + 1)
                            if len(this_left_nodes_relationship) == len(left_nodes) - 1:
                                self.insert_relationship_into_graph(self.find_token_by_index(left_node), "above",
                                                                    first_token)
        # TODO?
        if relationship == "above":
            pass
        if relation == "below":
            pass

        # Focus operations
        if self.focus != index_second_token:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus - index_second_token)
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus < index_second_token:
                focus_direction = "right"
            if self.focus > index_second_token:
                focus_direction = "left"
            # In a graph, there's no above/below, all tokens are "on the same layer"...
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = index_second_token
        self.difficulty.graph_amount_relationships = self.amount_of_relationships()

        # So supermodels are up to date as well
        if self.supermodels:
            for model in self.supermodels:
                model.insert(parsed_line)

        # Nothing can go wrong (I hope), so this returns True
        return True

    def create_from_parsed_line(self, parsed_line):
        """
        Given a parsed line, set up graph and enter first two tokens.

        :param parsed_line: The parsed line containing the first two tokens.
        """
        self.give_token_index(parsed_line.first_token)
        self.insert_token_into_graph(parsed_line.first_token)
        self.give_token_index(parsed_line.second_token)
        self.insert_token_into_graph(parsed_line.second_token)
        self.insert_relationship_into_graph(parsed_line.first_token, parsed_line.relation, parsed_line.second_token)
        self.difficulty.graph_amount_relationships += self.amount_of_relationships()

    def merge(self, graph, parsed_line):
        """
        Merge this graph with another graph object on the basis of parsed line (gives the relation
        between two tokens, which are part of different models).
        Uses strategy integrate, i.e. returns a list of merged content.

        :param: graph: The other graph object which with this one should be merged.
        :param: parsed_line: The parsed line that describes the relation between two models.

        :return new_content, focus: New content of merged graph and focus.
        """
        this_content = copy.deepcopy(self)
        tokens_in_this_content = this_content.content[0][1:]
        other_content = copy.deepcopy(graph)
        tokens_in_other_content = other_content.content[0][1:]
        if parsed_line.first_token in tokens_in_this_content:
            # Focus
            moved_focus_this_model = abs(this_content.focus - this_content.token_indices[parsed_line.first_token])
            moved_focus_other_model = abs(other_content.focus - other_content.token_indices[parsed_line.second_token])
            if this_content.focus != this_content.token_indices[parsed_line.first_token]:
                this_content.difficulty.focus_move_ops += 1
                moved_focus_by = abs(this_content.focus - this_content.token_indices[parsed_line.first_token])
                this_content.difficulty.focus_move_distance += moved_focus_by
                focus_direction = None
                if this_content.focus < this_content.token_indices[parsed_line.first_token]:
                    focus_direction = "right"
                if this_content.focus > this_content.token_indices[parsed_line.first_token]:
                    focus_direction = "left"
                # In a graph, there's no above/below, all tokens are "on the same layer"...
                if focus_direction == "various_directions" or this_content.focus_change_direction != focus_direction:
                    this_content.focus_change_direction = focus_direction
                    this_content.difficulty.focus_direction_changes += 1
            if other_content.focus != other_content.token_indices[parsed_line.second_token]:
                other_content.difficulty.focus_move_ops += 1
                moved_focus_by = abs(other_content.focus - other_content.token_indices[parsed_line.second_token])
                other_content.difficulty.focus_move_distance += moved_focus_by
                focus_direction = None
                if other_content.focus < other_content.token_indices[parsed_line.second_token]:
                    focus_direction = "right"
                if other_content.focus > other_content.token_indices[parsed_line.second_token]:
                    focus_direction = "left"
                # In a graph, there's no above/below, all tokens are "on the same layer"...
                if focus_direction == "various_directions" or other_content.focus_change_direction != focus_direction:
                    other_content.focus_change_direction = focus_direction
                    other_content.difficulty.focus_direction_changes += 1
            this_content.focus = this_content.token_indices[parsed_line.first_token]
            other_content.focus = other_content.token_indices[parsed_line.second_token]
            if moved_focus_this_model + moved_focus_other_model != 0:
                this_content.difficulty.focus_move_distance += moved_focus_other_model + moved_focus_this_model

            # Merge stuff
            if parsed_line.relation == "left":
                # This data structure is to the left of the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are to the left of all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "left", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
            if parsed_line.relation == "right":
                # This data structure is to the right of the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are to the right of all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "right", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
            if parsed_line.relation == "above":
                # This data structure is to the above of the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are to above all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "above", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
            if parsed_line.relation == "below":
                # This data structure is below the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are below all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "below", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
        if parsed_line.second_token in tokens_in_this_content:
            # Focus
            moved_focus_this_model = abs(this_content.focus - this_content.token_indices[parsed_line.second_token])
            moved_focus_other_model = abs(other_content.focus - other_content.token_indices[parsed_line.first_token])
            if this_content.focus != this_content.token_indices[parsed_line.second_token]:
                this_content.difficulty.focus_move_ops += 1
                moved_focus_by = abs(this_content.focus - this_content.token_indices[parsed_line.second_token])
                this_content.difficulty.focus_move_distance += moved_focus_by
                focus_direction = None
                if this_content.focus < this_content.token_indices[parsed_line.second_token]:
                    focus_direction = "right"
                if this_content.focus > this_content.token_indices[parsed_line.second_token]:
                    focus_direction = "left"
                # In a graph, there's no above/below, all tokens are "on the same layer"...
                if focus_direction == "various_directions" or this_content.focus_change_direction != focus_direction:
                    this_content.focus_change_direction = focus_direction
                    this_content.difficulty.focus_direction_changes += 1
            if other_content.focus != other_content.token_indices[parsed_line.first_token]:
                other_content.difficulty.focus_move_ops += 1
                moved_focus_by = abs(other_content.focus - other_content.token_indices[parsed_line.first_token])
                other_content.difficulty.focus_move_distance += moved_focus_by
                focus_direction = None
                if other_content.focus < other_content.token_indices[parsed_line.first_token]:
                    focus_direction = "right"
                if other_content.focus > other_content.token_indices[parsed_line.first_token]:
                    focus_direction = "left"
                # In a graph, there's no above/below, all tokens are "on the same layer"...
                if focus_direction == "various_directions" or other_content.focus_change_direction != focus_direction:
                    other_content.focus_change_direction = focus_direction
                    other_content.difficulty.focus_direction_changes += 1
            if moved_focus_this_model + moved_focus_other_model != 0:
                this_content.difficulty.focus_move_distance += moved_focus_other_model + moved_focus_this_model
            this_content.focus = this_content.token_indices[parsed_line.second_token]
            other_content.focus = other_content.token_indices[parsed_line.first_token]

            # Merge stuff
            if parsed_line.relation == "left":
                # This data structure is to the right of the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are to the right of all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "right", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
            if parsed_line.relation == "left":
                # This data structure is to the left of the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are to the left of all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "left", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
            if parsed_line.relation == "above":
                # This data structure is below the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are below all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "below", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
            if parsed_line.relation == "below":
                # This data structure is above the other data structure
                for token_there in tokens_in_other_content:
                    this_content.give_token_index(token_there)
                    this_content.insert_token_into_graph(token_there)
                    # All tokens from this graph are above all tokens in other graph
                    for token_here in tokens_in_this_content:
                        this_content.insert_relationship_into_graph(token_here, "above", token_there)
                # Take relationships of other graph as is
                for token_there_2 in tokens_in_other_content:
                    for token_there in tokens_in_other_content:
                        if token_there != token_there_2:
                            this_content.insert_relationship_into_graph(token_there,
                                                                        other_content.generate(token_there, token_there_2),
                                                                        token_there_2)
        # self.difficulty.graph_amount_relationships = this_content.amount_of_relationships()
        return this_content.content, this_content.focus

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
            if (relation, token) in self.annotations[indeterminately_inserted_token]:
                pass
            else:
                self.annotations[indeterminately_inserted_token].append((relation, token))
        else:
            self.annotations[indeterminately_inserted_token] = [(relation, token)]
        self.difficulty.annotation_ops += 1

    def variate_model(self, parsed_conclusion, how_far_removed=0):
        """
        Generate alternative model(s) based on annotations and how far removed on the neighborhood graph an
        alternative model is (based on how many swap operations are necessary to gain it from original model).

        :param parsed_conclusion: The conclusion that is to be verified.
        :param how_far_removed: How far on the neighborhood graph the returned alternative models may be.
        :return: bool: If within how_far_removed a model is found that holds under parsed_conclusion, True.
                       Otherwise, False.
        """
        # Swapping here works as follows:
        # "Hard" tokens are those which are referenced in annotations. These relationships won't change.
        # "Soft" tokens are those that are not mentioned. Relationships within soft tokens can be swapped.
        soft_tokens = [x for x in self.content[0][1:] if x not in self.annotations]

        # One valid graph is the original one.
        valid_graphs = [[self]]

        while how_far_removed > 0:
            for combination in valid_graphs[-1]:
                # print("Variating model, still {} times. "
                #       "Alternate models discovered: {}".format(how_far_removed - 1, valid_graphs))
                # In the last created layer of graph, is there a model in which the conclusion holds?
                if combination.generate(parsed_conclusion.first_token, parsed_conclusion.second_token, combination) == parsed_conclusion.relation:
                    return True
                else:
                    # Construct a new layer
                    valid_combinations_at_this_distance = []
                    for soft_token_1 in soft_tokens:
                        for soft_token_2 in soft_tokens:
                            if soft_token_1 != soft_token_2:
                                dc_combi = copy.deepcopy(combination)
                                new_graph = Graph('', self.insert_type, self.merge_type, self.difficulty,
                                                  (dc_combi.content, dc_combi.focus))
                                take_in = True
                                relationship = new_graph.generate(soft_token_1, soft_token_2)
                                # Now reverse this relationship
                                if relationship == "left":
                                    new_graph.insert_relationship_into_graph(soft_token_1, "right", soft_token_2)
                                if relationship == "right":
                                    new_graph.insert_relationship_into_graph(soft_token_1, "left", soft_token_2)
                                if relationship == "above":
                                    new_graph.insert_relationship_into_graph(soft_token_1, "below", soft_token_2)
                                if relationship == "below":
                                    new_graph.insert_relationship_into_graph(soft_token_1, "above", soft_token_2)
                                # Check that this didn't break any hard relation from annotations
                                for token in self.annotations:
                                    for relationship in self.annotations[token]:
                                        if self.generate(token, relationship[1], combination) != relationship[0]:
                                            take_in = False
                                # And it shouldn't have been seen before
                                for seen_combinations in valid_graphs:
                                    if new_graph in seen_combinations or \
                                                    new_graph.content in [x.content for x in valid_combinations_at_this_distance]:
                                        take_in = False
                                if take_in:
                                    valid_combinations_at_this_distance.append(new_graph)
                        if valid_combinations_at_this_distance:
                            valid_graphs.append(valid_combinations_at_this_distance)
            how_far_removed -= 1
        # If no valid graph was found, return False
        return False

    def evaluate_conclusion(self, parsed_conclusion):
        """
        Given a parsed conclusion, evaluate its truth and return Boolean t/f.

        :param parsed_conclusion: The parsed conclusion whose truth should be evaluated.
        :return: T/F
        """
        # Esp. in case of supermodel merge, sometimes tokens are not in this model at all
        if not parsed_conclusion.first_token in self.token_indices or not parsed_conclusion.second_token in self.token_indices:
            return False

        # Focus operations
        if self.focus != self.token_indices[parsed_conclusion.first_token]:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus - self.token_indices[parsed_conclusion.first_token])
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus < self.token_indices[parsed_conclusion.first_token]:
                focus_direction = "right"
            if self.focus > self.token_indices[parsed_conclusion.first_token]:
                focus_direction = "left"
            # In a graph, there's no above/below, all tokens are "on the same layer"...
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = self.token_indices[parsed_conclusion.second_token]
        if self.focus != self.token_indices[parsed_conclusion.second_token]:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus - self.token_indices[parsed_conclusion.second_token])
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus < self.token_indices[parsed_conclusion.second_token]:
                focus_direction = "right"
            if self.focus > self.token_indices[parsed_conclusion.second_token]:
                focus_direction = "left"
            # In a graph, there's no above/below, all tokens are "on the same layer"...
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = self.token_indices[parsed_conclusion.second_token]

        index_first_token = self.find(parsed_conclusion.first_token)
        index_second_token = self.find(parsed_conclusion.second_token)
        if self.content[index_first_token][index_second_token] == parsed_conclusion.relation:
            return True
        else:
            return False

    def generate(self, first_token, second_token, graph=None):
        """
        Given two tokens, return the relationship between them. (or "no_rel")

        :param first_token: The first token
        :param second_token: The second token
        :param graph: A graph for which the relationship should be evaluated
        :return: Their relationship as a string
        """
        if not graph:
            index_first_token = self.find(first_token)
            index_second_token = self.find(second_token)
            relationship = self.content[index_first_token][index_second_token]
        else:
            index_first_token = graph.find(first_token)
            index_second_token = graph.find(second_token)
            relationship = graph.content[index_first_token][index_second_token]

        if relationship == "x":
            return "no_rel"
        else:
            return relationship
