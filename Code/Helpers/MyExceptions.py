# pylint: disable=line-too-long, fix-me

__author__ = 'Phaina'

"""All exceptions that might be raised by the program."""


class ModelError(Exception):
    pass


class ModelNotInMemory(Exception):
    pass


class FoundTooManyModels(Exception):
    pass


class FocusError(Exception):
    pass


class MVPError(Exception):
    pass


class IndexError(Exception):
    pass