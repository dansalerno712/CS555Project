import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS25(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US25_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_unique_names_all_good(self):
        # remove the duplicate individuals and families
        self.individuals[0].name = "Hanna Cafiero"
        self.individuals[8].name = "Stephen Cafiero"
        self.individuals[0].birthday = "29 SEP 1990"
        self.individuals[8].birthday = "16 APR 1970"
        result, output = Checks.unique_first_names(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All children in the all families do not have the same names and birth dates.")
        # put things back
        self.individuals[0].name = "Jennifer Cafiero"
        self.individuals[8].name = "John Cafiero"
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[8].birthday = "16 APR 1968"

    def test_unique_names_and_birthday_bad(self):
        result, output = Checks.unique_first_names(
            self.individuals, self.families)
        self.assertEqual(result, False)
        c0 = [str(self.individuals[0]), str(self.individuals[3])]
        c1 = [str(self.individuals[1]), str(self.individuals[8])]
        self.assertEqual(
            output, "Error: " + str(self.families[0]) +
            " has children, ".join(c0) +
            ", with the same first name and birthday.\n" +
            "Error: " + str(self.families[1]) +
            " has children, ".join(c1) +
            ", with the same first name and birthday.\n")

    def test_unique_names_good(self):
        # edit things
        self.individuals[0].name = "Hanna Cafiero"
        self.individuals[8].name = "Stephen Cafiero"
        result, output = Checks.unique_first_names(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All children in the all families do not have the same names and birth dates.")
        # put them back
        self.individuals[0].name = "Jennifer Cafiero"
        self.individuals[8].name = "John Cafiero"

    def test_unique_birthdays_bad(self):
        # edit things
        self.individuals[0].birthday = "29 SEP 1990"
        self.individuals[8].birthday = "16 APR 1970"
        result, output = Checks.unique_first_names(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All children in the all families do not have the same names and birth dates.")
        # put things back
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[8].birthday = "16 APR 1968"

    def test_unique_names_empty_inputs(self):
        # edit things
        self.families = []
        self.individuals = []
        result, output = Checks.unique_first_names(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All children in the all families do not have the same names and birth dates.")
        # put things back
        individuals, families = parse("../testfiles/US22_test.ged")
        self.individuals = individuals
        self.families = families


if __name__ == '__main__':
    unittest.main()
