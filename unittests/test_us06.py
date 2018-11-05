import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS06(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US06_test.ged")
        self.families = families
        self.individuals = individuals

    # all tests need to be named test_<name_of_function>
    def test_marriages_good(self):
        # remove the duplicate individuals and families
        self.individuals[6].death = "17 JAN 2003"
        result, output = Checks.divorce_before_death(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All individuals were divorced before death.\n")
        # put things back
        self.individuals[6].death = "17 JAN 1989"

    def test_marriages_bad(self):
        result, output = Checks.divorce_before_death(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + self.individuals[6].ID + " was divorced in family " + self.families[1].ID + " after death.\n")

    def test_empty_families(self):
        result, output = Checks.divorce_before_death(self.individuals, [])
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All individuals were divorced before death.\n")


if __name__ == '__main__':
    unittest.main()
