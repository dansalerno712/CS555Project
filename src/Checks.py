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
    #Go through the familes
    for f in families:
        wife = next(x for x in individuals if x.ID == f.wife_ID)
        husband = next(x for x in individuals if x.ID == f.husband_ID)
        fMar = datetime.strptime(f.married, '%d %b %Y')
        #Compare families
        for f2 in families:
            #Dont compare to itself
            if(f == f2):
                continue
            f2Mar = datetime.strptime(f2.married, '%d %b %Y')
            #Make sure second marriage happend after original
            if(f2Mar > fMar):
                #Checks if wife
                if(wife.ID == f2.wife_ID):
                    #Spouse is alive and family is not divorced
                    if husband.alive and f.divorced is None:
                        flag = False
                        output+= "Error: " + str(wife) + " is/was married to multiple people at the same time\n"
                    #If family is divorced check if divorce happened before second marriage
                    elif f.divorced != None and f2Mar < datetime.strptime(f.divorced, '%d %b %Y'):
                        flag = False
                        output+= "Error: " + str(wife) + " is/was married to multiple people at the same time\n"
                    #If spouse is dead check if death happened before second marriage
                    elif((husband.death != None and f2Mar < datetime.strptime(husband.death, '%d %b %Y'))):
                        flag = False
                        output+= "Error: " + str(wife) + " is/was married to multiple people at the same time\n"
                #Check if husband
                if(husband.ID == f2.husband_ID):
                    #Spouse is alive and family is not divorced
                    if husband.alive and f.divorced is None:
                        flag = False
                        output+= "Error: " + str(husband) + " is/was married to multiple people at the same time\n"
                    #If family is divorced check if divorce happened before second marriage
                    elif((f.divorced!= None and f2Mar < datetime.strptime(f.divorced, '%d %b %Y'))):
                        flag = False
                        output+= "Error: " + str(husband) + " is/was married to multiple people at the same time\n"
                    #If spouse is dead check if death happened before second marriage
                    elif((wife.death != None and f2Mar < datetime.strptime(wife.death, '%d %b %Y'))):
                        flag = False
                        output+= "Error: " + str(husband) + " is/was married to multiple people at the same time\n"
    if flag:
        output += "No one is practicing polygamy\n"
    return (flag, output)



 