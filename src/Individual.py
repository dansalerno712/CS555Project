from Utils import parse_line, calculate_age


class Individual(object):
    """Class for an Individual that holds the data of an INDI in gedcom files

    Attributes:
        age (int): Age (in years)
        alive (boolean): true/false if the individual is alive
        birthday (string): String of date in the format %d %b %Y (from here http://strftime.org/)
        child (list): list of strings that match the ID of another family
        death (string): Either the date of death (same format as birthday) or None if the individual is alive
        gender (string): F/M depending on the gender of the individual
        ID (string): ID of the individual
        name (string): Name of the individual in the format Firstname /Lastname/
        spouse (list): List of strings that match the ID of another family
    """

    def __init__(self, tag_list):
        """Constructor for Individual

        Args:
            tag_list (list): A list of all the lines of the GEDCOM file relating to this Individual
        """
        super(Individual, self).__init__()
        # default values
        self.alive = True
        self.child = []
        self.spouse = []
        self.death = None

        # look at all lines we have
        for i in range(len(tag_list)):
            level, tag, args, valid = parse_line(tag_list[i])

            # only look at valid tags and get data from tags
            if valid:
                if tag == "NAME":
                    self.name = args
                elif tag == "SEX":
                    self.gender = args
                elif tag == "BIRT":
                    # skip a line to get the actual date
                    level, tag, args, valid = parse_line(tag_list[i + 1])
                    self.birthday = args
                elif tag == "DEAT":
                    self.alive = False
                    # skip a line to get the actual date
                    level, tag, args, valid = parse_line(tag_list[i + 1])
                    self.death = args
                elif tag == "INDI":
                    self.ID = args
                elif tag == "FAMC":
                    self.child.append(args)
                elif tag == "FAMS":
                    self.spouse.append(args)

        if hasattr(self, "birthday"):
            self.age = calculate_age(self.birthday)
        else:
            self.age = None
