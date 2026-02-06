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
                                    False, loc_data.get('locked', False), loc_data.get('key_id', -1))
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

    def count_returned_items(self) -> int:
        """Count how many required items have been returned to the target location."""
        target_loc_id = 1
        target_loc = self.get_location(target_loc_id)
        required_items = ["usb_drive", "laptop_charger", "lucky_mug"]
        count = 0
        for item_name in required_items:
            if item_name in target_loc.items:
                count += 1
        return count

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

    def check_secret_ending(self) -> bool:
        """Check if the player triggered the secret ending.
        
        Secret ending: open_ai_api_key is in the dorm room.
        """
        target_loc_id = 1
        target_loc = self.get_location(target_loc_id)
        return "open_ai_api_key" in target_loc.items


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
    menu = ["look", "inventory", "score", "log", "map", "quit", "help", "examine"]  # Regular menu options available at each location
    
    # Command aliases
    aliases = {
        "n": "go north",
        "s": "go south",
        "e": "go east",
        "w": "go west",
        "u": "go up",
        "d": "go down",
        "i": "inventory",
        "x": "examine",
        "l": "look"
    }
    
    choice = ""
    
    # Display intro
    print("=" * 60)
    print(" CSC111 PROJECT ADVENTURE: THE MISSING ITEMS ".center(60))
    print("=" * 60)
    print()
    print("OBJECTIVE: You have a critical project deadline approaching!")
    print("Find and return these items to your Dorm Room:")
    print("  • USB Drive (your project backup)")
    print("  • Laptop Charger (you need power!)")
    print("  • Lucky Mug (essential for success)")
    print()
    print("SELECT DIFFICULTY:")
    print("  1. Easy (40 moves)")
    print("  2. Normal (30 moves)")
    print()
    
    difficulty = ""
    while difficulty not in ["1", "2"]:
        difficulty = input("Enter difficulty (1/2): ").strip()
        if difficulty not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")
    
    if difficulty == "1":
        game.max_moves = 40
        print("\nDifficulty: EASY - You have 40 moves.")
    else:
        game.max_moves = 30
        print("\nDifficulty: NORMAL - You have 30 moves.")
    
    print("\nQUICK COMMANDS: n/s/e/w/u/d (directions), i (inventory), x (examine)")
    print("Type 'help' anytime for full command list.")
    print()
    print("⚡ SPEEDRUN CHALLENGE: Win in under 20 moves for an achievement! ⚡")
    print()
    input("Press ENTER to begin...")
    print()

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
        
        # Move warning and status
        moves_left = game.max_moves - game.moves
        items_returned = game.count_returned_items()
        if moves_left <= 5 and moves_left > 0:
            print(f" ⚠ WARNING: {moves_left} MOVES LEFT! ⚠ ".center(60))
            print(f" MOVES: {game.moves}/{game.max_moves}  |  ITEMS: {items_returned}/3 ".center(60))
        else:
            print(f" MOVES: {game.moves}/{game.max_moves}  |  ITEMS: {items_returned}/3 ".center(60))
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

        # Display exits summary and directional cross
        direction_commands = {
            "north": "go north",
            "east": "go east",
            "south": "go south",
            "west": "go west",
            "up": "go up",
            "down": "go down"
        }
        exit_names = {}
        for direction, command in direction_commands.items():
            if command in location.available_commands:
                dest_id = location.available_commands[command]
                exit_names[direction] = game.get_location(dest_id).name
            else:
                exit_names[direction] = ""

        available_dirs = [d for d, cmd in direction_commands.items()
                          if cmd in location.available_commands]
        if available_dirs:
            print(f"You can go: {', '.join(available_dirs)}")
        else:
            print("You can go: nowhere")

        def format_bracket(label: str) -> str:
            return f"[{label}]" if label else "[ ]"

        north = format_bracket(exit_names['north'])
        west = format_bracket(exit_names['west'])
        east = format_bracket(exit_names['east'])
        south = format_bracket(exit_names['south'])
        up = format_bracket(exit_names['up'])
        down = format_bracket(exit_names['down'])
        you = format_bracket("You")

        col_width = max(len(north), len(west), len(east), len(south), len(up), len(down), len(you))
        indent = " " * (col_width + 1)

        print()
        if exit_names['up']:
            print(f"{indent}UP: {up}")
        print(f"{indent}{north}")
        print(f"{west.ljust(col_width)} {you.ljust(col_width)} {east.ljust(col_width)}")
        print(f"{indent}{south}")
        if exit_names['down']:
            print(f"{indent}DOWN: {down}")
        print()

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
            print("  [Interact]: take <item>, examine <item>")
        if game.inventory:
            print("  [Interact]: drop <item>")
        print("  [Aliases]: n/s/e/w/u/d (move), i (inventory), x (examine), l (look)")
        print("-" * 60)

        # Validate choice
        choice = ""
        while not choice:
            raw_choice = input("\n> ").lower().strip()
            
            # Expand aliases
            if raw_choice in aliases:
                choice = aliases[raw_choice]
            elif raw_choice.startswith("x "):
                choice = "examine " + raw_choice[2:]
            else:
                choice = raw_choice
            
            if choice in menu:
                pass
            elif choice in location.available_commands:
                pass
            elif choice == "take" or choice.startswith("take ") or choice.startswith("drop ") or choice.startswith("examine "):
                pass
            else:
                print("That was an invalid option; try again.")
                choice = ""

        print("========")
        print("You decided to:", choice)
        if choice not in menu:
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
                print("  look (l) - View the full description of the current location")
                print("  inventory (i) - Check what items you are carrying")
                print("  examine (x) <item> - Examine an item in detail")
                print("  score - Check your current score")
                print("  log - View all events that have occurred")
                print("  map - Display a map of visited locations")
                print("  take [item] - Pick up an item")
                print("  drop [item] - Drop an item")
                print("  go north/south/east/west/up/down (n/s/e/w/u/d) - Move in a direction")
                print("  quit - Exit the game")
                print("  help - Display this help message")
            elif choice == "quit":
                confirm = input("Are you sure you want to quit? (yes/no): ").lower().strip()
                if confirm in ["yes", "y"]:
                    print("Thank you for playing! Goodbye.")
                    game.ongoing = False
                else:
                    print("Continuing game...")
            elif choice == "examine":
                if location.items or game.inventory:
                    examine_item = input("Which item do you want to examine? ").lower().strip()
                    if not examine_item:
                        print("Examine cancelled.")
                    else:
                        # Check location items
                        item_obj = None
                        for loc_item in location.items:
                            if loc_item.lower() == examine_item or (examine_item == "mug" and loc_item == "lucky_mug") or (examine_item == "usb" and loc_item == "usb_drive") or (examine_item == "charger" and loc_item == "laptop_charger") or (examine_item == "t-card" and loc_item == "t_card") or (examine_item == "card" and loc_item == "t_card") or (examine_item == "api" and loc_item == "open_ai_api_key") or (examine_item == "key" and loc_item == "open_ai_api_key") or (examine_item == "server" and loc_item == "server_room_key") or (examine_item == "room" and loc_item == "server_room_key"):
                                item_obj = game.find_item_by_name(loc_item)
                                break
                        # Check inventory
                        if not item_obj:
                            for inv_item in game.inventory:
                                if inv_item.name.lower() == examine_item or (examine_item == "mug" and inv_item.name == "lucky_mug") or (examine_item == "usb" and inv_item.name == "usb_drive") or (examine_item == "charger" and inv_item.name == "laptop_charger") or (examine_item == "t-card" and inv_item.name == "t_card") or (examine_item == "card" and inv_item.name == "t_card") or (examine_item == "api" and inv_item.name == "open_ai_api_key") or (examine_item == "key" and inv_item.name == "open_ai_api_key") or (examine_item == "server" and inv_item.name == "server_room_key") or (examine_item == "room" and inv_item.name == "server_room_key"):
                                    item_obj = inv_item
                                    break
                        if item_obj:
                            print(f"\n{item_obj.name.upper()}: {item_obj.description}")
                        else:
                            print(f"There is no {examine_item} to examine here.")
                else:
                    print("There are no items to examine.")

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
            
        elif choice.startswith("examine "):
            examine_item = choice.replace("examine ", "").strip()
            # Check location items
            item_obj = None
            for loc_item in location.items:
                if loc_item.lower() == examine_item or (examine_item == "mug" and loc_item == "lucky_mug") or (examine_item == "usb" and loc_item == "usb_drive") or (examine_item == "charger" and loc_item == "laptop_charger") or (examine_item == "t-card" and loc_item == "t_card") or (examine_item == "card" and loc_item == "t_card") or (examine_item == "api" and loc_item == "open_ai_api_key") or (examine_item == "key" and loc_item == "open_ai_api_key") or (examine_item == "server" and loc_item == "server_room_key") or (examine_item == "room" and loc_item == "server_room_key"):
                    item_obj = game.find_item_by_name(loc_item)
                    break
            # Check inventory
            if not item_obj:
                for inv_item in game.inventory:
                    if inv_item.name.lower() == examine_item or (examine_item == "mug" and inv_item.name == "lucky_mug") or (examine_item == "usb" and inv_item.name == "usb_drive") or (examine_item == "charger" and inv_item.name == "laptop_charger") or (examine_item == "t-card" and inv_item.name == "t_card") or (examine_item == "card" and inv_item.name == "t_card") or (examine_item == "api" and inv_item.name == "open_ai_api_key") or (examine_item == "key" and inv_item.name == "open_ai_api_key") or (examine_item == "server" and inv_item.name == "server_room_key") or (examine_item == "room" and inv_item.name == "server_room_key"):
                        item_obj = inv_item
                        break
            if item_obj:
                print(f"\n{item_obj.name.upper()}: {item_obj.description}")
            else:
                print(f"There is no {examine_item} to examine here.")
                
        elif choice == "take" or choice.startswith("take "):
            if choice == "take":
                if not location.items:
                    print("There is nothing to take here.")
                    continue
                if len(location.items) == 1:
                    item_name = location.items[0]
                else:
                    print(f"Items here: {', '.join(location.items)}")
                    item_name = input("Which item do you want to take? ").lower().strip()
                    if not item_name:
                        print("Take cancelled.")
                        continue
            else:
                item_name = choice.replace("take ", "").strip()
            # Special case for "mug" alias or exact matches
            items_to_check = location.items[:]
            found = False
            for loc_item in items_to_check:
                if loc_item.lower() == item_name.lower() or (item_name == "mug" and loc_item == "lucky_mug") or (item_name == "usb" and loc_item == "usb_drive") or (item_name == "charger" and loc_item == "laptop_charger") or (item_name == "t-card" and loc_item == "t_card") or (item_name == "card" and loc_item == "t_card") or (item_name == "api" and loc_item == "open_ai_api_key") or (item_name == "key" and loc_item == "open_ai_api_key") or (item_name == "server" and loc_item == "server_room_key") or (item_name == "room" and loc_item == "server_room_key"):
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
                if item.name.lower() == item_name.lower() or (item_name == "mug" and item.name == "lucky_mug") or (item_name == "usb" and item.name == "usb_drive") or (item_name == "charger" and item.name == "laptop_charger") or (item_name == "t-card" and item.name == "t_card") or (item_name == "card" and item.name == "t_card") or (item_name == "api" and item.name == "open_ai_api_key") or (item_name == "key" and item.name == "open_ai_api_key") or (item_name == "server" and item.name == "server_room_key") or (item_name == "room" and item.name == "server_room_key"):
                    item_obj = item
                    break
            
            if item_obj:
                game.inventory.remove(item_obj)
                location.items.append(item_obj.name)
                print(f"You dropped the {item_obj.name}.")
                
                # Check scoring
                if location.id_num == item_obj.target_position:
                    game.increase_score(item_obj.target_points)
                    # Show progress
                    items_count = game.count_returned_items()
                    if item_obj.name in ["usb_drive", "laptop_charger", "lucky_mug"]:
                        print(f"✓ Required item returned! ({items_count}/3 items back)")
                
                # Check for secret ending FIRST
                if game.check_secret_ending():
                    print("\n" + "=" * 60)
                    print(" 🤖 SECRET ENDING UNLOCKED! 🤖 ".center(60))
                    print("=" * 60)
                    print()
                    print("You stare at the OpenAI API key in your hand...")
                    print("'Why work hard when AI can do it for me?' you think.")
                    print()
                    print("You fire up your laptop and let the AI complete your assignment.")
                    print("You kick back, cross your hands behind your head and smile, relaxing while the code writes itself.")
                    print("'This is too easy!' you laugh, submitting the perfect project.")
                    print()
                    print("Three days later...")
                    print()
                    print("An email from the Academic Integrity Office appears in your inbox.")
                    print("Your TA noticed the AI-generated patterns in your code.")
                    print("The plagiarism detector flagged your entire submission.")
                    print()
                    print("📧 You have been charged with academic dishonesty.")
                    print("📉 Assignment grade: 0%")
                    print("⚖️  Academic penalty: Suspension from the course")
                    print()
                    print("💡 LESSON LEARNED: There are no shortcuts to real learning!")
                    print()
                    print(f"Moves used: {game.moves}")
                    print("=" * 60)
                    print()
                    print("          GAME OVER - SECRET ENDING")
                    print()
                    game.ongoing = False
                    
                # Check win condition
                elif game.check_win():
                    print("\n" + "=" * 60)
                    print(" 🎉🎊 MISSION COMPLETE! 🎊🎉 ".center(60))
                    print("=" * 60)
                    print()
                    print("🏆 YOU DID IT! 🏆")
                    print()
                    print("With all three items safely back in your dorm room,")
                    print("you fire up your laptop and submit the project!")
                    print()
                    print("The progress bar crawls to 100%...")
                    print("✓ Project submitted successfully!")
                    print()
                    print("You lean back with a satisfied grin. Crisis averted!")
                    print()
                    print("────────────────────────────────────────────────────────────")
                    print(f"   📊 FINAL STATS")
                    print("────────────────────────────────────────────────────────────")
                    print(f"   Moves Used: {game.moves}/{game.max_moves}")
                    print(f"   Final Score: {game.score} points")
                    print(f"   Items Recovered: 3/3 ✓")
                    if game.moves < 20:
                        print()
                        print("   ⚡⚡⚡ ACHIEVEMENT UNLOCKED! ⚡⚡⚡")
                        print("   🏃 SPEEDRUNNER: Completed in under 20 moves!")
                        print("   You're a legend! 🌟")
                    print()
                    print("────────────────────────────────────────────────────────────")
                    print()
                    print("Thanks for saving the day! See you next deadline! 👋")
                    print("=" * 60)
                    game.ongoing = False
            else:
                print(f"You are not carrying {item_name}.")

