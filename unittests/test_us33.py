import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS33(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US33_test.ged")
        self.individuals = individuals
        self.families = families

    def test_list_orphans_none(self):
        # edit things
        result, output = Checks.list_orphans(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No orphans found.\n")

    def test_list_orphans_over_18(self):
        # edit things
        self.individuals[1].alive = False
        self.individuals[2].alive = False
        result, output = Checks.list_orphans(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No orphans found.\n")
        self.individuals[1].alive = True
        self.individuals[2].alive = True

    def test_list_orphans_under_18(self):
        # edit things
        self.individuals[1].alive = False
        self.individuals[2].alive = False
        x = self.individuals[0]
        self.individuals[0].age = 17
        result, output = Checks.list_orphans(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[0])+"\n")
        self.individuals[0] = x
        self.individuals[1].alive = True
        self.individuals[2].alive = True
        

    def test_list_orphans_empty_inputs(self):
        # edit things
        self.families = []
        self.individuals = []
        result, output = Checks.list_orphans(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No orphans found.\n")
        # put things back
        individuals, families = parse("../testfiles/US33_test.ged")
        self.individuals = individuals
        self.families = families


if __name__ == '__main__':
    unittest.main()
