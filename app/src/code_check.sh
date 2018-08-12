#!/usr/bin/bash

# Updade pip just in case you are running an older version of pip
sudo pip install --upgrade pip

# pep8 is being deprecated and replaced by pycodestyle on some future date
sudo pip install pycodestyle

# Run the pycodestyle application on each python script to be analyzed
pycodestyle --first Abilities.py
pycodestyle --first Character.py
pycodestyle --first CharacterPC.py
pycodestyle --first CharacterNPC.py
pycodestyle --first CharacterVPC.py
pycodestyle --first Clock.py
pycodestyle --first Dice.py
pycodestyle --first Enchantress.py
pycodestyle --first Geography.py
pycodestyle --first Library.py
pycodestyle --first Schools.py
pycodestyle --first Smithy.py
pycodestyle --first Weapon.py

# Clean-up
rm *.pyc 2> /dev/null
