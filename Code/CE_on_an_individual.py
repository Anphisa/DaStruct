from os import listdir
from os.path import isfile, join
from json import dumps
import csv
import numpy
import operator
import random
from collections import defaultdict
from CentralExecutive import CentralExecutive

__author__ = 'Phaina'


"""
Go through a folder with premise files, build parameters.json and start CentralExecutive for a run.
Save for every game ID and configuration, which combination of data structures & data methods answered True or False.
Compare for every individual test subject which combination had the highest/second highest match with their answers.
Save those data structures that best represent the reasoning process of an individual in a table. Additionally, save
how many problems they solved correctly, what their mean time was for considering a problem and how often an answer
time deviated highly from that mean time.
"""


class CE_on_an_individual(object):
    def __init__(self, directory, individual_file, output_file):
        self.directory = directory
        self.individual_file = individual_file
        self.problems_with_evaluation_truths = None
        self.rating_dict = None
        how_many_solved_correctly, mean_answer_time, deviated_highly = self.analyze_individual(individual_file)
        self.every_data_combination_on_problem_files(self.directory)
        self.rating_dict = self.make_rating_dict(self.problems_with_evaluation_truths)
        self.compare_individual_with_data_structs(individual_file, self.problems_with_evaluation_truths, self.rating_dict)
        self.person_to_csv(sorted(self.rating_dict.items(), key=operator.itemgetter(1)), individual_file[:-4].split("-")[-2],
                           how_many_solved_correctly,
                           mean_answer_time, deviated_highly, output_file)

    def analyze_individual(self, individual_file):
        """
        Given the file of the performance of an individual test subject, return:
        a) How many problems were correctly solved
        b) What the mean answer time was
        c) How often answer times deviated highly from that mean

        :param individual_file: The file with performance of an individual
        :return: See above
        """
        ind = defaultdict(list)
        with open(individual_file) as file:
            f = csv.DictReader(file, delimiter=",")
            for row in f: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value
                    ind[k].append(v)
        how_many_solved_correctly = 0
        for lastcorrect in ind['lastcorrect']:
            if lastcorrect == "true":
                how_many_solved_correctly += 1
        answer_times = ind['answerTime']
        int_answer_times = []
        for answer_time in answer_times:
            int_answer_times.append(int(answer_time))
        mean_answer_time = numpy.mean(int_answer_times)
        standard_deviation_answer_time = numpy.std(int_answer_times, ddof=1)
        deviated_highly = 0
        for answer_time in int_answer_times:
            # Only consider those times were the individual was too fast. Too slow doesn't say that they were guessing.
            if mean_answer_time - standard_deviation_answer_time >= answer_time:
                deviated_highly += 1
        return how_many_solved_correctly, mean_answer_time, deviated_highly

    def every_data_combination_on_problem_files(self, directory):
        problem_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith(".pf")]
        data_structures = ["LinkedList", "InfiniteList", "BoundedList", "BinarySearchTree",
                           "BinarySearchTreeLimitedDepth", "BinarySearchTreeRandomTree", "BinarySearchTreeTrivial",
                           "Graph"]
        insert_types = ["fff", "ff"]
        merge_types = ["supermodel", "integrate"]
        # See https://en.wikipedia.org/wiki/Activation_function#Comparison_of_activation_functions
        activation_functions = ['x - 10', 'sum([exp(1)**(-((x - n)/2.)) for n in timesteps])',
                                'sum([exp(1)**(-((x - n)/3.)) for n in timesteps])',
                                '(lambda x: 2 if x > 2 else 3)(x)']
        problem_files_to_run_reports = dict()
        for problem_file in problem_files:
            # New dictionary for one problem ID to save all results of all combinations of data structures & methods
            new_dict = dict()
            for data_structure in data_structures:
                for insert_type in insert_types:
                    for merge_type in merge_types:
                        if data_structure == "BoundedList":
                            bounded_list_size_limit = [i for i in range(2, 4)]
                        else:
                            bounded_list_size_limit = [10]
                        if data_structure == "BinarySearchTreeLimitedDepth":
                            BST_depth_limit = [i for i in range(2, 4)]
                        else:
                            BST_depth_limit = [10]
                        if merge_type == "supermodel":
                            nested_supermodels = [i for i in range(2)]
                        else:
                            nested_supermodels = [10]
                        for how_far_removed in range(1):
                            for limit in bounded_list_size_limit:
                                for bst_limit in BST_depth_limit:
                                    for nested in nested_supermodels:
                                        for activation_function in activation_functions:
                                            data = {
                                                "filename": directory + str(problem_file),
                                                "data_structure": data_structure,
                                                "insert_type": insert_type,
                                                "merge_type": merge_type,
                                                "nested_supermodels": nested,
                                                "neighborhood_graph_removal_cap": how_far_removed,
                                                "bounded_list_size_limit": limit,
                                                "BST_depth_limit": bst_limit,
                                                "verbose": 0,
                                                "to_file": 0,
                                                "activation_function": activation_function
                                            }
                                            with open("parameters.json", "w") as parameters:
                                                parameters.write(dumps(data))
                                            # print "Now executing", problem_file, data_structure, insert_type, merge_type, \
                                                how_far_removed, bst_limit, nested, activation_function
                                            CE = CentralExecutive("parameters.json")
                                            conclusion_truth = CE.execute(return_truth_of_conclusion=True)
                                            new_dict[str(data_structure) + "," + str(insert_type) + "," \
                                                         + str(merge_type) + "," + str(limit) + "," \
                                                         + str(bst_limit) + "," + str(nested) + "," \
                                                         + str(activation_function)] = conclusion_truth
            problem_id = problem_file[:-3].split("_")[-1]
            problem_files_to_run_reports[int(problem_id)] = new_dict

        self.problems_with_evaluation_truths = problem_files_to_run_reports
        return

    def make_rating_dict(self, problem_files_to_evaluation_truths):
        """
        Given problem files to evaluation truths, make a dictionary with every possible combination of structs &
        methods, and map those to a 0, so they can be rated up according to individual's performance.
        """
        rating_dict = dict()
        for combination in problem_files_to_evaluation_truths[random.choice(problem_files_to_evaluation_truths.keys())]:
            rating_dict[combination] = 0
        return rating_dict

    def compare_individual_with_data_structs(self, individual_file, problems_with_evaluation_truths, rating_dict):
        """
        Given an individual's performance, compare every answer with that of the data structures.
        Return those combinations of data structures & methods that answered most like this individual did.

        :return: Combination of data structures & methods that have highest compatibility with answers of individual
        """
        ind = defaultdict(list)
        with open(individual_file) as file:
            f = csv.DictReader(file, delimiter=",")
            for row in f: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value
                    ind[k].append(v)
        task_ids = ind['Task-ID']
        last_correct = ind['lastcorrect']
        id_to_correct = dict()
        for i, id in enumerate(task_ids):
            if last_correct[i] == 'false':
                id_to_correct[int(id)] = False
            if last_correct[i] == 'true':
                id_to_correct[int(id)] = True
        for id in id_to_correct:
            for combination in problems_with_evaluation_truths[id]:
                if problems_with_evaluation_truths[id][combination] == id_to_correct[id]:
                    rating_dict[combination] += 1
        return sorted(rating_dict.items(), key=operator.itemgetter(1))

    def person_to_csv(self, rating_dict_for_person, person_id, how_many_solved, mean_answer_time, highest_deviations,
                      ofile):
        """
        Given an id for an individual and their rating dictionary, put their data:
        ID, how many solved, mean_answer_time, high_deviation_number, highest-likeliest, ..., 10th-highest-likeliest
        into a csv.
        """
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        counter = 0
        max = 200000000
        this_highest = []
        most_likely_structs = []
        for rating in reversed(rating_dict_for_person):
            if rating[-1] < max:
                if this_highest:
                    most_likely_structs.append(this_highest)
                max = rating[-1]
                counter += 1
                if counter == 4 or max == 0:
                    break
                this_highest = []
            this_highest.append(rating)
        if len(most_likely_structs) == 3:
            writer.writerow([person_id, how_many_solved, mean_answer_time, highest_deviations, most_likely_structs[0],
                            most_likely_structs[1], most_likely_structs[2]])
        elif len(most_likely_structs) == 2:
            writer.writerow([person_id, how_many_solved, mean_answer_time, highest_deviations, most_likely_structs[0],
                            most_likely_structs[1], ''])
        elif len(most_likely_structs) == 1:
            writer.writerow([person_id, how_many_solved, mean_answer_time, highest_deviations, most_likely_structs[0],
                             '', ''])

if __name__ == '__main__':
    folder_of_4Prem_pfs = "./experimental_data/Combined_data/comparison1-4prem/"
    folder_of_3Prem_pfs = "./experimental_data/Combined_data/comparison1-3prem/"
    folder_of_individuals = "./experimental_data/Individual_data/Ragni-in-prep/Ragni-in-prep/comparison1/new/"
    individuals_4_prem = [folder_of_individuals + f for f in listdir(folder_of_individuals) if isfile(join(folder_of_individuals, f)) \
                          and f.endswith(".csv") and f[:-4].split("-")[-1] == "4Prems"]
    individuals_3_prem = [folder_of_individuals + f for f in listdir(folder_of_individuals) if isfile(join(folder_of_individuals, f)) \
                          and f.endswith(".csv") and f[:-4].split("-")[-1] == "3Prems"]
    ofile_4_prem = open("individuals_data_structure_matches_comparison1_4prems.csv", "wb")
    ofile_3_prem = open("individuals_data_structure_matches_comparison1_3prems.csv", "wb")

    # First 4 prem
    writer = csv.writer(ofile_4_prem, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(["Individual ID", "Correctly solved problems", "Mean answer time",
                     "How many answer times were more than one std faster than mean",
                     "Most likely", "2nd most likely", "3rd most likely"])
    for individual_file in individuals_4_prem:
        print "Looking at individual", individual_file
        CE_on_an_individual(folder_of_4Prem_pfs, individual_file, ofile_4_prem)

    # Then 3 prem
    writer = csv.writer(ofile_3_prem, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(["Individual ID", "Correctly solved problems", "Mean answer time",
                     "How many answer times were more than one std faster than mean",
                     "Most likely", "2nd most likely", "3rd most likely"])
    for individual_file in individuals_3_prem:
        print "Looking at individual", individual_file
        CE_on_an_individual(folder_of_3Prem_pfs, individual_file, ofile_3_prem)

    ofile_3_prem.close()
    ofile_4_prem.close()
