import unittest
# this stuff is necessary because of how annoying it is to use relative imports. Instead
# of setting all that up just include the path to the src directory here then
# import things like normal
import sys
sys.path.append("../src")

from Family import Family
from Individual import Individual
from Parser import parse


class TestUS42(unittest.TestCase):
    # make sure to name the class Test<US#>

    # setup gets run before tests, so I use it to parse my test file and get the
    # data structures I need
    def setUp(self):
        self.indi = None


    def test_illegitimate_date_none(self):
        data = ['0 @I1@ INDI', '1 NAME Me /P/', '2 GIVN Me', '2 SURN P', '2 _MARNM P', '1 SEX M', '1 BIRT', '2 DATE 31 MAR 1997', '1 FAMC @F1@']
        self.indi = Individual(data)


    def test_illegitimate_date_birt(self):
        data = ['0 @I1@ INDI', '1 NAME Me /P/', '2 GIVN Me', '2 SURN P', '2 _MARNM P', '1 SEX M', '1 BIRT', '2 DATE 32 MAR 1997', '1 FAMC @F1@']
        with self.assertRaises(ValueError):
            self.indi = Individual(data)

    def test_illegitimate_date_death(self):
        data = ['0 @I4@ INDI', '1 NAME Grandpa /P/', '2 GIVN Grandpa', '2 SURN P', '2 _MARNM P', '1 SEX M', '1 BIRT', '2 DATE 1 APR 1910', '1 DEAT Y', '2 DATE 30 FEB 2000', '1 FAMS @F2@']
        with self.assertRaises(ValueError):
            self.indi = Individual(data)

    def test_illegitimate_date_marr(self):
        data = ['0 @<US04>F1@ FAM', '1 HUSB @<US04>I2@', '1 WIFE @<US04>I3@', '1 CHIL @<US04>I1@', '1 CHIL @<US04>I4@', '1 CHIL @<US04>I5@', '1 CHIL @<US04>I6@', '1 MARR', '2 DATE 31 APR 1960', '1 DIV', '2 DATE 3 MAR 1967', '1 _CURRENT Y']
        with self.assertRaises(ValueError):
            self.indi = Family(data)


    def test_illegitimate_date_div(self):
        data = ['0 @<US04>F1@ FAM', '1 HUSB @<US04>I2@', '1 WIFE @<US04>I3@', '1 CHIL @<US04>I1@', '1 CHIL @<US04>I4@', '1 CHIL @<US04>I5@', '1 CHIL @<US04>I6@', '1 MARR', '2 DATE 30 APR 1960', '1 DIV', '2 DATE 31 NOC 1967', '1 _CURRENT Y']
        with self.assertRaises(ValueError):
            self.indi = Family(data)
    
    def test_illegitimate_date_parse(self):
        with self.assertRaises(ValueError):
            individuals, families = parse("../testfiles/US42_test.ged")

if __name__ == '__main__':
    unittest.main()