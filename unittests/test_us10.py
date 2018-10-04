import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS10(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US10_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_all_individuals_married_after_14(self):
        # remove the duplicate individuals and families
        result, output = Checks.marriage_after_14(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All individuals were married above the age of 14.\n")
        # put things back

    def test_one_wife_married_under_14(self):
        self.individuals[2].birthday = "11 SEP 1961"
        result, output = Checks.marriage_after_14(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0].ID) + " is not a valid wedding. " + str(self.individuals[2].ID) + " was not above the age of 14.\n")
        self.individuals[2].birthday = "11 SEP 1951"


    def test_one_husband_married_under_14(self):
        # edit things
        self.individuals[1].birthday = "13 DEC 1961"
        result, output = Checks.marriage_after_14(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0].ID) + " is not a valid wedding. " + str(self.individuals[1].ID) + " was not above the age of 14.\n")
        # put them back
        self.individuals[1].birthday = "13 DEC 1951"

    def test_one_couple_married_under_14(self):
        # edit things
        self.families[0].married = "1 JUN 1962"
        result, output = Checks.marriage_after_14(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0].ID) + " is not a valid wedding. " + str(self.individuals[1].ID) + " was not above the age of 14.\n" +
            "Error: " + str(self.families[0].ID) + " is not a valid wedding. " + str(self.individuals[2].ID) + " was not above the age of 14.\n")
        # put things back
        self.families[0].married = "1 JUN 1975"

    def test_widowed_marriage_under_14(self):
        # edit things
        self.individuals[1].birthday = "13 DEC 1961"
        self.individuals[1].death = "1 JUL 1962"
        result, output = Checks.marriage_after_14(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0].ID) + " is not a valid wedding. " + str(self.individuals[1].ID) + " was not above the age of 14.\n")
        # put things back
        self.individuals[1].birthday = "13 DEC 1951"
        self.individuals[1].death = "None"


if __name__ == '__main__':
    unittest.main()
