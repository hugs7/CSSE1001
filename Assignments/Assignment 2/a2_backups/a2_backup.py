"""
End of Dayz
Assignment 2
Semester 1, 2021
CSSE1001/CSSE7030

A text-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

from typing import Tuple, Optional, Dict, List
import random
from a2_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "Hugo Burton, 46985123"
__email__ = "hugo.burton@uqconnect.edu.au"


class Entity:
    """
    Entity is an abstract class that is used to represent anything that can
    appear on the game's grid.
    For example: the game grid will always have a player, so a player is
    considered a type of entity. A game grid may also have a zombie, so a
    zombie is considered a type of entity.
    """

    def step(self, position: Position, game: "Game") -> None:
        """
        The step method is called on every entity in the game grid after each
        move made by the player, it controls what actions an entity will perform
        during the step event
        The abstract Entity class will not perform any action during the step
        event. Therefore, this method should do nothing.
        :param position: Position of this entity when the step event is
        triggered.
        :param game: The current instance of the game.
        :return: None.
        """

        pass

    def display(self) -> str:
        """
        Returns the character used to represent this entity in a text-based
        grid.
        :return: The character used to represent the entity (ie. P, Z, H, G, T)
        """

        raise NotImplementedError

    def __repr__(self) -> str:
        """
        A representation of the Entity.
        :return: A string representing the Entity
        """

        if isinstance(self, Pickup):
            pickup_names = {
                GARLIC: "Garlic",
                CROSSBOW: "Crossbow"
            }

            return "{0}({1})".format(pickup_names.get(self.display()),
                                     self.get_lifetime())
        elif isinstance(self, (Player, Zombie, TrackingZombie, Hospital)):
            pickup_names = {
                PLAYER: "Player",
                ZOMBIE: "Zombie",
                TRACKING_ZOMBIE: "TrackingZombie",
                HOSPITAL: "Hospital"
            }

            return "{0}()".format(pickup_names.get(self.display()))
        else:
            return "Entity()"


class Pickup(Entity):
    """
    Inherits from Entity.
    A Pickup is a special type of entity that the player is able to pickup and
    hold in their inventory.
    The Pickup class is an abstract class.
    """

    def __init__(self):
        """
        When a Pickup entity is created, the lifetime of the entity should be
        equal to its maximum lifetime (durability).
        """

        self._lifetime = LIFETIMES.get(self.display())
        self._health = self.get_durability()

    def display(self) -> str:
        """
        Display the pickup object.
        :return: NotImplementedError
        """

        raise NotImplementedError

    def get_durability(self) -> int:
        """
        Return the maximum number of steps the player is able to take while
        holding this item. After the player takes this many steps, the item
        disappears.
        The abstract Pickup class should never be placed in the grid, so this
        method should be implemented by the subclasses of Pickup only.
        To indicate that this method needs to be implemented by subclasses, this
        method should raise a NotImplementedError.
        :return: NotImplementedError.
        """

        raise NotImplementedError

    def get_lifetime(self) -> int:
        """
        Return the remaining steps a player can take with this instance of the
        item before the item disappears from the player's inventory.
        :return: Number of remaining steps player can take with item as int.
        """

        return self._health

    def hold(self) -> None:
        """
        The hold method is called on every pickup entity that the player is
        holding each time the player takes a step.
        This will result in the remaining lifetime of the pickup entity
        decreasing by one.
        :return: None
        """

        self._health -= 1


class Garlic(Pickup):
    """
    Inherits from Pickup.
    Garlic is an entity which the player can pickup.
    While the player is holding a garlic entity they cannot be infected ba a
    zombie. If they collide with a zombie while holding a garlic, the zombie
    will perish.
    """

    def __init__(self):
        """
        Constructor for the Garlic Entity.
        """

        super().__init__()

    def display(self) -> str:
        """
        Return the character used to represent the garlic entity in a text-based
        grid.
        A garlic should be represented by the 'G' character.
        :return:
        """

        return GARLIC

    def get_durability(self) -> int:
        """
        Return the durability of a garlic.
        A player can only hold a garlic entry for 10 steps.
        :return: Durability of garlic as int.
        """

        return LIFETIMES.get(GARLIC)


class Crossbow(Pickup):
    """
    Inherits from Pickup.
    Crossbow is an entity which the player can pickup.
    While the player is holding a crossbow entity they are able to use the fire
    action to launch a projectile in a given direction, removing the first
    zombie in that direction.
    """

    def __init__(self):
        """
        Constructor for the Crossbow Entity.
        """

        super().__init__()

    def display(self) -> str:
        """
        Return the character used to represent the crossbow entity in a
        text-based grid.
        A crossbow should be represented by the 'C' character.
        :return:
        """

        return CROSSBOW

    def get_durability(self) -> int:
        """
        Return the durability of a crossbow.
        A player can only hold a crossbow entity for 5 steps.
        :return: Durability of crossbow as int
        """

        return LIFETIMES.get(CROSSBOW)


class Hospital(Entity):
    """
    Inherits from Entity.
    A hospital is a subclass of the entity class that represents the hospital in
    the grid.
    The hospital is the entity that the player has to reach in order to win the
    game.
    """

    def display(self) -> str:
        """
        Returns the character 'H' for hospital.
        :return: Character for hospital.
        """

        return HOSPITAL


class Player(Entity):
    """
    Inherits from Entity.
    A player is a subclass of the entity class that represents the player that
    the user controls on the game grid.
    """

    def display(self) -> str:
        """
        Returns the character 'P' for player.
        :return: Character for player
        """

        return PLAYER


class VulnerablePlayer(Player):
    """
    Inherits from Player.
    The VulnerablePlayer class is a subclass of the Player, this class extends
    the player by allowing them to become infected.
    """

    def __init__(self):
        """
        When an object of the VulnerablePlayer is constructed, the player
        should not be infected.
        """

        self._infected = False

    def infect(self) -> None:
        """
        When the infect method is called, the player becomes infected and
        subsequent calls to is_infected return true.
        :return: None
        """

        self._infected = True

    def is_infected(self) -> bool:
        """
        Returns the current infectious state of a player.
        :return: True if player is infected, false if not.
        """

        return self._infected


class HoldingPlayer(VulnerablePlayer):
    """
    Inherits from VulnerablePlayer.
    The HoldingPlayer is a subclass of VulnerablePlayer that extends the
    existing functionality of the player.
    In particular, a holding player will now keep an inventory.
    """

    def __init__(self):
        """
        Constructor for HoldingPlayer.
        Instantiates an inventory for the HoldingPlayer.
        """

        super().__init__()
        self._holding_player_inventory = Inventory()

    def get_inventory(self) -> "Inventory":
        """
        Return the instance of the Inventory class that represents the player's
        inventory.
        :return: Instance of inventory of instantiated player.
        """

        return self._holding_player_inventory

    def infect(self) -> None:
        """
        Extend the existing infect method so that the player is immune to
        becoming infected if they are holding garlic.
        :return: None.
        """

        if not self.get_inventory().contains(GARLIC):
            super(HoldingPlayer, self).infect()

    def step(self, position: Position, game: "Game") -> None:
        """
        The step method for a holding player will notify its inventory that a
        step event has occurred.
        :param position: The position of this entity when the step event is
        triggered.
        :param game: The current game being played.
        :return: None.
        """

        self._holding_player_inventory.step()


class Zombie(Entity):
    """
    Inherits from Entity.
    The Zombie entity will wander the grid at random.
    The movement of a zombie is triggered by the player performing an action.
    i.e. the zombie moves during each step event.
    """

    def display(self) -> str:
        """
        Return the character used to represent the zombie entity in a
        text-based grid.
        A zombie should be represented by the 'Z' character.
        :return: Character representing Zombie ('Z').
        """

        return ZOMBIE

    def step(self, position: Position, game: "Game") -> None:
        """
        The step method for the zombie entity will move the zombie in a random
        direction.
        To implement this, generate a list of the possible directions to move
        in a random order by calling the random_directions function from the
        support code. Check each of the directions to see if the resultant
        position is available. The resultant position is the position you reach
        from moving in a given direction.
        If none of the resultant positions are available, do not move the
        zombie.
        If the position the zombie is going to move contains the player, the
        zombie should infect the player but not move to that position.
        :param position: The position of this zombie when the step event is
        triggered.
        :param game: The current game being played.
        :return: None.
        """

        final_positions = []

        # get all final positions given all moves
        for i in random_directions():
            x, y = i
            offset_position = Position(x, y)
            final_position = position.add(offset_position)
            if game.get_grid().in_bounds(final_position):
                entity_final_pos = game.get_grid().get_entity(final_position)
                if entity_final_pos is None:
                    final_positions.append(final_position)
                elif entity_final_pos is not None:
                    if entity_final_pos.display() == PLAYER:
                        final_positions.append(final_position)

        if final_positions:     # If there is/are legal moves
            chosen_position = random.choice(final_positions)
            entity_at_pos = game.get_grid().get_entity(chosen_position)
            if entity_at_pos is None:
                game.get_grid().move_entity(position, chosen_position)
            elif entity_at_pos is not None:
                if entity_at_pos.display() == PLAYER:
                    game.get_player().infect()


class TrackingZombie(Zombie):
    """
    Inherits from Zombie.
    The TrackingZombie is a more intelligent type of zombie which is able to see
    the player and move closer to the player.
    """

    def display(self) -> str:
        """
        Return the character used to represent the tracking zombie entity in a
        text-based grid.
        A tracking zombie should be represented by the 'T' character.
        :return: Character representing Tracking Zombie ('T').
        """

        return TRACKING_ZOMBIE

    def step(self, position: Position, game: "Game") -> None:
        """
        The step method for the tracking zombie will move the tracking zombie in
        the best possible direction to move closer to the player.
        To implement this, sort a list of possible directions to minimise the
        distance between the resultant position and the player's position. The
        resultant position is the position resulting from moving the tracking
        zombie in a direction.
        If there are multiple directions that result in being the same distance
        from the player, the direction should be picked in preference order
        picking 'W' first followed by 'S', 'N', and finally 'E'.
        :param position: The position of this zombie when the step event is
        triggered.
        :param game: The current game being played.
        :return: None.
        """

        final_positions = []
        player_position = game.get_grid().find_player()

        ordered_offsets = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        #                     A        S       W        D

        infect_player = False

        # get all final positions given all moves
        for i in ordered_offsets:
            x, y = i
            offset_position = Position(x, y)
            final_position = position.add(offset_position)
            if game.get_grid().in_bounds(final_position):
                entity_final_pos = game.get_grid().get_entity(final_position)
                if entity_final_pos is None:
                    # determine distance to player.
                    dis_to_player = final_position.distance(player_position)
                    # add to list
                    final_positions.append((position.add(offset_position),
                                            dis_to_player))
                if entity_final_pos is not None:
                    if entity_final_pos.display() == PLAYER:
                        infect_player = True
                        break

        if infect_player:
            game.get_player().infect()
        elif final_positions:
            # loop through moves to determine least distance to player
            min_distance = 999
            best_move = position
            for move in reversed(final_positions):
                final_position, distance = move
                if distance < min_distance:
                    min_distance = distance
                    best_move = final_position

            if game.get_grid().get_entity(best_move) == PLAYER:
                game.get_player().infect()
            elif game.get_grid().get_entity(best_move) is None:
                game.get_grid().move_entity(position, best_move)


class Grid:
    """
    The Grid class is used to represent the 2D grid of entities.
    The grid can vary in size but it is always a square.
    Each (x,y) position in the grid can only contain one entity at a time.
    """

    def __init__(self, side: int):
        """
        A grid is constructed with a size that dictates the length and width of
        the grid.
        Initially, a grid does not contain any entities.
        :param side: the magnitude of any side of the square grid as int.
        """

        self._size = side
        self._grid = [[None] * self.get_size() for _ in range(self.get_size())]
        # self._grid is an 2D array that signifies the grid

    def add_entity(self, position: Position, entity: Entity) -> None:
        """
        Place a given entity at a given position of the grid.
        If there is already an entity at the given position, the given entity
        will replace the existing entity.
        If the given position is outside the bounds of the grid, the entity
        should not be added.
        :param position: An (x,y) position in the grid to place the entity.
        :param entity: The entity to place on the grid.
        :return: None.
        """

        x, y = position.get_x(), position.get_y()
        self._grid[y][x] = entity

    def find_player(self) -> Optional[Position]:
        """
        Return the position of the player within the grid.
        Return None if there is no player in the grid.
        If the grid has multiple players (which it should not), returning any
        of the player positions is sufficient.
        :return: Position of player or none if no player present in grid.
        """

        for x in range(self.get_size()):        # for each column
            for y in range(self.get_size()):    # for each row
                position_pass = Position(x, y)
                if self.get_entity(position_pass) is not None:
                    if self.get_entity(position_pass).display() == PLAYER:
                        return position_pass

    def get_entities(self) -> List[Entity]:     # need to check this function
        """
        Returns a list of all the entities in the grid.
        Updating the returned list should have no side-effects. It would not
        modify the grid.
        :return: A list of all the entities in the grid.
        """

        entities = []

        for x in range(self.get_size()):        # for each column
            for y in range(self.get_size()):    # for each row
                if self.get_entity(Position(x, y)) is not None:
                    entities.append(self.get_entity(Position(x, y)))

        return entities

    def get_entity(self, position: Position) -> Optional[Entity]:
        """
        Returns the entity that is at the given position in the grid.
        If there is no entity at the given position, returns None.
        If the given position is out of bounds, returns None.
        :param position: The (x,y) position in the grid to check for an entity.
        :return: Entity at given position in grid or None if no entity present.
        """

        x, y = position.get_x(), position.get_y()

        return self._grid[y][x]

    def get_mapping(self) -> Dict[Position, Entity]:
        """
        Return a dictionary with the position instances as the keys and entity
        instances as the values.

        For every position in the grid that has an entity, the returned
        dictionary should contain an entry with the position instance mapped to
        the entity instance.

        :return: A dictionary of entities in the grid with positions as keys and
                 entities as values.
        """

        dictionary = {}

        for y, column in enumerate(self._grid):
            for x, character in enumerate(column):
                if character is not None:
                    position = Position(x, y)
                    dictionary.update({position: self.get_entity(position)})

        return dictionary

    def get_size(self) -> int:
        """
        Returns the side length of the grid.
        :return: side length of grid.
        """

        return self._size

    def in_bounds(self, position: Position) -> bool:
        """
        Returns True if the given position is within the bounds of the grid.
        For a position to be within the bounds of the grid, both the x and y
        coordinates have to be greater than or equal to zero but less than the
        size of the grid.
        :param position: an (x,y) tuple that is used to check if within bounds
        :return: bool True or False
        """

        x, y = position.get_x(), position.get_y()

        return x in range(self._size) and y in range(self._size)

    def move_entity(self, start: Position, end: Position) -> None:
        """
        Move an entity from the given start position to the given end position.

        - If the end position or start position is out of the grid bounds, do
          not attempt to move;
        - If there is no entity at the given start position, do not attempt to
          move;
        - If there is an entity at the given end position, replace that entity
          with the entity from the start position.

        The start position should not have an entity after moving.
        :param start: The position the entity is in initially.
        :param end: The position to which the entity will be moved.
        :return: None.
        """

        # if position is in bounds
        if self.in_bounds(start) and self.in_bounds(end):
            # if no entity at start position
            if self.get_entity(start) is not None:
                # overwrite entity at end position with entity at start position
                self.add_entity(end, self.get_entity(start))
                # remove start entity
                self.remove_entity(start)

    def remove_entity(self, position: Position) -> None:
        """
        Remove the entity if any at the given position.
        :param position: position of entity to be removed.
        :return: None.
        """

        x, y = position.get_x(), position.get_y()

        self._grid[y][x] = None

    def serialize(self) -> Dict[Tuple[int, int], str]:
        """
        Serialize the grid into a dictionary that maps tuples to characters.
        The tuples should have two values, the x and y coordinate representing a
        position. The characters are the display representation of the entity at
        that position. i.e. 'P' for player, 'H' for hospital.
        Only positions that have an entity should exist in the dictionary.
        :return: Dictionary of entities with x, y coordinate with name.
        """
        grid_dict = {}

        for y, column in enumerate(self._grid):
            for x, character in enumerate(column):
                position = Position(x, y)
                # if self.get_entity(position) is not None:
                if character is not None:
                    int_index = (x, y)
                    grid_dict.update({int_index:
                                      self.get_entity(position).display()})

        return grid_dict


class Game:
    """
    The game handles some of the logic for controlling the actions of the
    player within the grid.

    The Game class stores an instance of the Grid and keeps track of the player
    within the grid so that the player can be controlled.
    """

    def __init__(self, grid):
        """
        Constructor for Game takes the grid upon which the game is being played.
        Preconditions: The grid has a player. So grid.find_player() is not None.
        """

        self._game_grid = grid

        self._steps_made = 0      # number of steps made

        # player position
        self._player_position = self.get_grid().find_player()

        # player win/lose vars
        self._player_won = False        # there is a reason for there being
        self._player_lost = False       # two different variables here.

    def direction_to_offset(self, direction: str) -> Optional[Position]:
        """
        Convert a direction, as a string, to an offset position.

        The offset position can be added to a position to move in the given
        direction.

        If the given direction is not valid, this method should return None.
        :param direction: a direction in the form of a string.
        :return: if direction is valid, return a position, otherwise None.
        """

        # OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        #             down,     up    right    left
        #               S       W        D       A

        offsets = {
            "W": 1,
            "S": 0,
            "A": 3,
            "D": 2
        }

        if direction in DIRECTIONS:
            offset = OFFSETS[offsets.get(direction)]
            return Position(offset[0], offset[1])
        else:
            return None

    def get_grid(self) -> Grid:
        """
        Return the grid on which the game is being played.
        :return: the grid on which the game is being played.
        """

        return self._game_grid

    def get_player(self) -> Optional[HoldingPlayer]:
        """
        Return the instance of the Player class in the grid.

        If there is no player in the grid, return None. If there are multiple
        players within the grid, returning any player is sufficient.
        :return: Instance of Player in Grid, or None.
        """

        player_position = self.get_grid().find_player()
        if player_position is not None:
            return self.get_grid().get_entity(player_position)

    def get_steps(self) -> int:
        """
        Return the number of steps made in the game. ie. how many times the
        step method has been called.
        :return: number of steps made.
        """

        return self._steps_made

    def has_lost(self) -> bool:
        """
        Returns a boolean regarding if the player has lost the game or not.
        :return: True if player has lost game, false if not.
        """

        if isinstance(self.get_player(), Player):
            return self._player_lost
        elif isinstance(self.get_player(), (VulnerablePlayer, HoldingPlayer)):
            return self.get_player().is_infected()

    def has_won(self) -> bool:
        """
        Returns true if the player has won the game.

        The player wins the game by stepping onto the hospital. When the player
        steps on the hospital, there will be no hospital entity in the grid.
        :return: True if player has won game, false if not.
        """

        serialized_grid = self.get_grid().serialize()

        if HOSPITAL not in serialized_grid.values():
            self._player_won = True

        return self._player_won

    def move_player(self, offset: Position) -> None:
        """
        Move the player entity in the grid by a given offset.
        Add the offset to the current position of the player, move the player
        entity within the grid to the new position.
        If the new position is outside the bound of the grid, or there is no
        player in the grid, this method should not move the player.
        :param offset: A position to add to the player's current position to
        produce the player's new desired position.
        :return: None.
        """

        # get current player position
        player_pos = self.get_grid().find_player()

        if player_pos is not None:
            # add offset to current player position
            new_position = player_pos.add(offset)
            # determine if move to new position is valid
            if self.get_grid().in_bounds(new_position):
                print("here")
                entity_at_pos = self.get_grid().get_entity(new_position)
                print("Entity at pos: " + str(entity_at_pos))
                can_move = False
                if entity_at_pos is not None:
                    print(entity_at_pos.display())
                    if entity_at_pos.display() in (GARLIC, CROSSBOW): # todo test
                        can_move = True
                elif entity_at_pos is None:
                    can_move = True
                if can_move:
                    # move entity
                    self.get_grid().move_entity(player_pos, new_position)

    def step(self) -> None:
        """
        The step method is called after every action performed by the player.

        This method triggers the step event by calling the step method of every
        entity in the grid. When the entity's step method is called, it should
        pass the entity's current position and this game as parameters.

        Note: Do not call this method in the move_player method
        :return: None
        """

        self._steps_made += 1

        mapped_grid = self.get_grid().get_mapping()
        # returns Dict[Position, Entity]
        for position, entity in mapped_grid.items():  # should work todo test
            if entity.display() in [ZOMBIE, TRACKING_ZOMBIE, PLAYER]:
                entity.step(position, self)


class IntermediateGame(Game):
    """
    Inherits from Game
    An intermediate game extends some of the functionality of the basic game.
    Specifically, the intermediate game includes the ability for the player
    to lose the game when they become infected.
    """

    def has_lost(self) -> bool:
        """
        Return True if the player has lost the game.
        The player loses the game if they become infected by a zombie.
        :return: True if player becomes infected by zombie.
        """

        return self.get_player().is_infected()


class AdvancedGame(IntermediateGame):
    """
    Inherits from IntermediateGame.
    The AdvancedGame class extends IntermediateGame to add support for the
    player picking up a Pickup item when they come into contact with it.
    """

    def move_player(self, offset: Position) -> None:
        """
        Move the player entity in the grid by a given offset.
        If the player moves onto a Pickup item, it should be added to the
        player's inventory and removed from the grid.
        :param offset: A position to add to the player's current position to
        produce the player's new desired position.
        :return: None.
        """

        # get current player position
        current_player_pos = self.get_grid().find_player()

        if current_player_pos is not None:
            # add offset to current player position
            new_position = current_player_pos.add(offset)
            # determine if move to new position is valid
            if self.get_grid().in_bounds(new_position):
                # check for pickup at new_position
                pickup = self.get_grid().get_entity(new_position)
                if pickup:
                    if pickup.display() in PICKUP_ITEMS:
                        # add pickup to inventory       # todo fix this
                        self.get_player().get_inventory().add_item(pickup)

                        # remove pickup from grid
                        self.get_grid().remove_entity(new_position)
                # move entity
                self.get_grid().move_entity(current_player_pos, new_position)


class MapLoader:
    """
    The MapLoader class is used to read a map file and create an appropriate
    Grid instance which stores all the map file entities.
    The MapLoader class is an abstract class to allow for extensible map
    definitions. The BasicMapLoader class described below is a very simple
    implementation of the MapLoader which only handles the player and hospital
    entities.
    """

    def create_entity(self, token: str) -> Entity:
        """
        Create an return a new instance of the Entity class based on the
        provided token.
        For example, if the given token is 'P' a player instance will be
        returned.
        The abstract MapLoader class does not support any entities, when this
        method is called, it should raise a NotImplementedError.
        :param token: Character representing the Entity subtype
        :return: Instance of entity based on provided token.
        """

        raise NotImplementedError

    def load(self, filename: str) -> Grid:
        """
        Load a new Grid instance from a map file.
        Load will open the map file and read each line to find all the entities
        in the grid and add them to the new Grid instance.
        The create_entity method below is used to turn a character in the map
        file into an Entity Instance.
        Hint: The load_map function in the support code may be helpful.
        :param filename: Path where the map file should be found.
        :return: Grid instance.
        """

        loaded_map = load_map(filename)

        entity_locations, grid_size = loaded_map
        # print(entity_locations)
        # instantiate empty grid
        grid = Grid(grid_size)

        for position_tuple, entity_token in entity_locations.items():
            # print(entity_token)
            entity = self.create_entity(entity_token)
            # print(entity)
            x, y = position_tuple
            position = Position(x, y)
            grid.add_entity(position, entity)

        return grid


class BasicMapLoader(MapLoader):
    """
    Inherits from MapLoader.
    BasicMapLoader is a subclass of MapLoader which can handle map files which
    include the following entities:
        - Player; and
        - Hospital.
    """

    def create_entity(self, token: str) -> Entity:
        """
        Create and return a new instance of the Entity class based on the
        provided token.
        For example, if the given token 'P', a Player instance will be returned.
        The BasicMapLoader class only supports the Player and Hospital entities.
        When a token is provided that does not represent the Player or Hospital,
        this method should raise a ValueError.
        :param token: Character representing the Entity subtype
        :return: Instance of entity based on provided token.
        """

        entities = {
            PLAYER: Player(),
            HOSPITAL: Hospital()
        }

        try:
            return entities[token]
        except KeyError:
            raise ValueError


class IntermediateMapLoader(BasicMapLoader):
    """
    Inherits from BasicMapLoader.
    The IntermediateMapLoader class extends the BasicMapLoader to add support
    for new entities that are added in task 2 of the assignment.
    When a player token, 'P', is found, a VulnerablePlayer instance should be
    created instead of a Player.
    In addition to the entities handled by the BasicMapLoader, the
    IntermediateMapLoader should be able to load the following entities:
        - Zombie.
    """

    def create_entity(self, token: str) -> Entity:
        """
        Create an return a new instance of the Entity class based on the
        provided token.
        For example, if the given token is 'P' a VulnerablePlayer instance will
        be returned.
        :param token: Character representing the Entity subtype.
        :return: Instance of entity based on provided token.
        """

        entities = {
            PLAYER: VulnerablePlayer(),
            HOSPITAL: Hospital(),
            ZOMBIE: Zombie(),
        }

        try:
            return entities[token]
        except KeyError:
            raise ValueError


class AdvancedMapLoader(IntermediateMapLoader):
    """
    Inherits from IntermediateMapLoader.
    The AdvancedMapLoader class extends IntermediateMapLoader to add support for
    new entities that are added in task 3 of the assignment.

    When a player token, 'P', is found, a HoldingPlayer instance should be
    created instead of a Player or VulnerablePlayer.

    In addition to the entities handled by the IntermediateMapLoader, the
    AdvancedMapLoader should be able to load the following entities.
    - TrackingZombie;
    - Garlic; and
    - Crossbow.
    """

    def create_entity(self, token: str) -> Entity:
        """
        Create an return a new instance of the Entity class based on the
        provided token.
        For example, if the given token is 'P' a HoldingPlayer instance will be
        returned.
        :param token: Character representing the Entity subtype.
        :return: Instance of entity based on provided token.
        """

        entities = {
            PLAYER: HoldingPlayer(),
            HOSPITAL: Hospital(),
            ZOMBIE: Zombie(),
            TRACKING_ZOMBIE: TrackingZombie(),
            GARLIC: Garlic(),
            CROSSBOW: Crossbow()
        }

        try:
            return entities[token]
        except KeyError:
            raise ValueError


class Inventory:
    """
    An inventory holds a collection of entities which the player can pickup,
    i.e. Pickup subclasses.

    The player is only able to hold any given item for a duration, this is the
    lifetime of the item. Once the lifetime is exceeded the item will be
    destroyed by being removed from the inventory.
    """

    def __init__(self):
        """
        Constructor for the inventory.
        Defines a list used for storing pickups in the inventory.
        """

        self._inventory = []      # [pickup] List

    def add_item(self, item: Pickup) -> None:
        """
        Take a pickup entity and add it to the inventory.
        :param item: the item to be added to the inventory.
        :return: None.
        """
        # need to consider lifetime of each inventory item.
        # this is stored in the support file as
        # LIFETIMES = {GARLIC: 10, CROSSBOW: 5}

        self._inventory.append(item)   # put item in list

    def contains(self, pickup_id: str) -> bool:
        """
        Decide if the inventory contains any entities which return the given
        pickup_id from the entity's display method.
        :param pickup_id: The character token representing pickups in inventory.
        :return: True if inventory contains items, false if not.
        """

        for pickup in self.get_items():
            return pickup.display() == pickup_id

        # return any(pickup_id in sublist for sublist in self._inventory)

    def get_items(self) -> List[Pickup]:
        """
        Return the pickup entity instances currently stored in the inventory.
        :return: list of pickup entity instances currently in inventory.
        """

        return self._inventory

    def step(self) -> None:
        """
        Called every time the player steps as a part of the player's step
        method. The lifetime of every item in the inventory should decrease.
        Any items which have exceeded their lifetime in the player's inventory
        should be removed.
        :return: None.
        """

        for i, pickup in enumerate(self._inventory):
            pickup.hold()   # subtract 1 from all item's health
            if pickup.get_lifetime() <= 0:  # if item's health is 0 or below
                self._inventory.pop(i)  # remove pickup at position i


class TextInterface(GameInterface):
    """
    Inherits from GameInterface.
    A text-based interface between the user and the game instance.
    This class handles all input collection from the user and printing to the
    console.
    """

    def __init__(self, size: int):
        """
        The text-interface is constructed knowing the size of the game to be
        played, this allows the draw method to correctly print the right sized
        grid.
        :param size: The size of the game to be displayed and played.
        """

        self._game_size = size

    def draw(self, game: Game) -> None:
        """
        The draw method should print out the given game surrounded by '#'
        characters representing the border of the game.
        :param game: An instance of the game class that is to be displayed to
        the user by printing the grid.
        :return: None (all printed internally).
        """

        colours = {
            PLAYER: "\033[0;34;49m",
            BORDER: "\033[0;37;m",
            GARLIC: "\033[0;33;49m",
            ZOMBIE: "\033[0;32;49m",
            TRACKING_ZOMBIE: "\033[0;31;49m",
            CROSSBOW: "\033[0;36;49m",
            HOSPITAL: "\033[1;31;49m"
        }

        colour_switch = False

        # get serialized grid
        serialized_grid = game.get_grid().serialize()

        # row consisting of hashes of length 2 greater than size of map
        if colour_switch:
            border_print = colours.get(BORDER) + BORDER
        else:
            border_print = BORDER
        row_of_hashes = border_print * (game.get_grid().get_size() + 2)

        print(row_of_hashes)

        for y in range(game.get_grid().get_size()):
            print(border_print, end='')

            for x in range(game.get_grid().get_size()):
                current_pos = serialized_grid.get((x, y))
                if current_pos:
                    if colour_switch:
                        print(colours.get(current_pos) + current_pos, end='')
                    else:
                        print(current_pos, end='')
                else:
                    print(" ", end='')

            print(border_print)

        print(row_of_hashes)

    def handle_action(self, game: Game, action: str) -> None:   # todo test
        """
        The handle_action method is used to process the actions entered by the
        user during the game loop in the play method.
        This method should be able to handle all movement actions, i.e.
        'W', 'A', 'S', 'D'.
        If the given action is not a direction, this method should do nothing.
        :param game: The game that is currently being played.
        :param action: An action entered by the user during the game loop.
        :return: None.
        """

        move_offset = game.direction_to_offset(action)

        if move_offset:
            game.move_player(move_offset)

        # initiate the (game's) step event.
        game.step()

    def play(self, game: Game) -> None:
        """
        The play method implements the game loop, constantly prompting the user
        for their action, performing the action and printing the game until the
        game is over.
        :param game: The game to start playing.
        :return: None.
        """

        while True:
            # win / lose / print grid
            if game.has_won():
                print(WIN_MESSAGE)
                break
            elif game.has_lost():
                print(LOSE_MESSAGE)
                break
            else:
                self.draw(game)

            user_input = input(ACTION_PROMPT).upper()

            if user_input in DIRECTIONS or user_input in FIRE:
                self.handle_action(game, user_input)


class AdvancedTextInterface(TextInterface):
    """
    Inherits from TextInterface.
    A text-based interface between the user and the game instance.
    This class extend the existing functionality of TextInterface to include
    displaying the state of the player's inventory and a firing action.
    """

    def __init__(self, size: int):
        """
        Constructor for Advanced Text Interface.
        Inherits __init__() from TextInterface.
        :param size: The size of the game to be displayed and played.
        """

        super().__init__(size)

    def draw(self, game: Game) -> None:
        """
        The draw method should print out the given game surrounded by "#"
        characters representing the border of the game.
        This method should behave in the same way as the super class except if a
        player is currently holding items in their inventory.
        If the player is holding items in their inventory, 'The player is
        currently holding:' should be printed after the grid, followed by the
        representation of each item in the inventory on separate lines. See the
        examples for more details.
        :param game: An instance of the game class that is to be displayed to
        the user by printing the grid.
        :return: None.
        """

        super().draw(game)
        if not not game.get_player().get_inventory().get_items():
            print(HOLDING_MESSAGE)
            inventory_items = game.get_player().get_inventory().get_items()
            for item in inventory_items:
                print(item)

    def handle_action(self, game: Game, action: str) -> None:
        """
        The handle_action method for AdvancedTextInterface should extend the
        interface to be able to handle the fire action for a crossbow.
        If the user enters, 'F' for fire take the following actions:
        1. Check that the user has something to fire, i.e. a crossbow, if they
        do not hold a crossbow, print 'You are not holding anything to fire!'
        2. Prompt the user to enter a direction in which to fire, with
        'Direction to fire: '
        3. If the direction is not one of 'W', 'A', 'S', 'D', print 'Invalid
        firing direction entered!'
        4. Find the first entity, starting from the player's position in the
        direction specified.
        5. If there are no entities in that direction, or if the first entity
        is not a zombie, (zombies include tracking zombies), then print 'No
        zombie in that direction!'
        6. If the first entity in that direction is a zombie, remove the zombie.
        7. Trigger the step event.

        If the action is not fire, this method should behave the same as
        TextInterface.handle_action.
        :param game: The game that is currently being played.
        :param action: An action entered by the player during the game loop.
        :return: None.
        """

        if action == FIRE:
            private_inventory = game.get_player().get_inventory()
            if private_inventory.contains(CROSSBOW):
                while True:
                    fire_direction = input(FIRE_PROMPT).upper()
                    if fire_direction in DIRECTIONS:
                        break
                    else:
                        print(INVALID_FIRING_MESSAGE)

                fire_offset = game.direction_to_offset(fire_direction)
                player_position = game.get_grid().find_player()
                final_position = player_position
                while True:
                    final_position = final_position.add(fire_offset)
                    if game.get_grid().in_bounds(final_position):
                        entity_search = game.get_grid().\
                            get_entity(final_position)
                        if entity_search:
                            if entity_search.display() in ZOMBIES:
                                game.get_grid().remove_entity(final_position)
                                break
                        elif not entity_search:
                            continue
                    else:
                        print(NO_ZOMBIE_MESSAGE)
                        break
            else:
                print(NO_WEAPON_MESSAGE)
            game.step()
        else:
            super().handle_action(game, action)


def main():
    """
    Main function. Lets user select map, instantiates grid, instantiates game,
    hands of functionality to advanced_text_interface.play to run the main game
    loop.
    """

    print("Implement your solution and run this file")

    while True:
        map_selection = input("Select Map (1, 2, 3 ,4): ")

        try:
            map_selection = int(map_selection)
        except ValueError:
            continue

        if map_selection in range(1, 5 + 1):    # todo change this back to 4 + 1
            break

    map_filenames = {
        1: "maps/basic.txt",
        2: "maps/basic2.txt",
        3: "maps/basic3.txt",
        4: "maps/basic4.txt",
        5: "maps/hugosmap1.txt"     # todo will need to remove this
    }

    # instantiate grid
    filename = map_filenames.get(map_selection)
    grid = AdvancedMapLoader().load(filename)

    # instantiate game
    advanced_game = AdvancedGame(grid)
    grid_size = advanced_game.get_grid().get_size()
    advanced_text_interface = AdvancedTextInterface(grid_size)
    advanced_text_interface.play(advanced_game)


if __name__ == "__main__":
    main()
