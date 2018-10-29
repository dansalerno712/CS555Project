import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS21(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US21_test.ged")
        self.individuals = individuals
        self.families = families

    def test_bad_role_wife(self):
        flag, output = Checks.correct_gender_for_role(
            self.individuals, self.families)
        self.assertEqual(flag, False)
        self.assertEqual(output, str(
            self.individuals[1]) + " is a wife but not a female\n")

    def test_bad_role_husband(self):
        self.individuals[0].gender = "F"
        self.individuals[1].gender = "F"
        flag, output = Checks.correct_gender_for_role(self.individuals, self.families)
        self.assertEqual(flag, False)
        self.assertEqual(output, str(self.individuals[0]) + " is a husband but not a male\n")
        # put back
        self.individuals[0].gender = "M"
        self.individuals[1].gender = "M"

    def test_both_bad_roles(self):
        self.individuals[0].gender = "F"
        flag, output = Checks.correct_gender_for_role(self.individuals, self.families)
        self.assertEqual(flag, False)
        self.assertEqual(output, str(self.individuals[0]) + " is a husband but not a male\n" + str(
            self.individuals[1]) + " is a wife but not a female\n")
        # put back
        self.individuals[0].gender = "M"

    def test_all_good_roles(self):
        self.individuals[1].gender = "F"
        flag, output = Checks.correct_gender_for_role(self.individuals, self.families)
        self.assertEqual(flag, True)
        self.assertEqual(
            output, "All families have the correct gender for their roles\n")
        self.individuals[1].gender = "M"

    def test_empty_input(self):
        flag, output = Checks.correct_gender_for_role([], [])
        self.assertEqual(flag, True)
        self.assertEqual(
            output, "All families have the correct gender for their roles\n")


if __name__ == '__main__':
    unittest.main()
