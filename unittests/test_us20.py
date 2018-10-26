import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks
import Utils


class TestUS20(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US20_test.ged")
        self.individuals = individuals
        self.families = families

    def test_aunts_and_uncles_UNC(self):
        flag, output = Checks.aunts_and_uncles(self.individuals, self.families)
        self.assertEqual(flag, False)
        self.assertEqual(output, "Error: " + str(self.individuals[5]) + " is married to their niece or nephew.\n")

    def test_aunts_and_uncles_not(self):
        x = self.individuals[5]
        y = self.individuals[6]
        self.individuals[5].spouse = []
        self.individuals[6].spouse = []
        z = self.families.pop(2)
        flag, output = Checks.aunts_and_uncles(self.individuals, self.families)
        self.assertEqual(flag, True)
        self.assertEqual(output, "No aunts or uncles are married to nieces or nephews.\n")
        self.individuals[6] = y
        self.individuals[5] = x
        self.families.append(z)

    def test_aunts_and_uncles_empty_input(self):
        flag, output = Checks.aunts_and_uncles([],[])
        self.assertEqual(flag, True)
        self.assertEqual(output, "No aunts or uncles are married to nieces or nephews.\n")
        individuals, families = parse("../testfiles/US20_test.ged")
        self.individuals = individuals
        self.families = families
    

if __name__ == '__main__':
    unittest.main()
