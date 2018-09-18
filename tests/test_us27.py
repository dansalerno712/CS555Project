import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
from Utils import calculate_age


class TestUS27(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse(
            "../testfiles/Dan_Salerno_Project_01.ged")

        self.individuals = individuals
        self.families = families
        # since this is time dependent I'm hard coding my age here to compare to
        self.dans_age = 22

    # all tests need to be names test_<name_of_function>
    def test_age_calculation(self):
        self.assertEqual(calculate_age("12 JUL 1996"), self.dans_age)

    def test_age_print(self):
        # the age field should be set correctly in the printout of an individual
        self.assertIn("Age: " + str(self.dans_age), str(self.individuals[0]))


if __name__ == '__main__':
    unittest.main()
