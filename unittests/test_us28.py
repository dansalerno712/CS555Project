import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks
import Utils
import datetime

class TestUS28(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US28_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>

    def test_order_siblings_by_age(self):
        result, output = Checks.order_siblings_by_age(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Printing family: " + str(self.families[0].ID) + "\n{ID: @<US28>I1@| Name: Dan /Salerno/| Gender: M| Birthday: 12 JUL 1996| Age: 22| Alive: True| Death: None| Child: ['@<US28>F1@']| Spouse: []} \n{ID: @<US28>I2@| Name: Dan /Salerno/| Gender: M| Birthday: 12 MAY 1998| Age: 20| Alive: True| Death: None| Child: ['@<US28>F1@']| Spouse: []} " + "\n")

    def test_empty_siblings_input(self):
        flag, output = Checks.order_siblings_by_age([], [])
        self.assertEqual(flag, True)
        self.assertEqual(output, "No siblings to print.\n")


if __name__ == '__main__':
    unittest.main()
