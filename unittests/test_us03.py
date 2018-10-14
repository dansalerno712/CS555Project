import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS03(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US03_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_birth_before_death(self):
        result, output = Checks.birth_before_death(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(self.individuals[9]) + " has a death date before their birthday.\n")
    
        

    def test_all_correct(self):
        self.individuals[9].birthday = "7 JUL 1980"
        self.individuals[9].death = "3 JUN 2006"
        result, output = Checks.birth_before_death(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All individuals have death dates after birthdays.\n")

if __name__ == '__main__':
    unittest.main()
