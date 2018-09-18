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

    # all tests need to be named test_<name_of_function>
    def test_unique_IDs_all_good(self):
        # remove the duplicate individuals and families
        self.individuals[0].ID = "@I1@"
        self.families[1].ID = "@F2@"
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All IDs are unique")
        # put things back
        self.individuals[0].ID = "@I2@"
        self.families[1].ID = "@F3@"

    def test_unique_IDs_bad_individuals_and_families(self):
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0]) + " has a non-unique ID\n" +
            "Error: " + str(self.individuals[1]) + " has a non-unique ID\n" +
            "Error: " + str(self.families[1]) + " has a non-unique ID\n" +
            "Error: " + str(self.families[2]) + " has a non-unique ID\n")

    def test_unique_IDs_bad_individuals(self):
        # edit things
        self.families[1].ID = "@F2@"
        self.individuals[2].ID = "@I2@"
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0]) + " has a non-unique ID\n" +
            "Error: " + str(self.individuals[1]) + " has a non-unique ID\n" +
            "Error: " + str(self.individuals[2]) + " has a non-unique ID\n")
        # put them back
        self.families[1].ID = "@F3@"
        self.individuals[2].ID = "@I3@"

    def test_unique_IDs_bad_families(self):
        # edit things
        self.families[0].ID = "@F3@"
        self.individuals[0].ID = "@I1@"
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0]) + " has a non-unique ID\n" +
            "Error: " + str(self.families[1]) + " has a non-unique ID\n" +
            "Error: " + str(self.families[2]) + " has a non-unique ID\n")
        # put things back
        self.families[0].ID = "@F1@"
        self.individuals[0].ID = "@I2@"

    def test_unique_IDs_empty_inputs(self):
        # edit things
        self.families = []
        self.individuals = []
        result, output = Checks.unique_IDs(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All IDs are unique")
        # put things back
        individuals, families = parse("../testfiles/US22_test.ged")
        self.individuals = individuals
        self.families = families


if __name__ == '__main__':
    unittest.main()
