from Helpers import MyExceptions
from math import log, exp

__author__ = 'Phaina'


class Memory:
    def __init__(self, activation_function):
        """
        :var self.models: A list of all models (data structures) currently in memory
        :var self.supermodels: A list of all supermodels currently in memory (only if insert type is supermodel)
        :var self.model_in_focus: Index in models list of the model that is overall in focus (i.e. that attention is on)
        :var self.activation_function: The activation function that determines when tokens are forgotten.
        :var self.token_timestep: A dictionary that matches the moment in time (the premise number) at which a token
             was encountered so it can be forgotten again via activation function.
        """
        self.models = []
        self.supermodels = []
        self.model_in_focus = None
        self.activation_function = activation_function
        self.token_timestep = {}

    def __str__(self):
        return "Models in memory: " + str([str(model) for model in self.models]) + ", " + \
               "Model in focus: " + str(self.model_in_focus) + "\n" + \
               "Supermodels in memory: " + str([str(model) for model in self.supermodels]) + "\n"

    def insert(self, data_structure):
        """
        Insert a data_structure object into self.models
        """
        self.models.append(data_structure)

    def search(self, token):
        """
        Look for a token in all data structures currently in memory

        :param token: The token that is to be found
        :return: found_in: The data structure(s) in which the token was found or empty list
        """
        found_in = []
        for model in self.models:
            if model.find(token):
                found_in.append(model)
        return found_in

    def search_model(self, model_content):
        """
        Look for a model of certain content. If it exists already, True will be returned.

        :param model_content: The content which is searched, i.e. does a model have that content yet?
        :return: True/False, depending on whether a model with that content exists yet.
        """
        found_in = []
        for model in self.models:
            if model.content == model_content:
                found_in.append(model)
        if found_in:
            return True
        return False

    def search_supermodel(self, supermodel_content):
        """
        Look for a supermodel of certain content. If it exists already, True will be returned.

        :param supermodel_content: The content which is searched, i.e. does a supermodel have that content yet?
        :return: True/False, depending on whether a model with that content exists yet.
        """
        found_in = []
        for supermodel in self.supermodels:
            if supermodel.content == supermodel_content:
                found_in.append(supermodel)
        if found_in:
            return True
        return False

    def remove(self, data_structure):
        """
        Remove a data structure from self.memory.

        :param data_structure: The data structure that is to be removed from memory
        """
        if data_structure in self.models:
            self.models.remove(data_structure)
        else:
            raise MyExceptions.ModelNotInMemory("The searched model {} is not in memory, "
                                                "which consists of {}.".format(data_structure, self.models))

    def activation(self, time):
        """
        Using self.activation_function(time), where time is the number of premises read, forget tokens.
        """
        x = time
        # Ebbinghaus formula uses all seen timesteps (sums up over them)
        timesteps = set()
        for token in self.token_timestep:
            timesteps.add(self.token_timestep[token])

        now_forgotten = eval(self.activation_function)
        tokens_to_forget = []
        for token in self.token_timestep:
            if self.token_timestep[token] <= now_forgotten:
                tokens_to_forget.append(token)
        for token_to_forget in tokens_to_forget:
            in_models = self.search(token_to_forget)
            for model in in_models:
                model.forget(token_to_forget)
