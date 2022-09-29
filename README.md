# SecretSantaSolver

## Introduction

We all know the pain of secret santas in the family. Not only will you eventually need to come up with a creative and personal gift for you loved ones, one has to first actually find a way to assign your future recipient. This often involves many rounds of discussions, scribbling down notes, drawing your own name and thus, frustration. But fear no more. With SecretSantaSolver, you can easily do these assignments in a quick and fun way!

## Installation

SecretSantaSolver comes with no dependencies. The recommended way to install SecretSantaSolver is via the `pip` command

```
pip  install SecretSantaSolver
```

Alternatively, you can also install from the github source using poetry

```
git clone 
cd secretsantasolver
poetry install 
```

## Usage

The main (and only) class is `SecretSantaSolver`
You need to pass in the names of the persons involved. 
To enable you to also hand over the data, you can export the assigned pairs using the `export` method. This will write a `.txt` file per name to the provided path. Each file contains their secret santa, that you can send over via mail or other means.

```
import SecretSantaSolver 

names = [
    "Alex",
    "Jack",
    "Jill
]

santasolver = SecretSantaSolver.SecretSantaSolver(names = names)
santasolver.assign()
santasolver.export("path/to/folder")
```

If you want to prevent partners being the secretsanta of each other, you can also pass in the names of their partners and set the `prohibit_partners` flag to `True`:

```
names = [
    "Alex",
    "Jack",
    "Jill
]

partners = [
    "Jill",
    "",
    "Alex"
]

santasolver = SecretSantaSolver.SecretSantaSolver(names = names, partners = partners)
santasolver.assign(prohibit_partners = True)
santasolver.export("path/to/folder")
```