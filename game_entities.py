"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: unique identifier for this location
        - brief_description: a brief description of the location
        - long_description: a detailed description of the location
        - available_commands: a dictionary of commands available at this location
        - items: a list of items available at this location
        - visited: whether the player has visited this location

    Representation Invariants:
        - id_num is a unique integer identifier
        - brief_description and long_description are non-empty strings
        - available_commands is a dictionary of valid commands
        - items is a list of strings
        - visited is True or False
    """

    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool = False


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - id: unique identifier for this item
        - name: the name of the item
        - description: a description of what the item is
        - can_take: whether the player is allowed to take this item

    Representation Invariants:
        - id is a unique string identifier
        - name is a non-empty string
        - can_take is True or False
    """

    id: str
    name: str
    description: str
    can_take: bool


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })
