import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks

class TestUS30(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse(
            "../testfiles/US30_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_alive_marriage(self):
        self.individuals[0].death = None
        self.individuals[1].death = None
        self.individuals[0].alive = True
        self.individuals[1].alive = True
        result, output = Checks.list_living_married(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Husband: " + str(self.individuals[0].ID) + ", Wife: " + str(self.individuals[1].ID) + "\n")

    def test_dead_marriage(self):
        self.individuals[0].death = "01 JAN 2015"
        self.individuals[1].death = "01 JAN 2015"
        self.individuals[0].alive = False
        self.individuals[1].alive = False
        result, output = Checks.list_living_married(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No living married couples.\n")

    def test_empty_input(self):
        result, output = Checks.list_living_married([],[])
        self.assertEqual(result, True)
        self.assertEqual(output, "No living married couples.\n")


if __name__ == '__main__':
    unittest.main()
