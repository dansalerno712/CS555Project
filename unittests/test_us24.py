import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS24(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US24_test.ged")
        self.individuals = individuals
        self.families = families

    def test_unique_family_by_spouses_duplicate(self):
        result, output = Checks.unique_family_by_spouses(self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str((self.families[0].wife_name, self.families[0].husband_name, self.families[0].married)) + " appear in multiple families\n")

    def test_unique_family_by_spouses_dif_husb(self):
        x = self.families[0].husband_name
        self.families[0].husband_name = "NotDad"
        result, output = Checks.unique_family_by_spouses(self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All families have unique wife name, husband name, and marriage date\n")
        self.families[0].husband_name= x

    def test_unique_family_by_spouses_dif_wife(self):
        x = self.families[0].wife_name
        self.families[0].wife_name = "NotMom"
        result, output = Checks.unique_family_by_spouses(self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All families have unique wife name, husband name, and marriage date\n")
        self.families[0].wife_name= x

    def test_unique_family_by_spouses_dif_marr(self):
        x = self.families[0].married
        self.families[0].married = "1 JUN 1989"
        result, output = Checks.unique_family_by_spouses(self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All families have unique wife name, husband name, and marriage date\n")
        self.families[0].married= x

    def test_unique_family_by_spouses_empty_inputs(self):
        # edit things
        self.families = []
        result, output = Checks.unique_family_by_spouses(self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All families have unique wife name, husband name, and marriage date\n")
        # put things back
        individuals, families = parse("../testfiles/US24_test.ged")
        self.families = families


if __name__ == '__main__':
    unittest.main()
