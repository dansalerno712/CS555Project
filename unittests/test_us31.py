import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS31(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US31_test.ged")
        self.individuals = individuals
        self.families = families


    def test_living_single_two(self):
        result, output = Checks.living_single(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[5]) + " is single and over 30.\n" + str(self.individuals[6]) + " is single and over 30.\n")

    def test_living_single_one(self):
        y = self.individuals[6]
        self.individuals[6].age = 30
        result, output = Checks.living_single(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[5]) + " is single and over 30.\n" )
        self.individuals[6] = y
        
    def test_living_single_not(self):
        x = self.individuals[5]
        y = self.individuals[6]
        self.individuals[5].age = 29
        self.individuals[6].age = 30
        flag, output = Checks.living_single(self.individuals)
        self.assertEqual(flag, True)
        self.assertEqual(output, "No one is single and over 30.\n")
        self.individuals[6] = y
        self.individuals[5] = x

    def test_living_single_empty_inputs(self):
        # edit things
        self.individuals = []
        result, output = Checks.living_single(self.individuals)
        self.assertEqual(result, True)
        self.assertEqual(output, "No one is single and over 30.\n")
        # put things back
        individuals, families = parse("../testfiles/US31_test.ged")
        self.individuals = individuals


if __name__ == '__main__':
    unittest.main()
