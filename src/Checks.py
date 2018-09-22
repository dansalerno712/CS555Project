# This file stores all the various checks for Errors and Anomalies
from collections import Counter
from datetime import datetime

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

def no_bigamy(individuals, families):
    flag = True
    output = ""
    posCheaters = [ind for ind in individuals if len(ind.spouse) > 1]
    for pc in posCheaters:
        spouses = pc.spouse
        timelines = []
        for f in spouses
            wife = next(x for x in individuals if x.ID == f.wife)
            husband = next(x for x in individuals if x.ID == f.husband)
            married_date = datetime.strptime(f.married, '%d %b %Y')
            if f.divorced !=None:
                output+= "divorce"
                divorced_date = datetime.strptime(f.divorced, '%d %b %Y')
                timelines.append([married_date, divorced_date])
            elif i.gender == 'M' and  wife.death:
                death_date = datetime.strptime(wife.death, '%d %b %Y')
                timelines.append([married_date, wife.death])
            elif i.gender == 'F' and husband.death:
                death_date = datetime.strptime(husband.death, '%d %b %Y')
                timelines.append([married_date, husband.death])
            else:
                continue
        
    # for i in individuals:
    #     spouses = i.spouse
    #     indID = i.ID
    #     if len(spouses) > 1:
    #         output+= str(i) + "\n"
    #         fams = [fam for fam in families if fam.ID in spouses]
    #         timelines = []
    #         for f in fams:
    #             married_date = datetime.strptime(f.married, '%d %b %Y')
    #             if f.divorced !=None:
    #                 output+= "divorce"
    #                 divorced_date = datetime.strptime(f.divorced, '%d %b %Y')
    #                 timelines.append([married_date, divorced_date])
    #             elif i.gender == 'M':
    #                 wife = next(x for x in individuals if x.ID == f.wife)
    #                 if wife.death:
    #                     timelines.append([married_date, wife.death])
    #             elif i.gender == 'F':
    #                 print("hekko")
    #                 husband = next(x for x in individuals if x.ID == f.husband)
    #                 if husband.death:
    #                     timelines.append([married_date, husband.death])
    #             else:
    #                 continue
            # for t in timelines:
                # output+= str(timelines) + "\n"
    flag = False
    output+= "Error: " + str(posCheaters[0]) + " is married to multiple people\n"
    return (flag, output)



 