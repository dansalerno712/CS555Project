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


class TestUS35(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US35_test.ged")
        self.individuals = individuals

    def test_no_recent_births(self):
        self.individuals[1].birthday = "15 OCT 2008"
        flag, output = Checks.list_recent_births(self.individuals)
        self.assertEqual(flag, True)
        self.assertEqual(output, "No individuals born in the last 30 days\n")
        self.individuals[1].birthday = "15 OCT 2018"

    def test_one_recent_birth(self):
        # set the birthday to today
        self.individuals[1].birthday = datetime.datetime.now().strftime("%d %b %Y")
        flag, output = Checks.list_recent_births(self.individuals)
        self.assertEqual(flag, False)
        self.assertEqual(output, str(self.individuals[1]) + " was born within the last 30 days\n")
        self.individuals[1].birthday = "15 OCT 2018"

    def test_empty_input(self):
        flag, output = Checks.list_recent_births([])
        self.assertEqual(flag, True)
        self.assertEqual(output, "No individuals born in the last 30 days\n")
        individuals, families = parse("../testfiles/US35_test.ged")
        self.individuals = individuals


if __name__ == '__main__':
    unittest.main()
