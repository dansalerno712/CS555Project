import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS04(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        _, families = parse("../testfiles/US04_test.ged")
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_families_all_good(self):
        # remove the duplicate individuals and families
        self.families[1].divorced = "31 DEC 1980"
        result, output = Checks.marriage_before_divorce(self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All families are married before they are divorced\n")
        # put things back
        self.families[1].ID = "31 DEC 1979"

    def test_family_2_bad(self):
        result, output = Checks.marriage_before_divorce(self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[1]) + " has a divorce before a marriage\n")

    def test_family_1_bad(self):
        self.families[0].divorced = "3 MAR 1959"
        self.families[1].divorced = "31 DEC 1980"
        result, output = Checks.marriage_before_divorce(self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0]) + " has a divorce before a marriage\n")

    def test_families_all_bad(self):
        self.families[0].divorced = "3 MAR 1959"
        result, output = Checks.marriage_before_divorce(self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(self.families[0]) + " has a divorce before a marriage\n" + "Error: " + str(
            self.families[1]) + " has a divorce before a marriage\n")

    def test_empty_families(self):
        result, output = Checks.marriage_before_divorce([])
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All families are married before they are divorced\n")


if __name__ == '__main__':
    unittest.main()
