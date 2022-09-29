from secretsantasolver import SecretSantaSolver
import pytest
import random
import os


def test_init_checks():
    # Input nonunqiue names
    with pytest.raises(ValueError):
        SecretSantaSolver(names = ["Adam", "Adam", "Eve"])
    
    # Input nonunique partners
    with pytest.raises(ValueError):
        SecretSantaSolver(names = ["Adam", "Eve", "Jack"], partners = ["Eve", "Adam", "Adam"])
    
    # Input lists of unequal lengths
    with pytest.raises(ValueError):
        SecretSantaSolver(names = ["Adam", "Eve", "Jack"], partners = ["Eve", "Adam"])

    # Input partners that are not in the names list
        with pytest.raises(ValueError):
            SecretSantaSolver(names = ["Adam", "Eve"], partners = ["John", "Adam"])

def test_assign():
    names = [
        "Adam",
        "Eve",
        "Jack",
        "Jill",
        "John"
    ]

    partners = [
        "Eve",
        "Adam",
        "Jill",
        "Jack",
        ""
    ]

    SecretSanta = SecretSantaSolver(names = names, partners = partners)
    random.seed(42)
    SecretSanta.assign(prohibit_partners = True)
    assert SecretSanta.names == names
    assert SecretSanta.recievers == ["John", "Jack", "Adam", "Eve", "Jill"]
    
    SecretSanta.assign(prohibit_partners = False)
    assert SecretSanta.recievers == ["Jack", "Adam", "John", "Eve", "Jill"]

# Using pytest tmp_path fixture
def test_export(tmp_path):
    names = [
        "Adam",
        "Eve",
        "Jack"
    ]

    SecretSanta = SecretSantaSolver(names = names)
    random.seed(42)
    SecretSanta.assign()
    SecretSanta.export(tmp_path) 
    assert os.listdir(tmp_path) == ["Eve.txt", "Jack.txt", "Adam.txt"] 
    
    with open(tmp_path / "Adam.txt", "r") as f: 
        content = f.read()

    assert content == "Jack"

