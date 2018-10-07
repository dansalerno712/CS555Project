import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS01(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US02_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_birth_before_marriage(self):
        result, output = Checks.birth_before_marriage(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(self.individuals[11]) + " has a marriage before their birth.\n")
    
        

    def test_all_correct(self):
        self.individuals[11].birthday = "4 APR 1980"
        result, output = Checks.birth_before_marriage(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All individuals have a birthday before their marriage date.\n")

if __name__ == '__main__':
    unittest.main()
