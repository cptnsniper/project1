"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate
an entire playthrough of the game. Please consult the project handout for
instructions and details.

You can copy/paste your code from Assignment 1 into this file, and modify it as
needed to work with your game.

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
from event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    # TODO: Copy/paste your code from A1, and make adjustments as needed
    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """
        Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from the location at initial_location_id
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        # Add first event (initial location, no command to reach it)
        first_location = self._game.get_location()
        first_event = Event(first_location.id_num, first_location.long_description)
        self._events.add_event(first_event, None)

        # Generate the remaining events based on the commands and initial location
        self.generate_events(commands, first_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """
        Generate events in this simulation, based on current_location and commands, a valid list of commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from current_location
        """
        for command in commands:
            # Get next location ID from available_commands
            if command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
            else:
                next_location_id = current_location.id_num

            # Update game state
            self._game.current_location_id = next_location_id

            # Get the new location
            next_location = self._game.get_location()

            # Create event for the new location
            new_event = Event(next_location.id_num, next_location.long_description)

            # Add event with the command that led to it
            self._events.add_event(new_event, command)

            # Update current_location for next iteration
            current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        return self._events.get_id_log()

    def run(self) -> None:
        """
        Run the game simulation and log location descriptions.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    # TODO: Modify the code below to provide a walkthrough of commands needed to win and lose the game
    win_walkthrough = [
        "take t_card",
        "go north",
        "go east",
        "go north",
        "take usb_drive",
        "go south",
        "go south",
        "take laptop_charger",
        "go north",
        "go north",
        "go east",
        "take lucky_mug",
        "go west",
        "go south",
        "go west",
        "go south",
        "drop usb_drive",
        "drop laptop_charger",
        "drop lucky_mug"
    ]
    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["go north", "go south"] * 11  # Exceeds max moves (20)
    expected_log = [1] + [2, 1] * 11
    # Uncomment the line below to test your demo
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == sim.get_id_log()

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    inventory_demo = ["take t_card", "go north", "go east", "go north", "take usb_drive", "inventory"]
    expected_log = [1, 1, 2, 3, 4, 4, 4]
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    assert expected_log == sim.get_id_log()

    # Note on scores_demo: Laptop charger is in Bahen (Loc 5), which is South of UC (Loc 3).
    # UC <-> Bahen does not require T-Card (only Robarts Loc 4 does).
    # Dorm (1) -> Hallway (2) -> UC (3) -> Bahen (5).
    # So scores_demo does NOT necessarily need t_card if it stays clear of Robarts?
    # Actually, let's just make it safe by taking the card anyway so we test picking it up.
    scores_demo = ["take t_card", "score", "go north", "go east", "go south", "take laptop_charger", "score"]
    expected_log = [1, 1, 1, 2, 3, 5, 5, 5]
    sim = AdventureGameSimulation('game_data.json', 1, scores_demo)
    assert expected_log == sim.get_id_log()

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # sim = AdventureGameSimulation(...)
    # assert expected_log == sim.get_id_log()

    # Note: You can add more code below for your own testing purposes
