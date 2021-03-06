# This file stores all the various checks for Errors and Anomalies
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Utils import calculate_age_at_spec_date, get_children, get_siblings, get_spouses


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
    for family in families:
        mom_death = None
        dad_death = None
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
            continue
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
        output += "All children in the all families do not have the same names and birth dates.\n"
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


def list_recent_deaths(individuals):
    """US 35: List recent deaths

    Args:
        individuals (list): A list of inidividuals

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if nobody has died in the last 30 days,
        False otherwise. Output is a string that describes which individuals died in the last 30 days
    """
    flag = True
    output = ""
    # todays datetime
    today = datetime.now()
    for indi in individuals:
        # check to make sure they are dead
        if not indi.alive and indi.death is not None:
            # parse birthday into datetime
            death = datetime.strptime(indi.death, "%d %b %Y")
            # get difference
            delta = today - death

            # also need to make sure the baby isnt born in the future
            if delta.days <= 30 and delta.days >= 0:
                flag = False
                output += str(indi) + " died within the last 30 days\n"

    if flag:
        output = "No individuals died in the last 30 days\n"

    return (flag, output)


def siblings_should_not_marry(individuals, families):
    """US 18: Siblings Should Not Marry

    Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if no siblings have married,
        False otherwise. Output is a string that describes which individuals married their siblings.
    """
    flag = True
    output = ""
    for family in families:
        husband = [indi for indi in individuals if indi.ID == family.husband_ID]
        wife = [indi for indi in individuals if indi.ID == family.wife_ID]
        if not set(husband[0].child).isdisjoint(wife[0].child):
            flag = False
            output += "Error: " + str(husband[0].ID) + " and " + str(
                wife[0].ID) + " are siblings and should not marry.\n"
    if flag:
        output = "No siblings are married\n"
    return (flag, output)


def list_upcoming_anniversaries(individuals, families):
    """US 39: List upcoming anniversaries

    Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if there are no living couples with anniversaries in the next 30 days,
        False otherwise. Output is a string that describes which living couples have anniversaries in the next 30 days.
    """
    flag = True
    output = ""
    today = datetime.now()
    for family in families:
        husband = [indi for indi in individuals if indi.ID == family.husband_ID]
        wife = [indi for indi in individuals if indi.ID == family.wife_ID]
        marriage = datetime.strptime(family.married, "%d %b %Y")
        # puts marriage into the current year to calculate anniversary
        marriage = marriage.replace(year=today.year)
        delta = marriage - today
        if husband[0].alive and wife[0].alive and delta.days <= 30 and delta.days >= 0:
            flag = False
            output += "Note: " + \
                str(family.ID) + " has an upcoming anniversary on " + \
                str(family.married) + "\n"
    if flag:
        output = "No living couples have anniversaries in the next 30 days.\n"
    return (flag, output)


def list_living_married(individuals, families):
    """US 30: List living married

        Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

        Returns:
        tuple: Tuple of the form (bool, output). Bool is True if there are no living married couples,
        False otherwise. Output is a string that describes the living married couples.
    """
    flag = True
    output = ""
    for family in families:
        husband = [indi for indi in individuals if indi.ID == family.husband_ID]
        wife = [indi for indi in individuals if indi.ID == family.wife_ID]
        if husband != [] and wife != [] and husband[0].alive and wife[0].alive:
            flag = False
            output += "Husband: " + \
                str(husband[0].ID) + ", Wife: " + str(wife[0].ID) + "\n"
    if flag:
        output = "No living married couples.\n"
    return (flag, output)


def unique_name_birth(individuals, families):
    """US 23: Unique name and birth date

        Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

        Returns:
        tuple: Tuple of the form (bool, output). Bool is True if all names and birth dates are unique.
        False otherwise. Output is a string that lists all individuals with non-unique names and birth dates.
    """
    flag = True
    output = ""
    everyone = {}
    for individual in individuals:
        name = individual.name
        birthday = individual.birthday
        if (name, birthday) in everyone:
            flag = False
            everyone[(name, birthday)] += [individual.ID]
        else:
            everyone[(name, birthday)] = [individual.ID]
    if flag:
        output = "All unique names and birth dates.\n"
    else:
        for key in everyone:
            if len(everyone[key]) > 1:
                same = " ".join(everyone[key])
                output += same + " have the same name and birth date.\n"
    return (flag, output)


def aunts_and_uncles(individuals, families):
    """US 20: Aunts and uncles

        Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

        Returns:
        tuple: Tuple of the form (bool, output). Bool is True if No aunts or uncles are married to nieces or nephews.
        False otherwise. Output is a string that lists all individuals who are married to a niece or nephew.
    """
    flag = True
    output = ""

    for i in individuals:
        parent_siblings = get_siblings(i, individuals, families)
        children = get_children(i, individuals, families)
        for c in children:
            kid_spouses = get_spouses(c, individuals, families)
            creeps = list(set(parent_siblings).intersection(set(kid_spouses)))
            if(len(creeps) > 0):
                for cr in creeps:
                    flag = False
                    output += "Error: " + \
                        str(cr) + " is married to their niece or nephew.\n"
    if flag:
        output += "No aunts or uncles are married to nieces or nephews.\n"
    return (flag, output)


def living_single(individuals):
    """US 31: Living single

        Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

        Returns:
        tuple: Tuple of the form (bool, output). Bool is True if No one is single and over 30.
        False otherwise. Output is a string that lists all individuals who single and over 30.
    """
    flag = True
    output = ""
    for i in individuals:
        if(i.age > 30 and len(i.spouse) == 0):
            flag = False
            output += str(i) + " is single and over 30.\n"
    if flag:
        output += "No one is single and over 30.\n"
    return (flag, output)


def list_upcoming_birthdays(individuals):
    """US 38: List upcoming birthdays

    Args:
        individuals (list): A list of inidividuals

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if nobody has upcoming birthdays in the next
        30 days, False otherwise. Output is a string that describes which individuals have birthdays
        in the next 30 days
    """
    flag = True
    output = ""
    # todays datetime
    today = datetime.now()
    for indi in individuals:
        # parse birthday into datetime and set year to current year so we can compare days only
        born = datetime.strptime(
            indi.birthday, "%d %b %Y").replace(year=today.year)

        # get difference
        delta = born - today

        # also need to make sure the birthday is in the past
        if delta.days <= 30 and delta.days >= 0:
            flag = False
            output += str(indi) + " has a birthday in the next 30 days\n"

    if flag:
        output = "No individuals have birthdays in the next 30 days\n"

    return (flag, output)


def correct_gender_for_role(individuals, families):
    """US 38

    Args:
        individuals (list): A list of individuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if all roles have the correct gender in
        every family, False otherwise. Output is a string that describes any families with incorrect roles.
    """
    flag = True
    output = ""

    for fam in families:
        husband = next(
            (indi for indi in individuals if indi.ID == fam.husband_ID), False)
        wife = next(
            (indi for indi in individuals if indi.ID == fam.wife_ID), False)

        if husband and wife:
            if husband.gender != "M":
                flag = False
                output += str(husband) + " is a husband but not a male\n"
            if wife.gender != "F":
                flag = False
                output += str(wife) + " is a wife but not a female\n"

    if flag:
        output = "All families have the correct gender for their roles\n"

    return(flag, output)


def marriage_before_death(individuals, families):
    """US 05

    Args:
        individuals (list): A list of individuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if all marriages happen before death of
        each spouse, False otherwise. Output is a string that describes any marriages that occur after death.
    """
    flag = True
    output = ""
    for family in families:
        for individual in individuals:
            if (family.husband_ID == individual.ID or family.wife_ID == individual.ID) and not individual.alive:
                marriage_date = datetime.strptime(family.married, "%d %b %Y")
                death_date = datetime.strptime(individual.death, "%d %b %Y")
                if marriage_date > death_date:
                    flag = False
                    output += "Error: " + individual.ID + \
                        " was married in family " + family.ID + " after death.\n"
    if flag:
        output += "All individuals were married before death.\n"
    return (flag, output)


def divorce_before_death(individuals, families):
    """US 06

    Args:
        individuals (list): A list of individuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if all divorces happen before death of
        each spouse, False otherwise. Output is a string that describes any divorces that occur after death.
    """
    flag = True
    output = ""
    for family in families:
        for individual in individuals:
            if (family.husband_ID == individual.ID or family.wife_ID == individual.ID) and not individual.alive and family.divorced != None:
                divorce_date = datetime.strptime(family.divorced, "%d %b %Y")
                death_date = datetime.strptime(individual.death, "%d %b %Y")
                if divorce_date > death_date:
                    flag = False
                    output += "Error: " + individual.ID + \
                        " was divorced in family " + family.ID + " after death.\n"
    if flag:
        output += "All individuals were divorced before death.\n"
    return (flag, output)


def order_siblings_by_age(individuals, families):
    """US 28: Order siblings by age

    Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if there are no siblings to sort by age
        False otherwise. Output is a string that lists siblings sorted by age.
    """
    flag = True
    output = ""
    for family in families:
        sibling_IDs = family.children
        siblings = []
        for ID in sibling_IDs:
            siblings.append(
                next((indi for indi in individuals if indi.ID == ID), False))
        siblings.sort(key=lambda x: x.age, reverse=True)
        # sort sibilings
        output += "Printing family: " + str(family.ID) + "\n"
        for sib in siblings:
            if sib:
                flag = False
                output += str(sib) + " \n"
    if flag:
        output = "No siblings to print.\n"
    return (flag, output)


def parents_too_old(individuals, families):
    """US 12: Parents too old

    Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if no parents are too old
        False otherwise. Output is a string that lists parents that are too old.
    """
    flag = True
    output = ""
    for fam in families:
        husband = next(
            (indi for indi in individuals if indi.ID == fam.husband_ID), False)
        wife = next(
            (indi for indi in individuals if indi.ID == fam.wife_ID), False)
        if (husband and wife):
            husband_born = datetime.strptime(husband.birthday, "%d %b %Y")
            wife_born = datetime.strptime(wife.birthday, "%d %b %Y")
            for child in fam.children:
                c = next((indi for indi in individuals if indi.ID == child), False)
                if c:
                    child_born = datetime.strptime(c.birthday, "%d %b %Y")
                    dad_delta = relativedelta(child_born, husband_born)
                    if dad_delta.years >= 80:
                        flag = False
                        output += "Error: Father " + \
                            str(husband.ID) + " is too old for child " + \
                            str(c.ID) + "\n"
                    mom_delta = relativedelta(child_born, wife_born)
                    if mom_delta.years >= 60:
                        flag = False
                        output += "Error: Mother " + \
                            str(wife.ID) + " is too old for child " + \
                            str(c.ID) + "\n"

    if flag:
        output = "No parents are too old for their children.\n"
    return (flag, output)


def list_orphans(individuals, families):
    """US 33: Lists orphans

    Args:
        individuals (list): A list of inidividuals
        families (list): A list of families

    Returns:
        tuple: Tuple of the form (bool, output). Bool is True if no orphans (younger than 18 and both parents dead)
        False otherwise. Output is a string that lists orphans.
    """
    flag = True
    output = ""
    for fam in families:
        husband = next(
            (indi for indi in individuals if indi.ID == fam.husband_ID), False)
        wife = next(
            (indi for indi in individuals if indi.ID == fam.wife_ID), False)
        if not wife.alive and not husband.alive:
            kids = get_children(husband, individuals, families)
            if len(kids) != 0:
                for k in kids:
                    if k.age < 18:
                        flag = False
                        output += str(k) + "\n"
    if flag:
        output = "No orphans found.\n"
    return (flag, output)
