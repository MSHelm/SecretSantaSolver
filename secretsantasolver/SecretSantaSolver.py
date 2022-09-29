import random
import copy
from pathlib import Path

class SecretSantaSolver:
    """Solving Secret Santa Assignments
    """
    def __init__(self, names: list, partners: list = None):
        """Initialize the solver

        Args:
            names (list): Names of involved people
            partners (list, optional): Names of their partners. Each partner must also be part of the names list. Defaults to None.

        Raises:
            ValueError: if names are not unique
            ValueError: if partners are not unique
            ValueError: if partners is provided and is not of same length as name
            ValueError: if partners are not all included in names
        """
        self.names = names
        self.partners = partners

        # Check that names and partners are each unique
        if len(set(self.names)) != len(self.names):
            raise ValueError("Provided names are not unique!")

        
        if partners is not None:
            if len(set(self.partners)) != len(self.partners):
                raise ValueError("Provided partners are not unique!")

            # Check that names and partners are of equal length
            if len(self.names) != len(self.partners):
                raise ValueError("Unequal length of names and partners!")

            # Check that the partners are also all part of the names list 
            partners_unique = set([x for x in self.partners if x != ""])
            if not partners_unique.issubset(set(self.names)):
                raise ValueError("Not all partners where included in the names list!")
        

    def assign(self, prohibit_partners: bool = True):
        """Assign the names to each other, based on the settings

        Sets the reciever attribute of the class to the assigned giftees.
        This method does not return the list intentionally, to prevent accidentally revealing the assigned persons.

        Args:
            prohibit_partners (bool, optional): Whether partners should be prevented to be assigned to each other. Defaults to True.
        """
        self.prohibit_partners = prohibit_partners
        recievers_available = copy.deepcopy(self.names)
        recievers = []

        while len(recievers) == 0:
            for name in self.names:
                # Remove self and partner (if requested)
                if self.prohibit_partners and self.partners is not None:
                    partner = self.partners[self.names.index(name)]
                    candidates = [x for x in recievers_available if x not in [name, partner]]
                else:
                    candidates = [x for x in recievers_available if x not in name]

                if len(candidates) == 0:
                    # If no candidates remain we have run into a problem. Reset recievers and available recievers and start again.
                    recievers = []
                    recievers_available = copy.deepcopy(self.names)

                else:
                    reciever = random.choice(candidates)
                    recievers.append(reciever)
                    recievers_available.remove(reciever)

        self.recievers = recievers
    

    def export(self, path: str):
        """Export the assigned recievers

        For each name, it saves a txt file to the provided path. The file name is the secret santa, the content of the file is the name of the reciever.
        These files can then be sent to the respective participants

        Args:
            path (str): Path to save the files
        """
        path = Path(path)
        for i, name in enumerate(self.names):
            fname = name + ".txt"
            with open(path / fname, "x") as f:
                f.write(self.recievers[i])

