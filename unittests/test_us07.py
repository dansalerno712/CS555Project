import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks
import Utils


class TestUS07(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US07_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_all_individuals_under_150(self):
        # remove the duplicate individuals and families
        result, output = Checks.age_less_than_150(self.individuals)
        self.assertEqual(result, True)
        self.assertEqual(output, "All individuals are less than 150 years old.\n")
        # put things back

    def test_one_individual_over_150(self):
        self.individuals[0].birthday = "17 JAN 1866"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)
        result, output = Checks.age_less_than_150(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0].ID) + " is more than 150 years old.\n")
        self.individuals[0].birth = "29 SEP 1996"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)


    def test_multiple_individuals_over_150(self):
        # edit things
        self.individuals[0].birthday = "1 JAN 1866"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)
        self.individuals[1].birthday = "1 JAN 1866"
        self.individuals[1].age = Utils.calculate_age(self.individuals[1].birthday)
        self.individuals[2].birthday = "1 JAN 1866"
        self.individuals[2].age = Utils.calculate_age(self.individuals[2].birthday)
        self.individuals[3].birthday = "1 JAN 1866"
        self.individuals[3].age = Utils.calculate_age(self.individuals[3].birthday)
        self.individuals[4].birthday = "1 JAN 1866"
        self.individuals[4].age = Utils.calculate_age(self.individuals[4].birthday)
        self.individuals[5].birthday = "1 JAN 1866"
        self.individuals[5].age = Utils.calculate_age(self.individuals[5].birthday)
        result, output = Checks.age_less_than_150(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0].ID) + " is more than 150 years old.\n" +
            "Error: " + str(self.individuals[1].ID) + " is more than 150 years old.\n" +
            "Error: " + str(self.individuals[2].ID) + " is more than 150 years old.\n" +
            "Error: " + str(self.individuals[3].ID) + " is more than 150 years old.\n" +
            "Error: " + str(self.individuals[4].ID) + " is more than 150 years old.\n" +
            "Error: " + str(self.individuals[5].ID) + " is more than 150 years old.\n")
        # put them back
        individuals, families = parse("../testfiles/US07_test.ged")
        self.individuals = individuals

    def test_individual_over_150_and_death(self):
        # edit things
        self.individuals[0].birthday = "1 JAN 1866"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)
        self.individuals[0].death = "1 OCT 2018"
        result, output = Checks.age_less_than_150(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0].ID) + " is more than 150 years old.\n")
        # put things back
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)
        self.individuals[0].death = "None"

    def test_individual_under_150_and_death(self):
        # edit things
        self.individuals[0].death = "31 OCT 1996"
        result, output = Checks.age_less_than_150(self.individuals)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All individuals are less than 150 years old.\n")
        # put things back
        self.individuals[1].death = "None"

    def test_individual_exactly_150(self):
        # edit things
        self.individuals[0].birthday= "1 JAN 1866"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)
        result, output = Checks.age_less_than_150(self.individuals)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0].ID) + " is more than 150 years old.\n")
        # put things back
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[0].age = Utils.calculate_age(self.individuals[0].birthday)

if __name__ == '__main__':
    unittest.main()
