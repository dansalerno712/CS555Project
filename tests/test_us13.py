import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS13(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US13_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_sibling_spacings_all_good(self):
        result, output = Checks.sibling_spacings(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All siblings are born more than 8 months or less than 2 days apart\n")

    def test_sibling_spacings_twins_too_far(self):
        x = self.individuals[6].birthday 
        self.individuals[6].birthday = '6 MAR 1959'
        result, output = Checks.sibling_spacings(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(self.individuals[0]) + " and " + str(self.individuals[6]) + " are less than 8 months and more than 2 days apart.\n")
        self.individuals[6].birthday = x 

    def test_sibling_spacings_too_close(self):
        x = self.individuals[8].birthday 
        self.individuals[8].birthday = '9 DEC 1997'
        result, output = Checks.sibling_spacings(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(self.individuals[3]) + " and " + str(self.individuals[8]) + " are less than 8 months and more than 2 days apart.\n")
        self.individuals[8].birthday = x 

    def test_sibling_spacings_twins_too_far(self):
        x = self.individuals[6].birthday 
        self.individuals[6].birthday = '6 MAR 1959'
        result, output = Checks.sibling_spacings(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(self.individuals[0]) + " and " + str(self.individuals[6]) + " are less than 8 months and more than 2 days apart.\n")
        self.individuals[6].birthday = x 

    def test_sibling_spacings_too_close_and_too_far(self):
        y = self.individuals[6].birthday 
        self.individuals[6].birthday = '6 MAR 1959'
        x = self.individuals[8].birthday 
        self.individuals[8].birthday = '9 DEC 1997'
        result, output = Checks.sibling_spacings(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output,  "Error: " + str(self.individuals[3]) + " and " + str(self.individuals[8]) + " are less than 8 months and more than 2 days apart.\n"+
        "Error: " + str(self.individuals[0]) + " and " + str(self.individuals[6]) + " are less than 8 months and more than 2 days apart.\n")
        self.individuals[8].birthday = x 
        self.individuals[6].birthday = 7

    def test_sibling_spacings_empty_inputs(self):
        #set up scenario
        self.families = []
        self.individuals = []
        result, output = Checks.sibling_spacings(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output,  "All siblings are born more than 8 months or less than 2 days apart\n")
        # put things back
        individuals, families = parse("../testfiles/US13_test.ged")
        self.individuals = individuals
        self.families = families

if __name__ == '__main__':
    unittest.main()
