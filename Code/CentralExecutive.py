import copy
import uuid
from json import load
import Helpers.MyExceptions as MyExceptions
from Helpers.Helpers import Helpers
from Parser import Parser
from Memory import Memory
from Helpers.Difficulty import Difficulty
from DataStructures.InfiniteList import InfiniteList
from DataStructures.BoundedList import BoundedList
from DataStructures.BinarySearchTree import BinarySearchTree
from DataStructures.BinarySearchTreeTrivial import BinarySearchTreeTrivial
from DataStructures.BinarySearchTreeLimitedDepth import BinarySearchTreeLimitedDepth
from DataStructures.BinarySearchTreeRandomTree import BinarySearchTreeRandomTree
from DataStructures.LinkedList import LinkedList
from DataStructures.Graph import Graph

__author__ = 'Phaina'

"""Manage all necessary operations in order to parse premises and evaluate conclusions."""


class CentralExecutive(object):
    def __init__(self, parameter_json):
        """
        :var self.memory: Central memory instance for this "brain"
        :var self.difficulty: Central difficulty instance for measuring focus operations
        :var self.premises: A list of all premises for a problem
        :var self.conclusions: A list of all conclusions for a problem (to be checked)
        :var self.last_direction: The last direction that was taken (to notice direction changes)

        :var self.premises_and_conclusions_file: File where all premises and conclusions are gathered
        :var self.data_structure: Data structure that is to be used in this run
        Possibilities: InfiniteList, BoundedList, BinarySearchTree, BinarySearchTreeTrivial, BinarySearchTreeLimitedDepth,
                       BinarySearchTreeRandomTree, Graph
        :var self.merge_type: Merge type that is to be used in this run
        Possibilities: Integrate, Supermodel
        :var self.how_far_removed: Determines how far a variated model may be from preferred mental model on neighborhood
        graph
        :var self.helpers: General helper functions
        """
        self.difficulty = Difficulty()
        self.premises = []
        self.conclusions = []
        self.last_direction = None

        with open(parameter_json) as param_file:
            param = load(param_file)
            self.premises_and_conclusions_file = param["filename"]
            self.data_structure = param["data_structure"]
            self.insert_type = param["insert_type"]
            self.merge_type = param["merge_type"]
            self.nested_supermodels = param["nested_supermodels"]
            self.how_far_removed = param["neighborhood_graph_removal_cap"]
            self.bounded_list_size_limit = param["bounded_list_size_limit"]
            self.BST_depth_limit = param["BST_depth_limit"]
            self.helpers = Helpers(bool(param["verbose"]))
            self.statistics_to_file = bool(param["to_file"])
            self.activation_function = param["activation_function"]
            self.memory = Memory(self.activation_function)

    def get_lines_from_file(self, filename):
        """
        Open input file with premises and conclusions.

        :param filename: Name of the file which includes all premises and conclusions

        :return lines: File with premises and conclusions split into single lines
        """
        with open(filename) as f:
            lines = f.readlines()
        return lines

    def differentiate_premises_and_conclusions(self, lines):
        """
        Differentiate between premises and conclusions in input file.
        Fill self.premises and self.conclusions lists (class variables of CentralExecutive).

        :param lines: File with premises and conclusions split into single lines

        :var self.premises: Class variable containing all premises to be considered
        :var self.conclusions: Class variable containing all conclusions to be verified
        """
        for line in lines:
            parsed_line = Parser(line, self.memory)
            if parsed_line.type == "Conclusion":
                self.conclusions.append(parsed_line)
            elif parsed_line.type == "Premise":
                self.premises.append(parsed_line)

    def delete_from_memory(self, data_structure_object):
        """
        Delete a data structure object from memory.

        :param data_structure_object: The object that is to be deleted from memory.
        """
        self.memory.remove(data_structure_object)

    def type_of_premise(self, first_token, second_token):
        """
        Determine the type of a premise.

        As per Ragni & Knauf (2013), differentiate between three types of premises:
        Type 1/3: Two new tokens (i.e. neither token is found in memory)
        Type 2: One new token (i.e. one token is found in memory and other has to be integrated)
        Type 4: Connecting submodels (i.e. both tokens are found and their submodels have to be integrated)

        :param first_token: First token to be searched in memory.
        :param second_token: Second token to be searched in memory.

        :var found_first_token: The model in which first_token was found (if it was found).
        :var found_second_token: The model in which second_token was found (if it was found).

        :return type: The type of the premise from which first_token and second_token are taken.
        """
        found_first_token = self.memory.search(first_token)
        found_second_token = self.memory.search(second_token)
        if not found_first_token and not found_second_token:
            type = 1
        if found_first_token or found_second_token:
            type = 2
        if found_first_token and found_second_token:
            type = 4
        return type

    def create_new_model(self, parsed_premise, data_structure, content=None, returns=False):
        """
        Create a new model in memory for a premise of type 1/3.

        :param parsed_premise: The premise that is to be made into a new model and inserted into memory.
        :param content: Optionally content of new data structure
        :param returns: Optionally whether new model is returned or if False, inserted into memory
        """
        if data_structure == "InfiniteList":
            new_model = InfiniteList(parsed_premise, self.insert_type, self.merge_type, self.difficulty, content)
        if data_structure == "BoundedList":
            new_model = BoundedList(parsed_premise, self.insert_type, self.merge_type, self.bounded_list_size_limit,
                                    self.difficulty, content)
        if data_structure == "BinarySearchTree":
            new_model = BinarySearchTree(0, parsed_premise, self.insert_type, self.merge_type, self.difficulty)
        if data_structure == "BinarySearchTreeTrivial":
            new_model = BinarySearchTreeTrivial(0, parsed_premise, self.insert_type, self.merge_type, self.difficulty)
        if data_structure == "BinarySearchTreeLimitedDepth":
            new_model = BinarySearchTreeLimitedDepth(0, parsed_premise, self.insert_type, self.merge_type,
                                                     self.difficulty, self.BST_depth_limit)
        if data_structure == "BinarySearchTreeRandomTree":
            new_model = BinarySearchTreeRandomTree(0, parsed_premise, self.insert_type, self.merge_type, self.difficulty)
        if data_structure == "LinkedList":
            new_model = LinkedList(parsed_premise, self.insert_type, self.merge_type, self.difficulty, content)
        if data_structure == "Graph":
            new_model = Graph(parsed_premise, self.insert_type, self.merge_type, self.difficulty, content)
        if not returns:
            self.memory.insert(new_model)
        else:
            return new_model

        # For noticing which model is in focus overall (i.e. which model the attention is on), either a new focus is
        # needed or if content was set (i.e. a new model was created by a merge), then the focus changes too.
        new_model_in_focus_index = self.memory.models.index(new_model)
        if self.memory.model_in_focus != new_model_in_focus_index or content:
            self.memory.model_in_focus = new_model_in_focus_index
            if len(self.memory.models) > 1:
                # So the 1st model doesn't count as a model attention change, only after that creating a new model
                # will change attention/the focus of viewer
                self.difficulty.model_attention_changes += 1

    def insert_into_model(self, model, parsed_premise):
        """
        Insert parsed premise into existing model for premise of type 2.
        Parser already places focus on the token that has been found in memory.

        :param: model: The model that the premise is to be inserted into
        :param parsed_premise: The premise that is to be made into a new model and inserted into memory.
        """
        # If the insertion is taking place into a model that is not currently in focus, the overall focus has to change
        model_to_be_inserted_into_index = self.memory.models.index(model)
        if self.memory.model_in_focus != model_to_be_inserted_into_index:
            self.memory.model_in_focus = model_to_be_inserted_into_index
            self.difficulty.model_attention_changes += 1
        # Then do normal insertion process. If it doesn't work (no model to insert into, e.g. in case of bounded lists),
        # create a new model instead.
        if model.insert(parsed_premise):
            pass
        else:
            self.create_new_model(parsed_premise, self.data_structure)

    def merge_two_models(self, parsed_premise):
        """
        Parsed_premise is of type 4, i.e. both tokens are already part of a model or several models.
        If these models are separate, they have to be merged.

        :var model_of_first_token: The model in which first_token was found (if it was found).
        :var model_of_second_token: The model in which second_token was found (if it was found).

        :param parsed_premise: The premise whose tokens both are already part of a model/models.
        """
        model_of_first_token = self.memory.search(parsed_premise.first_token)
        model_of_second_token = self.memory.search(parsed_premise.second_token)

        # First, shift attention to model that is to be inserted into. Then, shift attention to model that is to be
        # inserted.
        if self.memory.model_in_focus != self.memory.models.index(model_of_first_token[0]):
            self.memory.model_in_focus = self.memory.models.index(model_of_second_token[0])
            self.difficulty.model_attention_changes += 2
        # If attention already is on model that is to be inserted into, only shift attention to model that is to be
        # inserted.
        else:
            self.memory.model_in_focus = self.memory.models.index(model_of_second_token[0])
            self.difficulty.model_attention_changes += 1

        if model_of_first_token == model_of_second_token:
            if self.evaluate_conclusion(parsed_premise):
                return
            else:
                raise MyExceptions.ModelError("A premise was found that did not hold with previous premises. "
                                              "The premise: {}.".format(parsed_premise))
        else:
            # They were found in different models.
            if len(model_of_first_token) > 1 or len(model_of_second_token) > 1:
                raise MyExceptions.FoundTooManyModels("Trying to merge too many models. Trying to join {} and {},"
                                                      "there may only be one model on either side, "
                                                      "but there are more.".format(model_of_first_token,
                                                                                   model_of_second_token))
            else:
                self.difficulty.grouping_ops += 1
                self.difficulty.grouping_size += (len(model_of_first_token[0]) + len(model_of_second_token[0]))
                if self.merge_type == "integrate":
                    self.difficulty.write_ops += len(model_of_second_token[0])
                    if self.data_structure == "BinarySearchTree" or \
                       self.data_structure == "BinarySearchTreeTrivial" or \
                       self.data_structure == "BinarySearchTreeLimitedDepth" or \
                       self.data_structure == "BinarySearchTreeRandomTree":
                        merged_tree = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        if merged_tree:
                            self.delete_from_memory(model_of_first_token[0])
                            self.delete_from_memory(model_of_second_token[0])
                            merged_tree[0].focus = merged_tree[1]
                            self.memory.insert(merged_tree[0])
                            self.memory.model_in_focus = self.memory.models.index(merged_tree[0])
                            self.difficulty.model_attention_changes += 1
                    else:
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        if merged_content:
                            self.delete_from_memory(model_of_first_token[0])
                            self.delete_from_memory(model_of_second_token[0])
                            # The last attention change is already taken care of by create_new_model()
                            self.create_new_model('', self.data_structure, merged_content)
                elif self.merge_type == "supermodel" and self.nested_supermodels >= 1:
                    if self.data_structure == "InfiniteList":
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        merged_content = self.create_new_model('', 'InfiniteList', merged_content, True)
                    elif self.data_structure == "LinkedList":
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        merged_content = self.create_new_model('', 'LinkedList', merged_content, True)
                    elif self.data_structure == "BoundedList":
                        # A supermodel should not be bound by bounded_list_size_limit
                        tmp_bounded_list_cap = copy.deepcopy(self.bounded_list_size_limit)
                        model_of_first_token[0].limit = 100
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        merged_content = self.create_new_model('', 'InfiniteList', merged_content, True)
                        model_of_first_token[0].limit = tmp_bounded_list_cap
                    elif self.data_structure == "BinarySearchTreeLimitedDepth":
                        # A supermodel should not be bound by BST_depth_limit
                        tmp_bst_depth_limit = copy.deepcopy(self.BST_depth_limit)
                        model_of_first_token[0].limit = 100
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        merged_content[0].focus = merged_content[1]
                        merged_content = merged_content[0]
                        model_of_first_token[0].limit = tmp_bst_depth_limit
                    elif self.data_structure == "Graph":
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        merged_content = Graph('', self.insert_type, self.merge_type, self.difficulty, merged_content)
                    else:
                        merged_content = model_of_first_token[0].merge(model_of_second_token[0], parsed_premise)
                        merged_content[0].focus = merged_content[1]
                        merged_content = merged_content[0]
                    merged_content.supermodel_index = 1
                    self.difficulty.supermodels_created += 1
                    model_of_first_token[0].supermodels.append(merged_content)
                    model_of_second_token[0].supermodels.append(merged_content)
                    self.memory.supermodels.append(merged_content)

    def evaluate_conclusion(self, parsed_conclusion):
        """
        Determine whether a given conclusion is correct or not.

        :param parsed_conclusion: The conclusion that is to be verified.
        """
        model_first_token = self.memory.search(parsed_conclusion.first_token)
        model_second_token = self.memory.search(parsed_conclusion.second_token)

        if self.merge_type == "integrate":
            if set(model_first_token) & set(model_second_token):
                evaluation = True
                for model in set(model_first_token) & set(model_second_token):
                    if not model.evaluate_conclusion(parsed_conclusion):
                        if model.variate_model(parsed_conclusion, self.how_far_removed):
                            return True
                        else:
                            evaluation = False
                return evaluation
            else:
                self.helpers.verboseprint("The tokens of this conclusion are not part of the same model."\
                                        "The conclusion: {}. All models: {}".format(parsed_conclusion,
                                                                                    self.memory.models))
                evaluation = False
                return evaluation
        if self.merge_type == "supermodel":
            for model in model_first_token:
                if model.evaluate_conclusion(parsed_conclusion):
                    return True
                if not model.evaluate_conclusion(parsed_conclusion):
                    if model.variate_model(parsed_conclusion, self.how_far_removed):
                        return True
            for model in model_second_token:
                if model.evaluate_conclusion(parsed_conclusion):
                    return True
                if not model.evaluate_conclusion(parsed_conclusion):
                    if model.variate_model(parsed_conclusion, self.how_far_removed):
                        return True
            return False

    def premise_to_memory(self, parsed_premise, timestep):
        """
        Add a premise to memory according to its type, i.e. create a new model, integrate into a model or merge models.

        :param parsed_premise: The premise that is to be added into memory
        :param timestep: The step in time at which the token(s) are added to memory (for activation function).
               That equals the how-manieth-premise this was.
        """
        if self.last_direction is None:
            self.last_direction = parsed_premise.relation
        if parsed_premise.relation != self.last_direction:
            self.last_direction = parsed_premise.relation
            self.difficulty.premise_direction_changes += 1

        type_of_premise = self.type_of_premise(parsed_premise.first_token, parsed_premise.second_token)
        if type_of_premise == 1:
            self.difficulty.layer_count += 1
            self.difficulty.write_ops += 2
            self.difficulty.focus_move_ops += 1
            self.difficulty.focus_move_distance += 1
            self.create_new_model(parsed_premise, self.data_structure)
            self.memory.token_timestep[parsed_premise.first_token] = timestep
            self.memory.token_timestep[parsed_premise.second_token] = timestep
        if type_of_premise == 2:
            self.difficulty.insert_ops += 1
            self.difficulty.write_ops += 1
            first_token_in_memory = self.memory.search(parsed_premise.first_token)
            second_token_in_memory = self.memory.search(parsed_premise.second_token)
            # Move ops and move distance handled by models.
            if first_token_in_memory:
                for element in first_token_in_memory:
                    self.insert_into_model(element, parsed_premise)
                    self.memory.token_timestep[parsed_premise.second_token] = timestep
            if second_token_in_memory:
                for element in second_token_in_memory:
                    self.insert_into_model(element, parsed_premise)
                    self.memory.token_timestep[parsed_premise.first_token] = timestep
        if type_of_premise == 4:
            self.difficulty.merge_ops += 1
            if self.merge_type == "integrate":
                self.difficulty.del_layer_ops += 1  # Because one layer will be deleted
            self.merge_two_models(parsed_premise)   # Move distance and move ops handled by models.

    def combine_supermodels(self, max_depth, depth=1):
        """
        Combine already existing supermodels in memory to higher supermodels if nesting parameter allows.

        :param max_depth: The maximum depth of nested supermodels (i.e. how many supermodel "level"s may be created)
        :param depth: The current depth of nested supermodels. This is usually 1 since one layer of supermodels
        was already created
        """
        # Compare every supermodel with every other supermodel
        for model in self.memory.supermodels:
            if type(model) == BinarySearchTree or type(model) == BinarySearchTreeRandomTree \
                or type(model) == BinarySearchTreeLimitedDepth or type(model) == BinarySearchTreeTrivial \
                    or type(model) == LinkedList:
                this_content = model.to_infinite_list()
                this_model_to_combine = InfiniteList('', self.insert_type, self.merge_type, self.difficulty, (this_content, (0, 0)))
            else:
                this_model_to_combine = model
            for other_model in self.memory.supermodels:
                if type(other_model) == BinarySearchTree or type(other_model) == BinarySearchTreeRandomTree \
                    or type(other_model) == BinarySearchTreeLimitedDepth or type(other_model) == BinarySearchTreeTrivial \
                        or type(other_model) == LinkedList:
                    oth_content = other_model.to_infinite_list()
                    other_model_to_combine = InfiniteList('', self.insert_type, self.merge_type, self.difficulty,
                                               (oth_content, (0, 0)))
                else:
                    other_model_to_combine = other_model
                cont2 = False
                for this_row in this_model_to_combine.content:
                    cont = False
                    for other_row in other_model_to_combine.content:
                        this_row_set = set(this_row)
                        other_row_set = set(other_row)
                        # Only look at pairs of supermodels where one is not a subset of the other
                        if this_row_set & other_row_set == this_row_set or this_row_set & other_row_set == other_row_set:
                            cont = True
                    if cont:
                        cont2 = True
                if cont2:
                    continue

                # Is this model to the left in the merge or the other model?
                this_model_left = False
                other_model_left = False

                merged_content = []
                common_rows = {}
                # Compare every row of this model with every row of other model (because matches may be shifted due to
                # one model having more rows, maybe a row on top of the identical content that is to be merged)
                for j, this_row in enumerate(this_model_to_combine.content):
                    for l, other_row in enumerate(other_model_to_combine.content):
                        # The tokens that the two supermodels have in common in this row
                        common_tokens = set(this_row) & set(other_row)
                        if common_tokens and common_tokens != set('x'):
                            if j not in common_rows:
                                # Take note of which rows are "lined up" to each other
                                common_rows[j] = (l,)
                            else:
                                raise MyExceptions.IndexError("Too many common rows in combine_supermodel!")
                            # For every common token, save its position in this and other supermodel to later
                            # see which model is to the left (where the token indices are higher) and which model
                            # is to the right (token indices are lower)
                            # E.g. [['A', 'B']] and [['B', 'C']]. First one is to the left because 'B' index is higher.
                            indices_in_this_model = {}
                            indices_in_other_model = {}
                            for common_token in common_tokens:
                                indices_in_this_model[common_token] = this_model_to_combine.find_index(common_token)
                                indices_in_other_model[common_token] = other_model_to_combine.find_index(common_token)
                            for common_token in indices_in_this_model:
                                if indices_in_this_model[common_token] > indices_in_other_model[common_token]:
                                    this_model_left = True
                                else:
                                    this_model_left = False
                                if indices_in_other_model[common_token] > indices_in_this_model[common_token]:
                                    other_model_left = True
                                else:
                                    other_model_left = False

                            if this_model_left and not other_model_left:
                                # For later correctly gluing content together, save the position of the leftmost common
                                # token in this model.
                                min_left = 20000
                                for left in indices_in_this_model.values():
                                    if left[1] < min_left:
                                        min_left = left[1]
                                # Differentiate by the amount of rows because of situation described above: What if one
                                # of the supermodels has content above the to-be-merged-part?
                                mod_rows = this_model_to_combine.rows()
                                oth_mod_rows = other_model_to_combine.rows()
                                if mod_rows >= oth_mod_rows:
                                    for k, row in enumerate(this_model_to_combine.content):
                                        if k in common_rows:
                                            common_with = common_rows[k][0]
                                            merged_content.append(row[:min_left] + other_model_to_combine.content[common_with])
                                        else:
                                            merged_content.append(row + ['x' for x in other_model_to_combine.content[0]])
                                if oth_mod_rows > mod_rows:
                                    for k, row in enumerate(other_model_to_combine.content):
                                        row_partner = None
                                        for key in common_rows:
                                            if k in common_rows[key]:
                                                row_partner = key
                                        if row_partner:
                                            merged_content.append(this_model_to_combine.content[row_partner][:min_left] + row)
                                        else:
                                            merged_content.append(['x' for x in this_model_to_combine.content[0]] + row)
                            if other_model_left and not this_model_left:
                                # For later correctly gluing content together, save the position of the leftmost common
                                # token in this model.
                                min_left = 20000
                                for left in indices_in_other_model.values():
                                    if left[1] < min_left:
                                        min_left = left[1]
                                # Differentiate by the amount of rows because of situation described above: What if one
                                # of the supermodels has content above the to-be-merged-part?
                                mod_rows = this_model_to_combine.rows()
                                oth_mod_rows = other_model_to_combine.rows()
                                if mod_rows >= oth_mod_rows:
                                    for k, row in enumerate(this_model_to_combine.content):
                                        if k in common_rows:
                                            common_with = common_rows[k][0]
                                            merged_content.append(other_model_to_combine.content[common_with][:min_left] + row)
                                        else:
                                            merged_content.append(['x' for x in other_model_to_combine.content[0]] + row)
                                if oth_mod_rows > mod_rows:
                                    for k, row in enumerate(other_model_to_combine.content):
                                        row_partner = None
                                        for key in common_rows:
                                            if k in common_rows[key]:
                                                row_partner = key
                                        if row_partner:
                                            merged_content.append(row[:min_left] + this_model_to_combine.content[row_partner])
                                        else:
                                            merged_content.append(row + ['x' for x in this_model_to_combine.content[0]])
                            elif this_model_left and other_model_left or not this_model_left and not other_model_left:
                                print this_model_left, other_model_left
                                raise MyExceptions.IndexError("No model left or all models left in combine supermodels")

                        if merged_content:
                            higher_supermodel = InfiniteList('', self.insert_type, self.merge_type, self.difficulty,
                                                             (merged_content, (0, 0)))
                            if not self.memory.search_supermodel(higher_supermodel.content):
                                higher_supermodel.supermodel_index = max(this_model_to_combine.supermodel_index,
                                                                         other_model_to_combine.supermodel_index) + 1
                                # Depth is the nesting depth of supermodels. Break if this supermodel is "too high up"
                                depth = higher_supermodel.supermodel_index
                                if depth > max_depth:
                                    return
                                self.difficulty.supermodels_created += 1
                                model.supermodels.append(higher_supermodel)
                                other_model.supermodels.append(higher_supermodel)
                                self.memory.supermodels.append(higher_supermodel)

    def instance_statistics(self):
        """
        Write instance statistics (difficulty measures, end content of models and supermodels in memory, conclusion
        evaluation, ...) into a txt file.
        """
        file_name = self.premises_and_conclusions_file[:-3] + "_" + self.data_structure + "_" + self.insert_type + \
        "_" + self.merge_type + str(uuid.uuid4()) + "_instance_statistics.txt"
        with open(file_name, "w") as instance_file:
            instance_file.write("Parameters: \n")
            instance_file.write("Data_structure: " + self.data_structure + "\n")
            instance_file.write("Insert_type: " + self.insert_type + "\n")
            instance_file.write("Merge_type: " + self.merge_type + "\n")
            instance_file.write("Nested_supermodels: " + str(self.nested_supermodels) + "\n")
            instance_file.write("Neighborhood_graph_removal_cap: " + str(self.how_far_removed) + "\n")
            instance_file.write("Bounded_list_size_limit: " + str(self.bounded_list_size_limit) + "\n")
            instance_file.write("BST_depth_limit: " + str(self.BST_depth_limit) + "\n")
            instance_file.write("Activation function: " + str(self.activation_function) + "\n")
            instance_file.write("_____________________________________\n")
            instance_file.write("Memory content: \n")
            instance_file.write(str(self.memory))
            instance_file.write("_____________________________________\n")
            instance_file.write("Conclusions: \n")
            for conclusion in self.conclusions:
                if self.evaluate_conclusion(conclusion):
                    instance_file.write("Conclusion '" + conclusion.first_token + " " + conclusion.relation + " " +
                                        conclusion.second_token + "' is true. \n")
                else:
                    instance_file.write("Conclusion '" + conclusion.first_token + " " + conclusion.relation + " " +
                                        conclusion.second_token + "' is false. \n")
            instance_file.write("_____________________________________\n")
            instance_file.write(str(self.difficulty))

    def execute(self, return_truth_of_conclusion=False):
        """
        Execute an instance of Central Executive.
        """
        self.helpers.verboseprint("Your parameters are: \n"
                                  "Insert type: {},\n"
                                  "Data structure: {},\n"
                                  "Merge type: {},\n"
                                  "Activation function: {},\n"
                                  "How far removed on neighborhood graph: {}.".format(self.insert_type,
                                                                                      self.data_structure,
                                                                                      self.merge_type,
                                                                                      self.activation_function,
                                                                                      self.how_far_removed))
        lines = self.get_lines_from_file(self.premises_and_conclusions_file)
        self.differentiate_premises_and_conclusions(lines)

        # Differentiate between different premise types and treat them accordingly
        self.helpers.verboseprint("_____________________________________\n"
                                  "Reading premises and building models:")
        premises_read = 0
        for premise in self.premises:
            premises_read += 1
            self.helpers.verboseprint("I'm now adding premise '"
                                      + premise.first_token, premise.relation, premise.second_token +
                                      "' to memory.")
            self.premise_to_memory(premise, premises_read)
            self.memory.activation(premises_read)

        # If merge_type is supermodels, combine all possible supermodels now
        if self.merge_type == "supermodel" and self.nested_supermodels >= 1:
            self.combine_supermodels(self.nested_supermodels, 1)
        self.helpers.verboseprint("\n______________________\n"
                                  "Memory content is now:")
        self.helpers.verboseprint(self.memory)

        # Then evaluate the truth of all conclusions and return their truth value.
        self.helpers.verboseprint("_____________________\n"
                                  "Evaluating conclusions:")
        for conclusion in self.conclusions:
            if self.evaluate_conclusion(conclusion):
                self.helpers.verboseprint("Conclusion '"
                                          + conclusion.first_token, conclusion.relation, conclusion.second_token
                                          + "' is true.")
                if return_truth_of_conclusion:
                    return True
            else:
                self.helpers.verboseprint("Conclusion '"
                                          + conclusion.first_token, conclusion.relation, conclusion.second_token
                                          + "' is false.")
                if return_truth_of_conclusion:
                    return False

        # Give difficulty measures for given problem.
        self.helpers.verboseprint("\n___________________")
        self.helpers.verboseprint(self.difficulty)

        # Write a statistical file giving output, difficulty, etc.
        if self.statistics_to_file:
            self.instance_statistics()


if __name__ == '__main__':
    CE = CentralExecutive("parameters.json")
    CE.execute()
