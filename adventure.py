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
        - moves: the number of moves the player has taken so far
        - max_moves: the maximum number of moves allowed before game over

    Representation Invariants:
        - self.current_location_id in self._locations
        - self.ongoing is True or False
        - self.score >= 0
        - self.moves >= 0
        - self.max_moves > 0
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
    moves: int
    max_moves: int

    # Constants
    MAX_MOVES = 20

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
        self.moves = 0  # player's moves
        self.max_moves = AdventureGame.MAX_MOVES  # max number of moves

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_commands'], loc_data['items'],
                                    False, loc_data.get('locked', False), loc_data.get('key_id', None))
            locations[loc_data['id']] = location_obj

        items = []

        for item_data in data['items']:
            item_obj = Item(item_data['id'], item_data['name'], item_data['description'], item_data['can_take'],
                            item_data['target_position'], item_data['target_points'])
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

    def display_map(self) -> None:
        """Display a map showing visited locations and unexplored paths."""
        print("=== MAP ===")

        # Collect visited locations
        visited_locations = [loc for loc in self._locations.values() if loc.visited]

        if not visited_locations:
            print("You haven't explored anywhere yet.")
            return

        for location in visited_locations:
            # Mark current location
            if location.id_num == self.current_location_id:
                print(f"\n[*] {location.name} (YOU ARE HERE)")
            else:
                print(f"\n[ ] {location.name}")

            # Show connections
            for command, dest_id in location.available_commands.items():
                dest_location = self._locations.get(dest_id)
                if dest_location and dest_location.visited:
                    print(f"    {command} -> {dest_location.name}")
                else:
                    print(f"    {command} -> ?")

    def find_item_by_name(self, name: str) -> Optional[Item]:
        """Return the Item object with the given name, or None if not found.
        
        Preconditions:
            - name is not empty
        """
        for item in self._items:
            if item.name.lower() == name.lower():
                return item
        return None

    def check_win(self) -> bool:
        """Check if the player has won the game.
        
        The player wins if they have returned all required items (usb_drive, laptop_charger, lucky_mug)
        to the target location (Location 1: Dorm Room).
        """
        # Win condition: specific items are at their target positions
        # Required: usb_drive (id 1), laptop_charger (id 2), lucky_mug (id 3)
        # Target for all is Dorm Room (id 1)
        
        target_loc_id = 1
        target_loc = self.get_location(target_loc_id)
        
        required_items = ["usb_drive", "laptop_charger", "lucky_mug"]
        
        for item_name in required_items:
            if item_name not in target_loc.items:
                return False
        return True


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "map", "quit", "help"]  # Regular menu options available at each location
    choice = ""

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Check lose condition
        if game.moves >= game.max_moves:
            print("GAME OVER: You have run out of time!")
            game.ongoing = False
            break

        location = game.get_location()

        #  Note that the <choice> variable should be the command which led to this event
        event = Event(game.current_location_id, location.long_description)
        game_log.add_event(event, choice if choice else None)

        # --- UI DISPLAY ---
        print("\n" * 2)
        print("=" * 60)
        print(f" MOVES: {game.moves}/{game.max_moves}  |  SCORE: {game.score} ".center(60))
        print("=" * 60)

        # Print Location Header (REQUIRED)
        print(f"LOCATION {location.id_num}: {location.name.upper()}")
        print("-" * 60)

        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)
        print("-" * 60)

        # Display Items
        if location.items:
            print(f" [!] ITEMS HERE: {', '.join(location.items)}")
        else:
            print(" [ ] No items visible.")

        # Display possible actions
        print("-" * 60)
        print(" OPTIONS:")
        print("  [System]: look, inventory, score, log, map, help, quit")
        
        move_cmds = [cmd for cmd in location.available_commands if cmd.startswith("go")]
        other_cmds = [cmd for cmd in location.available_commands if not cmd.startswith("go")]
        
        if move_cmds:
            print(f"  [Travel]: {', '.join(move_cmds)}")
        if other_cmds:
            print(f"  [Action]: {', '.join(other_cmds)}")
        
        if location.items:
            print("  [Interact]: take <item>")
        if game.inventory:
            print("  [Interact]: drop <item>")
        print("-" * 60)

        # Validate choice
        choice = ""
        while not choice:
            choice = input("\n> ").lower().strip()
            
            if choice in menu:
                pass
            elif choice in location.available_commands:
                pass
            elif choice.startswith("take ") or choice.startswith("drop "):
                pass
            else:
                print("That was an invalid option; try again.")
                choice = ""

        print("========")
        print("You decided to:", choice)
        game.moves += 1

        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "inventory":
                game.display_inventory()
            elif choice == "score":
                print(f"Your current score: {game.score}")
            elif choice == "look":
                print(location.long_description)
            elif choice == "map":
                game.display_map()
            elif choice == "help":
                print("Available commands:")
                print("  look - View the full description of the current location")
                print("  inventory - Check what items you are carrying")
                print("  score - Check your current score")
                print("  log - View all events that have occurred")
                print("  map - Display a map of visited locations")
                print("  take [item] - Pick up an item")
                print("  drop [item] - Drop an item")
                print("  quit - Exit the game")
                print("  help - Display this help message")
            elif choice == "quit":
                print("Thank you for playing! Goodbye.")
                game.ongoing = False

        elif choice in location.available_commands:
            # Handle movement
            next_location_id = location.available_commands[choice]
            next_location = game.get_location(next_location_id)
            
            can_move = True
            
            # Check if location is locked
            if next_location.locked:
                has_key = False
                key_name = ""
                # Find key name for feedback
                for item in game._items:
                    if item.id == next_location.key_id:
                        key_name = item.name
                        break
                
                # Check player inventory for the key
                for item in game.inventory:
                    if item.id == next_location.key_id:
                        has_key = True
                        break
                
                if has_key:
                    print(f"You swipe your {key_name} and the door unlocks.")
                    next_location.locked = False # Unlock permanently
                else:
                    print(f"The entrance to {next_location.name} is locked.")
                    print(f"You need a {key_name if key_name else 'key capability'} to enter.")
                    can_move = False

            if can_move:
                game.current_location_id = next_location_id
                print(f"You move to location {game.current_location_id}.")
            
        elif choice.startswith("take "):
            item_name = choice.replace("take ", "").strip()
            # Special case for "mug" alias or exact matches
            items_to_check = location.items[:]
            found = False
            for loc_item in items_to_check:
                if loc_item.lower() == item_name.lower() or (item_name == "mug" and loc_item == "lucky_mug") or (item_name == "usb" and loc_item == "usb_drive") or (item_name == "charger" and loc_item == "laptop_charger") or (item_name == "t-card" and loc_item == "t_card") or (item_name == "card" and loc_item == "t_card"):
                    item_obj = game.find_item_by_name(loc_item)
                    if item_obj and item_obj.can_take:
                        game.add_item_to_inventory(item_obj)
                        location.items.remove(loc_item)
                        print(f"You picked up the {loc_item}.")
                        found = True
                        break
                    else:
                        print(f"You cannot take {item_name}.")
                        found = True
                        break
            if not found:
                 print(f"There is no {item_name} here.")
                
        elif choice.startswith("drop "):
            item_name = choice.replace("drop ", "").strip()
            # Find item in inventory
            item_obj = None
            for item in game.inventory:
                if item.name.lower() == item_name.lower() or (item_name == "mug" and item.name == "lucky_mug") or (item_name == "usb" and item.name == "usb_drive") or (item_name == "charger" and item.name == "laptop_charger") or (item_name == "t-card" and item.name == "t_card") or (item_name == "card" and item.name == "t_card"):
                    item_obj = item
                    break
            
            if item_obj:
                game.inventory.remove(item_obj)
                location.items.append(item_obj.name)
                print(f"You dropped the {item_obj.name}.")
                
                # Check scoring
                if location.id_num == item_obj.target_position:
                    game.increase_score(item_obj.target_points)
                    
                # Check win condition
                if game.check_win():
                    print("CONGRATULATIONS! You have returned all missing items and saved the project!")
                    game.ongoing = False
            else:
                print(f"You are not carrying {item_name}.")

