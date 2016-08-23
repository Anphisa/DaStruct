# The influence of mental representations on human relational reasoning: Analyzing data structures as cognitive models

This is my bachelor's thesis. It's supposed to check different data structures & methods for their use in modelling human behavior.
More specifically, for human behavior in spatial reasoning, i.e. how humans perform in tasks like:

- The rat is to the left of the cat.
- The cat is to the right of the dinosaur.
- Is the dinosaur to the right of the rat?

So to test how to best model human behavior, failures and successes, I'm trying some data structures for their ability in this endeavour.

## Thesis
This directory contains my thesis. I.e., here the theory and implementation is explained and described and results from the modelling tests are given.

## Code
This directory contains actual, live code. The most important parts of code are:

- parameters.json - Here parameters can be changed for *how* to model human behavior, i.e. which data structures, insert types, etc. should be used.
- In parameters.json there's also the parameter "filename", specify your desired problem txt name here.
- TestCase1.txt - Current test case file. Specify problems in form P: A left B and C: B right A, where P is premise and C is conclusion.
- CentralExecutive.py - Executing this with "python CentralExecutive.py" will read premises and conclusions from the file you specified and treat them with the parameters you specified. Very exciting. Will it work?
- UnitTest.py - Executing this should result in "ok", by which you know that there are probably only a few bugs left in the code. Plus, you can derive some implementation details from the tests.

### How-to for trying out the code
- Write a premise file. See Code/TestCase1.txt for an example
- Open parameters.json. See if it looks good to you. You can specify:
	- "verbose" - whether the program gives output on the shell, 0 or 1
	- "merge type" - "integrate" or "supermodel" 
	- "activation function" - give an activation function. Timestep t has to be called x here. One example:
		- "(lambda x: 2 if x > 2 else 3)(x)"
	- "data structure" - give your preferred data structure. Possibilities:
		- BinarySearchTree
		- InfiniteList
		- Graph
		- ... (see thesis)
	- "insert type" - "ff" or "fff"
	- "nested supermodels" - how far supermodels should be nested, as an int
	- "filename" - the filename of your premisefile, e.g.
		- "TestCase1.txt"
	- "bounded list size limit" - the size limit of bounded list, as an int
	- "BST depth limit" - the maximum depth of a BinarySearchTree, as an int
	- "neighborhood graph removal cap" - how far an alternative model may be on the neighborhood graph from the preferred model, as an int
- Do the analysis of the problem file by executing the following commands (using python 2.7):
	- python
	- CE = CentralExecutive("parameters.json")
	- CE.execute()

### Other parts of code
- "CE on a combination folder" and "CE on an individual" are (messy) scripts for evaluating the performance of a test group (combination folder) or an individual participant.
- The folder "Experimental data" contains the data that was used for the experiments and evaluations.
