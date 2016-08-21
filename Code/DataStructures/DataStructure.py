__author__ = 'Phaina'

"""Abstract parent class of all possible data structures."""


class DataStructure(object):
    def __init__(self):
        """
        In child classes, create_from_parsed_line a new object of type DataStructure, taking parsed_line as first premise for model.

        """
        pass

    def insert(self, parsed_line):
        """
        Insert a new model into existing data structure.

        We simply assume that "left" means that the LO (located object) is to the left of the RO (reference object)
        and along exactly the same line in a spatial array (Ragni & Knauf, 2013).

        :param parsed_line: The current line as parsed by Parser, i.e. first_token, relation, second_token

        :return: bool: Whether insert worked or not
        """
        return

    def annotate(self, token, relation, indeterminately_inserted_token):
        """
        If a new token is to be inserted and its position is not determinate, the located object that it is
        related to needs to be annotated with that information.

        :param token: The token that is already in the model and needs to be annotated
        :param relation: The relation with which the new token is to be indeterminately inserted
        :param indeterminately_inserted_token: The new token that is to be indeterminately inserted
        """
        return

    def merge(self, data_structure, parsed_line):
        """
        Merge two models.

        :param data_structure: The other data structure that is to be merged with current one.
        """
        return

    def find(self, token):
        """
        Find occurrence of token in current model.

        :param token: The token that is to be found
        """
        return

    def variate_model(self, parsed_conclusion, how_far_removed=0):
        """
        Generate alternative model(s) based on annotations.

        :param parsed_conclusion: The conclusion that is to be verified.
        :param how_far_removed: How far on the neighborhood graph the returned alternative models may be.
        :return: All alternative models.
        """
        return

    def evaluate_conclusion(self, parsed_conclusion):
        """
        Given a conclusion, verify its truth in current model.

        We simply assume that "left" means that the LO (located object) is to the left of the RO (reference object)
        and along exactly the same line in a spatial array (Ragni & Knauf, 2013).

        :param parsed_conclusion: The conclusion to be verified.

        :return: True/False
        """
        return

    def generate(self, first_token, second_token):
        """
        Given two tokens, return the relationship between them as represented in the model.

        :param first_token: First token
        :param second_token: Second token
        :return: Relationship between the two tokens
        """
        return
