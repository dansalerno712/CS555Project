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


class TestUS12(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US12_test.ged")
        self.individuals = individuals
        self.families = families

    def test_parents_are_not_too_old(self):
        # set birthday to 10 days in the future
        flag, output = Checks.parents_too_old(self.individuals, self.families)
        self.assertEqual(flag, True)
        self.assertEqual(output, "No parents are too old for their children.\n")

    def test_mom_too_old(self):
        # set the birthday to 10 days in the past
        self.individuals[1].birthday = "25 NOV 1776"
        flag, output = Checks.parents_too_old(self.individuals, self.families)
        self.assertEqual(flag, False)
        self.assertEqual(
            output, "Error: Mother " + str(self.families[0].wife_ID) + " is too old for child " + str(self.individuals[0].ID) + "\n")
        # put back
        self.individuals[1].birthday = "1 JUN 1960"


if __name__ == '__main__':
    unittest.main()
