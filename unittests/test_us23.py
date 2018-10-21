import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks

class TestUS23(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse(
            "../testfiles/US23_test.ged")
        self.individuals = individuals
        self.families = families
        self.name = "Dan /Salerno/"
        self.birthdate = "12 JUL 1996"

    # all tests need to be named test_<name_of_function>
    def test_all_unique(self):
        self.individuals[0].name = "Dan1 /Salerno"
        self.individuals[0].birthday = "13 JUN 1995"
        result, output = Checks.unique_name_birth(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All unique names and birth dates.\n")
        self.individuals[0].name = self.name
        self.individuals[0].birthday = self.birthdate
    

    def test_not_unique(self):
        result, output = Checks.unique_name_birth(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, self.individuals[0].ID + " " + self.individuals[1].ID + " have the same name and birth date.\n")
    
    def test_not_unique_names(self):
        self.individuals[0].birthday = "13 JUN 1995"
        result, output = Checks.unique_name_birth(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All unique names and birth dates.\n")
        self.individuals[0].birthday = self.birthdate
    
    def test_not_unique_birthdates(self):
        self.individuals[0].name = "Dan1 /Salerno"
        result, output = Checks.unique_name_birth(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All unique names and birth dates.\n")
        self.individuals[0].name = self.name
    
    def test_empty_input(self):
        result, output = Checks.unique_name_birth([], [])
        self.assertEqual(result, True)
        self.assertEqual(output, "All unique names and birth dates.\n")


if __name__ == '__main__':
    unittest.main()
