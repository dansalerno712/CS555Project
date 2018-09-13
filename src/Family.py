from Utils import parse_line


class Family(object):
    """Class for the family object in gedcom

    Attributes:
        children (list): A list of strings that are the IDs of the children of the family
        divorced (string): String of date of divorced in the format %d %b %Y or None if not divorced
        husband_ID (string): ID of the husband individual
        husband_name (string): name of the husband individual
        ID (string): Unique identifier of the family
        married (string): String of marriage date in the format %d %b %Y (from here http://strftime.org/)
        wife_ID (string): ID of the wife individual
        wife_name (string): name of the wife individual
    """

    def __init__(self, tag_list):
        """Constructor for Family

        Args:
            tag_list (list): A list of all the lines of the GEDCOM file relating to this Family
        """
        super(Family, self).__init__()
        # default values
        self.divorced = None
        self.children = []
        self.husband_name = None
        self.wife_name = None

        # look at all the lines we have
        for i in range(len(tag_list)):
            level, tag, args, valid = parse_line(tag_list[i])

            # ignore invalid lines and get data from the correct tags
            if valid:
                if tag == "FAM":
                    self.ID = args
                elif tag == "HUSB":
                    self.husband_ID = args
                elif tag == "WIFE":
                    self.wife_ID = args
                elif tag == "MARR":
                    # skip a line to get the actual date
                    level, tag, args, valid = parse_line(tag_list[i + 1])
                    self.married = args
                elif tag == "CHIL":
                    self.children.append(args)
                elif tag == "DIV":
                    # skip a line to get the actual date
                    level, tag, args, valid = parse_line(tag_list[i + 1])
                    self.divorced = args
