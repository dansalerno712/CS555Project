import sys
from Parser import parse
import Checks


def main():
    ''' Parses the GEDCOM file from the input and stores the Individuals and Families'''
    # check for correct inputs
    if len(sys.argv) != 2:
        print("Usage: python parser.py <file_path>")
        return

    path = sys.argv[1]

    individuals, families = parse(path)

    # for project 3, print individuals and families in order
    individuals.sort(key=lambda x: x.ID)
    families.sort(key=lambda x: x.ID)

    print("=============Individuals==============")
    for indi in individuals:
        print("ID: " + indi.ID + "\tName: " + indi.name)

    print("=============Families==============")
    for fam in families:
        print("ID: " + fam.ID + "\tHusband Name: " +
              fam.husband_name + "\tWife Name: " + fam.wife_name)

    print("==============Error/Anomaly Checks============")
    print("User Story 22: Unique IDs")
    result, output = Checks.unique_IDs(individuals, families)
    print(output)
    print("User Story 04: Marriage Before Divorce")
    result, output = Checks.marriage_before_divorce(families)
    print(output)
    print("User Story 01: Dates Before Current Date")
    result, output = Checks.dates_before_current_date(individuals, families)
    print(output)


if __name__ == '__main__':
    main()
