# Dan Salerno, Jennifer Cafiero, Brianne Trollo, Derek Pulaski
# CS 555
# Project 3

import sys
from Family import Family
from Individual import Individual
from Utils import parse_line


def main():
    ''' Parses the GEDCOM file from the input and stores the Individuals and Families'''
    # check for correct inputs
    if len(sys.argv) != 2:
        print("Usage: python parser.py <file_path>")
        return

    path = sys.argv[1]

    # get the info from the gedcom file
    with open(path, 'r') as file:
        lines = [line.rstrip() for line in file]

    # stores various data
    individuals_data = []
    families_data = []
    indexes = []

    # grab the indexes of INDI or FAM tags
    for i in range(len(lines)):
        level, tag, args, valid = parse_line(lines[i])

        if tag == "INDI":
            indexes.append((i, "INDI"))
        elif tag == "FAM":
            indexes.append((i, "FAM"))

    # grab the lines that correspond to the INDIs and FAMs
    for i in range(len(indexes) - 1):
        index, tag = indexes[i]
        next_index, _ = indexes[i + 1]

        if tag == "INDI":
            # make sure to grab the last set of data if we are at the end
            if i == (len(indexes) - 2):
                individuals_data.append(lines[index:next_index])
                individuals_data.append(lines[next_index:])
            else:
                individuals_data.append(lines[index:next_index])

        if tag == "FAM":
            if i == (len(indexes) - 2):
                families_data.append(lines[index:next_index])
                families_data.append(lines[next_index:])
            else:
                families_data.append(lines[index:next_index])

    # Creating the actual objects
    individuals = []
    families = []

    for data in individuals_data:
        indi = Individual(data)
        individuals.append(indi)

    for data in families_data:
        fam = Family(data)

        # get the husband and wife names which are linked from Individuals
        husband = [man for man in individuals if man.ID == fam.husband_ID]
        wife = [woman for woman in individuals if woman.ID == fam.wife_ID]

        if len(wife) > 0:
            fam.wife_name = wife[0].name

        if len(husband) > 0:
            fam.husband_name = husband[0].name

        families.append(fam)

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


if __name__ == '__main__':
    main()
