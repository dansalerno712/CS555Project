import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks
import Utils


class TestUS18(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US18_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_all_individuals_dont_marry_siblings(self):
        self.families[2].wife_ID = "@<US18>I12@"
        # remove the duplicate individuals and families
        result, output = Checks.siblings_should_not_marry(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No siblings are married\n")
        # put things back
        self.families[2].wife_ID = "@<US18>I4@"

    def test_one_married_couple_is_siblings(self):
        result, output = Checks.siblings_should_not_marry(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[2].husband_ID) + " and " + str(self.families[2].wife_ID) + " are siblings and should not marry.\n")

    def test_empty_input(self):
        flag, output = Checks.siblings_should_not_marry([],[])
        self.assertEqual(flag, True)
        self.assertEqual(output, "No siblings are married\n")
        individuals, families = parse("../testfiles/US18_test.ged")
        self.individuals = individuals
        self.families = families
    

if __name__ == '__main__':
    unittest.main()
