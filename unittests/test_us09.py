import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS09(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US09_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_child_born_before_both_parents_death(self):
        # remove the duplicate individuals and families
        result, output = Checks.birth_before_parents_death(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All children are born before the death of the mother or within nine months of the death of the father.")
        # put things back

    def test_child_born_after_mom_death(self):
        self.individuals[2].death = "17 JAN 1996"
        result, output = Checks.birth_before_parents_death(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0]) + " has a child " + str(self.individuals[0].ID) + " born after the mother's death.\n")
        self.individuals[2].death = "None"

    def test_child_born_after_dad_death(self):
        # edit things
        self.individuals[1].death = "1 MAR 1995"
        result, output = Checks.birth_before_parents_death(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0]) + " has a child " + str(self.individuals[0].ID) + " born more than 9 months after the father's death.\n")
        # put them back
        self.individuals[1].death = "None"

    def test_children_born_after_both_parents_death(self):
        # edit things
        self.individuals[1].death = "1 MAR 1995"
        self.individuals[2].death = "1 MAR 1995"
        result, output = Checks.birth_before_parents_death(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0]) + " has a child " + str(self.individuals[0].ID) + " born after the mother's death.\n" + "Error: " + str(self.families[0]) + " has a child " + str(self.individuals[0].ID) + " born more than 9 months after the father's death.\n")
        # put things back
        self.individuals[1].death = "None"
        self.individuals[2].death = "None"

    def test_child_born_within_9m_dad_death(self):
        # edit things
        self.individuals[1].death = "1 SEP 1996"
        result, output = Checks.birth_before_parents_death(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(
            output, "All children are born before the death of the mother or within nine months of the death of the father.")
        # put things back
        self.individuals[1].death = "None"


if __name__ == '__main__':
    unittest.main()
