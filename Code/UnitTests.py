import unittest

from Parser import Parser
from CentralExecutive import CentralExecutive
from DataStructures.InfiniteList import InfiniteList
from DataStructures.BoundedList import BoundedList
from DataStructures.BinarySearchTree import BinarySearchTree
from DataStructures.LinkedList import LinkedList

__author__ = 'Phaina'


class TestParser(unittest.TestCase):
    def test_premise(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        self.assertEqual(parsed_line.first_token, 'A')
        self.assertEqual(parsed_line.relation, 'left')
        self.assertEqual(parsed_line.type, 'Premise')
        self.assertEqual(parsed_line.second_token, 'C')

    def test_conclusion(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        line = "C: A left C"
        parsed_line = Parser(line, ce.memory)
        self.assertEqual(parsed_line.type, 'Conclusion')


class TestCentralExecutive(unittest.TestCase):
    def test_parsing(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        for conclusion in ce.conclusions:
            self.assertIsInstance(conclusion, Parser)
            self.assertEqual(conclusion.type, "Conclusion")


class TestMemory(unittest.TestCase):
    def test_finding(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        found_in = ce.memory.search('A')
        self.assertEqual(len(found_in), 1)
        line2 = "P: A left B"
        parsed_line2 = Parser(line2, ce.memory)
        inflist2 = InfiniteList(parsed_line2, 'fff', 'integrate', ce.difficulty)
        self.assertTrue(ce.memory.search_model(inflist2.content))


class TestInfiniteList(unittest.TestCase):
    def test_creating(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        inflist = InfiniteList(parsed_line, ce.insert_type, ce.merge_type, ce.difficulty)
        self.assertEqual(inflist.content, [['A', 'C']])

    def test_find(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        inflist = InfiniteList(parsed_line, "fff", "integrate", ce.difficulty)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        inflist.insert(parsed_line2)
        self.assertEqual(inflist.find_index('A'), (0, 0))
        self.assertTrue(inflist.find('A'))
        self.assertEqual(inflist.find_index('D'), (0, 2))
        self.assertTrue(inflist.find('D'))

    def test_insert_one_dimensional_ff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        inflist = InfiniteList(parsed_line, "ff", "integrate", ce.difficulty)
        ce.memory.insert(inflist)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        inflist.insert(parsed_line2)
        self.assertEqual(inflist.content, [['A', 'B', 'C']])
        line3 = "P: D right C"
        parsed_line3 = Parser(line3, ce.memory)
        inflist.insert(parsed_line3)
        self.assertEqual(inflist.content, [['A', 'B', 'C', 'D']])

    def test_insert_two_dimensional_ff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: C left D"
        parsed_line = Parser(line, ce.memory)
        inflist = InfiniteList(parsed_line, "ff", "integrate", ce.difficulty)
        ce.memory.insert(inflist)
        line2 = "P: A above C"
        parsed_line2 = Parser(line2, ce.memory)
        inflist.insert(parsed_line2)
        self.assertEqual(inflist.content, [['A', 'x'], ['C', 'D']])
        line3 = "P: B above D"
        parsed_line3 = Parser(line3, ce.memory)
        inflist.insert(parsed_line3)
        self.assertEqual(inflist.content, [['A', 'B'], ['C', 'D']])
        line4 = "P: Y above C"
        parsed_line4 = Parser(line4, ce.memory)
        inflist.insert(parsed_line4)
        self.assertEqual(inflist.content, [['A', 'B'], ['Y', 'x'], ['C', 'D']])
        line5 = "P: Z below D"
        parsed_line5 = Parser(line5, ce.memory)
        inflist.insert(parsed_line5)
        self.assertEqual(inflist.content, [['A', 'B'], ['Y', 'x'], ['C', 'D'], ['x', 'Z']])
        line6 = "P: E right D"
        parsed_line6 = Parser(line6, ce.memory)
        inflist.insert(parsed_line6)
        self.assertEqual(inflist.content, [['A', 'B', 'x'], ['Y', 'x', 'x'], ['C', 'D', 'E'], ['x', 'Z', 'x']])

    def test_insert_one_dimensional_fff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        inflist = InfiniteList(parsed_line, "fff", "integrate", ce.difficulty)
        ce.memory.insert(inflist)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        inflist.insert(parsed_line2)
        self.assertEqual(inflist.content, [['B', 'A', 'C']])
        line3 = "P: D right C"
        parsed_line3 = Parser(line3, ce.memory)
        inflist.insert(parsed_line3)
        self.assertEqual(inflist.content, [['B', 'A', 'C', 'D']])

    def test_insert_two_dimensional_fff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: C left D"
        parsed_line = Parser(line, ce.memory)
        inflist = InfiniteList(parsed_line, "fff", "integrate", ce.difficulty)
        self.assertEqual(inflist.content, [["C", "D"]])
        ce.memory.insert(inflist)
        line2 = "P: A above C"
        parsed_line2 = Parser(line2, ce.memory)
        inflist.insert(parsed_line2)
        self.assertEqual(inflist.content, [['A', 'x'], ['C', 'D']])
        line3 = "P: B above D"
        parsed_line3 = Parser(line3, ce.memory)
        inflist.insert(parsed_line3)
        self.assertEqual(inflist.content, [['A', 'B'], ['C', 'D']])
        line4 = "P: Y above C"
        parsed_line4 = Parser(line4, ce.memory)
        inflist.insert(parsed_line4)
        self.assertEqual(inflist.content, [['Y', 'x'], ['A', 'B'], ['C', 'D']])
        line5 = "P: Z below B"
        parsed_line5 = Parser(line5, ce.memory)
        inflist.insert(parsed_line5)
        self.assertEqual(inflist.content, [['Y', 'x'], ['A', 'B'], ['C', 'D'], ['x', 'Z']])
        line6 = "P: U below C"
        parsed_line6 = Parser(line6, ce.memory)
        inflist.insert(parsed_line6)
        self.assertEqual(inflist.content, [['Y', 'x'], ['A', 'B'], ['C', 'D'], ['U', 'Z']])

    def test_evaluation(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        inflist1 = InfiniteList(parsed_premise1, "ff", "integrate", ce.difficulty)
        self.assertEqual(inflist1.content, [['A', 'B']])
        ce.memory.insert(inflist1)
        line2 = "P: B left C"
        parsed_premise2 = Parser(line2, ce.memory)
        inflist1.insert(parsed_premise2)
        self.assertEqual(inflist1.content, [['A', 'B', 'C']])
        line3 = "C: A left C"
        parsed_conclusion = Parser(line3, ce.memory)
        self.assertTrue(inflist1.evaluate_conclusion(parsed_conclusion))

    def test_generation(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        inflist1 = InfiniteList(parsed_premise1, "ff", "integrate", ce.difficulty)
        ce.memory.insert(inflist1)
        line2 = "P: B left C"
        parsed_premise2 = Parser(line2, ce.memory)
        inflist1.insert(parsed_premise2)
        relation = inflist1.generate('A', 'C')
        self.assertEqual(relation, "left")
        line3 = "P: D below C"
        parsed_premise3 = Parser(line3, ce.memory)
        inflist1.insert(parsed_premise3)
        relation2 = inflist1.generate('A', 'D')
        self.assertEqual(relation2, "no_rel")

    def test_merge(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "integrate"
        lines = ['P: A left B\n', 'P: F left G\n', 'P: A above F\n',
                 'P: Y left E\n', 'P: C left D\n', 'P: C below Y\n',
                 'P: A right D\n', 'C: B right C\n']
        ce.differentiate_premises_and_conclusions(lines)
        for premise in ce.premises:
            ce.premise_to_memory(premise, 1)
        for conclusion in ce.conclusions:
            self.assertTrue(ce.evaluate_conclusion(conclusion))
        lines2 = ['P: A left B\n', 'P: C left D\n', 'P: A above C\n',
                  'P: Y left E\n', 'P: F left G\n', 'P: F below Y\n',
                  'P: B left F\n', 'C: B above D\n']
        ce2 = CentralExecutive("parameters_for_unittests.json")
        ce2.data_structure = "InfiniteList"
        ce2.differentiate_premises_and_conclusions(lines2)
        for premise in ce2.premises:
            ce2.premise_to_memory(premise, 1)
        for conclusion in ce2.conclusions:
            self.assertTrue(ce2.evaluate_conclusion(conclusion))

    def test_annotate(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        inflist1 = InfiniteList(parsed_premise1, "fff", "integrate", ce.difficulty)
        ce.memory.insert(inflist1)
        line2 = "P: C left B"
        parsed_premise2 = Parser(line2, ce.memory)
        inflist1.insert(parsed_premise2)
        self.assertEqual(inflist1.annotations['C'], [('left', 'B')])
        line3 = "P: D left C"
        parsed_premise3 = Parser(line3, ce.memory)
        inflist1.insert(parsed_premise3)
        self.assertEqual(inflist1.annotations['C'], [('left', 'B'), ('right', 'D')])
        line4 = "P: E right C"
        parsed_premise4 = Parser(line4, ce.memory)
        inflist1.insert(parsed_premise4)
        self.assertEqual(inflist1.annotations['E'], [('right', 'C')])
        line5 = "P: F above E"
        parsed_premise5 = Parser(line5, ce.memory)
        inflist1.insert(parsed_premise5)
        line6 = "P: G above E"
        parsed_premise6 = Parser(line6, ce.memory)
        inflist1.insert(parsed_premise6)
        self.assertEqual(inflist1.annotations['G'], [('above', 'E')])

    def test_variate_model(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.how_far_removed = 5
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        inflist1 = InfiniteList(parsed_premise1, "fff", "integrate", ce.difficulty)
        ce.memory.insert(inflist1)
        line2 = "P: C left B"
        parsed_premise2 = Parser(line2, ce.memory)
        inflist1.insert(parsed_premise2)
        line3 = "P: D left C"
        parsed_premise3 = Parser(line3, ce.memory)
        inflist1.insert(parsed_premise3)
        line4 = "P: E right C"
        parsed_premise4 = Parser(line4, ce.memory)
        inflist1.insert(parsed_premise4)
        line5 = "C: D right B"
        parsed_conclusion1 = Parser(line5, ce.memory)
        self.assertFalse(inflist1.evaluate_conclusion(parsed_conclusion1))
        self.assertFalse(inflist1.variate_model(parsed_conclusion1, ce.how_far_removed))
        line6 = "C: A left C"
        parsed_conclusion2 = Parser(line6, ce.memory)
        self.assertFalse(inflist1.evaluate_conclusion(parsed_conclusion2))
        self.assertTrue(inflist1.variate_model(parsed_conclusion2, ce.how_far_removed))


class TestBoundedList(unittest.TestCase):
    def testBoundedCreating(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BoundedList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        boundedlist1 = BoundedList(parsed_line, "fff", "integrate", 3, ce.difficulty)
        ce.memory.insert(boundedlist1)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        boundedlist1.insert(parsed_line2)
        self.assertEqual(boundedlist1.content, [['A', 'B', 'C']])
        ce2 = CentralExecutive("parameters_for_unittests.json")
        ce2.data_structure = "BoundedList"
        line3 = "P: A left B"
        parsed_line3 = Parser(line3, ce2.memory)
        boundedlist3 = BoundedList(parsed_line3, "fff", "integrate", 2, ce.difficulty)
        ce2.memory.insert(boundedlist3)
        line4 = "P: B left C"
        parsed_line4 = Parser(line4, ce2.memory)
        ce2.insert_into_model(boundedlist3, parsed_line4)
        self.assertEqual(boundedlist3.content, [['A', 'B']])
        self.assertEqual(len(ce2.memory.models), 2)


class TestDifficultyMeasures(unittest.TestCase):
    def testMoveMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.insert_type = "fff"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.focus_move_ops, 1)
        self.assertEqual(ce.difficulty.focus_move_distance, 1)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.focus_move_ops, 3)
        self.assertEqual(ce.difficulty.focus_move_distance, 4)

    def testWriteMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.write_ops, 2)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.write_ops, 3)

    def testInsertMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.insert_ops, 0)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.insert_ops, 1)
        line3 = "P: A left D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.insert_ops, 2)

    def testMergeMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: F left G"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.merge_ops, 0)
        line3 = "P: B above F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.merge_ops, 1)

    def testPremiseDirectionChangeMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: F left G"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.premise_direction_changes, 0)
        line3 = "P: H right A"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.premise_direction_changes, 1)

    def testFocusDirectionChangeMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.focus_direction_changes, 0)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.focus_direction_changes, 2)
        line3 = "P: A left D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.focus_direction_changes, 4)
        line4 = "P: A below F"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.difficulty.focus_direction_changes, 6)

    def testModelAttentionChanges(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: F left G"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.model_attention_changes, 1)
        line3 = "P: B below F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.model_attention_changes, 3)
        line4 = "P: Z right T"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.difficulty.model_attention_changes, 4)

    def testAnnotationMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.annotation_ops, 0)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.annotation_ops, 1)
        line3 = "P: A left D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.annotation_ops, 2)
        line4 = "P: Z left D"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.difficulty.annotation_ops, 3)

    def testGroupingMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: F left G"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.grouping_ops, 0)
        self.assertEqual(ce.difficulty.grouping_size, 0)
        line3 = "P: B below F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.grouping_ops, 1)
        self.assertEqual(ce.difficulty.grouping_size, 4)
        line4 = "P: Z right T"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        line5 = "P: T left A"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(ce.difficulty.grouping_ops, 2)
        self.assertEqual(ce.difficulty.grouping_size, 10)

    def testLayerMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.layer_count, 1)
        self.assertEqual(ce.difficulty.del_layer_ops, 0)
        line2 = "P: F left G"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.difficulty.layer_count, 2)
        self.assertEqual(ce.difficulty.del_layer_ops, 0)
        line3 = "P: B below F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.layer_count, 2)
        self.assertEqual(ce.difficulty.del_layer_ops, 1)


class TestSuperModelMerge(unittest.TestCase):
    def testInsertIntoSuperModel(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "supermodel"
        ce.merge_instead_of_supermodel = 0
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: B left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.supermodels[0].content, [['A', 'B', 'C', 'D']])
        line4 = "P: D left E"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.memory.supermodels[0].content, [['A', 'B', 'C', 'D', 'E']])

    def testEvaluateSuperModelsNoBounds(self):
        # The "perfect" case, no (relevant) bounds
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "supermodel"
        ce.merge_instead_of_supermodel = 0
        ce.nested_supermodels = 10
        lines = ['P: A left B\n', 'P: C left D\n', 'P: B left C\n',
                 'P: E left F\n', 'P: D left E\n', 'P: G left H\n',
                 'P: F left G\n', 'C: A left H\n']
        ce.differentiate_premises_and_conclusions(lines)
        for premise in ce.premises:
            ce.premise_to_memory(premise, 1)
        ce.combine_supermodels(ce.nested_supermodels, 1)
        for conclusion in ce.conclusions:
            self.assertTrue(ce.evaluate_conclusion(conclusion))

    def testSuperModelTwoD(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "supermodel"
        ce.merge_instead_of_supermodel = 0
        ce.nested_supermodels = 10
        line = "P: A below C"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: D left E"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: A left D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        conc = "C: A left E"
        parsed_conc = Parser(conc, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc))
        line4 = "P: E below F"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        conc2 = "C: F right C"
        parsed_conc2 = Parser(conc2, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc2))
        line5 = "P: G above H"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        line6 = "P: H left J"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        line7 = "P: D left H"
        parsed_line7 = Parser(line7, ce.memory)
        ce.premise_to_memory(parsed_line7, 1)
        conc3 = "C: J right A"
        parsed_conc3 = Parser(conc3, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_conc3))
        ce.combine_supermodels(ce.nested_supermodels, 1)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc3))

    def testSuperModelWithNestBound(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "supermodel"
        ce.merge_instead_of_supermodel = 0
        ce.nested_supermodels = 1
        lines = ['P: A left B\n', 'P: C left D\n', 'P: B left C\n',
                 'P: E left F\n', 'P: D left E\n', 'P: G left H\n',
                 'P: F left G\n', 'C: A left H\n']
        ce.differentiate_premises_and_conclusions(lines)
        for premise in ce.premises:
            ce.premise_to_memory(premise, 1)
        ce.combine_supermodels(ce.nested_supermodels, 1)
        for conclusion in ce.conclusions:
            self.assertFalse(ce.evaluate_conclusion(conclusion))
        ce2 = CentralExecutive("parameters_for_unittests.json")
        ce2.data_structure = "InfiniteList"
        ce2.merge_type = "supermodel"
        ce2.merge_instead_of_supermodel = 0
        ce2.nested_supermodels = 3
        lines = ['P: A left B\n', 'P: C left D\n', 'P: B left C\n',
                 'P: E left F\n', 'P: D left E\n', 'P: G left H\n',
                 'P: F left G\n', 'C: A left H\n']
        ce2.differentiate_premises_and_conclusions(lines)
        for premise in ce2.premises:
            ce2.premise_to_memory(premise, 1)
        ce2.combine_supermodels(ce2.nested_supermodels, 1)
        for conclusion in ce2.conclusions:
            self.assertTrue(ce2.evaluate_conclusion(conclusion))

    def testSuperModelWithBoundedList(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BoundedList"
        ce.merge_type = "supermodel"
        ce.bounded_list_size_limit = 20
        ce.nested_supermodels = 1
        lines = ['P: A left B\n', 'P: C left D\n', 'P: B left C\n',
                 'P: E left F\n', 'P: D left E\n', 'P: G left H\n',
                 'P: F left G\n', 'C: A left H\n']
        ce.differentiate_premises_and_conclusions(lines)
        for premise in ce.premises:
            ce.premise_to_memory(premise, 1)
        ce.combine_supermodels(ce.nested_supermodels, 1)
        for conclusion in ce.conclusions:
            self.assertFalse(ce.evaluate_conclusion(conclusion))
        ce2 = CentralExecutive("parameters_for_unittests.json")
        ce2.data_structure = "BoundedList"
        ce2.merge_type = "supermodel"
        ce.bounded_list_size_limit = 2
        ce2.nested_supermodels = 3
        lines = ['P: A left B\n', 'P: C left D\n', 'P: B left C\n',
                 'P: E left F\n', 'P: D left E\n', 'P: G left H\n',
                 'P: F left G\n', 'C: A left H\n']
        ce2.differentiate_premises_and_conclusions(lines)
        for premise in ce2.premises:
            ce2.premise_to_memory(premise, 1)
        ce2.combine_supermodels(ce2.nested_supermodels, 1)
        for conclusion in ce2.conclusions:
            self.assertTrue(ce2.evaluate_conclusion(conclusion))

    def testSuperModelDifficultyMeasures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "InfiniteList"
        ce.merge_type = "supermodel"
        ce.merge_instead_of_supermodel = 0
        ce.nested_supermodels = 10
        line = "P: A below C"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: D left E"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: A left D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        conc = "C: A left E"
        parsed_conc = Parser(conc, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc))
        self.assertEqual([4, 4, 4, 0, 1, 1, 1, 1, 2, 3, 0, 1, 4, 2, 0], [ce.difficulty.focus_move_ops,
                                                                         ce.difficulty.focus_move_distance,
                                                                         ce.difficulty.write_ops,
                                                                         ce.difficulty.insert_ops,
                                                                         ce.difficulty.merge_ops,
                                                                         ce.difficulty.supermodels_created,
                                                                         ce.difficulty.supermodels_accessed,
                                                                         ce.difficulty.premise_direction_changes,
                                                                         ce.difficulty.focus_direction_changes,
                                                                         ce.difficulty.model_attention_changes,
                                                                         ce.difficulty.annotation_ops,
                                                                         ce.difficulty.grouping_ops,
                                                                         ce.difficulty.grouping_size,
                                                                         ce.difficulty.layer_count,
                                                                         ce.difficulty.del_layer_ops])
        line4 = "P: E below F"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        conc2 = "C: F right C"
        parsed_conc2 = Parser(conc2, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc2))
        self.assertEqual([8, 9, 5, 1, 1, 1, 2, 2, 6, 3, 0, 1, 4, 2, 0], [ce.difficulty.focus_move_ops,
                                                                         ce.difficulty.focus_move_distance,
                                                                         ce.difficulty.write_ops,
                                                                         ce.difficulty.insert_ops,
                                                                         ce.difficulty.merge_ops,
                                                                         ce.difficulty.supermodels_created,
                                                                         ce.difficulty.supermodels_accessed,
                                                                         ce.difficulty.premise_direction_changes,
                                                                         ce.difficulty.focus_direction_changes,
                                                                         ce.difficulty.model_attention_changes,
                                                                         ce.difficulty.annotation_ops,
                                                                         ce.difficulty.grouping_ops,
                                                                         ce.difficulty.grouping_size,
                                                                         ce.difficulty.layer_count,
                                                                         ce.difficulty.del_layer_ops])
        line5 = "P: G above H"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        line6 = "P: H left J"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        line7 = "P: D left H"
        parsed_line7 = Parser(line7, ce.memory)
        ce.premise_to_memory(parsed_line7, 1)
        self.assertEqual([12, 14, 8, 2, 2, 2, 2, 4, 9, 6, 0, 2, 10, 3, 0], [ce.difficulty.focus_move_ops,
                                                                         ce.difficulty.focus_move_distance,
                                                                         ce.difficulty.write_ops,
                                                                         ce.difficulty.insert_ops,
                                                                         ce.difficulty.merge_ops,
                                                                         ce.difficulty.supermodels_created,
                                                                         ce.difficulty.supermodels_accessed,
                                                                         ce.difficulty.premise_direction_changes,
                                                                         ce.difficulty.focus_direction_changes,
                                                                         ce.difficulty.model_attention_changes,
                                                                         ce.difficulty.annotation_ops,
                                                                         ce.difficulty.grouping_ops,
                                                                         ce.difficulty.grouping_size,
                                                                         ce.difficulty.layer_count,
                                                                         ce.difficulty.del_layer_ops])
        conc3 = "C: J right A"
        parsed_conc3 = Parser(conc3, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_conc3))
        ce.combine_supermodels(ce.nested_supermodels, 1)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc3))

    def test_merge_supermodel_BST_2D(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.merge_type = "supermodel"
        ce.merge_instead_of_supermodel = 0
        ce.nested_supermodels = 10
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: E left F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: B left C"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        line5 = "P: D left E"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        conc = "C: A left F"
        parsed_conc = Parser(conc, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_conc))
        ce.combine_supermodels(ce.nested_supermodels, 1)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc))

    def test_merge_supermodel_BST_2D_complex(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.merge_type = "supermodel"
        ce.nested_supermodels = 10
        line = "P: A right B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: E above F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: B left C"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        line5 = "P: D left E"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        conc = "C: A left E"
        parsed_conc = Parser(conc, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_conc))
        ce.combine_supermodels(ce.nested_supermodels, 1)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc))

    def test_merge_supermodel_LinkedList_2D_complex(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.merge_type = "supermodel"
        ce.nested_supermodels = 10
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: E left F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: B left C"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        line5 = "P: D left E"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        conc = "C: A left F"
        parsed_conc = Parser(conc, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_conc))
        ce.combine_supermodels(ce.nested_supermodels, 1)
        self.assertTrue(ce.evaluate_conclusion(parsed_conc))


class TestBinarySearchTree(unittest.TestCase):
    def test_creating(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        bst1 = BinarySearchTree((0, 0), parsed_line, "fff", "integrate", ce.difficulty)
        ce.memory.insert(bst1)
        self.assertEqual(1, len(ce.memory.models))
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        bst2 = BinarySearchTree((0, 0), parsed_line2, "fff", "integrate", ce.difficulty)
        ce.memory.insert(bst2)
        self.assertEqual(2, len(ce.memory.models))

    def test_find(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        bst1= BinarySearchTree(0, parsed_line, "fff", "integrate", ce.difficulty)
        self.assertEqual(0, bst1.find_key('A'))
        self.assertEqual(1, bst1.find_key('B'))
        self.assertTrue(bst1.find(token='A'))
        self.assertTrue(bst1.find(token='B'))
        self.assertFalse(bst1.find(token='C'))

    def test_insert_one_dimensional_ff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "ff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left B"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(1, len(ce.memory.models))
        self.assertEqual('A', ce.memory.models[0].token)
        self.assertEqual('C', ce.memory.models[0].right.token)
        self.assertEqual('B', ce.memory.models[0].right.right.token)
        line3 = "P: E left F"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: F left G"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual('G', ce.memory.models[1].right.right.token)

    def test_length(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        # Assert that length of a tree is equal independent of at which node the length is queried
        self.assertEqual(len(ce.memory.models[0]), 2)
        self.assertEqual(len(ce.memory.models[0].right), 2)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(len(ce.memory.models[0]), 3)
        self.assertEqual(len(ce.memory.models[0].right), 3)
        self.assertEqual(len(ce.memory.models[0].right.right), 3)

    def test_insert_one_dimensional_fff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left B"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(1, len(ce.memory.models))
        self.assertEqual('A', ce.memory.models[0].token)
        self.assertEqual('B', ce.memory.models[0].right.token)
        self.assertEqual('C', ce.memory.models[0].left.token)
        line3 = "P: D left B"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(1, len(ce.memory.models))
        self.assertEqual('A', ce.memory.models[0].token)
        self.assertEqual('B', ce.memory.models[0].right.token)
        self.assertEqual('C', ce.memory.models[0].left.token)
        self.assertEqual('D', ce.memory.models[0].left.left.token)

    def test_insert_two_dimensional_ff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "ff"
        ce.merge_type = "integrate"
        ce.how_far_removed = 0
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A above D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(len(ce.memory.models), 1)
        self.assertEqual(ce.memory.models[0].below.token, "D")
        line3 = "P: D left E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].below.right.token, "E")
        line4 = "C: B above E"
        parsed_line4 = Parser(line4, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_line4))
        line5 = "C: A left E"
        parsed_line5 = Parser(line5, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line5))
        line6 = "P: A left C"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        self.assertEqual(ce.memory.models[0].right.token, "C")
        line7 = "C: C above E"
        parsed_line7 = Parser(line7, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_line7))
        self.assertFalse(ce.evaluate_conclusion(parsed_line4))

    def test_insert_two_dimensional_fff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        ce.how_far_removed = 0
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A above D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(len(ce.memory.models), 1)
        self.assertEqual(ce.memory.models[0].below.token, "D")
        line3 = "P: D left E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].below.right.token, "E")
        line4 = "C: B above E"
        parsed_line4 = Parser(line4, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_line4))
        line5 = "C: A left E"
        parsed_line5 = Parser(line5, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line5))
        line6 = "P: A left C"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        self.assertEqual(ce.memory.models[0].right.token, "B")
        self.assertEqual(ce.memory.models[0].right.right.token, "C")
        line7 = "C: C above E"
        parsed_line7 = Parser(line7, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line7))
        self.assertTrue(ce.evaluate_conclusion(parsed_line4))

    def test_merge_one_dimensional(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: B left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(len(ce.memory.models), 1)
        self.assertEqual(ce.memory.models[0].right.right.right.token, 'D')
        line4 = "P: E left F"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(len(ce.memory.models), 2)
        line5 = "P: D left E"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(len(ce.memory.models), 1)
        self.assertEqual(ce.memory.models[0].right.right.right.right.right.token, 'F')
        line = "P: G right H"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: I right J"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: H right I"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(len(ce.memory.models), 2)
        self.assertEqual(ce.memory.models[1].right.left.token, 'H')
        line4 = "P: K right L"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(len(ce.memory.models), 3)
        line5 = "P: H right K"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(len(ce.memory.models), 2)
        self.assertEqual(ce.memory.models[1].right.right.left.token, "H")

    def test_merge_two_dimensional(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: E below D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].below.below.token, "E")
        ce.memory.remove(ce.memory.models[0])
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: D above E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].below.below.token, "E")
        ce.memory.remove(ce.memory.models[0])
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: A below E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].below.below.token, "A")
        ce.memory.remove(ce.memory.models[0])
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: F below D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: Z right E"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.memory.models[0].below.below.token, "E")
        self.assertEqual(ce.memory.models[0].below.below.right.token, "Z")

    def test_annotate(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.memory.models[0].annotations["C"], [('left', 'A')])
        line3 = "P: D left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].annotations["C"], [('left', 'A'), ('right', 'D')])

    def test_variate_model(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.how_far_removed = 5
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        BST = BinarySearchTree(None, parsed_premise1, ce.insert_type, ce.merge_type, ce.difficulty)
        ce.memory.insert(BST)
        line2 = "P: C left B"
        parsed_premise2 = Parser(line2, ce.memory)
        BST.insert(parsed_premise2)
        line3 = "P: D left C"
        parsed_premise3 = Parser(line3, ce.memory)
        BST.insert(parsed_premise3)
        line4 = "P: E right C"
        parsed_premise4 = Parser(line4, ce.memory)
        BST.insert(parsed_premise4)
        line5 = "C: D right B"
        parsed_conclusion1 = Parser(line5, ce.memory)
        self.assertFalse(BST.evaluate_conclusion(parsed_conclusion1))
        self.assertFalse(BST.variate_model(parsed_conclusion1, ce.how_far_removed))
        line6 = "C: A left C"
        parsed_conclusion2 = Parser(line6, ce.memory)
        self.assertFalse(BST.evaluate_conclusion(parsed_conclusion2))
        self.assertTrue(BST.variate_model(parsed_conclusion2, ce.how_far_removed))

    def test_generation(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A above D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: E right D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].generate("B", "E"), "above")
        self.assertEqual(ce.memory.models[0].generate("B", "A"), "right")
        self.assertEqual(ce.memory.models[0].generate("D", "A"), "below")
        self.assertEqual(ce.memory.models[0].generate("D", "E"), "left")
        line4 = "P: A above X"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.memory.models[0].generate("X", "D"), "below")

    def test_depth_measure(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: B left E"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 2)
        line3 = "P: C left E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: D right E"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 3)
        line5 = "P: F right E"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 4)
        line6 = "P: G left C"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 4)

    def test_depth_measure_merge(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C right D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 1)
        line3 = "P: C left A"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: D left E"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 3)
        line5 = "P: Y left Z"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 3)
        line6 = "P: E right Y"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 5)

    def test_difficulty_measures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C right A"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: D left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.focus_move_ops, 4)
        self.assertEqual(ce.difficulty.focus_move_distance, 7)
        self.assertEqual(ce.difficulty.focus_direction_changes, 3)
        self.assertEqual(ce.difficulty.focus_key_distance, 7)
        self.assertEqual(ce.difficulty.BST_depth, 2)

    def test_difficulty_measures_easier_example(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: A left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.focus_move_ops, 2)
        self.assertEqual(ce.difficulty.focus_move_distance, 6)
        self.assertEqual(ce.difficulty.focus_direction_changes, 2)
        self.assertEqual(ce.difficulty.focus_key_distance, 6)
        self.assertEqual(ce.difficulty.BST_depth, 2)

    def test_difficulty_measures_3D(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line0 = "P: A above E"
        parsed_line0 = Parser(line0, ce.memory)
        ce.premise_to_memory(parsed_line0, 1)
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C right A"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: D left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.focus_move_ops, 6)
        self.assertEqual(ce.difficulty.focus_move_distance, 9)


class TestBinarySearchTreeTrivial(unittest.TestCase):
    def test_difference_to_BST(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTreeTrivial"
        ce.insert_type = "ff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A above D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(len(ce.memory.models), 1)
        self.assertEqual(ce.memory.models[0].below.token, "D")
        line3 = "P: D left E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].below.right.token, "E")
        line4 = "C: B above E"
        parsed_line4 = Parser(line4, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_line4))
        line5 = "C: A left E"
        parsed_line5 = Parser(line5, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line5))
        line6 = "P: A left C"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 1)
        self.assertEqual(ce.memory.models[0].right.token, "B")
        self.assertEqual(ce.memory.models[0].right.left.token, "C")
        line7 = "C: C above E"
        parsed_line7 = Parser(line7, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line7))


class TestBinarySearchTreeLimitedDepth(unittest.TestCase):
    def test_difference_to_BST(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTreeLimitedDepth"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        ce.BST_depth_limit = 2
        line = "P: B right A"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C right D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 1)
        line3 = "P: C left A"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: E right B"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(ce.memory.models[0].root.depth, 2)


class TestBinarySearchTreeRandomTree(unittest.TestCase):
    def test_difference_to_BST(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "BinarySearchTreeRandomTree"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left B"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: D left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        line4 = "P: E right A"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        # No test here because due to the structure of a random search tree, it will look different every time.
        # However, feel free to look at some possibilities:
        # print ce.memory


class TestLinkedList(unittest.TestCase):
    def test_create(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.memory.models[0].content[0].token, 'A')
        self.assertEqual(ce.memory.models[0].content[0].pointing_to.token, 'B')
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[1].content[0].token, 'C')
        self.assertEqual(ce.memory.models[1].content[0].pointing_to.token, 'D')

    def test_insert_fff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[0].content[0].pointing_to.pointing_to.token, 'C')
        line3 = "P: D left A"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        self.assertEqual(ce.memory.models[0].content[0].token, 'D')
        line4 = "P: A above E"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 4)
        self.assertEqual(ce.memory.models[0].content[1].token, 'x')
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.token, 'E')
        line5 = "P: E left Z"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 5)
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.pointing_to.token, 'Z')

    def test_insert_ff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "ff"
        ce.merge_type = "integrate"
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[0].content[0].pointing_to.token, 'B')
        line3 = "P: A above E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        self.assertEqual(ce.memory.models[0].content[1].token, 'E')
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.token, 'x')
        line4 = "P: E left Z"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 4)
        self.assertEqual(ce.memory.models[0].content[1].token, 'E')
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.token, 'Z')
        line5 = "P: Z right Y"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 5)
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.token, 'Y')
        line6 = "P: F below B"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 6)
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.pointing_to.token, 'F')

    def test_annotate(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        inflist1 = InfiniteList(parsed_premise1, "fff", "integrate", ce.difficulty)
        ce.memory.insert(inflist1)
        line2 = "P: C left B"
        parsed_premise2 = Parser(line2, ce.memory)
        inflist1.insert(parsed_premise2)
        self.assertEqual(inflist1.annotations['C'], [('left', 'B')])
        line3 = "P: D left C"
        parsed_premise3 = Parser(line3, ce.memory)
        inflist1.insert(parsed_premise3)
        self.assertEqual(inflist1.annotations['C'], [('left', 'B'), ('right', 'D')])
        line4 = "P: E right C"
        parsed_premise4 = Parser(line4, ce.memory)
        inflist1.insert(parsed_premise4)
        self.assertEqual(inflist1.annotations['E'], [('right', 'C')])
        line5 = "P: F above E"
        parsed_premise5 = Parser(line5, ce.memory)
        inflist1.insert(parsed_premise5)
        line6 = "P: G above E"
        parsed_premise6 = Parser(line6, ce.memory)
        inflist1.insert(parsed_premise6)
        self.assertEqual(inflist1.annotations['G'], [('above', 'E')])

    def test_merge_one_dimensional(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.merge_type = "integrate"
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        ce.premise_to_memory(parsed_premise1, 1)
        line2 = "P: C left D"
        parsed_premise2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_premise2, 2)
        line3 = "P: B left C"
        parsed_premise3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_premise3, 3)
        self.assertEqual(ce.memory.models[0].content[0].pointing_to.pointing_to.token, 'C')
        self.assertEqual(len(ce.memory.models), 1)
        line4 = "P: E left F"
        parsed_premise4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_premise4, 4)
        line5 = "P: G left H"
        parsed_premise5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_premise5, 5)
        self.assertEqual(len(ce.memory.models), 3)
        line6 = "P: H right F"
        parsed_premise6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_premise6, 6)
        self.assertEqual(ce.memory.models[1].content[0].pointing_to.pointing_to.token, 'G')
        self.assertEqual(len(ce.memory.models), 2)

    def test_merge_three_dimensional(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.merge_type = "integrate"
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        ce.premise_to_memory(parsed_premise1, 1)
        line2 = "P: C left D"
        parsed_premise2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_premise2, 2)
        self.assertEqual(len(ce.memory.models), 2)
        line3 = "P: B above C"
        parsed_premise3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_premise3, 3)
        self.assertEqual(len(ce.memory.models), 1)
        self.assertEqual(ce.memory.models[0].content[0].token, 'A')
        self.assertEqual(ce.memory.models[0].content[1].pointing_to.token, 'C')

    def test_complicated_merge(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.merge_type = "integrate"
        lines = ['P: A left B\n', 'P: F left G\n', 'P: A above F\n',
                 'P: Y left E\n', 'P: C left D\n', 'P: C below Y\n',
                 'P: A right D\n', 'C: B right C\n']
        ce.differentiate_premises_and_conclusions(lines)
        for premise in ce.premises:
            ce.premise_to_memory(premise, 1)
        for conclusion in ce.conclusions:
            self.assertTrue(ce.evaluate_conclusion(conclusion))
        lines2 = ['P: A left B\n', 'P: C left D\n', 'P: A above C\n',
                  'P: Y left E\n', 'P: F left G\n', 'P: F below Y\n',
                  'P: B left F\n', 'C: B above D\n']
        ce2 = CentralExecutive("parameters_for_unittests.json")
        ce2.data_structure = "LinkedList"
        ce2.differentiate_premises_and_conclusions(lines2)
        for premise in ce2.premises:
            ce2.premise_to_memory(premise, 1)
        for conclusion in ce2.conclusions:
            self.assertTrue(ce2.evaluate_conclusion(conclusion))

    def test_evaluate(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A above D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        line3 = "P: D left E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        line4 = "C: B above E"
        parsed_line4 = Parser(line4, ce.memory)
        self.assertTrue(ce.evaluate_conclusion(parsed_line4))
        line5 = "C: A left E"
        parsed_line5 = Parser(line5, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line5))
        line6 = "P: A left C"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 4)
        line7 = "C: C above E"
        parsed_line7 = Parser(line7, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line7))

    def test_generation(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A above D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        line3 = "P: E right D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        self.assertEqual(ce.memory.models[0].generate("B", "E"), "above")
        self.assertEqual(ce.memory.models[0].generate("B", "A"), "right")
        self.assertEqual(ce.memory.models[0].generate("D", "A"), "below")
        self.assertEqual(ce.memory.models[0].generate("D", "E"), "left")
        line4 = "P: A above X"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 4)
        self.assertEqual(ce.memory.models[0].generate("X", "D"), "below")

    def test_variate_model(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.how_far_removed = 5
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        linkedlist = LinkedList(parsed_premise1, ce.insert_type, ce.merge_type, ce.difficulty)
        ce.memory.insert(linkedlist)
        line2 = "P: C left B"
        parsed_premise2 = Parser(line2, ce.memory)
        linkedlist.insert(parsed_premise2)
        line3 = "P: D left C"
        parsed_premise3 = Parser(line3, ce.memory)
        linkedlist.insert(parsed_premise3)
        line4 = "P: E right C"
        parsed_premise4 = Parser(line4, ce.memory)
        linkedlist.insert(parsed_premise4)
        line5 = "C: D right B"
        parsed_conclusion1 = Parser(line5, ce.memory)
        self.assertFalse(linkedlist.evaluate_conclusion(parsed_conclusion1))
        self.assertFalse(linkedlist.variate_model(parsed_conclusion1, ce.how_far_removed))
        line6 = "C: A left C"
        parsed_conclusion2 = Parser(line6, ce.memory)
        self.assertFalse(linkedlist.evaluate_conclusion(parsed_conclusion2))
        self.assertTrue(linkedlist.variate_model(parsed_conclusion2, ce.how_far_removed))

    def test_difficulty_measures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C right A"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: D left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.difficulty.focus_move_ops, 4)
        self.assertEqual(ce.difficulty.focus_move_distance, 7)
        self.assertEqual(ce.difficulty.focus_direction_changes, 3)

    def test_failed_comp1(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A right B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C right A"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        line3 = "C: B right C"
        parsed_line3 = Parser(line3, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_line3))

    def test_failed_fourstage(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "LinkedList"
        ce.insert_type = "ff"
        ce.merge_type = "integrate"
        line = "P: A right B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: B right C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        line3 = "P: C left D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        conc = "C: D right B"
        parsed_conc = Parser(conc, ce.memory)
        self.assertFalse(ce.evaluate_conclusion(parsed_conc))


class TestGraph(unittest.TestCase):
    def test_create(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(len(ce.memory.models), 2)
        self.assertEqual(ce.memory.models[0].content, [['x', 'A', 'B'], ['A', 'x', 'left'], ['B', 'right', 'x']])

    def test_insert_fff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.memory.models[0].generate('A', 'B'), 'left')
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[0].generate('A', 'B'), 'left')
        self.assertEqual(ce.memory.models[0].generate('A', 'C'), 'left')
        self.assertEqual(ce.memory.models[0].generate('C', 'A'), 'right')
        line3 = "P: D left A"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        self.assertEqual(ce.memory.models[0].generate('D', 'A'), 'left')
        self.assertEqual(ce.memory.models[0].generate('C', 'D'), 'right')
        line4 = "P: A above E"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 4)
        line5 = "P: E right Z"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 5)
        self.assertEqual(ce.memory.models[0].generate('A', 'B'), 'left')
        self.assertEqual(ce.memory.models[0].generate('A', 'E'), 'above')
        self.assertEqual(ce.memory.models[0].generate('D', 'Z'), 'above')
        line6 = "P: E left Y"
        parsed_line6 = Parser(line6, ce.memory)
        ce.premise_to_memory(parsed_line6, 6)
        self.assertEqual(ce.memory.models[0].generate('B', 'Y'), 'above')

    def test_insert_ff(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "ff"
        ce.merge_type = "integrate"
        line = "P: A left C"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: B left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[0].generate('B', 'A'), 'right')
        line3 = "P: A above E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        line4 = "P: E left Z"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 4)
        self.assertEqual(ce.memory.models[0].generate('B', 'Z'), 'above')
        self.assertEqual(ce.memory.models[0].generate('A', 'Z'), 'no_rel')
        line5 = "P: Z right Y"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 5)
        self.assertEqual(ce.memory.models[0].generate('E', 'Y'), 'left')
        self.assertEqual(ce.memory.models[0].generate('Z', 'Y'), 'right')
        self.assertEqual(ce.memory.models[0].generate('B', 'Y'), 'above')
        self.assertEqual(ce.memory.models[0].generate('B', 'Z'), 'no_rel')

    def test_annotate(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: A left C"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[0].annotations["C"], [('right', 'A')])
        line3 = "P: D left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)
        self.assertEqual(ce.memory.models[0].annotations["C"], [('right', 'A'), ('right', 'D')])
        self.assertEqual(ce.memory.models[0].annotations["D"], [('left', 'C')])

    def test_merge_one_dimensional(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: B left C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].generate('A', 'D'), 'left')
        self.assertEqual(len(ce.memory.models), 1)
        line4 = "P: E left F"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(len(ce.memory.models), 2)
        line5 = "P: D left E"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(ce.memory.models[0].generate('A', 'F'), 'left')
        self.assertEqual(len(ce.memory.models), 1)
        line = "P: G right H"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: I right J"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: H right I"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(len(ce.memory.models), 2)
        self.assertEqual(ce.memory.models[1].generate('H', 'I'), 'right')
        line4 = "P: K right L"
        parsed_line4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_line4, 1)
        self.assertEqual(len(ce.memory.models), 3)
        line5 = "P: H right K"
        parsed_line5 = Parser(line5, ce.memory)
        ce.premise_to_memory(parsed_line5, 1)
        self.assertEqual(len(ce.memory.models), 2)
        self.assertEqual(ce.memory.models[1].generate('L', 'G'), 'left')

    def test_merge_two_dimensional(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: E below D"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].generate('A', 'F'), 'above')
        ce.memory.remove(ce.memory.models[0])
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: D above E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].generate('A', 'F'), 'above')
        ce.memory.remove(ce.memory.models[0])
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: A below E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].generate('E', 'A'), 'above')
        ce.memory.remove(ce.memory.models[0])
        line = "P: A above D"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: E above F"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 1)
        line3 = "P: A left E"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 1)
        self.assertEqual(ce.memory.models[0].generate('D', 'F'), 'left')

    def test_variate(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        ce.how_far_removed = 10
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        line2 = "P: C left B"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.memory.models[0].annotations['B'], [('right', 'C')])
        conc = "P: C right A"
        parsed_conc = Parser(conc, ce.memory)
        self.assertFalse(ce.memory.models[0].evaluate_conclusion(parsed_conc))
        self.assertTrue(ce.evaluate_conclusion(parsed_conc))

    def test_variate_more_complex(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.how_far_removed = 5
        line1 = "P: A left B"
        parsed_premise1 = Parser(line1, ce.memory)
        ce.premise_to_memory(parsed_premise1, 1)
        line2 = "P: C left B"
        parsed_premise2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_premise2, 2)
        line3 = "P: D left C"
        parsed_premise3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_premise3, 3)
        line4 = "P: E right C"
        parsed_premise4 = Parser(line4, ce.memory)
        ce.premise_to_memory(parsed_premise4, 4)
        line5 = "C: D right B"
        parsed_conclusion1 = Parser(line5, ce.memory)
        self.assertFalse(ce.memory.models[0].evaluate_conclusion(parsed_conclusion1))
        self.assertFalse(ce.memory.models[0].variate_model(parsed_conclusion1, ce.how_far_removed))
        line6 = "C: A left C"
        parsed_conclusion2 = Parser(line6, ce.memory)
        self.assertFalse(ce.memory.models[0].evaluate_conclusion(parsed_conclusion2))
        self.assertTrue(ce.memory.models[0].variate_model(parsed_conclusion2, ce.how_far_removed))

    def test_difficulty_measures(self):
        ce = CentralExecutive("parameters_for_unittests.json")
        ce.data_structure = "Graph"
        ce.insert_type = "fff"
        ce.merge_type = "integrate"
        line = "P: A left B"
        parsed_line = Parser(line, ce.memory)
        ce.premise_to_memory(parsed_line, 1)
        self.assertEqual(ce.difficulty.graph_amount_relationships, 1)
        line2 = "P: C left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(len(ce.memory.models), 2)
        self.assertEqual(ce.difficulty.graph_amount_relationships, 2)
        self.assertEqual(ce.difficulty.write_ops, 4)
        self.assertEqual(ce.difficulty.insert_ops, 0)
        line2 = "P: E left D"
        parsed_line2 = Parser(line2, ce.memory)
        ce.premise_to_memory(parsed_line2, 2)
        self.assertEqual(ce.difficulty.graph_amount_relationships, 3)
        self.assertEqual(ce.difficulty.write_ops, 5)
        self.assertEqual(ce.difficulty.insert_ops, 1)
        line3 = "P: B right C"
        parsed_line3 = Parser(line3, ce.memory)
        ce.premise_to_memory(parsed_line3, 3)


if __name__ == '__main__':
    unittest.main()