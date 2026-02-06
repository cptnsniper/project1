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
        - name: the name of this location
        - brief_description: a brief description of the location
        - long_description: a detailed description of the location
        - available_commands: a dictionary of commands available at this location
        - items: a list of items available at this location
        - visited: whether the player has visited this location
        - locked: whether the location is locked and requires a key to enter
        - key_id: the ID of the item required to unlock this location (-1 if no key is needed)

    Representation Invariants:
        - id_num is a unique integer identifier
        - name is a non-empty string
        - brief_description and long_description are non-empty strings
        - available_commands is a dictionary of valid commands
        - items is a list of strings
        - visited is True or False
        - locked is True or False
    """

    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool = False
    locked: bool = False
    key_id: int = -1


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - id: unique identifier for this item
        - name: the name of the item
        - description: a description of what the item is
        - can_take: whether the player is allowed to take this item
        - target_position: the location ID where this item should be delivered
        - target_points: the points awarded for delivering this item

    Representation Invariants:
        - id is a unique identifier
        - name is a non-empty string
        - can_take is True or False
        - target_position is a valid location ID
        - target_points is a non-negative integer
    """

    id: int
    name: str
    description: str
    can_take: bool
    target_position: int
    target_points: int


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
