import datetime

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
