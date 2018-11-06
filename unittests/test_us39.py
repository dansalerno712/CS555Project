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

class TestUS39(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US39_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_no_upcoming_anniversaries(self):
        # remove the duplicate individuals and families
        result, output = Checks.list_upcoming_anniversaries(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No living couples have anniversaries in the next 30 days.\n")


    def test_one_upcoming_anniversary(self):
        today = datetime.datetime.now()
        upcoming_anniversary = datetime.datetime(
            2018, today.month, today.day) + datetime.timedelta(days=10)
        self.families[0].married = upcoming_anniversary.strftime("%d %b %Y")
        self.families[0].divorced = "None"
        result, output = Checks.list_upcoming_anniversaries(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Note: " + str(self.families[0].ID) + " has an upcoming anniversary on " + str(self.families[0].married) +"\n")
        # put things back
        self.families[0].married = "1 JAN 1960"
        self.families[0].divorced = "3 MAR 1967"

    def test_one_upcoming_anniversary_different_year(self):
        today = datetime.datetime.now()
        upcoming_anniversary = datetime.datetime(
            2000, today.month, today.day) + datetime.timedelta(days=10)
        self.families[0].married = upcoming_anniversary.strftime("%d %b %Y")
        self.families[0].divorced = "None"
        result, output = Checks.list_upcoming_anniversaries(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Note: " + str(self.families[0].ID) + " has an upcoming anniversary on " + str(self.families[0].married) +"\n")
        # put things back
        self.families[0].married = "1 JAN 1960"
        self.families[0].divorced = "3 MAR 1967"

    def test_empty_input(self):
        flag, output = Checks.list_upcoming_anniversaries([], [])
        self.assertEqual(flag, True)
        self.assertEqual(output, "No living couples have anniversaries in the next 30 days.\n")
        individuals, families = parse("../testfiles/US39_test.ged")
        self.families = families


if __name__ == '__main__':
    unittest.main()
