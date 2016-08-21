__author__ = 'Phaina'

"""Read lines of type "P: A left B" and create Parser object containing tokens and their relationship."""


class Parser:
    """Create a parsed object."""

    def __init__(self, line, memory):
        """
        Initialize all objects which are to be filled by parsing a given line.

        :param line: Line given (containing one premise or one conclusion).

        :var self.type: Type of line: Premise or conclusion.
        :var self.first_token: The first token.
        :var self.second_token: The second token.
        :var self.relation: The relation between the two tokens.
        :var self.focus: The token as string (not index) that is currently in focus.
        """
        self.line = line
        self.memory = memory
        self.type = None
        self.first_token = None
        self.second_token = None
        self.relation = None
        self.focus = None

        self.parse()

    def __str__(self):
        return "Parsed: " + self.first_token + " " + self.relation + " " + self.second_token

    def invert(self):
        if self.relation == "right":
            self.relation = "left"
            return
        if self.relation == "left":
            self.relation = "right"
            return
        if self.relation == "above":
            self.relation = "below"
            return
        if self.relation == "below":
            self.relation = "above"
            return

    def parse(self):
        """
        Read line and fill class variables with its values.

        :var self.type: Type of line: Premise or conclusion.
        :var self.first_token: The object in focus.
        :var self.second_token: The object that is not in focus.
        :var self.relation: The relation between the two objects.
        """
        self.relation = self.line.split()[2]

        if self.line.split()[0] == "P:":
            self.type = "Premise"
        elif self.line.split()[0] == "C:":
            self.type = "Conclusion"

        self.first_token = self.line.split()[1]
        self.second_token = self.line.split()[3]

        # Setting the focus for parsed object
        # Type 1 premise, focus goes to the left
        if not self.memory.search(self.first_token) and not self.memory.search(self.second_token):
            self.focus = self.first_token
        # Type 2 premise, focus goes to located object
        if self.memory.search(self.first_token) and not self.memory.search(self.second_token):
            self.focus = self.first_token
        if not self.memory.search(self.first_token) and self.memory.search(self.second_token):
            self.focus = self.second_token
        # Type 4 premise, focus goes left
        if self.memory.search(self.first_token) and self.memory.search(self.second_token):
            self.focus = self.first_token
