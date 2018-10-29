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


class TestUS38(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US38_test.ged")
        self.individuals = individuals

    def test_one_upcoming_birthday(self):
        # set birthday to 10 days in the future
        today = datetime.datetime.now()
        upcoming_birthday = datetime.datetime(
            2000, today.month, today.day) + datetime.timedelta(days=10)
        self.individuals[0].birthday = upcoming_birthday.strftime("%d %b %Y")
        flag, output = Checks.list_upcoming_birthdays(self.individuals)
        self.assertEqual(flag, False)
        self.assertEqual(output, str(
            self.individuals[0]) + " has a birthday in the next 30 days\n")
        # put stuff back
        self.individuals[0].birthday = "25 NOV 2000"

    def test_no_upcoming_birthdays(self):
        # set the birthday to 10 days in the past
        today = datetime.datetime.now()
        non_upcoming_birthday = datetime.datetime(
            2000, today.month, today.day) - datetime.timedelta(days=10)
        self.individuals[0].birthday = non_upcoming_birthday.strftime(
            "%d %b %Y")
        flag, output = Checks.list_upcoming_birthdays(self.individuals)
        self.assertEqual(flag, True)
        self.assertEqual(
            output, "No individuals have birthdays in the next 30 days\n")
        # put back
        self.individuals[0].birthday = "25 NOV 2000"

    def test_empty_input(self):
        flag, output = Checks.list_upcoming_birthdays([])
        self.assertEqual(flag, True)
        self.assertEqual(
            output, "No individuals have birthdays in the next 30 days\n")


if __name__ == '__main__':
    unittest.main()
