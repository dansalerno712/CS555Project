import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS22(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US22_test.ged")

        self.individuals = individuals
        self.families = families

    # all tests need to be names test_<name_of_function>
    def test_unique_IDs_all_good(self):
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All IDs are unique")

    def test_unique_IDs_bad_individuals(self):
        # make a duplicate individual ID
        self.individuals[0].ID = "@I2@"
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: Dan /Salerno/ (ID: @I2@) has a non-unique ID\n")
        # put it back
        self.individuals[0].ID = "@I1@"


if __name__ == '__main__':
    unittest.main()
