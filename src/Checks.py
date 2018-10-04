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
    """US 04
    Checks to make sure that a marriage occurs before a divorce

    Args:
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all divorces exist after a marriage,
        this returns (True, "All families are married before they are divorced\n"). If the divorces
        are not all preceeded by a marriage, this returns (False, <a string to output that lists errors>).
    """
    flag = True
    output = ""
    for family in families:
        if family.divorced is not None:
            married_date = datetime.strptime(family.married, '%d %b %Y')
            divorced_date = datetime.strptime(family.divorced, '%d %b %Y')
            if married_date > divorced_date:
                flag = False
                output += "Error: " + str(family) + \
                    " has a divorce before a marriage\n"
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
            output += "Error: " + str(individual) + \
                " has a birth after current date.\n"
        if individual.death is not None:
            death_date = datetime.strptime(individual.death, '%d %b %Y')
            if death_date > curr:
                flag = False
                output += "Error: " + \
                    str(individual) + " has a death after current date.\n"
    for family in families:
        married_date = datetime.strptime(family.married, '%d %b %Y')
        if married_date > curr:
            flag = False
            output += "Error: " + str(family) + \
                " has a marriage after current date.\n"
        if family.divorced is not None:
            divorced_date = datetime.strptime(family.divorced, '%d %b %Y')
            if divorced_date > curr:
                flag = False
                output += "Error: " + str(family) + \
                    " has a divorce after current date.\n"
    if flag:
        output += "All dates are after current date."
    return (flag, output)


def birth_before_parents_death(individuals, families):
    """
    US09
    Checks to make sure that a child's birth occurs before the parents' deaths

    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all births occur before parents' deaths, this returns
        (True, "All children are born before the death of the mother or within nine months of the death of the father.")
        If the children are born after the death of the mother or more than nine months after the death of the father,
        this returns (False, <a string to output that lists errors>).
    """
    flag = True
    output = ""
    mom_death = None
    dad_death = None
    for family in families:
        children = {}
        for individual in individuals:
            if individual.ID == family.wife_ID:
                if individual.death is not None:
                    mom_death = datetime.strptime(individual.death, '%d %b %Y')
            elif individual.ID == family.husband_ID:
                if individual.death is not None:
                    dad_death = datetime.strptime(individual.death, '%d %b %Y')
            else:
                if individual.ID in family.children:
                    children[individual.ID] = individual
        for c in children:
            child = children[c]
            child_birthday = datetime.strptime(child.birthday, '%d %b %Y')
            if mom_death is not None and child_birthday > mom_death:
                flag = False
                output += "Error: " + \
                    str(family) + " has a child " + str(child.ID) + \
                    " born after the mother's death.\n"
            if dad_death is not None and child_birthday > (dad_death + relativedelta(months=9)):
                flag = False
                output += "Error: " + str(family) + " has a child " + str(
                    child.ID) + " born more than 9 months after the father's death.\n"
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
                            children[individual.name] = [
                                individual.birthday, [str(individual)]]
                    else:
                        continue
            for key in children.keys():
                if len(children[key][1]) > 1:
                    output += "Error: " + str(family) + " has children, ".join(
                        children[key][1]) + ", with the same first name and birthday.\n"
    if flag:
        output += "All children in the all families do not have the same names and birth dates."
    return (flag, output)

def age_less_than_150(individuals):
    """US 07
    Checks to make sure that an individual is less than 150 years old

    Args:
        individuals (list): List of Individual objects

    Returns:
        tuple: Tuple in the form (result, output). If all individuals are less than 150 years old,
        this returns (True, "All individuals are less than 150 years old\n"). If there are individuals
        over the age of 150, this returns (False, <a string to output that lists errors>).
    """
    flag = True
    output = ""
    curr_date = datetime.now()
    for individual in individuals:
        if individual.alive:
            # birth_date = datetime.strptime(individual.birthday, '%d %b %Y')
            # age = curr_date - birth_date
            if individual.age > 150:
                flag = False
                output += "Error: " + str(individual.ID) + " is more than 150 years old.\n"
    if flag:
        output += "All individuals are less than 150 years old.\n"
    return (flag, output)

def no_bigamy(individuals, families):
    """
    US11
    Checks that each individual is only married to one partner at a time
    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all individuals are married to one person at a time, this returns
        (True, "No one is practicing polygamy"). If all individuals are not married to one person at a time, this returns
        (False, <a string to output that lists errors>)
    """
    flag = True
    output = ""
    # Go through the familes
    for f in families:
        wife = next(x for x in individuals if x.ID == f.wife_ID)
        husband = next(x for x in individuals if x.ID == f.husband_ID)
        fMar = datetime.strptime(f.married, '%d %b %Y')
        # Compare families
        for f2 in families:
            # Dont compare to itself
            if(f == f2):
                continue
            f2Mar = datetime.strptime(f2.married, '%d %b %Y')
            # Make sure second marriage happend after original
            if(f2Mar > fMar):
                # Checks if wife
                if(wife.ID == f2.wife_ID):
                    # Spouse is alive and family is not divorced
                    if husband.alive and f.divorced is None:
                        flag = False
                        output += "Error: " + \
                            str(wife) + " is/was married to multiple people at the same time\n"
                    # If family is divorced check if divorce happened before second marriage
                    elif f.divorced is not None and f2Mar < datetime.strptime(f.divorced, '%d %b %Y'):
                        flag = False
                        output += "Error: " + \
                            str(wife) + " is/was married to multiple people at the same time\n"
                    # If spouse is dead check if death happened before second marriage
                    elif((husband.death is not None and f2Mar < datetime.strptime(husband.death, '%d %b %Y'))):
                        flag = False
                        output += "Error: " + \
                            str(wife) + " is/was married to multiple people at the same time\n"
                # Check if husband
                if(husband.ID == f2.husband_ID):
                    # Spouse is alive and family is not divorced
                    if husband.alive and f.divorced is None:
                        flag = False
                        output += "Error: " + \
                            str(husband) + \
                            " is/was married to multiple people at the same time\n"
                    # If family is divorced check if divorce happened before second marriage
                    elif((f.divorced is not None and f2Mar < datetime.strptime(f.divorced, '%d %b %Y'))):
                        flag = False
                        output += "Error: " + \
                            str(husband) + \
                            " is/was married to multiple people at the same time\n"
                    # If spouse is dead check if death happened before second marriage
                    elif((wife.death is not None and f2Mar < datetime.strptime(wife.death, '%d %b %Y'))):
                        flag = False
                        output += "Error: " + \
                            str(husband) + \
                            " is/was married to multiple people at the same time\n"
    if flag:
        output += "No one is practicing polygamy\n"
    return (flag, output)


def sibling_spacings(individuals, families):
    """
    US13
    Checks that all siblings are born more than 8 months or less than 2 days apart
    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all siblings are born more than 8 months or less than 2 days apart, this returns
        (True, "All siblings are born more than 8 months or less than 2 days apart"). If all siblings are born more than 8 months or less than 2 days apart, this returns
        (False, <a string to output that lists errors>)
    """
    flag = True
    output = ""
    fam_children = [fam.children for fam in families]
    checked = []
    for kids in fam_children:
        if(len(kids) < 2):
            continue
        kid_indis = [kid for kid in individuals if kid.ID in kids]
        for k in kid_indis:
            k1_bday = datetime.strptime(k.birthday, '%d %b %Y')
            for k2 in kid_indis:
                k2_bday = datetime.strptime(k2.birthday, '%d %b %Y')
                if(k == k2):
                    continue
                elif (k, k2) in checked or (k2, k) in checked:
                    continue
                bday_diff_months = abs(
                    k1_bday.year - k2_bday.year) * 12 + k1_bday.month - k2_bday.month
                bday_diff_days = abs(k1_bday - k2_bday)
                if(bday_diff_days.days > 1 and bday_diff_months < 8):
                    checked.append((k, k2))
                    flag = False
                    # Diff in days: " + str(bday_diff_days) + "\n" + "Diff in months: " + str(bday_diff_months) + "\n"
                    output += "Error: " + \
                        str(k) + " and " + str(k2) + \
                        " are less than 8 months and more than 2 days apart.\n"
    if(flag):
        output += "All siblings are born more than 8 months or less than 2 days apart\n"
    return (flag, output)


def fewer_than_15_sibilings(families):
    """US 15: Fewer than 15 sibilings

    Args:
        families (list): A list of family objects

    Returns:
        tuple: Tuple in the form (result, output). If all families have less than 15 sibilings, output is
        All families have less than 15 sibilings. Else, output contains the families that have too many
        sibiling
    """
    flag = True
    output = ""

    for fam in families:
        if len(fam.children) >= 15:
            flag = False
            output += "Error: family " + \
                str(fam) + " has 15 or more sibilings\n"

    if flag:
        output += "All families have less than 15 sibilings\n"

    return (flag, output)


def list_deceased(individuals):
    """US 29: List deceased. Doesnt return anything, just prints things

    Args:
        individuals (list): A list of individuals from the file

    Returns:
        string: The deceased individuals as strings
    """
    flag = True
    output = ""
    for indi in individuals:
        if indi.death is not None:
            flag = False
            output += str(indi) + "\n"

    if flag:
        output = "No deceased individuals\n"

    return (flag, output)

def marriage_after_14(individuals, families):
    """
    US10
    Checks to make sure that marriage occurs at least 14 years after birth of both spouses
    (parents must be at least 14 years old)

    Args:
        individuals (list): List of Individual objects
        families (list): List of Family objects

    Returns:
        tuple: Tuple in the form (result, output). If all marriages occur after the age of 14, this returns
        (True, ""All individuals were married above the age of 14.") If individuals are less than 14 when a
        marriage occurs, this returns (False, <a string to output that lists errors>).
    """
    flag = True
    output = ""
    for family in families:
        wedding_date = datetime.strptime(family.married, '%d %b %Y')
        for individual in individuals:
            birth_date = datetime.strptime(individual.birthday, '%d %b %Y')
            if individual.ID == family.wife_ID or individual.ID == family.husband_ID:
                wedding_age = wedding_date - birth_date
                if wedding_age.days < (14 * 365):
                    flag = False
                    output += "Error: " + str(family.ID) + " is not a valid wedding. " + str(individual.ID) + " was not above the age of 14.\n"
    if flag:
        output += "All individuals were married above the age of 14.\n"

    return (flag, output)
