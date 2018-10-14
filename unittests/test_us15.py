import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Parser import parse
import Checks


class TestUS15(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        individuals, families = parse("../testfiles/US15_test.ged")
        self.families = families

    # all tests need to be named test_<name_of_function>
    def test_family_with_too_many_siblings(self):
        result, output = Checks.fewer_than_15_sibilings(self.families)
        self.assertEqual(result, False)
        self.assertEqual(output,
                         "Error: family {ID: @<US15>F1@| Married: 1 JUN 1975| Divorced: None| Husband ID: @<US15>I16@| Husband Name: Michael /Salerno/| Wife ID: @<US15>I17@| Wife Name: Gail /Salerno/| Children: ['@<US15>I1@', '@<US15>I2@', '@<US15>I3@', '@<US15>I4@', '@<US15>I5@', '@<US15>I6@', '@<US15>I7@', '@<US15>I8@', '@<US15>I9@', '@<US15>I10@', '@<US15>I11@', '@<US15>I12@', '@<US15>I13@', '@<US15>I14@', '@<US15>I15@']} has 15 or more siblings\n")

    def test_good_family(self):
        # make family good size
        self.families[0].children = self.families[0].children[:10]
        result, output = Checks.fewer_than_15_siblings(self.families)
        self.assertEqual(result, True)
        self.assertEqual(output, "All families have less than 15 siblings\n")
        # put it back
        individuals, families = parse("../testfiles/US15_test.ged")
        self.families = families

    def test_empty_input(self):
        result, output = Checks.fewer_than_15_siblings([])
        self.assertEqual(result, True)
        self.assertEqual(output, "All families have less than 15 siblings\n")


if __name__ == '__main__':
    unittest.main()
