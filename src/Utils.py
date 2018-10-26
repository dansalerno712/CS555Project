import datetime
from prettytable import PrettyTable

# stores the valid tags for each level
# NOTE: INDI and FAM are not included in the level 0 tags because they are a special case
# that is checked later
valid_map = {
    "0": ["HEAD", "TRLR", "NOTE"],
    "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
    "2": ["DATE"]
}


def is_valid(level, tag):
    """Function to determine if the given leve and tag combo is valid

    Args:
        level (String): The level from the GEDCOM line
        tag (String): The tag from the GEDCOM line

    Returns:
        String: Y/N depending on if the tag is valid
    """
    if level in valid_map and tag in valid_map[level]:
        return "Y"
    else:
        return "N"


def parse_line(line):
    """Takes a line of the gedcom file and returns the level, tag, and arguments

    Args:
        line (string): The current line of the gedcom file

    Returns:
        (level, tag, args, valid): A tuple which contains the level, tag, args, and validity of the tag
    """
    split = line.split(" ")
    level = split[0]

    if (level == "0" and len(split) == 3 and (split[2] == "INDI" or split[2] == "FAM")):
        tag = split[2]
        args = split[1]
        valid = "Y"
    else:
        tag = split[1]

        # if there are args, we need to rejoin them since they were split on spaces
        if len(split) > 2:
            args = ' '.join(split[2:])
        else:
            args = ''

        valid = is_valid(level, tag)

    return (level, tag, args, valid)


def calculate_age(born_string):
    """Calculate the age of a person

    Args:
        born_string (string): Date string of an Individuals birthday

    Returns:
        int: How many years old the person is
    """
    today = datetime.date.today()
    born = datetime.datetime.strptime(born_string, "%d %b %Y").date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def pretty_print(individuals, families):
    """Prints all individuals and families in a table using pretty table

    Args:
        individuals (list): list of Individual objects
        families (list): list of Family objects
    """
    print("==============================Individuals===============================")
    i_table = PrettyTable()
    i_table.field_names = ["ID", "Name", "Gender",
                           "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    for indi in individuals:
        i_table.add_row([indi.ID, indi.name, indi.gender, indi.birthday,
                         indi.age, indi.alive, indi.death, indi.child, indi.spouse])

    print(i_table)

    print("==============================Families===============================")
    f_table = PrettyTable()
    f_table.field_names = ["ID", "Married", "Divorced", "Husband ID",
                           "Husband Name", "Wife ID", "Wife Name", "Children"]
    for fam in families:
        f_table.add_row([fam.ID, fam.married, fam.divorced, fam.husband_ID,
                         fam.husband_name, fam.wife_ID, fam.wife_name, fam.children])

    print(f_table)


def calculate_age_at_spec_date(born_string, date_string):
    """Helper for list_large_age_difference
        Calculate the age of a person at specific date

    Args:
        born_string (string): Date string of an Individuals birthday
        date_string (string): Date string to check age of individual at
    Returns:
        int: How many years old the person was at date_string
    """
    specDate = datetime.datetime.strptime(date_string, "%d %b %Y").date()
    born = datetime.datetime.strptime(born_string, "%d %b %Y").date()
    return specDate.year - born.year - ((specDate.month, specDate.day) < (born.month, born.day))

def get_siblings(indi, individuals, families):
    """
     Args:
        indi (individual): individual to lookup
        individuals (list): list of individuals
        families (list): list of families
    Returns:
        list: list of siblings of indi
    """
    siblings_ID = next((fam.children for fam  in families if indi.ID in fam.children), [])
    return [i for i in individuals if i.ID in siblings_ID]

def get_children(indi, individuals, families):
    """
     Args:
        indi (individual): individual to lookup
        individuals (list): list of individuals
        families (list): list of families
    Returns:
        list: list of children of indi
    """
    children_ID =  next((fam.children for fam  in families if indi.ID == fam.husband_ID or indi.ID == fam.wife_ID), [])
    return [i for i in individuals if i.ID in children_ID]

def get_spouses(indi, individuals, families):
    """
     Args:
        indi (individual): individual to lookup
        individuals (list): list of individuals
        families (list): list of families
    Returns:
        list: list of spouses of indi
    """
    if(indi.gender == 'F'):
        spouses_ID = [fam.husband_ID for fam  in families if fam.ID in indi.spouse]
        return [i for i in individuals if i.ID in spouses_ID]
    else:
        spouses_ID = [fam.wife_ID for fam  in families if fam.ID in indi.spouse]
        return [i for i in individuals if i.ID in spouses_ID]
