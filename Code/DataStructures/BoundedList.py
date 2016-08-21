# pylint: disable=line-too-long, fix-me

from InfiniteList import InfiniteList

__author__ = 'Phaina'

"""BoundedList is a data structure that consists of nested lists with a cap on elements included in nested lists."""


class BoundedList(InfiniteList):
    def __init__(self, parsed_line, insert_type, merge_type, limit, difficulty, content=None):
        """
        :param limit: Sets the limit of tokens inserted into this data structure

        :var self.size: The current size of BoundedList object (2 at the beginning, if initialized from a parsed line,
                        because a parsed line contains two tokens)
        """
        super(BoundedList, self).__init__(parsed_line, insert_type, merge_type, difficulty, content)

        self.limit = limit
        if not content:
            self.size = 2
        else:
            # Content must be of type list, so this will result in size of content and therefore size of bounded list.
            self.size = 0
            for row in content:
                for column in row:
                    if column != "x":
                        self.size += 1

    def __str__(self):
        return "BoundedList content: " + str(self.content)

    def insert(self, parsed_line):
        """
        Given a parsed object (first_token, relation, second_token), insert it into this data structure.
        If size would grow over size limit of self.limit, return False so a new BoundedList object can be created instead.

        Fill free space with x's for possible gaps, so that situations such as:
        ['A',  x,  'B']
        ['C', 'D', 'E']
        are accounted for.

        :param parsed_line: A parsed line

        :return: bool: Whether insert worked or not.
        """
        if self.size < self.limit:
            super(BoundedList, self).insert(parsed_line)
            self.size += 1
            return True
        else:
            return False

    def merge(self, infinite_list, parsed_line):
        merged_object = super(BoundedList, self).merge(infinite_list, parsed_line)
        merged_object = InfiniteList('', self.insert_type, self.merge_type, self.difficulty, merged_object)
        if len(merged_object) <= self.limit:
            return super(BoundedList, self).merge(infinite_list, parsed_line)
        else:
            # They can't be merged. Don't merge.
            pass
