import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks

class TestUS29(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse(
            "../testfiles/US29_test.ged")
        self.individuals = individuals

    # all tests need to be named test_<name_of_function>
    def test_deaths(self):
        result, output = Checks.list_deceased(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(output, str(self.individuals[0]) + "\n" + str(self.individuals[1]) + "\n")

    def test_alive(self):
        self.individuals[0].death = None
        self.individuals[1].death = None
        result, output = Checks.list_deceased(self.individuals)
        self.assertEqual(result, True)
        self.assertEqual(output, "No deceased individuals\n")
        individuals, families = parse(
            "../testfiles/US29_test.ged")
        self.individuals = individuals

    def test_empty_input(self):
        result, output = Checks.list_deceased([])
        self.assertEqual(result, True)
        self.assertEqual(output, "No deceased individuals\n")


if __name__ == '__main__':
    unittest.main()
