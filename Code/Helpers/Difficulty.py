# pylint: disable=line-too-long, fix-me

__author__ = 'Phaina'

"""A singleton for all data structure objects to store difficulty statistics, such as focus operations."""


class Difficulty(object):
    def __init__(self):
        """
        Describes difficulty measures for a problem.

        :var self.focus_move_ops: How often the focus was moved at all.
              E.g. [[A, B]] focus is on 'A' (0,0). Next premise: C right B. Focus is moved to B. One focus move op.
              Focus is moved to C, because it's inserted, one more focus move up.
        :var self.focus_move_distance: How far the focus was moved.
              Example above: The focus was moved from 'A' to 'B', so a distance of 1.
        :var self.write_ops: How often new information was written.
             E.g. parsing first premise A left B: Two write operations.
             E.g. merging [[A, D]] and [[F, G]] on basis of D above F: 6 write operations (4 for basis models and 2
             more because [[F, G]] is merged into [[A, D]] and therefore "written again".
        :var self.insert_ops: How often new information was inserted into an existing model.
             E.g. [[A, B]], inserting C right B. One insert op.
        :var self.merge_ops: How often a merge operation took place.
             E.g. merging [[A, D]] and [[F, G]] on basis of D above F: One merge op.
        :var self.premise_direction_changes: How often the direction of premises was changed.
             E.g. first premises are all of form "X left Y". A premise of form "X right Y" is read. One direction change
        :var self.focus_direction_changes: How often the direction of focus inside a model was changed.
             E.g. first premise A left B, [[A, B]], second premise A left C, [[A, B, C]].
             Focus changes from A to B (direction right), then from B to A (located object, direction left), then
             from A to C (reference object, direction right).
        :var self.focus_key_distance: How far the focus changed keywise (in a BST). I.e. if I insert "A left B" with
             keys: {'A':0, 'B': 10}, the key distance would be 10.
        :var self.linked_list_followed_pointing_to: How often a pointer was followed in linked list. Since linked list
             is almost the same as InfiniteList, the only difference is how often a link was followed from one node
             to another in linked list.
        :var self.model_attention_changes: How often the model which is currently "in attention" is changed.
             I.e. shifting overall focus (i.e. attention) from one model to another.
             E.g. Creating a new layer, focuses attention on new model.
             Or merging two models focuses on on model that is integrated into then integrated model,
             then new model which is newly created by this merge.
        :var self.annotation_ops: How often annotations in case of ambiguous premises were made.
             E.g. [[A, B, C]], then premise D left B. In case of fff-insert, new model would be [[D, A, B, C]],
             but because the insert was ambiguous, D is annotated. One annotation op.
        :var self.grouping_ops: How often model contents were grouped for merge operations.
        :var self.grouping_size: The size of those groups.
             E.g. merging [[A, D]] and [[F, G]] on basis D above F: One grouping op, grouping size is 4.
        :var self.layer_count: How many single models were created.
        :var self.del_layer_ops: How often single models were deleted. Models are deleted when they are merged into
             another model.
        """
        self.focus_move_ops = 0
        self.focus_move_distance = 0
        self.write_ops = 0
        self.insert_ops = 0
        self.merge_ops = 0
        self.supermodels_created = 0
        self.supermodels_accessed = 0
        self.premise_direction_changes = 0
        self.focus_direction_changes = 0
        self.focus_key_distance = 0
        self.linked_list_followed_pointing_to = 0
        self.model_attention_changes = 0
        self.annotation_ops = 0
        self.grouping_ops = 0
        self.grouping_size = 0
        self.layer_count = 0
        self.del_layer_ops = 0
        self.graph_amount_relationships = 0
        self.BST_depth = 0

    def __str__(self):
        return "Difficulty is: \n" \
               "{} move operations for focus, \n" \
               "{} move distance for focus, \n" \
               "{} write operations, \n" \
               "{} insert operations, \n" \
               "{} merge operations, \n" \
               "{} supermodels created, \n" \
               "{} supermodels accessed, \n" \
               "{} premise direction changes, \n" \
               "{} focus direction changes, \n" \
               "{} model in attention/focus changes, \n" \
               "{} annotation operations made, \n" \
               "{} grouping operations, \n" \
               "{} was the size of all grouped models which were merged, \n" \
               "{} was the BST depth, \n" \
               "{} was the focus key distance in a BST, \n" \
               "{} was the number of times a pointer in a linked list was followed, \n" \
               "{} was the amount of relationships recorded in a graph, \n" \
               "{} single models (=layers) created, \n" \
               "{} delete layer operations. ".format(self.focus_move_ops,
                                                     self.focus_move_distance,
                                                     self.write_ops,
                                                     self.insert_ops,
                                                     self.merge_ops,
                                                     self.supermodels_created,
                                                     self.supermodels_accessed,
                                                     self.premise_direction_changes,
                                                     self.focus_direction_changes,
                                                     self.model_attention_changes,
                                                     self.annotation_ops,
                                                     self.grouping_ops,
                                                     self.grouping_size,
                                                     self.BST_depth,
                                                     self.focus_key_distance,
                                                     self.linked_list_followed_pointing_to,
                                                     self.graph_amount_relationships,
                                                     self.layer_count,
                                                     self.del_layer_ops)