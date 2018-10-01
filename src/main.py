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
        print(indi)

    print("=============Families==============")
    for fam in families:
        print(fam)

    print("==============Error/Anomaly Checks============")
    print("User Story 27: Print Age")
    if len(individuals) > 0:
        print(individuals[0])
    print()

    print("User Story 22: Unique IDs")
    result, output = Checks.unique_IDs(individuals, families)
    print(output)

    print("User Story 04: Marriage Before Divorce")
    result, output = Checks.marriage_before_divorce(families)
    print(output)

    print("User Story 01: Dates Before Current Date")
    result, output = Checks.dates_before_current_date(individuals, families)
    print(output)

    print("User Story 09: Birth Before the Death of Parents")
    result, output = Checks.birth_before_parents_death(individuals, families)
    print(output)

    print("User Story 25: Unique First Names in Families")
    result, output = Checks.unique_first_names(individuals, families)
    print(output)

    print("User Story 11: No bigamy")
    result, output = Checks.no_bigamy(individuals, families)
    print(output)

    print("User Story 13: Sibling spacings")
    result, output = Checks.sibling_spacings(individuals, families)
    print(output)

    print("User Story 15: Fewer than 15 sibilings")
    result, output = Checks.fewer_than_15_sibilings(families)
    print(output)

    print("User Story 29: List deceased")
    output = Checks.list_deceased(individuals)
    print(output)


if __name__ == '__main__':
    main()
