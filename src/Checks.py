# This file stores all the various checks for Errors and Anomalies
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta

def unique_IDs(individuals, families):
    """US 22
    Checks to make sure all individual IDs are unique and all
    family IDs are unique

    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all IDs are unique, this returns
        (True, "All IDs are unique"). If the IDs are not all unique, this returns
        (False, <a string to output that lists errors>)
    """

    # pull the IDs from the individuals and families
    indi_IDs = [indi.ID for indi in individuals]
    fam_IDs = [fam.ID for fam in families]

    # get a list of the duplicate IDs
    duplicate_indi_IDs = [ID for ID, count in Counter(
        indi_IDs).items() if count > 1]
    duplicate_fam_IDs = [ID for ID, count in Counter(
        fam_IDs).items() if count > 1]

    # if both duplicate lists are empty then everything is unique
    if len(duplicate_indi_IDs) == 0 and len(duplicate_fam_IDs) == 0:
        return (True, "All IDs are unique")
    else:
        output = ""

        # generate error messages
        for ID in duplicate_indi_IDs:
            duplicated_indis = [indi for indi in individuals if indi.ID == ID]

            for indi in duplicated_indis:
                output += "Error: " + str(indi) + " has a non-unique ID\n"

        for ID in duplicate_fam_IDs:
            duplicated_fams = [fam for fam in families if fam.ID == ID]

            for fam in duplicated_fams:
                output += "Error: " + str(fam) + " has a non-unique ID\n"

        return (False, output)

def marriage_before_divorce(families):
    flag = True
    output = ""
    for family in families:
        if family.divorced != None:
            married_date = datetime.strptime(family.married, '%d %b %Y')
            divorced_date = datetime.strptime(family.divorced, '%d %b %Y')
            if married_date > divorced_date:
                flag = False
                output += "Error: " + str(family) + " has a divorce before a marriage\n"
    if flag:
        output += "All families are married before they are divorced\n"
    return (flag, output)

def dates_before_current_date(individuals, families):
    """
    US01
    Checks all dates are before the current date
    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all dates are before current date, this returns
        (True, "All dates are after current date."). If the dates are not all before current date, this returns
        (False, <a string to output that lists errors>)
    """
    flag = True
    output = ""
    curr = datetime.now()
    for individual in individuals:
        birth_date = datetime.strptime(individual.birthday, '%d %b %Y')
        if birth_date > curr:
            flag = False
            output += "Error: " + str(individual) + " has a birth after current date.\n"
        if individual.death != None:
            death_date = datetime.strptime(individual.death, '%d %b %Y')
            if death_date > curr:
                flag = False
                output += "Error: " + str(individual) + " has a death after current date.\n"
    for family in families:
        married_date = datetime.strptime(family.married, '%d %b %Y')
        if married_date > curr:
            flag = False
            output += "Error: " + str(family) + " has a marriage after current date.\n"
        if family.divorced != None:
            divorced_date = datetime.strptime(family.divorced, '%d %b %Y')
            if divorced_date > curr:
                flag = False
                output += "Error: " + str(family) + " has a divorce after current date.\n"
    if flag:
        output += "All dates are after current date."
    return (flag, output)

def birth_before_parents_death(individuals, families):
    flag = True
    output = ""
    mom_death = None
    dad_death = None
    for family in families:
        children = {}
        for individual in individuals:
            if individual.ID == family.wife_ID:
                if individual.death != None:
                    mom_death = datetime.strptime(individual.death, '%d %b %Y')
            elif individual.ID == family.husband_ID:
                if individual.death != None:
                    dad_death = datetime.strptime(individual.death, '%d %b %Y')
            else:
                if individual.ID in family.children:
                    children[individual.ID] = individual
        for c in children:
            child = children[c]
            child_birthday = datetime.strptime(child.birthday, '%d %b %Y')
            if mom_death != None and child_birthday > mom_death:
                flag = False
                output += "Error: " + str(family) + " has a child " + str(child.ID) + " born after the mother's death.\n"
            if dad_death != None and child_birthday > (dad_death + relativedelta(months = 9)):
                flag = False
                output += "Error: " + str(family) + " has a child " + str(child.ID) + " born more than 9 months after the father's death.\n"
    if flag:
        output += "All children are born before the death of the mother or within nine months of the death of the father."
    return (flag, output)
    
def unique_first_names(individuals, families):
    """
    US25
    Checks that no more than one child with the same name and birth date should appear in a family
    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all first names in families are unique, this returns
        (True, "All first names are unique"). If the first names are not all unique, this returns
        (False, <a string to output that lists errors>)
    """
    flag = True
    output = ""
    for family in families:
        if family.children == []:
            break
        else:
            children = {}
            for child in family.children:
                for individual in individuals:
                    if individual.ID == child:
                        if individual.name in children and children[individual.name][0] == individual.birthday:
                            flag = False
                            children[individual.name][1] += [str(individual)]
                        else:
                            children[individual.name] = [individual.birthday, [str(individual)]]
                    else:
                        continue
            for key in children.keys():
                if len(children[key][1]) > 1:
                    output += "Error: " + str(family) + " has children, ".join(children[key][1]) + ", with the same first name and birthday.\n"
    if flag:
        output += "All children in the all families do not have the same names and birth dates."
    return (flag, output)
