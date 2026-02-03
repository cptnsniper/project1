"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the ID of the current location of the player in the game
        - ongoing: whether the game is ongoing (True) or has ended (False)
        - inventory: list of Item objects the player is carrying
        - score: the player's current score

    Representation Invariants:
        - self.current_location_id in self._locations
        - self.ongoing is True or False
        - self.score >= 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int
    ongoing: bool
    inventory: list[Item]
    score: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.inventory = []  # items the player is carrying
        self.score = 0  # player's score

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []

        for item_data in data['items']:
            item_obj = Item(item_data['id'], item_data['name'], item_data['description'], item_data['can_take'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def add_item_to_inventory(self, item: Item) -> None:
        """Add an item to the player's inventory."""
        self.inventory.append(item)

    def display_inventory(self) -> None:
        """Display the player's current inventory."""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You are carrying:")
            for item in self.inventory:
                print(f"  - {item.name}: {item.description}")

    def increase_score(self, points: int) -> None:
        """Increase the player's score by the given number of points."""
        self.score += points
        print(f"Score increased by {points}! Total score: {self.score}")


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit", "help"]  # Regular menu options available at each location
    choice = ""

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        event = Event(game.current_location_id, choice)
        game_log.add_event(event)

        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE
        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit, help")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "inventory":
                game.display_inventory()
            elif choice == "score":
                print(f"Your current score: {game.score}")
            elif choice == "look":
                print(location.long_description)
            elif choice == "help":
                print("Available commands:")
                print("  look - View the full description of the current location")
                print("  inventory - Check what items you are carrying")
                print("  score - Check your current score")
                print("  log - View all events that have occurred")
                print("  quit - Exit the game")
                print("  help - Display this help message")
            elif choice == "quit":
                print("Thank you for playing! Goodbye.")
                game.ongoing = False

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            
            # Check if the result is an integer (location change) or a string (item interaction)
            if isinstance(result, int):
                game.current_location_id = result
                print(f"You move to location {game.current_location_id}.")
            else:
                # Handle item interactions (e.g., taking or using an item)
                if choice.startswith("take"):
                    item_name = choice.replace("take ", "").strip()
                    if item_name in location.items:
                        print(f"You picked up the {item_name}.")
                        location.items.remove(item_name)
                    else:
                        print(f"You cannot take {item_name}.")
                elif choice.startswith("use"):
                    item_name = choice.replace("use ", "").strip()
                    print(f"You used the {item_name}.")
                else:
                    print(f"You performed the action: {choice}")
