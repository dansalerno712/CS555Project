import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS34(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US34_test.ged")
        self.individuals = individuals
        self.families = families


    def test_list_large_age_difference_not_twice(self):
        # edit things
        x = self.individuals[3].birthday
        self.individuals[3].birthday = "1 Apr 1911"
        result, output = Checks.list_large_age_difference(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No couples where the older spouse was twice as old as the younger spouse at the time of marriage\n")
        self.individuals[3].birthday = x

    def test_list_large_age_difference_husb_twice(self):
        # edit things
        result, output = Checks.list_large_age_difference(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[3]) + " and "+str(self.individuals[4])+"\n")

    def test_list_large_age_difference_wife_twice(self):
        # edit things
        x = self.individuals[3].birthday
        self.individuals[3].birthday = self.individuals[4].birthday 
        self.individuals[4].birthday  = x
        result, output = Checks.list_large_age_difference(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[4]) + " and "+str(self.individuals[3])+"\n")
        self.individuals[4].birthday = self.individuals[3].birthday 
        self.individuals[3].birthday = x

    def test_list_large_age_difference_mutli(self):
        x = self.families[0].married
        self.families[0].married = "1 May 1990"
        result, output = Checks.list_large_age_difference(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[1]) + " and "+str(self.individuals[2])+"\n"+ \
             str(self.individuals[3]) + " and "+str(self.individuals[4])+"\n")
        self.families[0].married = x
        

    def test_list_large_age_difference_empty_inputs(self):
        # edit things
        self.families = []
        self.individuals = []
        result, output = Checks.list_large_age_difference(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No couples where the older spouse was twice as old as the younger spouse at the time of marriage\n")
        # put things back
        individuals, families = parse("../testfiles/US34_test.ged")
        self.individuals = individuals
        self.families = families


if __name__ == '__main__':
    unittest.main()
