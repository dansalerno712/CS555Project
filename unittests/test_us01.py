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
        individuals, families = parse("../testfiles/US01_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_all_dates_before_current(self):
        # remove the duplicate individuals and families
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[6].death = "17 JAN 2015"
        self.families[1].married = "1 JAN 1960"
        self.families[0].divorced = "31 DEC 1979"
        result, output = Checks.dates_before_current_date(
            self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All dates are after current date.")
        # put things back
        self.individuals[0].birthday = "29 SEP 2022"
        self.individuals[6].death = "17 JAN 3131"
        self.families[1].married = "1 JAN 3000"
        self.families[0].divorced = "3 MAR 2222"

    def test_marriage_after_current(self):
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[6].death = "17 JAN 2015"
        self.families[0].divorced = "31 DEC 1979"
        result, output = Checks.dates_before_current_date(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[1]) + " has a marriage after current date.\n")
        self.families[0].divorced = "3 MAR 2222"
        self.individuals[0].birthday = "29 SEP 2022"
        self.individuals[6].death = "17 JAN 3131"

    def test_divorce_after_current(self):
        # edit things
        self.individuals[0].birthday = "29 SEP 1996"
        self.individuals[6].death = "17 JAN 2015"
        self.families[1].married = "1 JAN 1960"
        result, output = Checks.dates_before_current_date(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.families[0]) + " has a divorce after current date.\n")
        # put them back
        self.individuals[0].birthday = "29 SEP 2022"
        self.individuals[6].death = "17 JAN 3131"
        self.families[1].married = "1 JAN 3000"

    def test_death_after_current(self):
        # edit things
        self.individuals[0].birthday = "29 SEP 1996"
        self.families[1].married = "1 JAN 1960"
        self.families[0].divorced = "31 DEC 1979"
        result, output = Checks.dates_before_current_date(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[6]) + " has a death after current date.\n")
        # put things back
        self.individuals[0].birthday = "29 SEP 2022"
        self.families[1].married = "1 JAN 3000"
        self.families[0].divorced = "3 MAR 2222"

    def test_birth_after_current(self):
        # edit things
        self.individuals[6].death = "17 JAN 2015"
        self.families[1].married = "1 JAN 1960"
        self.families[0].divorced = "31 DEC 1979"
        result, output = Checks.dates_before_current_date(
            self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[0]) + " has a birth after current date.\n")
        # put things back
        self.individuals[6].death = "17 JAN 3131"
        self.families[1].married = "1 JAN 3000"
        self.families[0].divorced = "3 MAR 2222"


if __name__ == '__main__':
    unittest.main()
