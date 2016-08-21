# The influence of mental representations on human relational reasoning: Analyzing data structures as cognitive models

This is my bachelor's thesis. It's supposed to check different data structures & methods for their use in modelling human behavior.
More specifically, for human behavior in spatial reasoning, i.e. how humans perform in tasks like:

- The rat is to the left of the cat.
- The cat is to the right of the dinosaur.
- Is the dinosaur to the right of the rat?

So to test how to best model human behavior, failures and successes, I'm trying some data structures for their ability in this endeavour.

## Code
This directory contains actual, live code. The most important parts of code are:

- parameters.json - Here parameters can be changed for *how* to model human behavior, i.e. which data structures, insert types, etc. should be used.
- In parameters.json there's also the parameter "filename", specify your desired problem txt name here.
- TestCase1.txt - Current test case file. Specify problems in form P: A left B and C: B right A, where P is premise and C is conclusion.
- CentralExecutive.py - Executing this with "python CentralExecutive.py" will read premises and conclusions from the file you specified and treat them with the parameters you specified. Very exciting. Will it work?
- UnitTest.py - Executing this should result in "ok", by which you know that there are probably only a few bugs left in the code. Plus, you can derive some implementation details from the tests.

## Literatur
This directory contains the literature my thesis is based on.

## Texs
This directory contains the text for my thesis. I.e., here the theory and implementation is explained and described and results from the modelling tests are given.
