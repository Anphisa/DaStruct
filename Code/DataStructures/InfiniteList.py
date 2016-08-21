import copy
from Helpers import MyExceptions
from DataStructure import DataStructure

__author__ = 'Phaina'

"""InfiniteList is a data structure that consists of nested infinite lists (nesting is for 2D)."""


class InfiniteList(DataStructure):
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
        super(InfiniteList, self).__init__()

        self.difficulty = difficulty
        self.insert_type = insert_type
        self.merge_type = merge_type
        self.focus = None
        self.focus_change_direction = None
        self.annotations = dict()
        self.supermodel_index = 0
        self.supermodels = []

        if content is None:
            self.create_from_parsed_line(parsed_line)
        else:
            # Content is a tuple: (content of list, focus of content)
            self.content = content[0]
            self.focus = content[1]

    def __str__(self):
        return "InfiniteList content: " + str(self.content)

    def __len__(self):
        size = 0
        for row in self.content:
            for column in row:
                if column != "x":
                    size += 1
        return size

    def rows(self):
        return len(self.content)

    def columns(self):
        return len(self.content[0])

    def create_from_parsed_line(self, parsed_line):
        """
        Insert tokens from parsed line into an infinite list in correct order as determined by relation.

        :param parsed_line: Initial parsed line.

        :var parsed_line.relation: Determines the relation between the two tokens
        :var parsed_line.first_token, parsed_line.second_token: The two tokens to be inserted into the data structure.
        """
        if parsed_line.relation == "left":
            self.content = [[parsed_line.first_token, parsed_line.second_token]]
        elif parsed_line.relation == "right":
            self.content = [[parsed_line.second_token, parsed_line.first_token]]
        elif parsed_line.relation == "above":
            self.content = [[parsed_line.first_token], [parsed_line.second_token]]
        elif parsed_line.relation == "below":
            self.content = [[parsed_line.second_token], [parsed_line.first_token]]

        # Set initial focus to that of the parsed line
        if parsed_line.focus:
            if len(parsed_line.focus) == 1:
                if parsed_line.focus == parsed_line.first_token:
                    self.focus = self.find_index(parsed_line.second_token)
                else:
                    self.focus = self.find_index(parsed_line.first_token)
                if self.focus is None:
                    raise MyExceptions.FocusError("InfiniteList.create_from_parsed_line focus went to None")
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
                                                        "InfiniteList.create_from_parsed_line()")

    def find(self, token):
        """
        Return True or False depending on whether token exists in this data structure.

        :param token: The token to be found
        :return: True/False depending on whether token exists in this data structure
        """
        if self.find_index(token) is not None:
            return True
        return False

    def find_index(self, token):
        """
        Return index of token in this data structure.

        :param token: The token to be found
        :return: Index of token (row, column)
        """
        index = None
        for i, item in enumerate(self.content):
            if item.count(token) != 0:
                index = i, item.index(token)
        return index

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
        index_of_token = self.find_index(token)
        self.content[index_of_token[0]][index_of_token[1]] = 'forgotten'

    def insert(self, parsed_line):
        """
        Given a parsed object (first_token, relation, second_token), insert it into this data structure.

        Fill free space with x's for possible gaps, so that situations such as:
        ['A',  x,  'B']
        ['C', 'D', 'E']
        are accounted for.

        :param: parsed_line: A parsed line (premise or conclusion)

        :var: self.insert_type: ff: First fit, fff: First free fit

        :return: True if insert worked
        """
        if self.find(parsed_line.first_token):
            located_object = parsed_line.first_token
            located_object_index = self.find_index(parsed_line.first_token)
            reference_object = parsed_line.second_token
        else:
            # In this case the relation has to be inverted, because it's always LO rel RO.
            parsed_line.invert()
            located_object = parsed_line.second_token
            located_object_index = self.find_index(parsed_line.second_token)
            reference_object = parsed_line.first_token

        # Currently self.focus is not actually changed here but only at the end of insert. This is not critical
        # since insert function can't be left in the middle. Would be more elegant to fix this.
        # Need to move focus to located object first
        if self.focus != located_object_index:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus[0] - located_object_index[0]) + abs(self.focus[1] - located_object_index[1])
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus[0] == located_object_index[0] and \
               self.focus[1] < located_object_index[1]:
                focus_direction = "right"
            if self.focus[0] == located_object_index[0] and \
               self.focus[1] > located_object_index[1]:
                focus_direction = "left"
            if self.focus[0] > located_object_index[0] and \
               self.focus[1] == located_object_index[1]:
                focus_direction = "up"
            if self.focus[0] < located_object_index[0] and \
               self.focus[1] == located_object_index[1]:
                focus_direction = "down"
            if self.focus[0] != located_object_index[0] and \
               self.focus[1] != located_object_index[1]:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1

        # If the insertion is indeterminate, i.e. the position of the token is not absolutely obvious,
        # annotate the RO so that in the model variation phase alternative models can be constructed
        indeterminate = True
        if parsed_line.relation == "left":
            if (located_object_index[1] == len(self.content[located_object_index[0]]) - 1) or \
               (self.content[located_object_index[0]][located_object_index[1] + 1] == 'x'):
                indeterminate = False
        if parsed_line.relation == "right":
            if (located_object_index[1] == 0) or \
               (self.content[located_object_index[0]][located_object_index[1] - 1] == 'x'):
                indeterminate = False
        if parsed_line.relation == "below":
            if (located_object_index[0] == 0) or \
               (self.content[located_object_index[0] - 1][located_object_index[1]] == 'x'):
                indeterminate = False
        if parsed_line.relation == "above":
            if (located_object_index[0] == len(self.content) - 1) or \
               (self.content[located_object_index[0] + 1][located_object_index[1]] == 'x'):
                indeterminate = False
        if indeterminate:
            parsed_line.invert()
            self.annotate(self.content[located_object_index[0]][located_object_index[1]], parsed_line.relation,
                          reference_object)
            parsed_line.invert()
        # If the LO is itself ambiguous in position, it might need to be moved in the MVP.
        # Therefore it'll be annotated with new information so that it doesn't get moved/switched wrongly.
        if self.content[located_object_index[0]][located_object_index[1]] in self.annotations:
            self.annotations[self.content[located_object_index[0]][located_object_index[1]]].append(
                (parsed_line.relation,
                 reference_object))

        if self.insert_type == "ff":
            if parsed_line.relation == "right":
                # Located object is to the right of reference object.
                self.content[located_object_index[0]].insert(located_object_index[1], reference_object)
                for i, item in enumerate(self.content):
                    if i != located_object_index[0]:
                        self.content[i].insert(located_object_index[1], "x")
            if parsed_line.relation == "left":
                # Located object is to the left of reference object.
                self.content[located_object_index[0]].insert(located_object_index[1] + 1, reference_object)
                for i, item in enumerate(self.content):
                    if i != located_object_index[0]:
                        self.content[i].insert(located_object_index[1] + 1, "x")
            else:
                second_layer = ["x" for x in self.content[located_object_index[0]]]
                second_layer[located_object_index[1]] = reference_object
                if parsed_line.relation == "below":
                    # Located object is below reference object.
                    if located_object_index[0] == 0 or \
                       self.content[located_object_index[0] - 1][located_object_index[1]] != 'x':
                        # Either there's no layer below or the position that second token would take is occupied
                        self.content.insert(located_object_index[0], second_layer)
                    else:
                        # There's a layer above and it's free
                        self.content[located_object_index[0] - 1][located_object_index[1]] = reference_object
                if parsed_line.relation == "above":
                    # Located object is above reference object
                    if located_object_index[0] == len(self.content) - 1 or \
                       self.content[located_object_index[0] + 1][located_object_index[1]] != 'x':
                        # Either there's no layer above or the position is occupied
                        self.content.insert(located_object_index[0] + 1, second_layer)
                    else:
                        # There's a layer below and it's free
                        self.content[located_object_index[0] + 1][located_object_index[1]] = reference_object

        if self.insert_type == "fff":
            if parsed_line.relation == "right":
                # Located object is right of reference object.
                x_pos = None
                for i, token in enumerate(self.content[located_object_index[0]][:located_object_index[1]]):
                    # Everything that is to the left of first token
                    if token == "x":
                        x_pos = i
                if x_pos is not None:
                    # The leftmost 'x' (by natural traversal order of list) is now replaced by first token
                    self.content[located_object_index[0]][x_pos] = reference_object
                else:
                    # No 'x' was found, need to insert at left edge of list.
                    self.content[located_object_index[0]].insert(0, reference_object)
                    for i, layer in enumerate(self.content):
                        if i != located_object_index[0]:
                            self.content[i].insert(0, "x")
            if parsed_line.relation == "left":
                # Located object is left of reference object.
                x_pos = None
                for i, token in enumerate(self.content[located_object_index[0]][located_object_index[1] + 1:]):
                    # Everything that is to the right of the first token
                    if token == "x":
                        x_pos = i
                        break
                if x_pos is not None:
                    # The rightmost 'x' (due to breaking after finding first 'x') is now replaced by second token
                    self.content[located_object_index[0]][x_pos] = reference_object
                else:
                    # No 'x' was found, need to insert at right edge of list.
                    self.content[located_object_index[0]].append(reference_object)
                    for i, layer in enumerate(self.content):
                        if i != located_object_index[0]:
                            self.content[i].append('x')
            else:
                second_layer = ["x" for x in self.content[located_object_index[0]]]
                second_layer[located_object_index[1]] = reference_object
                if parsed_line.relation == "below":
                    # Located object is below reference object.
                    if located_object_index[0] == 0:
                        # There is no layer above, it needs to be inserted
                        self.content.insert(0, second_layer)
                    else:
                        # There is at least one layer above, second token needs to be inserted into one of them
                        x_pos = None
                        for i in range(len(self.content[:located_object_index[0]])):
                            if self.content[i][located_object_index[1]] == "x":
                                x_pos = i
                        if x_pos is not None:
                            self.content[x_pos][located_object_index[1]] = reference_object
                        else:
                            # There is no free position above, a new layer has to be inserted at the top
                            self.content.insert(0, second_layer)
                if parsed_line.relation == "above":
                    # Located object is above reference object.
                    if located_object_index[0] == len(self.content) - 1:
                        # There is no layer below, it needs to be inserted
                        self.content.append(second_layer)
                    else:
                        # There is at least one layer below, second token needs to be inserted into one of them
                        x_pos = None
                        for i in range(len(self.content[located_object_index[0] + 1:])):
                            if self.content[i + located_object_index[0] + 1][located_object_index[1]] == "x":
                                x_pos = i + located_object_index[0] + 1
                                break
                        if x_pos is not None:
                            self.content[x_pos][located_object_index[1]] = reference_object
                        else:
                            # There is no free position below, a new layer has to be appended to the end
                            self.content.append(second_layer)

        # Difficulty measure difficulty.focus_move_distance is updated by the distance that focus had to move
        # self.focus is also updated to new focus object
        located_object_now_at = self.find_index(located_object)
        moved_focus_by = abs(located_object_now_at[0] - self.find_index(reference_object)[0]) \
                         + abs(located_object_now_at[1] - self.find_index(reference_object)[1])
        if moved_focus_by != 0:
            # Noticing in which direction the focus changed
            if located_object_now_at[0] == self.find_index(reference_object)[0] and \
               located_object_now_at[1] < self.find_index(reference_object)[1]:
                focus_direction = "right"
            if located_object_now_at[0] == self.find_index(reference_object)[0] and \
               located_object_now_at[1] > self.find_index(reference_object)[1]:
                focus_direction = "left"
            if located_object_now_at[0] > self.find_index(reference_object)[0] and \
               located_object_now_at[1] == self.find_index(reference_object)[1]:
                focus_direction = "up"
            if located_object_now_at[0] < self.find_index(reference_object)[0] and \
               located_object_now_at[1] == self.find_index(reference_object)[1]:
                focus_direction = "down"
            if self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            # Noticing focus distance and updating self.focus
            self.difficulty.focus_move_distance += moved_focus_by
            self.focus = self.find_index(reference_object)
            self.difficulty.focus_move_ops += 1
            if self.focus is None:
                raise MyExceptions.FocusError("Insert focus went to None")

        # So supermodels are up to date as well
        if self.supermodels:
            for model in self.supermodels:
                model.insert(parsed_line)
        # Returns true because there's no condition (such as size limit) under which insert would not be carried out.
        return True

    def merge(self, infinite_list, parsed_line):
        """
        Merge this infinite list with another infinite list object on the basis of parsed line (gives the relation
        between two tokens, which are part of different models).
        Uses strategy integrate, i.e. returns a list of merged content.

        E.g. Merge:
        [['A', 'B'], ['C', 'D']] with [['Y', 'E'], ['F', 'G']]
        on basis 'B left Y' yields
        [['A', 'B', 'Y', 'E'], ['C', 'D', 'F', 'G']].

        :param: infinite_list: The other infinite list object which with this one should be merged.
        :param: parsed_line: The parsed line that describes the relation between two models.

        :return new_content, self.focus: New content of merged nested lists and focus for that nested list.
        """
        self_content = copy.deepcopy(self.content)
        other_list_content = copy.deepcopy(infinite_list.content)

        if self.find(parsed_line.first_token):
            index_of_token_in_this_model = self.find_index(parsed_line.first_token)
            index_of_token_in_other_model = infinite_list.find_index(parsed_line.second_token)
        else:
            index_of_token_in_this_model = self.find_index(parsed_line.second_token)
            index_of_token_in_other_model = infinite_list.find_index(parsed_line.first_token)

        if parsed_line.relation == "left":
            if index_of_token_in_this_model[0] == index_of_token_in_other_model[0]:
                # Tokens are on same height.
                if len(self_content) == len(other_list_content):
                    # Can simply zip the two infinite lists.
                    pass
                elif len(self_content) > len(other_list_content):
                    # Append empty lines to infinite list so it's long enough to be zipped.
                    for i in range(len(self_content) - len(other_list_content)):
                        other_list_content.append(['x' for x in other_list_content[0]])
                elif len(other_list_content) > len(self_content):
                    # Append empty lines to infinite list so it's long enough to be zipped.
                    for i in range(len(other_list_content) - len(self_content)):
                        self_content.append(['x' for x in self_content[0]])
            else:
                # Tokens are not on the same height. The height difference needs to be padded
                # with 'x's so that the lists can be zipped.
                if index_of_token_in_this_model[0] > index_of_token_in_other_model[0]:
                    for i in range(index_of_token_in_this_model[0] - index_of_token_in_other_model[0]):
                        self_content.append(['x' for x in self_content[0]])
                        other_list_content.insert(0, ['x' for x in other_list_content[0]])
                if index_of_token_in_other_model[0] > index_of_token_in_this_model[0]:
                    for i in range(index_of_token_in_other_model[0] - index_of_token_in_this_model[0]):
                        other_list_content.append(['x' for x in other_list_content[0]])
                        self_content.insert(0, ['x' for x in self_content[0]])
            # The lists are zipped and can then be used to create_from_parsed_line a new infinite list object.
            new_content = [a + b for a, b in zip(self_content, other_list_content)]
        if parsed_line.relation == "right":
            if index_of_token_in_this_model[0] == index_of_token_in_other_model[0]:
                # Tokens are on same height.
                if len(self_content) == len(other_list_content):
                    # Can simply zip the two infinite lists.
                    pass
                elif len(self_content) > len(other_list_content):
                    # Append empty lines to infinite list so it's long enough to be zipped.
                    for i in range(len(self_content) - len(other_list_content)):
                        other_list_content.append(['x' for x in other_list_content[0]])
                elif len(other_list_content) > len(self_content):
                    # Append empty lines to infinite list so it's long enough to be zipped.
                    for i in range(len(other_list_content) - len(self_content)):
                        self_content.append(['x' for x in self_content[0]])
            else:
                # Tokens are not on the same height. The height difference needs to be padded
                # with 'x's so that the lists can be zipped.
                if index_of_token_in_this_model[0] > index_of_token_in_other_model[0]:
                    for i in range(index_of_token_in_this_model[0] - index_of_token_in_other_model[0]):
                        self_content.append(['x' for x in self_content[0]])
                        other_list_content.insert(0, ['x' for x in other_list_content[0]])
                if index_of_token_in_other_model[0] > index_of_token_in_this_model[0]:
                    for i in range(index_of_token_in_other_model[0] - index_of_token_in_this_model[0]):
                        other_list_content.append(['x' for x in other_list_content[0]])
                        self_content.insert(0, ['x' for x in self_content[0]])
            # The lists are zipped and can then be used to create_from_parsed_line a new infinite list object.
            new_content = [a + b for a, b in zip(other_list_content, self_content)]
        if parsed_line.relation == "above":
            if index_of_token_in_this_model[1] == index_of_token_in_other_model[1]:
                # Tokens are at same vertical position.
                pass
            elif index_of_token_in_this_model[1] > index_of_token_in_other_model[1]:
                # Token is further to the right in this model than in other model. Both have to be padded.
                for i in range(index_of_token_in_this_model[1] - index_of_token_in_other_model[1]):
                    # The vertical difference that has to be padded.
                    for i in range(len(self_content) - 1):
                        # Padded in every layer (i.e. column)
                        self_content[i].append('x')
                    for i in range(len(other_list_content) - 1):
                        other_list_content[i].insert(0, 'x')
            elif index_of_token_in_this_model[1] < index_of_token_in_other_model[1]:
                # Token is further to the left in this model than in other model. Both have to be padded.
                for i in range(index_of_token_in_other_model[1] - index_of_token_in_this_model[1]):
                    for i in range(len(self_content) - 1):
                        self_content[i].insert(0, 'x')
                    for i in range(len(other_list_content) - 1):
                        other_list_content[i].append('x')
            new_content = [x for x in self_content]
            for element in other_list_content:
                new_content.append(element)
        if parsed_line.relation == "below":
            if index_of_token_in_this_model[1] == index_of_token_in_other_model[1]:
                # Tokens are at same vertical position.
                pass
            elif index_of_token_in_this_model[1] > index_of_token_in_other_model[1]:
                # Token is further to the right in this model than in other model. Both have to be padded.
                for i in range(index_of_token_in_this_model[1] - index_of_token_in_other_model[1]):
                    # The vertical difference that has to be padded.
                    for i in range(len(self_content) - 1):
                        # Padded in every layer (i.e. column)
                        self_content[i].append('x')
                    for i in range(len(other_list_content) - 1):
                        other_list_content[i].insert(0, 'x')
            elif index_of_token_in_this_model[1] < index_of_token_in_other_model[1]:
                # Token is further to the left in this model than in other model. Both have to be padded.
                for i in range(index_of_token_in_other_model[1] - index_of_token_in_this_model[1]):
                    for i in range(len(self_content) - 1):
                        self_content[i].insert(0, 'x')
                    for i in range(len(other_list_content) - 1):
                        other_list_content[i].append('x')
            new_content = [x for x in other_list_content]
            for element in self_content:
                new_content.append(element)

        # Difficulty measure difficulty.focus_move_ops is determined by whether the focus needed to be changed in one
        # or both models.
        moved_focus_this_model = abs(self.focus[0] - index_of_token_in_this_model[0]) \
                                 + abs(self.focus[1] - index_of_token_in_this_model[1])
        moved_focus_other_model = abs(infinite_list.focus[0] - index_of_token_in_other_model[0]) \
                                  + abs(infinite_list.focus[1] - index_of_token_in_other_model[1])
        if moved_focus_this_model:
            self.difficulty.focus_move_ops += 1
            # Noticing in which direction the focus changed
            if self.focus[0] == index_of_token_in_this_model[0] and \
               self.focus[1] < index_of_token_in_this_model[1]:
                focus_direction = "right"
            if self.focus[0] == index_of_token_in_this_model[0] and \
               self.focus[1] > index_of_token_in_this_model[1]:
                focus_direction = "left"
            if self.focus[0] > index_of_token_in_this_model[0] and \
               self.focus[1] == index_of_token_in_this_model[1]:
                focus_direction = "up"
            if self.focus[0] < index_of_token_in_this_model[0] and \
               self.focus[1] == index_of_token_in_this_model[1]:
                focus_direction = "down"
            if self.focus[0] != index_of_token_in_this_model[0] and \
               self.focus[1] != index_of_token_in_this_model[1]:
                # The focus changed both in horizontal as well as in vertical direction
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
        if moved_focus_other_model:
            infinite_list.difficulty.focus_move_ops += 1
            # Noticing in which direction the focus changed
            if infinite_list.focus[0] == index_of_token_in_other_model[0] and \
               infinite_list.focus[1] < index_of_token_in_other_model[1]:
                focus_direction = "right"
            if infinite_list.focus[0] == index_of_token_in_other_model[0] and \
               infinite_list.focus[1] > index_of_token_in_other_model[1]:
                focus_direction = "left"
            if infinite_list.focus[0] > index_of_token_in_other_model[0] and \
               infinite_list.focus[1] == index_of_token_in_other_model[1]:
                focus_direction = "up"
            if infinite_list.focus[0] < index_of_token_in_other_model[0] and \
               infinite_list.focus[1] == index_of_token_in_other_model[1]:
                focus_direction = "down"
            if infinite_list.focus[0] != index_of_token_in_other_model[0] and \
                 infinite_list.focus[1] != index_of_token_in_other_model[1]:
                # The focus changed both in horizontal as well as in vertical direction
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or infinite_list.focus_change_direction != focus_direction:
                infinite_list.focus_change_direction = focus_direction
                infinite_list.difficulty.focus_direction_changes += 1
        # Difficulty measure difficulty.moved_focus_by is moved by the distance that focus has to travel to mentioned
        # token in the merge premise
        moved_focus_by = abs(self.focus[0] - index_of_token_in_this_model[0]) \
                         + abs(self.focus[1] - index_of_token_in_this_model[1]) \
                         + abs(infinite_list.focus[0] - index_of_token_in_other_model[0]) \
                         + abs(infinite_list.focus[1] - index_of_token_in_other_model[1])
        if moved_focus_by != 0:
            self.difficulty.focus_move_distance += moved_focus_by
            self.focus = index_of_token_in_this_model
            infinite_list.focus = index_of_token_in_other_model
            if self.focus is None or infinite_list.focus is None:
                raise MyExceptions.FocusError("Merge focus went to None")
        # Return new merged infinite list with entries from both
        return new_content, self.focus

    def variate_model(self, parsed_conclusion, how_far_removed=0):
        """
        Generate alternative model(s) based on annotations and how far removed on the neighborhood graph an
        alternative model is (based on how many swap operations are necessary to gain it from original model).

        :param parsed_conclusion: The conclusion that is to be verified.
        :param how_far_removed: How far on the neighborhood graph the returned alternative models may be.
        :return: bool: If within how_far_removed a model is found that holds under parsed_conclusion, True.
                       Otherwise, False.
        """
        index_first_token = self.find_index(parsed_conclusion.first_token)
        index_second_token = self.find_index(parsed_conclusion.second_token)

        if not index_first_token or not index_second_token:
            return False

        # First, the array is generated in which a conclusion was falsified and which will now be variated.
        # This can either be a row or a column.
        if parsed_conclusion.relation == "left" or parsed_conclusion.relation == "right":
            array_for_swapping = self.content[index_first_token[0]]
        elif parsed_conclusion.relation == "above" or parsed_conclusion.relation == "below":
            array_for_swapping = []
            for row in self.content:
                array_for_swapping.append(row[index_first_token[1]])

        if not array_for_swapping:
            raise MyExceptions.MVPError("Array for MVP couldn't be constructed. "
                                                    "InfiniteList.variate_model()")

        if parsed_conclusion.first_token not in array_for_swapping or parsed_conclusion.second_token not in array_for_swapping:
            return False

        # The swappable part is determined by leftmost and rightmost border. The border is determined by looking
        # at which tokens are "hard" tokens, i.e. referenced in annotations. Those don't move anymore and
        # therefore shouldn't be included in the swapping.
        leftmost_swappable_index = len(array_for_swapping) - 1
        rightmost_swappable_index = 0
        for i, element in enumerate(array_for_swapping):
            if element in self.annotations:
                for annotation in self.annotations[element]:
                    if array_for_swapping.index(annotation[1]) < leftmost_swappable_index:
                        leftmost_swappable_index = array_for_swapping.index(annotation[1])
                    if array_for_swapping.index(annotation[1]) > rightmost_swappable_index:
                        rightmost_swappable_index = array_for_swapping.index(annotation[1])
        swappable_part_of_array = array_for_swapping[leftmost_swappable_index:rightmost_swappable_index + 1]

        if not swappable_part_of_array:
            return False

        # One valid combination is the original one.
        valid_combinations_of_array = [[swappable_part_of_array]]

        # While we are at most how_far_removed nodes away from original one, construct further layers of graph.
        while how_far_removed > 0:
            for combination in valid_combinations_of_array[-1]:
                # print("Variating model, still {} times. "
                #       "Alternate models discovered: {}".format(how_far_removed - 1, valid_combinations_of_array))
                # In the last created layer of graph, is there a model in which the conclusion holds?
                if self.evaluate_relation(parsed_conclusion.first_token, parsed_conclusion.relation,
                                          parsed_conclusion.second_token, combination):
                    return True
                else:
                    # Construct a new layer
                    valid_combinations_at_this_distance = []
                    for i, token in enumerate(combination):
                        if token in self.annotations:
                            # The token that is annotated (and therefore movable) is swapped through the array.
                            # Other tokens are not swapped! Only one token.
                            # E.g.: Swap C through ABC -> CAB, ACB, ABC.
                            immovable_part_of_array = combination[:i] + combination[i + 1:]
                            for j in range(0, len(combination)):
                                if j != i:
                                    possible_combination = copy.deepcopy(immovable_part_of_array)
                                    possible_combination.insert(j, token)
                                    take_in = True
                                    # For that swap to hold, all annotations must hold
                                    for annotation in self.annotations[token]:
                                        if not self.evaluate_relation(token, annotation[0], annotation[1],
                                                                      possible_combination):
                                            take_in = False
                                    # And it shouldn't have been seen before
                                    for seen_combinations in valid_combinations_of_array:
                                        if possible_combination in seen_combinations:
                                            take_in = False
                                    if take_in:
                                        # The node is added to current layer of nodes
                                        valid_combinations_at_this_distance.append(possible_combination)
                    # Then the new layer is appended to complete graph.
                    if valid_combinations_at_this_distance:
                        valid_combinations_of_array.append(valid_combinations_at_this_distance)
            how_far_removed -= 1

        # If no model was found in which conclusion holds, return False
        return False

    def evaluate_conclusion(self, parsed_conclusion):
        """
        Evaluate truth of a parsed conclusion in current model.

        :param: parsed_conclusion: The parsed conclusion whose truth in this model should be evaluated.
        """
        index_first_token = self.find_index(parsed_conclusion.first_token)
        index_second_token = self.find_index(parsed_conclusion.second_token)

        if index_first_token is not None and index_second_token is not None:
            if parsed_conclusion.relation == "left":
                evaluation = index_first_token[0] == index_second_token[0] and index_first_token[1] < index_second_token[1]
            if parsed_conclusion.relation == "right":
                evaluation = index_first_token[0] == index_second_token[0] and index_first_token[1] > index_second_token[1]
            if parsed_conclusion.relation == "above":
                evaluation = index_first_token[1] == index_second_token[1] and index_first_token[0] < index_second_token[0]
            if parsed_conclusion.relation == "below":
                evaluation = index_first_token[1] == index_second_token[1] and index_first_token[0] > index_second_token[0]
            if evaluation:
                return evaluation
        else:
            if self.supermodels:
                for supermodel in self.supermodels:
                    self.difficulty.supermodels_accessed += 1
                    return supermodel.evaluate_conclusion(parsed_conclusion)
            return False

    def evaluate_relation(self, located_object, relation, reference_object, model=None):
        """
        Evaluate truth of a relation in current model.
        :param located_object: The located object that the relation is referencing.
        :param relation: The relation between the two tokens.
        :param reference_object: The reference object that the relation is referring to.
        :param model: If not self.content should be used, but an external model is to be checked
        """
        if model is None:
            index_first_token = self.find_index(located_object)
            index_second_token = self.find_index(reference_object)
        else:
            if located_object in model and reference_object in model:
                index_first_token = [0, model.index(located_object)]
                index_second_token = [0, model.index(reference_object)]
            else:
                return False

        # Focus operations
        if self.focus != index_first_token:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus[0] - index_first_token[0]) + abs(self.focus[1] - index_first_token[1])
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus[0] == index_first_token[0] and \
               self.focus[1] < index_first_token[1]:
                focus_direction = "right"
            if self.focus[0] == index_first_token[0] and \
               self.focus[1] > index_first_token[1]:
                focus_direction = "left"
            if self.focus[0] > index_first_token[0] and \
               self.focus[1] == index_first_token[1]:
                focus_direction = "up"
            if self.focus[0] < index_first_token[0] and \
               self.focus[1] == index_first_token[1]:
                focus_direction = "down"
            if self.focus[0] != index_first_token[0] and \
               self.focus[1] != index_first_token[1]:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = index_first_token

        if self.focus != index_second_token:
            self.difficulty.focus_move_ops += 1
            moved_focus_by = abs(self.focus[0] - index_second_token[0]) + abs(self.focus[1] - index_second_token[1])
            self.difficulty.focus_move_distance += moved_focus_by
            focus_direction = None
            if self.focus[0] == index_second_token[0] and \
               self.focus[1] < index_second_token[1]:
                focus_direction = "right"
            if self.focus[0] == index_second_token[0] and \
               self.focus[1] > index_second_token[1]:
                focus_direction = "left"
            if self.focus[0] > index_second_token[0] and \
               self.focus[1] == index_second_token[1]:
                focus_direction = "up"
            if self.focus[0] < index_second_token[0] and \
               self.focus[1] == index_second_token[1]:
                focus_direction = "down"
            if self.focus[0] != index_second_token[0] and \
               self.focus[1] != index_second_token[1]:
                focus_direction = "various_directions"
            if focus_direction == "various_directions" or self.focus_change_direction != focus_direction:
                self.focus_change_direction = focus_direction
                self.difficulty.focus_direction_changes += 1
            self.focus = index_second_token

        if relation == "left":
            return index_first_token[0] == index_second_token[0] and index_first_token[1] < index_second_token[1]
        if relation == "right":
            return index_first_token[0] == index_second_token[0] and index_first_token[1] > index_second_token[1]
        if relation == "above":
            return index_first_token[1] == index_second_token[1] and index_first_token[0] < index_second_token[0]
        if relation == "below":
            return index_first_token[1] == index_second_token[1] and index_first_token[0] > index_second_token[0]

    def generate(self, first_token, second_token):
        """
        Given two tokens, return the relationship between them as represented in the model.

        :param first_token: First token
        :param second_token: Second token
        :return: Relationship between the two tokens
        """
        index_first_token = self.find_index(first_token)
        index_second_token = self.find_index(second_token)

        if index_first_token[0] == index_second_token[0]:
            if index_first_token[1] < index_second_token[1]:
                return "left"
            if index_first_token[1] > index_second_token[1]:
                return "right"
        if index_first_token[1] == index_second_token[1]:
            if index_first_token[0] < index_second_token[0]:
                return "above"
            if index_first_token[0] > index_second_token[0]:
                return "below"
        else:
            return "no_rel"
