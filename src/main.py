import sys
from Parser import parse
import Checks
from Utils import pretty_print


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

    pretty_print(individuals, families)

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

    print("User Story 07: Less than 150 years old")
    result, output = Checks.age_less_than_150(individuals)
    print(output)

    print("User Story 11: No bigamy")
    result, output = Checks.no_bigamy(individuals, families)
    print(output)

    print("User Story 13: Sibling spacings")
    result, output = Checks.sibling_spacings(individuals, families)
    print(output)

    print("User Story 15: Fewer than 15 siblings")
    result, output = Checks.fewer_than_15_siblings(families)
    print(output)

    print("User Story 29: List deceased")
    result, output = Checks.list_deceased(individuals)
    print(output)

    print("User Story 10: Marriage after 14")
    result, output = Checks.marriage_after_14(individuals, families)
    print(output)

    print("User Story 03: Birth before Death")
    result, output = Checks.birth_before_death(individuals, families)
    print(output)

    print("User Story 02: Birth before Marriage")
    result, output = Checks.birth_before_marriage(individuals, families)
    print(output)

    print("User Story 24: Unique family by spouses")
    result, output = Checks.unique_family_by_spouses(families)
    print(output)

    print("User Story 34: List large age difference")
    result, output = Checks.list_large_age_difference(individuals, families)
    print(output)

    print("User Story 35: List recent births")
    result, output = Checks.list_recent_births(individuals)
    print(output)

    print("User Story 36: List recent deaths")
    result, output = Checks.list_recent_deaths(individuals)
    print(output)

    print("User Story 18: Siblings should not marry")
    result, output = Checks.siblings_should_not_marry(individuals, families)
    print(output)

    print("User Story 39: List upcoming anniversaries")
    result, output = Checks.list_upcoming_anniversaries(individuals, families)
    print(output)

    print("User Story 30: List living married")
    result, output = Checks.list_living_married(individuals, families)
    print(output)

    print("User Story 23: Unique name and birth date")
    result, output = Checks.unique_name_birth(individuals, families)
    print(output)

    print("User Story 20: Aunts and Uncles")
    result, output = Checks.aunts_and_uncles(individuals, families)
    print(output)

    print("User Story 31: Living Single")
    result, output = Checks.living_single(individuals)
    print(output)

    print("User Story 38: List Upcoming Birthdays")
    result, output = Checks.list_upcoming_birthdays(individuals)
    print(output)

    print("User Story 21: Correct Gender for Role")
    result, output = Checks.correct_gender_for_role(individuals, families)
    print(output)

    print("User Story 05: Marriage Before Death")
    result, output = Checks.marriage_before_death(individuals, families)
    print(output)

    print("User Story 06: Divorce Before Death")
    result, output = Checks.divorce_before_death(individuals, families)
    print(output)

    print("User Story 28: Order siblings by age")
    result, output = Checks.order_siblings_by_age(individuals, families)
    print(output)

    print("User Story 12: Parents too old")
    result, output = Checks.parents_too_old(individuals, families)
    print(output)

    print("User Story 33: List orphans")
    result, output = Checks.list_orphans(individuals, families)
    print(output)
    


if __name__ == '__main__':
    main()
