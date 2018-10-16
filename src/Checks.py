# This file stores all the various checks for Errors and Anomalies
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Utils import calculate_age_at_spec_date


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
    for individual in individuals:
        if individual.alive:
            # birth_date = datetime.strptime(individual.birthday, '%d %b %Y')
            # age = curr_date - birth_date
            if individual.age > 150:
                flag = False
                output += "Error: " + \
                    str(individual.ID) + " is more than 150 years old.\n"
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
                if(wife.ID == f2.wife_ID):
                    innerFlag, out = no_bigamy_spouse_checker(
                        wife, husband, f, f2)
                    flag = innerFlag and flag
                    output += out
                if(husband.ID == f2.husband_ID):
                    innerFlag, out = no_bigamy_spouse_checker(
                        husband, wife, f, f2)
                    flag = innerFlag and flag
                    output += out
    if flag:
        output += "No one is practicing polygamy\n"
    return (flag, output)


def no_bigamy_spouse_checker(checked, spouse, f, f2):
    flag = True
    output = ""
    fMar = datetime.strptime(f.married, '%d %b %Y')
    f2Mar = datetime.strptime(f2.married, '%d %b %Y')
    if (spouse.alive and f.divorced is None) or (f.divorced is not None and f2Mar < datetime.strptime(f.divorced, '%d %b %Y')) or ((spouse.death is not None and f2Mar < datetime.strptime(spouse.death, '%d %b %Y'))):
        flag = False
        output += "Error: " + \
            str(checked) + " is/was married to multiple people at the same time\n"
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
        (True, "All siblings are born more than 8 months or less than 2 days apart"). If all siblings are born less than 8 months or more than 2 days apart, this returns
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


def fewer_than_15_siblings(families):
    """US 15: Fewer than 15 siblings

    Args:
        families (list): A list of family objects

    Returns:
        tuple: Tuple in the form (result, output). If all families have less than 15 siblings, output is
        All families have less than 15 siblings. Else, output contains the families that have too many
        sibling
    """
    flag = True
    output = ""

    for fam in families:
        if len(fam.children) >= 15:
            flag = False
            output += "Error: family " + \
                str(fam) + " has 15 or more siblings\n"

    if flag:
        output += "All families have less than 15 siblings\n"

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
                    output += "Error: " + str(family.ID) + " is not a valid wedding. " + str(
                        individual.ID) + " was not above the age of 14.\n"
    if flag:
        output += "All individuals were married above the age of 14.\n"

    return (flag, output)


def birth_before_death(individuals, families):
    """
    US03
    Checks to make sure birth of an individual is before their death

    Args:
    individuals (list): List of Individual objects
    families (list): List of Family objects

    Returns:
    tuple: Tuple in the form (result, output). If all births are before deaths, this returns
    (True, ""All individuals were born before their death.") If individuals have a death before
    their birthday, this returns (False, <a string to output that lists errors>).
    """
    flag = True
    output = ""
    for individual in individuals:
        if individual.death is not None:
            death = datetime.strptime(individual.death, '%d %b %Y')
            birth = datetime.strptime(individual.birthday, '%d %b %Y')
            if death < birth:
                flag = False
                output += "Error: " + \
                    str(individual) + " has a death date before their birthday.\n"
    if flag:
        output += "All individuals have death dates after birthdays.\n"
    return (flag, output)


def birth_before_marriage(individuals, families):
    """
    US02
    Checks to make sure birth of an individual is before their marriage

    Args:
    individuals (list): List of Individual objects
    families (list): List of Family objects

    Returns:
    tuple: Tuple in the form (result, output). If all births are before marriage, this returns
    (True, ""All individuals were born before their marriage.") If individuals have a marriage before
    their birthday, this returns (False, <a string to output that lists errors>).
    """
    flag = True
    output = ""
    for family in families:
        wedding_date = datetime.strptime(family.married, '%d %b %Y')
        for individual in individuals:
            birth_date = datetime.strptime(individual.birthday, '%d %b %Y')
            if individual.ID == family.wife_ID or individual.ID == family.husband_ID:
                if birth_date > wedding_date:
                    flag = False
                    output += "Error: " + \
                        str(individual) + " has a marriage before their birth.\n"
    if flag:
        output += "All individuals have a birthday before their marriage date.\n"
    return (flag, output)


def unique_family_by_spouses(families):
    """
    US24
    Checks that All families have unique wife name, husband name, and marriage date
        tuple: Tuple in the form (result, output). If All families have unique wife name, husband name, and marriage date, this returns
        (True, "All families have unique wife name, husband name, and marriage date"). If familes have duplicate wife name, husband name, and marriage date, this returns
        (False, <a string to output that lists errors>)
    """
    flag = True
    output = ""
    couples = [(fam.wife_name, fam.husband_name, fam.married)
               for fam in families]
    dup_couples = [fam for fam, count in Counter(couples).items() if count > 1]
    if len(dup_couples) > 0:
        flag = False
        for c in dup_couples:
            output += "Error: " + str(c) + " appear in multiple families\n"
    if flag:
        output += "All families have unique wife name, husband name, and marriage date\n"
    return (flag, output)


def list_large_age_difference(individuals, families):
    """
    US24
    List all couples who were married when the older spouse was more than twice as old as the younger spouse
        tuple: Tuple in the form (result, output). If there are no couples with large age diff, this returns
        (True, "No couples where the older spouse was twice as old as the younger spouse at the time of marriage\n").
        If there are couples with large age diff, this returns
        (False, <a string to output that lists couples>)
    """
    flag = True
    output = ""
    for f in families:
        wife = next(x for x in individuals if x.ID == f.wife_ID)
        husband = next(x for x in individuals if x.ID == f.husband_ID)
        wifeAgeMarr = calculate_age_at_spec_date(wife.birthday, f.married)
        husbAgeMarr = calculate_age_at_spec_date(husband.birthday, f.married)
        if wifeAgeMarr >= husbAgeMarr * 2:
            flag = False
            output += str(wife) + " and " + str(husband) + "\n"
        elif husbAgeMarr >= wifeAgeMarr * 2:
            flag = False
            output += str(husband) + " and " + str(wife) + "\n"

    if flag:
        output += "No couples where the older spouse was twice as old as the younger spouse at the time of marriage\n"
    return (flag, output)


def list_recent_births(individuals):
    """US 35: List recent births

    Args:
        individuals (list): A list of inidividuals

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if nobody has been born in the last 30 days,
        False otherwise. Output is a string that describes which individuals were born in the last 30 days
    """
    flag = True
    output = ""
    # todays datetime
    today = datetime.now()
    for indi in individuals:
        # parse birthday into datetime
        born = datetime.strptime(indi.birthday, "%d %b %Y")
        # get difference
        delta = today - born

        # also need to make sure the baby isnt born in the future
        if delta.days <= 30 and delta.days >= 0:
            flag = False
            output += str(indi) + " was born within the last 30 days\n"

    if flag:
        output = "No individuals born in the last 30 days\n"

    return (flag, output)
