import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS11(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US11_test.ged")
        self.individuals = individuals
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_no_bigamy_no_div_or_death(self):
        result, output = Checks.no_bigamy(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(output, "Error: " + str(
            self.individuals[1]) + " is/was married to multiple people at the same time\n")

    def test_no_bigamy_after_div(self):
        self.families[0].divorced = '1 MAR 1980'
        result, output = Checks.no_bigamy(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No one is practicing polygamy\n")
        self.families[0].divorced = None

    def test_no_bigamy_after_death(self):
        # set up scenario
        self.individuals[0].death = '1 MAR 1980'
        self.individuals[0].alive = False
        result, output = Checks.no_bigamy(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No one is practicing polygamy\n")
        # put things back
        self.individuals[0].death = None
        self.individuals[0].alive = True

    def test_no_bigamy_marr_b4_death(self):
        # set up scenario
        x = self.individuals[7].death
        self.individuals[7].death = None
        self.individuals[7].alive = True
        result, output = Checks.no_bigamy(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[1]) + " is/was married to multiple people at the same time\n" +
            "Error: " + str(self.individuals[6]) + " is/was married to multiple people at the same time\n")
        # put things back
        self.individuals[7].death = x
        self.individuals[7].alive = False

    def test_no_bigamy_marr_b4_div(self):
        # set up scenario
        x = self.families[3].divorced
        self.families[3].divorced = '13 JUN 2003'
        result, output = Checks.no_bigamy(self.individuals, self.families)
        self.assertEqual(result, False)
        self.assertEqual(
            output, "Error: " + str(self.individuals[1]) + " is/was married to multiple people at the same time\n" +
            "Error: " + str(self.individuals[2]) + " is/was married to multiple people at the same time\n")
        # put things back
        self.families[3].divorced = x

    def test_no_bigamy_empty_inputs(self):
        # set up scenario
        self.families = []
        self.individuals = []
        result, output = Checks.no_bigamy(self.individuals, self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "No one is practicing polygamy\n")
        # put things back
        individuals, families = parse("../testfiles/US11_test.ged")
        self.individuals = individuals
        self.families = families


if __name__ == '__main__':
    unittest.main()
