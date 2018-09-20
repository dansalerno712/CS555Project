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
