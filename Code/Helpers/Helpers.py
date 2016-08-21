# pylint: disable=line-too-long, fix-me

from __future__ import print_function

__author__ = 'Phaina'

"""General helper functions."""


class Helpers:
    def __init__(self, verbose):
        self.verboseprint = print if verbose else lambda *a, **k: None

    def combine_lists(self, list1, list2):
        if set(list1) & set(list2):
            if list2.index(list1[0]) > 0:
                return list1[:] + list2[:list2.index(list1[0])]
            elif list1.index(list2[0]) > 0:
                return list1[:list1.index(list2[0])] + list2[:]
        return False
