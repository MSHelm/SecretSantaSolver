import random
import copy
from pathlib import Path

class SecretSantaSolver:
    """Solving Secret Santa Assignments
    """
    def __init__(self, names: list, partners: list = None, previous_recievers: list = None):
        """Initialize the solver

        Args:
            names (list): Names of involved people
            partners (list, optional): Names of their partners. Each partner must also be part of the names list. Defaults to None.
            previous_recievers (list, optional): Name of previous reciever for each name. Defaults to None.

        Raises:
            ValueError: if names are not unique
            ValueError: if partners are not unique
            ValueError: if partners is provided and is not of same length as name
            ValueError: if partners are not all included in names
        """
        self.names = names
        self.partners = partners
        self.previous_recievers = previous_recievers

        # Check that names and partners are each unique
        if len(set(self.names)) != len(self.names):
            raise ValueError("Provided names are not unique!")
        
        # Check previous recievers, if provided
        if self.previous_recievers is not None:
            if len(set(self.previous_recievers)) != len(self.previous_recievers):
                raise ValueError("Provided previous recievers are not unique!")
            
            # Previous recievers should be a subset (or identical) to the current names
            if all([x in self.partners for x in self.previous_recievers]) == False:
                raise ValueError("Provided previous_recievers contains names that are not in current names")
        
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
        

    def assign(self, prohibit_partners: bool = True, prohibit_previous_recievers: bool = False):
        """Assign the names to each other, based on the settings

        Sets the reciever attribute of the class to the assigned giftees.
        This method does not return the list intentionally, to prevent accidentally revealing the assigned persons.

        Args:
            prohibit_partners (bool, optional): Whether partners should be prevented to be assigned to each other. Defaults to True.
            prohibit_previous_recievers (bool, optional): Whether previous reciever should be prevented to be assigned again. Default sto False.
        """
        # Check that prohibition flags also have necessary information from object instatiation
        if prohibit_partners and self.partners is None:
            raise ValueError("Requested to prohibit partners, but no partners provided!")
        if prohibit_previous_recievers and self.previous_recievers is None:
            raise ValueError("Requested to prohibit previous reciever, but not previous recievers provided!")

        self.prohibit_partners = prohibit_partners
        self.prohibit_previous_recievers = prohibit_previous_recievers

        recievers_available = copy.deepcopy(self.names)
        recievers = []

        k = 0
        while len(recievers) == 0:
            for i, name in enumerate(self.names):
                # Define allowed recievers, based on prohibited partners or previous recievers.
                excluded_recievers = [name] # Never gift yourself :)
                if self.prohibit_partners and self.partners is not None:
                    partner = self.partners[i]
                    excluded_recievers.append(partner)
                # Remove self and partner (if requested)
                if self.prohibit_previous_recievers and self.prohibit_previous_recievers is not None:
                    previous_reciever = self.previous_recievers[i]
                    excluded_recievers.append(previous_reciever)

                print(f"Excluded recievers for {name}: {excluded_recievers}")
                
                candidates = [x for x in recievers_available if x not in excluded_recievers]
                print(f"Candidates for {name}: {candidates}")
                
                if len(candidates) == 0:
                    # If no candidates remain we have run into a problem. Reset recievers and available recievers and start again.
                    recievers = []
                    recievers_available = copy.deepcopy(self.names)

                else:
                    reciever = random.choice(candidates)
                    recievers.append(reciever)
                    recievers_available.remove(reciever)
            k += 1

            # Break if we cannot find a solution after an appropriate number of tries. This indicates a combination for which a solution is impossible)
            if k > 100:
                raise ValueError("Did not find a solution after 100 iterations. Maybe there is no possible solution?")

        self.recievers = recievers
    

    def export(self, path: str):
        """Export the assigned recievers

        For each name, it saves a txt file to the provided path. The file name is the secret santa, the content of the file is the name of the reciever.
        These files can then be sent to the respective participants

        Args:
            path (str): Path to save the files
        """
        path = Path(path)
        for name, reciever in zip(self.names, self.recievers):
            fname = name + ".txt"
            with open(path / fname, "x") as f:
                f.write(reciever)