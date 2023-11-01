#!/usr/bin/env python3

"""
Sample test suite for CSSE1001 / 7030 Assignment 2 marking.
"""

__author__ = "Mike Pham"

import inspect
import random
from pathlib import Path
from typing import Tuple, Optional, Dict, List

from testrunner import AttributeGuesser, OrderedTestCase, RedirectStdIO, \
                       TestMaster, skipIfFailed

SEED = 1001.2021
MAPS_DIR = Path("maps")


class Position:
    def __init__(self, x: int, y: int): pass

    def get_x(self) -> int: pass

    def get_y(self) -> int: pass

    def add(self, position: 'Position') -> 'Position': pass

    def add_offset(self, offset: Tuple[int, int]) -> 'Position': pass


class GameInterface:
    def draw(self, game) -> None: pass

    def play(self, game) -> None: pass


class Entity:
    def step(self, position: Position, game: "Game") -> None: pass

    def display(self) -> str: pass


class Player(Entity):
    pass


class Hospital(Entity):
    pass


class Grid:
    def __init__(self, size: int): pass

    def get_size(self) -> int: pass

    def in_bounds(self, position: Position) -> bool: pass

    def add_entity(self, position: Position, entity: Entity) -> None: pass

    def remove_entity(self, position: Position) -> None: pass

    def get_entity(self, position: Position) -> Optional[Entity]: pass

    def get_mapping(self) -> Dict[Position, Entity]: pass

    def get_entities(self) -> List[Entity]: pass

    def move_entity(self, start: Position, end: Position) -> None: pass

    def find_player(self) -> Optional[Position]: pass

    def serialize(self) -> Dict[Tuple[int, int], str]: pass


class MapLoader:
    def load(self, filename: str) -> Grid: pass

    def create_entity(self, token: str) -> Entity: pass


class BasicMapLoader(MapLoader):
    pass


class Game:
    def __init__(self, grid: Grid): pass

    def get_grid(self) -> Grid: pass

    def get_player(self) -> Optional[Player]: pass

    def step(self) -> None: pass

    def get_steps(self) -> int: pass

    def move_player(self, offset: Position) -> None: pass

    def direction_to_offset(self, direction: str) -> Optional[Position]: pass

    def has_won(self) -> bool: pass

    def has_lost(self) -> bool: pass


class TextInterface(GameInterface):
    def __init__(self, size: int): pass

    def handle_action(self, game: Game, action: str) -> None: pass


class VulnerablePlayer(Player):
    def infect(self) -> None: pass

    def is_infected(self) -> bool: pass


class Zombie(Entity):
    pass


class IntermediateGame(Game):
    pass


class IntermediateMapLoader(MapLoader):
    pass


class TrackingZombie(Zombie):
    pass


class Pickup(Entity):
    def get_lifetime(self) -> int: pass

    def get_durability(self) -> int: pass

    def hold(self) -> None: pass


class Garlic(Pickup):
    pass


class Crossbow(Pickup):
    pass


class Inventory:
    def step(self) -> None: pass

    def add_item(self, item: Pickup) -> None: pass

    def get_items(self) -> List[Pickup]: pass

    def contains(self, pickup_id: str) -> bool: pass


class HoldingPlayer(VulnerablePlayer):
    def get_inventory(self) -> Inventory: pass


class AdvancedGame(IntermediateGame):
    pass


class AdvancedMapLoader(IntermediateMapLoader):
    pass


class AdvancedTextInterface(TextInterface):
    pass
##
##
##class TextInterfaceWithInventory:
##    pass


class A2Support:
    GameInterface = GameInterface
    Position = Position

    @staticmethod
    def load_map(filename: str) -> Tuple[Dict[Tuple[int, int], str], int]: pass

    @staticmethod
    def random_directions() -> List[Tuple[int, int]]: pass


class A2:
    AdvancedGame = AdvancedGame
    AdvancedMapLoader = AdvancedMapLoader
    AdvancedTextInterface = AdvancedTextInterface
    BasicMapLoader = BasicMapLoader
    Crossbow = Crossbow
    Entity = Entity
    Game = Game
    GameInterface = GameInterface
    Garlic = Garlic
    Grid = Grid
    HoldingPlayer = HoldingPlayer
    Hospital = Hospital
    IntermediateGame = IntermediateGame
    IntermediateMapLoader = IntermediateMapLoader
    Inventory = Inventory
    MapLoader = MapLoader
    MapLoader = MapLoader
    Pickup = Pickup
    Player = Player
    Position = Position
    TextInterface = TextInterface
    TrackingZombie = TrackingZombie
    VulnerablePlayer = VulnerablePlayer
    Zombie = Zombie


class TestA2(OrderedTestCase):
    """ Base for all a1 test cases """
    a2: A2
    a2_support: A2Support


class TestFunctionality(TestA2):
    """ Base for all A2 functionality tests. """

    TEST_DATA = (Path(__file__).parent / 'test_data').resolve()

    @staticmethod
    def set_seed(seed=SEED, skip_numbers=0):
        """ helper method for settings random seed """
        random.seed(seed)
        for _ in range(skip_numbers):
            random.random()  # skip next random number

    def load_test_data(self, filename: str):
        """ load test data from file """
        with open(self.TEST_DATA / filename, encoding='utf8') as file:
            return file.read()

    def write_test_data(self, filename: str, output: str):
        """ write test data to file """
        with open(self.TEST_DATA / filename, 'w', encoding='utf8') as file:
            file.write(output)


class TestDesign(TestA2):
    def test_clean_import(self):
        """ Test no prints on import """
        self.assertIsCleanImport(self.a2,
                                 msg="You should not be printing on "
                                     "import for a2.py")

    def test_doc_strings(self):
        """ Test all classes and functions have documentation strings """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        ignored = frozenset(('__str__', '__repr__'))

        for cls_name, cls in inspect.getmembers(a2, predicate=inspect.isclass):
            self.aggregate(self.assertDocString, cls)
            defined = vars(cls)
            for func_name, func in inspect.getmembers(cls,
                                                      predicate=inspect.isfunction):
                if func_name in ignored or func_name not in defined:
                    continue
                self.aggregate(self.assertRecursiveDocString, cls, func_name,
                               a2)

        self.aggregate_tests()

    def _aggregate_class_and_functions_defined(self, module, test_class,
                                               sub_class_of=None):
        """
            Helper method to test a class has all the required methods
            and signatures.
        """
        cls_name = test_class.__name__
        if not self.aggregate(self.assertClassDefined, module, cls_name,
                              tag=cls_name):
            return

        if sub_class_of and hasattr(module, sub_class_of):
            self.aggregate(self.assertIsSubclass, getattr(module, cls_name),
                           getattr(module, sub_class_of))

        cls = getattr(module, cls_name)
        empty = inspect.Parameter.empty
        for func_name, func in inspect.getmembers(test_class,
                                                  predicate=inspect.isfunction):
            params = inspect.signature(func).parameters
            if self.aggregate(self.assertFunctionDefined, cls, func_name,
                              len(params), tag=f'{cls_name}.{func_name}'):
                # logic should be moved to testrunner.py
                for p1, p2 in zip(params.values(), inspect.signature(
                        getattr(cls, func_name)).parameters.values()):
                    if p1.default == empty and p2.default != empty:
                        self.aggregate(self.fail,
                                       msg=f"expected '{p2.name}' to not have default value but got '{p2.default}'",
                                       tag=f'{cls_name}.{func_name}.{p1.name}')
                    elif p1.default != empty and p2.default == empty:
                        self.aggregate(self.fail,
                                       msg=f"expected '{p2.name}' to have default value '{p1.default}'",
                                       tag=f'{cls_name}.{func_name}.{p1.name}')
                    else:
                        self.aggregate(self.assertEqual, p1.default, p2.default,
                                       msg=f"expected '{p2.name}' to have default value '{p1.default}' but got '{p2.default}'",
                                       tag=f'{cls_name}.{func_name}.{p1.name}')

    def test_classes_and_functions_defined_task_1(self):
        """
        Test all specified classes and functions defined correctly for task 1.
        """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        self._aggregate_class_and_functions_defined(a2, Entity)
        self._aggregate_class_and_functions_defined(a2, Player, 'Entity')
        self._aggregate_class_and_functions_defined(a2, Hospital, 'Entity')
        self._aggregate_class_and_functions_defined(a2, Grid)
        self._aggregate_class_and_functions_defined(a2, MapLoader)
        self._aggregate_class_and_functions_defined(a2, BasicMapLoader,
                                                    'MapLoader')
        self._aggregate_class_and_functions_defined(a2, Game)
        self._aggregate_class_and_functions_defined(a2, TextInterface,
                                                    'GameInterface')
        self.aggregate_tests()

    @skipIfFailed(test_name=test_classes_and_functions_defined_task_1)
    def test_classes_and_functions_defined_task_2(self):
        """
        Test all specified classes and functions defined correctly for task 2.
        """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        self._aggregate_class_and_functions_defined(a2, VulnerablePlayer,
                                                    "Player")
        self._aggregate_class_and_functions_defined(a2, Zombie, "Entity")
        self._aggregate_class_and_functions_defined(a2, IntermediateGame,
                                                    "Game")
        self._aggregate_class_and_functions_defined(a2,
                                                    IntermediateMapLoader,
                                                    "BasicMapLoader")
        self.aggregate_tests()

    @skipIfFailed(test_name=test_classes_and_functions_defined_task_2)
    def test_classes_and_functions_defined_task_3(self):
        """
        Test all specified classes and functions defined correctly for task 3.
        """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        self._aggregate_class_and_functions_defined(a2, TrackingZombie,
                                                    "Zombie")
        self._aggregate_class_and_functions_defined(a2, Pickup, "Entity")
        self._aggregate_class_and_functions_defined(a2, Garlic, "Pickup")
        self._aggregate_class_and_functions_defined(a2, Crossbow, "Pickup")
        self._aggregate_class_and_functions_defined(a2, Inventory)
        self._aggregate_class_and_functions_defined(a2, HoldingPlayer,
                                                    "VulnerablePlayer")
        self._aggregate_class_and_functions_defined(a2, AdvancedGame,
                                                    "IntermediateGame")
        self._aggregate_class_and_functions_defined(a2, AdvancedMapLoader,
                                                    "IntermediateMapLoader")
        self._aggregate_class_and_functions_defined(a2, AdvancedTextInterface,
                                                    "TextInterface")
        self.aggregate_tests()


class TestGenericEntity(TestFunctionality):
    """ Base class for testing Entity instances. """
    def setUp(self) -> None:
        self._grid = self.a2.Grid(4)
        self._position1 = self.a2_support.Position(1, 2)
        self._game = self.a2.Game(self._grid)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="Entity")
class TestEntity(TestGenericEntity):
    """ Test Entity """

    def setUp(self) -> None:
        super().setUp()
        self._entity = self.a2.Entity()

    def test_step(self):
        """ Test Entity.step returns None """
        self.assertIsNone(self._entity.step(self._position1, self._game))

    def test_display(self):
        """ Test display raises NotImplementedError """
        self.assertRaises(NotImplementedError, self._entity.display)

    def test_repr(self):
        """ Test Entity.repr returns correct representation """
        self.assertEqual("Entity()", repr(self._entity))


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="Player")
class TestPlayer(TestGenericEntity):
    """ Test Player """

    def setUp(self) -> None:
        super().setUp()
        self._player = self.a2.Player()

    def test_step(self):
        """ Test Player.step returns None """
        self.assertIsNone(self._player.step(self._position1, self._game))

    def test_display(self):
        """ Test display returns "P" """
        self.assertEqual("P", self._player.display())

    def test_repr(self):
        """ Test Player.repr returns correct representation """
        self.assertEqual("Player()", repr(self._player))


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="Hospital")
class TestHospital(TestGenericEntity):
    """ Test Hospital """

    def setUp(self) -> None:
        super().setUp()
        self._hospital = self.a2.Hospital()

    def test_step(self):
        """ Test Hospital.step returns None """
        self.assertIsNone(self._hospital.step(self._position1, self._game))

    def test_display(self):
        """ Test display returns "H" """
        self.assertEqual("H", self._hospital.display())

    def test_repr(self):
        """ Test Hospital.repr returns correct representation """
        self.assertEqual("Hospital()", repr(self._hospital))


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="Grid")
class TestGrid(TestFunctionality):
    """ Base class for testing Grid. """

    def setUp(self) -> None:
        self._grid = self.a2.Grid(4)
        self._position1 = self.a2_support.Position(2, 2)
        self._top_left = self.a2_support.Position(0, 0)
        self._top_right = self.a2_support.Position(3, 0)
        self._bottom_left = self.a2_support.Position(0, 3)
        self._bottom_right = self.a2_support.Position(3, 3)
        self._invalid_neg_x = self.a2_support.Position(-1, 3)
        self._invalid_neg_y = self.a2_support.Position(2, -2)
        self._invalid_x1 = self.a2_support.Position(4, 2)
        self._invalid_x2 = self.a2_support.Position(6, 1)
        self._invalid_y1 = self.a2_support.Position(2, 4)
        self._invalid_y2 = self.a2_support.Position(3, 5)
        self._invalid_xy = self.a2_support.Position(5, 5)
        self._player = self.a2.Player()
        self._hospital = self.a2.Hospital()


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="Grid")
class TestGridSample(TestGrid):
    """ Test Grid Sample """

    def test_get_size(self):
        """ Test Grid.get_size """
        self.assertEqual(4, self._grid.get_size())

    def test_in_bounds_valid(self):
        """ Test in bounds with valid position """
        self.assertTrue(self._grid.in_bounds(self._position1))

    def test_in_bounds_negative_x(self):
        """ Test in bounds with negative x coordinate """
        self.assertFalse(self._grid.in_bounds(self._invalid_neg_x))

    def test_in_bounds_invalid_x2(self):
        """ Test in bounds with x coordinate greater than grid size """
        self.assertFalse(self._grid.in_bounds(self._invalid_x2))

    def test_in_bounds_invalid_y2(self):
        """ Test in bounds with y coordinate greater than grid size """
        self.assertFalse(self._grid.in_bounds(self._invalid_y2))

    def test_add_entity_new_entity(self):
        """ Test add entity with new entity """
        self.assertIsNone(self._grid.add_entity(self._position1, self._player))
        self.assertIs(self._grid.get_entity(self._position1), self._player)

    def test_add_entity_replace_entity(self):
        """ Test add entity overwrite existing entity """
        self.assertIsNone(self._grid.add_entity(self._position1,
                                                self._hospital))
        self.assertIsNone(self._grid.add_entity(self._position1, self._player))
        self.assertIs(self._grid.get_entity(self._position1), self._player)

    def test_remove_entity(self):
        """ Test remove entity """
        self._grid.add_entity(self._position1, self._player)
        self.assertIsNone(self._grid.remove_entity(self._position1))
        self.assertIsNone(self._grid.get_entity(self._position1))

    def test_get_entity_empty(self):
        """ Test get entity at empty position """
        self.assertIsNone(self._grid.get_entity(self._position1))

    def test_get_mapping(self):
        """ Test get mapping """
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._bottom_right, self._hospital)
        self._grid.add_entity(self._top_right, self._hospital)
        expected = {
            self._top_right: self._hospital,
            self._bottom_right: self._hospital,
            self._position1: self._player
        }
        self.assertDictEqual(self._grid.get_mapping(), expected)

    def test_get_mapping_empty(self):
        """ Test get mapping with empty grid """
        self.assertDictEqual(self._grid.get_mapping(), {})

    def test_get_mapping_replaced_position(self):
        """ Test get mapping after replacing entity at a position """
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._position1, self._hospital)
        expected = {self._position1: self._hospital}
        self.assertDictEqual(self._grid.get_mapping(), expected)

    def test_get_mapping_after_move(self):
        """ Test get mapping after moving an entity """
        self._grid.add_entity(self._position1, self._player)
        self._grid.move_entity(self._position1, self._top_right)
        expected = {self._top_right: self._player}
        self.assertDictEqual(self._grid.get_mapping(), expected)

    def test_get_entities(self):
        """ Test get entities """
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._bottom_right, self._hospital)
        self._grid.add_entity(self._top_right, self._hospital)
        expected = [self._player, self._hospital, self._hospital]
        self.assertListSimilar(self._grid.get_entities(), expected)

    def test_get_entities_empty(self):
        """ Test get entities with empty grid """
        self.assertListSimilar(self._grid.get_entities(), [])

    def test_get_entities_replaced_position(self):
        """ Test get entities after replacing entity at a position """
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._position1, self._hospital)
        expected = [self._hospital]
        self.assertListSimilar(self._grid.get_entities(), expected)

    def test_move_entity(self):
        """ Test moving an entity """
        self._grid.add_entity(self._position1, self._player)
        self._grid.move_entity(self._position1, self._top_left)
        self.assertIs(self._grid.get_entity(self._top_left), self._player)
        self.assertIsNone(self._grid.get_entity(self._position1))

    def test_move_entity_start_out_of_bound(self):
        """ Test attempting to move an entity from an invalid start position """
        self.assertIsNone(self._grid.move_entity(self._invalid_x1,
                                                 self._top_left))

    def test_move_entity_replace_end(self):
        """ Test moving entity and replacing the entity at the end position """
        self._grid.add_entity(self._bottom_right, self._hospital)
        self._grid.add_entity(self._top_left, self._player)
        self.assertIsNone(self._grid.move_entity(self._top_left,
                                                 self._bottom_right))
        self.assertIsNone(self._grid.get_entity(self._top_left))
        self.assertIs(self._grid.get_entity(self._bottom_right), self._player)

    def test_find_player(self):
        """ Test find player in grid """
        self._grid.add_entity(self._bottom_right, self._player)
        self.assertEqual(self._grid.find_player(), self._bottom_right)

    def test_find_player_moved(self):
        """ Test find player, after moving player """
        self._grid.add_entity(self._bottom_right, self._player)
        self._grid.move_entity(self._bottom_right, self._position1)
        self.assertEqual(self._grid.find_player(), self._position1)
        self.assertIsNone(self._grid.get_entity(self._bottom_right))

    def test_serialize(self):
        """ Test serialize """
        self._grid.add_entity(self._top_left, self._hospital)
        self._grid.add_entity(self._bottom_right, self._player)
        expected = {
            (0, 0): "H",
            (3, 3): "P"
        }
        self.assertDictEqual(self._grid.serialize(), expected)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="MapLoader")
class TestMapLoader(TestFunctionality):
    """ Test MapLoader """

    def test_create_entity(self):
        """ Test abstract create_entity method """
        loader = self.a2.MapLoader()
        with self.assertRaises(NotImplementedError):
            loader.create_entity("P")


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="BasicMapLoader")
class TestBasicMapLoader(TestFunctionality):
    """ Test BasicMapLoader """

    def test_create_player(self):
        """ Test creating a player with a basic map loader """
        loader = self.a2.BasicMapLoader()
        self.assertIsInstance(loader.create_entity("P"), self.a2.Player)

    def test_create_hospital(self):
        """ Test creating a hospital with a basic map loader """
        loader = self.a2.BasicMapLoader()
        self.assertIsInstance(loader.create_entity("H"), self.a2.Hospital)

    def test_create_invalid_zombie(self):
        """ Test attempting to create a zombie with a basic map loader in task 1 """
        loader = self.a2.BasicMapLoader()
        self.assertRaises(ValueError, loader.create_entity, "Z")

    def test_create_invalid_entity(self):
        """ Test attempting to create an invalid entity with a basic map loader """
        loader = self.a2.BasicMapLoader()
        self.assertRaises(ValueError, loader.create_entity, "A")

    def test_load_basic_map(self):
        """ Test loading a basic map """
        loader = self.a2.BasicMapLoader()
        grid = loader.load(str(MAPS_DIR / "basic.txt"))
        player_pos = self.a2_support.Position(0, 1)
        hospital_pos = self.a2_support.Position(4, 4)
        player = grid.get_entity(player_pos)
        hospital = grid.get_entity(hospital_pos)
        self.assertIsInstance(player, self.a2.Player)
        self.assertIsInstance(hospital, self.a2.Hospital)
        self.assertListSimilar(grid.get_entities(), [hospital, player])
        expected_mapping = {player_pos: player, hospital_pos: hospital}
        self.assertDictEqual(grid.get_mapping(), expected_mapping)


class TestGameTask1(TestFunctionality):
    """ Base class for testing Game Task 1 """

    def setUp(self) -> None:
        self._grid = self.a2.Grid(6)
        self._position1 = self.a2_support.Position(0, 3)
        self._position2 = self.a2_support.Position(5, 5)
        self._player = self.a2.Player()
        self._hospital = self.a2.Hospital()
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._position2, self._hospital)
        self._game = self.a2.Game(self._grid)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="Game")
class TestGameSample(TestGameTask1):
    """ Test Game Sample """

    def test_get_grid(self):
        """ Test get grid """
        self.assertIs(self._game.get_grid(), self._grid)

    def test_get_player(self):
        """ Test get player in game """
        self.assertIs(self._game.get_player(), self._player)

    def test_step_returns_none(self):
        """ Test calling step returns None """
        self.assertIsNone(self._game.step())

    def test_get_steps(self):
        """ Test get_steps """
        for i in range(100):
            self.assertEqual(self._game.get_steps(), i)
            self._game.step()

    def test_move_player(self):
        """ Test moving the player """
        self.assertIsNone(self._game.move_player(self.a2_support.Position(2, 2)))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(2, 5))

    def test_move_player_negative_offset(self):
        """ Test moving the player with a negative offset """
        self.assertIsNone(self._game.move_player(self.a2_support.Position(0, -2)))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(0, 1))

    def test_direction_to_offset_W(self):
        """ Test converting 'W' direction to offset """
        self.assertEqual(self._game.direction_to_offset("W"),
                         self.a2_support.Position(0, -1))

    def test_direction_to_offset_lowercase(self):
        """ Test converting lowercase directions to offset """
        self.assertIsNone(self._game.direction_to_offset("w"))
        self.assertIsNone(self._game.direction_to_offset("a"))
        self.assertIsNone(self._game.direction_to_offset("s"))
        self.assertIsNone(self._game.direction_to_offset("d"))

    def test_has_won_true(self):
        """ Test has won returning True """
        self._game.move_player(self.a2_support.Position(5, 2))
        self.assertTrue(self._game.has_won())

    def test_has_won_false(self):
        """ Test has won returning False """
        self.assertFalse(self._game.has_won())


class TestInterface(TestFunctionality):
    """ Base class for testing user interfaces. """
    def setUp(self) -> None:
        self._hospital_pos = self.a2_support.Position(4, 4)
        self._player_pos = self.a2_support.Position(1, 1)
        self._grid = self.a2.Grid(5)
        self._grid.add_entity(self._hospital_pos, self.a2.Hospital())
        self._grid.add_entity(self._player_pos, self.a2.Player())

    def _run_play(self, file_in: str, file_out: str, stop_early: bool):
        """ runs the play function and captures output """
        data_in = self.load_test_data(file_in)

        error = None
        result = None
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = data_in
            try:
                result = self._interface.play(self._game)
            except EOFError as err:
                error = err

        # self.write_test_data(file_out, stdio.stdinout)
        expected = self.load_test_data(file_out)
        if error is not None and not stop_early:
            last_output = "\n\n".join(stdio.stdinout.rsplit("\n\n")[-20:])
            raise AssertionError(
                f'Your program is asking for more input when it should have '
                f'ended\nEOFError: {error}\n\n{last_output}'
            ).with_traceback(error.__traceback__)

        return expected, result, stdio

    def assertPlay(self, file_in: str, file_out: str, stop_early: bool = False):
        """ assert the play function ran correctly """
        expected, result, stdio = self._run_play(file_in, file_out,
                                                 stop_early=stop_early)
        self.assertMultiLineEqual(stdio.stdinout, expected)
        if stdio.stdin != '':
            self.fail(msg="Not all input was read")
        self.assertIsNone(result,
                          msg="play function should not return a non None value")


class TestTextInterfaceRoot(TestInterface):
    """ Base class for testing text interfaces. """

    def setUp(self) -> None:
        super().setUp()
        self._game = self.a2.Game(self._grid)
        self._interface = self.a2.TextInterface(5)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_1.__name__,
              tag="TextInterface")
class TestTextInterface(TestTextInterfaceRoot):
    """ Test TextInterface """

    def test_draw(self):
        """ Test drawing a simple game """
        expected = "#######\n" \
                   "#     #\n" \
                   "# P   #\n" \
                   "#     #\n" \
                   "#     #\n" \
                   "#    H#\n" \
                   "#######\n"
        with RedirectStdIO(stdout=True) as stdio:
            self._interface.draw(self._game)

        self.assertMultiLineEqual(stdio.stdout, expected)

    def test_handle_action_move_up_player_correct_position(self):
        """ Test handling action of player moving up and positioning player correctly """
        self.assertIsNone(self._interface.handle_action(self._game, "W"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(1, 0))

    def test_handle_action_move_up_player_correct_display(self):
        """ Test handling action of player moving up and displaying player in correct position """
        self.assertIsNone(self._interface.handle_action(self._game, "W"))
        expected = "#######\n" \
                   "# P   #\n" \
                   "#     #\n" \
                   "#     #\n" \
                   "#     #\n" \
                   "#    H#\n" \
                   "#######\n"
        with RedirectStdIO(stdout=True) as stdio:
            self._interface.draw(self._game)

        self.assertMultiLineEqual(stdio.stdout, expected)

    def test_handle_multiple_valid_actions(self):
        """ Test handling multiple valid actions """
        self.assertIsNone(self._interface.handle_action(self._game, "W"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(1, 0))
        self.assertIsNone(self._interface.handle_action(self._game, "D"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(2, 0))
        self.assertIsNone(self._interface.handle_action(self._game, "S"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(2, 1))
        self.assertIsNone(self._interface.handle_action(self._game, "A"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(1, 1))

    def test_handle_invalid_command_player_not_moved(self):
        """ Test handling invalid command, ensuring player did not move """
        self.assertIsNone(self._interface.handle_action(self._game, "N"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(1, 1))

    def test_handle_invalid_command_player_display_correctly(self):
        """ Test handling invalid command, ensuring player displays in same position """
        self.assertIsNone(self._interface.handle_action(self._game, "N"))
        expected = "#######\n" \
                   "#     #\n" \
                   "# P   #\n" \
                   "#     #\n" \
                   "#     #\n" \
                   "#    H#\n" \
                   "#######\n"
        with RedirectStdIO(stdout=True) as stdio:
            self._interface.draw(self._game)

        self.assertMultiLineEqual(stdio.stdout, expected)

    def test_handle_invalid_action_left(self):
        """ Test handling invalid move left action when at left edge of grid """
        self._game.move_player(self.a2_support.Position(-1, 0))
        self.assertIsNone(self._interface.handle_action(self._game, "A"))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(0, 1))

    def test_play_basic_map(self):
        """ Test play with map as basic.txt """
        self.assertPlay("basic.in", "basic.out")

    def test_play_basic_map_invalid_commands(self):
        """ Test play with map as basic.txt with invalid commands """
        self.assertPlay("invalid.in", "invalid.out")


class TestVulnerablePlayerRoot(TestGenericEntity):
    """ Base class for testing VulnerablePlayer. """

    def setUp(self) -> None:
        super().setUp()
        self._player = self.a2.VulnerablePlayer()


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="VulnerablePlayer")
class TestVulnerablePlayer(TestVulnerablePlayerRoot):
    """ Test VulnerablePlayer """

    def test_is_infected(self):
        """ Test is_infected returns False after instantiating VulnerablePlayer """
        self.assertFalse(self._player.is_infected())

    def test_infect(self):
        """ Test infecting player """
        self._player.infect()
        self.assertTrue(self._player.is_infected())

    def test_display(self):
        """ Test vulnerable player display """
        self.assertEqual(self._player.display(), "P")


class TestZombieRoot(TestGenericEntity):
    """ Base class for testing Zombie. """

    def setUp(self) -> None:
        super().setUp()
        self._zombie = self.a2.Zombie()
        self._grid.add_entity(self._position1, self._zombie)
        self.set_seed()

    def _find_zombie_position(self):
        for position, entity in self._grid.get_mapping().items():
            if isinstance(entity, self.a2.Zombie):
                return position


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="Zombie")
class TestZombie(TestZombieRoot):
    """ Test Zombie """

    def test_display(self):
        """ Test Zombie display """
        self.assertEqual(self._zombie.display(), "Z")

    def test_step(self):
        """ Test moving Zombie using step """
        expected_positions = [(1, 1), (2, 1), (3, 1), (2, 1),
                              (3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (1, 2)]
        current_position = self._position1
        for expected_position in expected_positions:
            self._zombie.step(current_position, self._game)
            current_position = self.a2_support.Position(*expected_position)
            self.assertEqual(self._find_zombie_position(), current_position)

    def test_infect_player(self):
        """ Test calling step results in player infected """
        player = self.a2.VulnerablePlayer()
        self._grid.add_entity(self.a2_support.Position(1, 1), player)
        self._zombie.step(self._position1, self._game)
        self.assertTrue(player.is_infected())
        self.assertEqual(self._find_zombie_position(), self._position1)


class TestGameTask2(TestFunctionality):
    """ Base class for testing task 2 of the game. """
    def setUp(self) -> None:
        self._grid = self.a2.Grid(6)
        self._position1 = self.a2_support.Position(0, 3)
        self._position2 = self.a2_support.Position(5, 5)
        self._position3 = self.a2_support.Position(3, 1)
        self._hospital = self.a2.Hospital()
        self._player = self.a2.VulnerablePlayer()
        self._zombie = self.a2.Zombie()
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._position2, self._hospital)
        self._grid.add_entity(self._position3, self._zombie)
        self.set_seed()

    def _find_zombie_position(self, zombie):
        for position, entity in self._grid.get_mapping().items():
            if entity is zombie:
                return position


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="VulnerablePlayer")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="Zombie")
class TestSimpleGamePolymorphismTask2(TestGameTask2):
    """ Test Simple Game Polymorphism Task 2 """
    
    def setUp(self) -> None:
        super().setUp()
        self._game = self.a2.Game(self._grid)

    def test_game_won(self):
        """ Test move vulnerable player to win position """
        self._game.get_grid().move_entity(self._position1, self._position2)
        self.assertTrue(self._game.has_won())

    @skipIfFailed(TestZombie, TestZombie.test_step)
    def test_step_zombie_moved(self):
        """ Test calling step moves the zombie in the correct directions """
        expected_positions = [(3, 0), (4, 0), (5, 0), (4, 0), (5, 0), (4, 0),
                              (4, 1), (3, 1), (3, 2), (3, 1)]
        for i in range(10):
            self.assertIsNone(self._game.step())
            self.assertEqual(self._find_zombie_position(self._zombie),
                             self.a2_support.Position(*expected_positions[i]))

    @skipIfFailed(TestZombie, TestZombie.test_infect_player)
    @skipIfFailed(TestVulnerablePlayer, TestVulnerablePlayer.test_infect)
    def test_step_zombie_infect_player(self):
        """ Test calling step causes zombie to infect player """
        self._grid.move_entity(self._position1, self.a2_support.Position(3, 0))
        self.assertIsNone(self._game.step())
        self.assertTrue(self._player.is_infected())


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="IntermediateGame")
class TestIntermediateGameSample(TestGameTask2):
    """ Test IntermediateGame Sample """

    def setUp(self) -> None:
        super().setUp()
        self._game = self.a2.IntermediateGame(self._grid)

    def test_get_grid(self):
        """ Test get grid """
        self.assertIs(self._game.get_grid(), self._grid)

    def test_get_player(self):
        """ Test get player in game """
        self.assertIs(self._game.get_player(), self._player)

    def test_step_returns_none(self):
        """ Test calling step returns None """
        self.assertIsNone(self._game.step())

    def test_get_steps(self):
        """ Test get_steps """
        for i in range(100):
            self.assertEqual(self._game.get_steps(), i)
            self._game.step()

    def test_move_player(self):
        """ Test moving the player """
        self.assertIsNone(self._game.move_player(self.a2_support.Position(2, 2)))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(2, 5))

    def test_move_player_negative_offset(self):
        """ Test moving the player with a negative offset """
        self.assertIsNone(self._game.move_player(self.a2_support.Position(0, -2)))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(0, 1))

    def test_direction_to_offset_W(self):
        """ Test converting 'W' direction to offset """
        self.assertEqual(self._game.direction_to_offset("W"),
                         self.a2_support.Position(0, -1))

    def test_direction_to_offset_lowercase(self):
        """ Test converting lowercase directions to offset """
        self.assertIsNone(self._game.direction_to_offset("w"))
        self.assertIsNone(self._game.direction_to_offset("a"))
        self.assertIsNone(self._game.direction_to_offset("s"))
        self.assertIsNone(self._game.direction_to_offset("d"))

    def test_has_won_true(self):
        """ Test has won returning True """
        self._game.move_player(self.a2_support.Position(5, 2))
        self.assertTrue(self._game.has_won())

    def test_has_won_false(self):
        """ Test has won returning False """
        self.assertFalse(self._game.has_won())

    @skipIfFailed(TestZombie, TestZombie.test_step)
    def test_step_zombie_moved(self):
        """ Test calling step moves the zombie in the correct directions """
        expected_positions = [(3, 0), (4, 0), (5, 0), (4, 0), (5, 0), (4, 0),
                              (4, 1), (3, 1), (3, 2), (3, 1)]
        for i in range(10):
            self.assertIsNone(self._game.step())
            self.assertEqual(self._find_zombie_position(self._zombie),
                             self.a2_support.Position(*expected_positions[i]))

    @skipIfFailed(TestZombie, TestZombie.test_infect_player)
    @skipIfFailed(TestVulnerablePlayer, TestVulnerablePlayer.test_infect)
    def test_step_zombie_infect_player(self):
        """ Test calling step causes zombie to infect player """
        self._grid.move_entity(self._position1, self.a2_support.Position(3, 0))
        self.assertIsNone(self._game.step())
        self.assertTrue(self._player.is_infected())

    @skipIfFailed(TestZombie, TestZombie.test_step)
    def test_step_two_zombies(self):
        """ Test calling step with two zombies """
        zombie2 = self.a2.Zombie()
        self._grid.add_entity(self.a2_support.Position(4, 4), zombie2)
        expected_positions = [(3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 1),
                              (5, 0), (4, 0), (3, 0), (3, 1)]
        expected_positions2 = [(5, 4), (4, 4), (3, 4), (2, 4), (2, 3), (2, 4),
                               (1, 4), (1, 3), (1, 4), (1, 3)]
        for i in range(10):
            self.assertIsNone(self._game.step())
            self.assertEqual(self._find_zombie_position(self._zombie),
                             self.a2_support.Position(*expected_positions[i]))
            self.assertEqual(self._find_zombie_position(zombie2),
                             self.a2_support.Position(*expected_positions2[i]))


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="IntermediateMapLoader")
class TestIntermediateMapLoader(TestFunctionality):
    """ Test IntermediateMapLoader """

    def test_create_player(self):
        """ Test creating a vulnerable player """
        loader = self.a2.IntermediateMapLoader()
        self.assertIsInstance(loader.create_entity("P"),
                              self.a2.VulnerablePlayer)

    def test_create_hospital(self):
        """ Test creating a hospital """
        loader = self.a2.IntermediateMapLoader()
        self.assertIsInstance(loader.create_entity("H"), self.a2.Hospital)

    def test_create_zombie(self):
        """ Test creating a zombie """
        loader = self.a2.IntermediateMapLoader()
        self.assertIsInstance(loader.create_entity("Z"), self.a2.Zombie)

    def test_create_invalid_entity(self):
        """ Test attempting to create an invalid entity with an intermediate map loader """
        loader = self.a2.IntermediateMapLoader()
        self.assertRaises(ValueError, loader.create_entity, "A")

    def test_load_basic_map(self):
        """ Test loading a basic map with an intermediate map loader """
        loader = self.a2.IntermediateMapLoader()
        grid = loader.load(str(MAPS_DIR / "basic2.txt"))
        player_pos = self.a2_support.Position(8, 0)
        hospital_pos = self.a2_support.Position(5, 6)
        zombie_pos1 = self.a2_support.Position(5, 3)
        zombie_pos2 = self.a2_support.Position(5, 4)
        player = grid.get_entity(player_pos)
        hospital = grid.get_entity(hospital_pos)
        zombie1 = grid.get_entity(zombie_pos1)
        zombie2 = grid.get_entity(zombie_pos2)
        self.assertIsInstance(player, self.a2.VulnerablePlayer)
        self.assertIsInstance(hospital, self.a2.Hospital)
        self.assertIsInstance(zombie1, self.a2.Zombie)
        self.assertIsInstance(zombie2, self.a2.Zombie)
        self.assertListSimilar(grid.get_entities(), [hospital, player,
                                                     zombie1, zombie2])
        expected_mapping = {player_pos: player, hospital_pos: hospital,
                            zombie_pos1: zombie1, zombie_pos2: zombie2}
        self.assertDictEqual(grid.get_mapping(), expected_mapping)


class TestTextInterfaceTask2Root(TestInterface):
    """ Base class for testing the task 2 text interface. """
    
    def setUp(self) -> None:
        super().setUp()
        self._zombie_pos = self.a2_support.Position(3, 2)
        self._zombie_pos2 = self.a2_support.Position(3, 0)
        self._grid.add_entity(self._player_pos, self.a2.VulnerablePlayer())
        self._grid.add_entity(self._zombie_pos, self.a2.Zombie())
        self._grid.add_entity(self._zombie_pos2, self.a2.Zombie())
        self._game = self.a2.IntermediateGame(self._grid)
        self._interface = self.a2.TextInterface(5)
        self.set_seed()


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="TextInterface")
class TestTextInterfaceTask2(TestTextInterfaceTask2Root):
    """ Test TextInterface Task 2 """

    def test_play_map_with_zombies(self):
        """ Test play map with zombies """
        self.assertPlay("with_zombies.in", "with_zombies.out")

    def test_lose_game_with_zombies(self):
        """ Test play and lose game with zombie """
        self._grid.add_entity(self.a2_support.Position(1, 3), self.a2.Zombie())
        self.assertPlay("lose.in", "lose.out")


class TestTrackingZombieRoot(TestGenericEntity):
    """ Base class for testing TrackingZombie. """
    
    def setUp(self) -> None:
        self._grid = self.a2.Grid(6)
        self._game = self.a2.Game(self._grid)
        self._zombie = self.a2.TrackingZombie()
        self._zombie2 = self.a2.TrackingZombie()
        self._player = self.a2.VulnerablePlayer()

    def _find_zombie_position(self, zombie):
        for position, entity in self._grid.get_mapping().items():
            if entity is zombie:
                return position

    def _test_step(self, zombie_position, player_position, expected_positions):
        self._grid.add_entity(player_position, self._player)
        self._grid.add_entity(zombie_position, self._zombie)
        current_position = zombie_position
        for position in expected_positions:
            self._zombie.step(current_position, self._game)
            current_position = self.a2_support.Position(*position)
            self.assertEqual(self._find_zombie_position(self._zombie),
                             current_position)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3,
              tag="TrackingZombie")
class TestTrackingZombie(TestTrackingZombieRoot):
    """ Test TrackingZombie """
    
    def test_display(self):
        """ Test TrackingZombie display """
        self.assertEqual(self._zombie.display(), "T")

    def test_step_from_E(self):
        """ Test move closer to player from east side """
        zombie_position = self.a2_support.Position(5, 3)
        player_position = self.a2_support.Position(0, 3)
        expected_positions = [(4, 3), (3, 3), (2, 3), (1, 3)]
        self._test_step(zombie_position, player_position, expected_positions)

    def test_step_from_W(self):
        """ Test move closer to player from west side """
        zombie_position = self.a2_support.Position(0, 4)
        player_position = self.a2_support.Position(5, 4)
        expected_positions = [(1, 4), (2, 4), (3, 4), (4, 4)]
        self._test_step(zombie_position, player_position, expected_positions)

    def test_step_from_N(self):
        """ Test move closer to player from north side """
        zombie_position = self.a2_support.Position(4, 0)
        player_position = self.a2_support.Position(4, 5)
        expected_positions = [(4, 1), (4, 2), (4, 3), (4, 4)]
        self._test_step(zombie_position, player_position, expected_positions)

    def test_step_from_S(self):
        """ Test move closer to player from south side """
        zombie_position = self.a2_support.Position(3, 5)
        player_position = self.a2_support.Position(3, 0)
        expected_positions = [(3, 4), (3, 3), (3, 2), (3, 1)]
        self._test_step(zombie_position, player_position, expected_positions)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3,
              tag="Garlic")
class TestGarlic(TestGenericEntity):
    """ Test Garlic """

    def setUp(self) -> None:
        super().setUp()
        self._garlic = self.a2.Garlic()

    def test_display(self):
        """ Test display """
        self.assertEqual(self._garlic.display(), "G")

    def test_get_durability(self):
        """ Test get durability """
        self.assertEqual(self._garlic.get_durability(), 10)

    def test_get_lifetime(self):
        """ Test get lifetime after instantiating """
        self.assertEqual(self._garlic.get_lifetime(), 10)

    def test_get_lifetime_with_hold(self):
        """ Test holding decreases lifetime """
        for i in range(10):
            self.assertIsNone(self._garlic.hold())
            self.assertEqual(self._garlic.get_lifetime(), 10 - i - 1)

    def test_step(self):
        """ Test step does nothing """
        for i in range(10):
            self.assertIsNone(self._garlic.step(self._position1, self._game))
            self.assertEqual(self._garlic.get_lifetime(), 10)
            self.assertEqual(self._garlic.get_durability(), 10)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3,
              tag="Crossbow")
class TestCrossbow(TestGenericEntity):
    """ Test Crossbow """

    def setUp(self) -> None:
        super().setUp()
        self._crossbow = self.a2.Crossbow()

    def test_display(self):
        """ Test display """
        self.assertEqual(self._crossbow.display(), "C")

    def test_get_durability(self):
        """ Test get durability """
        self.assertEqual(self._crossbow.get_durability(), 5)

    def test_get_lifetime(self):
        """ Test get lifetime after instantiating """
        self.assertEqual(self._crossbow.get_lifetime(), 5)

    def test_get_lifetime_with_hold(self):
        """ Test holding decreases lifetime """
        for i in range(5):
            self.assertIsNone(self._crossbow.hold())
            self.assertEqual(self._crossbow.get_lifetime(), 5 - i - 1)

    def test_step(self):
        """ Test step does nothing """
        for i in range(5):
            self.assertIsNone(self._crossbow.step(self._position1, self._game))
            self.assertEqual(self._crossbow.get_lifetime(), 5)
            self.assertEqual(self._crossbow.get_durability(), 5)


class TestInventoryRoot(TestFunctionality):
    """ A base class for testing the inventory. """
    def setUp(self) -> None:
        self._garlic = self.a2.Garlic()
        self._crossbow = self.a2.Crossbow()
        self._inventory = self.a2.Inventory()


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              tag="Inventory")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3,
              tag="Garlic")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3,
              tag="Crossbow")
class TestInventory(TestInventoryRoot):
    """ Test Inventory """

    def test_get_items(self):
        """ Test get items returning an empty list initially """
        self.assertListEqual(self._inventory.get_items(), [])

    def test_add_item(self):
        """ Test add one item """
        self.assertIsNone(self._inventory.add_item(self._garlic))
        self.assertListEqual(self._inventory.get_items(), [self._garlic])

    def test_add_items(self):
        """ Test add two different items """
        self.assertIsNone(self._inventory.add_item(self._garlic))
        self.assertIsNone(self._inventory.add_item(self._crossbow))
        self.assertListSimilar(self._inventory.get_items(),
                               [self._garlic, self._crossbow])

    def test_contains_false(self):
        """ Test inventory contains nothing initially """
        self.assertFalse(self._inventory.contains("G"))
        self.assertFalse(self._inventory.contains("C"))

    def test_contains_after_add(self):
        """ Test inventory contains an item after adding that item """
        self._inventory.add_item(self._garlic)
        self.assertTrue(self._inventory.contains("G"))
        self.assertFalse(self._inventory.contains("C"))

    def test_step(self):
        """ Test step decreases inventory item's lifetime """
        self._inventory.add_item(self._crossbow)
        self._inventory.add_item(self._garlic)
        for i in range(5):
            self.assertEqual(self._crossbow.get_lifetime(), 5 - i)
            self.assertEqual(self._garlic.get_lifetime(), 10 - i)
            self.assertIsNone(self._inventory.step())


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "HoldingPlayer")
class TestHoldingPlayer(TestGenericEntity):
    """ Test HoldingPlayer """
    
    def setUp(self) -> None:
        super().setUp()
        self._player = self.a2.HoldingPlayer()

    def test_display(self):
        """ Test holding player display """
        self.assertEqual(self._player.display(), "P")

    def test_is_infected(self):
        """ Test is_infected returns False after instantiating player """
        self.assertFalse(self._player.is_infected())

    def test_infect(self):
        """ Test infecting player """
        self._player.infect()
        self.assertTrue(self._player.is_infected())

    @skipIfFailed(TestDesign,
                  TestDesign.test_classes_and_functions_defined_task_3.__name__,
                  tag="Inventory")
    def test_empty_inventory(self):
        """ Test holding player empty inventory """
        self.assertListEqual(self._player.get_inventory().get_items(), [])

    @skipIfFailed(TestDesign,
                  TestDesign.test_classes_and_functions_defined_task_3.__name__,
                  tag="Inventory")
    @skipIfFailed(TestDesign,
                  TestDesign.test_classes_and_functions_defined_task_3,
                  tag="Garlic")
    def test_step_with_inventory(self):
        """ Test calling step triggers the step event of the inventory """
        garlic = self.a2.Garlic()
        self._player.get_inventory().add_item(garlic)
        self._grid.add_entity(self.a2_support.Position(2, 2), self._player)
        self._grid.add_entity(self.a2_support.Position(2, 3), garlic)
        for i in range(10):
            self._player.step(self.a2_support.Position(2, 2), self._game)
            self.assertEqual(garlic.get_lifetime(), 10 - i - 1)

    @skipIfFailed(TestDesign,
                  TestDesign.test_classes_and_functions_defined_task_3.__name__,
                  tag="Inventory")
    @skipIfFailed(TestDesign,
                  TestDesign.test_classes_and_functions_defined_task_3,
                  tag="Garlic")
    def test_infect_with_garlic(self):
        """ Test that a player holding garlic is not infected """
        garlic = self.a2.Garlic()
        self._player.get_inventory().add_item(garlic)
        self._player.infect()
        self.assertFalse(self._player.is_infected())


class TestGameTask3(TestFunctionality):
    """ A base class for testing task 3 of the game. """

    def setUp(self) -> None:
        self._grid = self.a2.Grid(6)
        self._position1 = self.a2_support.Position(0, 3)
        self._position2 = self.a2_support.Position(5, 5)
        self._position3 = self.a2_support.Position(3, 1)
        self._position4 = self.a2_support.Position(3, 0)
        self._position5 = self.a2_support.Position(2, 1)
        self._position6 = self.a2_support.Position(3, 2)
        self._hospital = self.a2.Hospital()
        self._player = self.a2.HoldingPlayer()
        self._zombie = self.a2.Zombie()
        self._garlic = self.a2.Garlic()
        self._crossbow = self.a2.Crossbow()
        self._tracking_zombie = self.a2.TrackingZombie()
        self._grid.add_entity(self._position1, self._player)
        self._grid.add_entity(self._position2, self._hospital)
        self._grid.add_entity(self._position3, self._zombie)
        self._grid.add_entity(self._position4, self._tracking_zombie)
        self._grid.add_entity(self._position5, self._garlic)
        self._grid.add_entity(self._position6, self._crossbow)
        self.set_seed()

    def _find_zombie_position(self, zombie):
        for position, entity in self._grid.get_mapping().items():
            if entity is zombie:
                return position


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "HoldingPlayer")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "TestTrackingZombie")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "Garlic")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "Crossbow")
class TestSimpleGamePolymorphismTask3(TestGameTask3):
    """ Test Simple Game Polymorphism Task 3 """
    def setUp(self) -> None:
        super().setUp()
        self._game = self.a2.Game(self._grid)

    def test_step_with_task3_entities(self):
        """ Test calling step with task 3 entities """
        expected_positions1 = [(4, 1), (5, 1), (5, 2), (4, 2), (5, 2), (4, 2),
                               (4, 3), (3, 3), (3, 4), (3, 3)]
        expected_positions2 = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 2),
                               (0, 2), (0, 2), (0, 2), (0, 2)]
        for i in range(10):
            self.assertIsNone(self._game.step())
            expected_mapping = {
                self.a2_support.Position(0, 3): self._player,
                self.a2_support.Position(5, 5): self._hospital,
                self.a2_support.Position(2, 1): self._garlic,
                self.a2_support.Position(3, 2): self._crossbow,
                self.a2_support.Position(*expected_positions1[i]): self._zombie,
                self.a2_support.Position(*expected_positions2[i]): self._tracking_zombie
            }
            self.assertDictEqual(self._game.get_grid().get_mapping(),
                                 expected_mapping)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "HoldingPlayer")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "TestTrackingZombie")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "Garlic")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "Crossbow")
class TestIntermediateGamePolymorphismTask3(TestGameTask3):
    """ Test Intermediate Game Polymorphism Task 3 """
    def setUp(self) -> None:
        super().setUp()
        self._game = self.a2.IntermediateGame(self._grid)

    def test_step_with_task3_entities(self):
        """ Test calling step with task 3 entities """
        expected_positions1 = [(4, 1), (5, 1), (5, 2), (4, 2), (5, 2), (4, 2),
                               (4, 3), (3, 3), (3, 4), (3, 3)]
        expected_positions2 = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 2),
                               (0, 2), (0, 2), (0, 2), (0, 2)]
        for i in range(10):
            self.assertIsNone(self._game.step())
            if i >= 5:
                self.assertTrue(self._game.has_lost())
            else:
                self.assertFalse(self._game.has_lost())
            expected_mapping = {
                self.a2_support.Position(0, 3): self._player,
                self.a2_support.Position(5, 5): self._hospital,
                self.a2_support.Position(2, 1): self._garlic,
                self.a2_support.Position(3, 2): self._crossbow,
                self.a2_support.Position(*expected_positions1[i]): self._zombie,
                self.a2_support.Position(*expected_positions2[i]): self._tracking_zombie
            }
            self.assertDictEqual(self._game.get_grid().get_mapping(),
                                 expected_mapping)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "AdvancedGame")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "TestTrackingZombie")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "HoldingPlayer")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "Garlic")
@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              "Crossbow")
class TestAdvancedGameSample(TestGameTask3):
    """Test Advanced Game Sample """
    def setUp(self) -> None:
        super().setUp()
        self._game = self.a2.AdvancedGame(self._grid)

    def test_get_grid(self):
        """ Test get grid """
        self.assertIs(self._game.get_grid(), self._grid)

    def test_get_player(self):
        """ Test get player in game """
        self.assertIs(self._game.get_player(), self._player)

    def test_step_returns_none(self):
        """ Test calling step returns None """
        self.assertIsNone(self._game.step())

    def test_get_steps(self):
        """ Test get_steps """
        for i in range(100):
            self.assertEqual(self._game.get_steps(), i)
            self._game.step()

    def test_move_player(self):
        """ Test moving the player """
        self.assertIsNone(self._game.move_player(self.a2_support.Position(2, 2)))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(2, 5))

    def test_move_player_negative_offset(self):
        """ Test moving the player with a negative offset """
        self.assertIsNone(self._game.move_player(self.a2_support.Position(0, -2)))
        self.assertEqual(self._game.get_grid().find_player(),
                         self.a2_support.Position(0, 1))

    def test_direction_to_offset_W(self):
        """ Test converting 'W' direction to offset """
        self.assertEqual(self._game.direction_to_offset("W"),
                         self.a2_support.Position(0, -1))

    def test_direction_to_offset_lowercase(self):
        """ Test converting lowercase directions to offset """
        self.assertIsNone(self._game.direction_to_offset("w"))
        self.assertIsNone(self._game.direction_to_offset("a"))
        self.assertIsNone(self._game.direction_to_offset("s"))
        self.assertIsNone(self._game.direction_to_offset("d"))

    def test_has_won_true(self):
        """ Test has won returning True """
        self._game.move_player(self.a2_support.Position(5, 2))
        self.assertTrue(self._game.has_won())

    def test_has_won_false(self):
        """ Test has won returning False """
        self.assertFalse(self._game.has_won())

    def test_has_lost(self):
        """ Test has lost """
        self.assertFalse(self._game.has_lost())

    @skipIfFailed(TestZombie, TestZombie.test_step)
    def test_step_zombie_moved(self):
        """ Test calling step moves the zombie in the correct directions """
        expected_positions = [(4, 1), (5, 1), (5, 2), (4, 2), (5, 2), (4, 2),
                              (4, 3), (3, 3), (3, 4), (3, 3)]
        expected_positions2 = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 2),
                               (0, 2), (0, 2), (0, 2), (0, 2)]
        for i in range(10):
            self.assertIsNone(self._game.step())
            self.assertEqual(self._find_zombie_position(self._zombie),
                             self.a2_support.Position(*expected_positions[i]))
            self.assertEqual(self._find_zombie_position(self._tracking_zombie),
                             self.a2_support.Position(*expected_positions2[i]))

    def test_step_zombie_infect_player(self):
        """ Test calling step causes zombie to infect player """
        self._grid.move_entity(self._position1, self.a2_support.Position(4, 1))
        self.assertIsNone(self._game.step())
        self.assertTrue(self._player.is_infected())

    def test_step_tracking_zombie_infect_player(self):
        """ Test calling step causes tracking zombie to infect player """
        self._grid.move_entity(self._position1, self.a2_support.Position(2, 0))
        self.assertIsNone(self._game.step())
        self.assertTrue(self._player.is_infected())

    @skipIfFailed(TestDesign,
                  TestDesign.test_classes_and_functions_defined_task_3.__name__,
                  "Inventory")
    def test_move_player_pick_up(self):
        """ Test move player and pick up an item """
        self.assertListEqual(self._player.get_inventory().get_items(), [])
        self._game.move_player(self.a2_support.Position(2, -2))
        self.assertListEqual(self._player.get_inventory().get_items(),
                             [self._garlic])
        expected_mapping = {
            self._position5: self._player,
            self._position2: self._hospital,
            self._position3: self._zombie,
            self._position4: self._tracking_zombie,
            self._position6: self._crossbow,
        }
        self.assertDictEqual(self._game.get_grid().get_mapping(),
                             expected_mapping)


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_2.__name__,
              tag="AdvancedMapLoader")
class TestAdvancedMapLoader(TestFunctionality):
    """ Test AdvancedMapLoader """

    def test_create_player(self):
        """ Test creating a holding player """
        loader = self.a2.AdvancedMapLoader()
        self.assertIsInstance(loader.create_entity("P"), self.a2.HoldingPlayer)

    def test_create_hospital(self):
        """ Test creating a hospital """
        loader = self.a2.AdvancedMapLoader()
        self.assertIsInstance(loader.create_entity("H"), self.a2.Hospital)

    def test_create_zombie(self):
        """ Test creating a zombie """
        loader = self.a2.AdvancedMapLoader()
        self.assertIsInstance(loader.create_entity("Z"), self.a2.Zombie)

    def test_create_garlic(self):
        """ Test creating a garlic """
        loader = self.a2.AdvancedMapLoader()
        self.assertIsInstance(loader.create_entity("G"), self.a2.Garlic)

    def test_create_crossbow(self):
        """ Test creating a crossbow """
        loader = self.a2.AdvancedMapLoader()
        self.assertIsInstance(loader.create_entity("C"), self.a2.Crossbow)

    def test_create_tracking_zombie(self):
        """ Test creating a tracking zombie """
        loader = self.a2.AdvancedMapLoader()
        self.assertIsInstance(loader.create_entity("T"), self.a2.TrackingZombie)

    def test_create_invalid_entity(self):
        """ Test attempting to create an invalid entity with an advanced map loader """
        loader = self.a2.AdvancedMapLoader()
        self.assertRaises(ValueError, loader.create_entity, "A")

    def test_load_basic_map(self):
        """ Test loading a basic map with an advanced map loader """
        loader = self.a2.AdvancedMapLoader()
        grid = loader.load(str(MAPS_DIR / "basic3.txt"))
        player_pos = self.a2_support.Position(8, 0)
        hospital_pos = self.a2_support.Position(5, 6)
        zombie_pos1 = self.a2_support.Position(5, 3)
        zombie_pos2 = self.a2_support.Position(5, 4)
        tracking_zombie_pos = self.a2_support.Position(3, 7)
        player = grid.get_entity(player_pos)
        hospital = grid.get_entity(hospital_pos)
        zombie1 = grid.get_entity(zombie_pos1)
        zombie2 = grid.get_entity(zombie_pos2)
        tracking_zombie = grid.get_entity(tracking_zombie_pos)
        self.assertIsInstance(player, self.a2.VulnerablePlayer)
        self.assertIsInstance(hospital, self.a2.Hospital)
        self.assertIsInstance(zombie1, self.a2.Zombie)
        self.assertIsInstance(zombie2, self.a2.Zombie)
        self.assertIsInstance(tracking_zombie, self.a2.TrackingZombie)
        self.assertListSimilar(grid.get_entities(), [hospital, player,
                                                     zombie1, zombie2,
                                                     tracking_zombie])
        expected_mapping = {player_pos: player, hospital_pos: hospital,
                            zombie_pos1: zombie1, zombie_pos2: zombie2,
                            tracking_zombie_pos: tracking_zombie}
        self.assertDictEqual(grid.get_mapping(), expected_mapping)


class TestTextInterfaceTask3Root(TestInterface):
    """ Base class for testing the task 3 text interface. """

    def setUp(self) -> None:
        super().setUp()
        self._zombie_pos = self.a2_support.Position(3, 2)
        self._zombie_pos2 = self.a2_support.Position(4, 0)
        self._garlic_pos = self.a2_support.Position(0, 2)
        self._crossbow_pos = self.a2_support.Position(0, 4)
        self._player = self.a2.HoldingPlayer()
        self._tracking_zombie = self.a2.TrackingZombie()
        self._grid.add_entity(self._player_pos, self._player)
        self._grid.add_entity(self._zombie_pos, self.a2.Zombie())
        self._grid.add_entity(self._zombie_pos2, self._tracking_zombie)
        self._grid.add_entity(self._garlic_pos, self.a2.Garlic())
        self._grid.add_entity(self._crossbow_pos, self.a2.Crossbow())
        self._game = self.a2.AdvancedGame(self._grid)
        self._interface = self.a2.TextInterface(5)
        self.set_seed()

    def _find_zombie_position(self, zombie):
        for position, entity in self._grid.get_mapping().items():
            if entity is zombie:
                return position


@skipIfFailed(TestDesign,
              TestDesign.test_classes_and_functions_defined_task_3.__name__,
              tag="AdvancedTextInterface")
class TestAdvancedTextInterface(TestTextInterfaceTask3Root):
    def setUp(self) -> None:
        super().setUp()
        self._interface = self.a2.AdvancedTextInterface(5)

    def test_draw_task3(self):
        """ Test draw with task 3 items """
        expected = "#######\n" \
                   "#    T#\n" \
                   "# P   #\n" \
                   "#G  Z #\n" \
                   "#     #\n" \
                   "#C   H#\n" \
                   "#######\n"
        with RedirectStdIO(stdout=True) as stdio:
            self._interface.draw(self._game)

        self.assertMultiLineEqual(stdio.stdout, expected)

    def test_draw_holding_player(self):
        """ Test draw player holding items """
        self._player.get_inventory().add_item(self.a2.Garlic())
        self._player.get_inventory().add_item(self.a2.Crossbow())
        expected = "#######\n" \
                   "#    T#\n" \
                   "# P   #\n" \
                   "#G  Z #\n" \
                   "#     #\n" \
                   "#C   H#\n" \
                   "#######\n" \
                   "The player is currently holding:\n" \
                   "Garlic(10)\n" \
                   "Crossbow(5)\n"
        with RedirectStdIO(stdout=True) as stdio:
            self._interface.draw(self._game)
        self.assertMultiLineEqual(stdio.stdout, expected)

    def test_handle_action_pick_up_item(self):
        """ Test handle action picking up item """
        garlic = self.a2.Garlic()
        self._grid.add_entity(self.a2_support.Position(0, 1), garlic)
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = "A\n"
            self._interface.handle_action(self._game, "A")
        self.assertMultiLineEqual(stdio.stdinout, "")
        self.assertListEqual(self._player.get_inventory().get_items(), [garlic])
        self.assertEqual(garlic.get_lifetime(), 9)

    def test_handle_action_fire(self):
        """ Test handle fire action killing zombie """
        self._player.get_inventory().add_item(self.a2.Crossbow())
        self._game.move_player(self.a2_support.Position(-1, -1))
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = "D\n"
            self._interface.handle_action(self._game, "F")
        self.assertMultiLineEqual(stdio.stdinout, "Direction to fire: D\n")
        self.assertIsNone(self._find_zombie_position(self._tracking_zombie))

    def test_handle_action_fire_no_zombie(self):
        """ Test handle fire action no zombie case """
        self._player.get_inventory().add_item(self.a2.Crossbow())
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = "A\n"
            self._interface.handle_action(self._game, "F")
        self.assertMultiLineEqual(stdio.stdinout, "Direction to fire: A\nNo "
                                                  "zombie in that direction!\n")

    def test_player_with_garlic(self):
        """ Test game where player picks up garlic """
        self.assertPlay("with_garlic_advanced.in", "with_garlic_advanced.out")

    def test_player_with_crossbow(self):
        """ Test game where player picks up crossbow """
        self.assertPlay("with_crossbow_advanced.in",
                        "with_crossbow_advanced.out")

    def test_crossbow_shoot(self):
        """ Test game where player shoots zombie using crossbow """
        self.assertPlay("crossbow_shoot.in", "crossbow_shoot.out")

    def test_crossbow_missed_shot(self):
        """ Test game where player shoots and misses """
        self.assertPlay("crossbow_missed.in", "crossbow_missed.out")


def main():
    """ run tests """
    test_cases = [
        TestDesign,
        TestEntity,
        TestPlayer,
        TestHospital,
        TestGridSample,
        TestMapLoader,
        TestBasicMapLoader,
        TestGameSample,
        TestTextInterface,
        TestVulnerablePlayer,
        TestZombie,
        TestSimpleGamePolymorphismTask2,
        TestIntermediateGameSample,
        TestIntermediateMapLoader,
        TestTextInterfaceTask2,
        TestTrackingZombie,
        TestGarlic,
        TestCrossbow,
        TestInventory,
        TestHoldingPlayer,
        TestSimpleGamePolymorphismTask3,
        TestIntermediateGamePolymorphismTask3,
        TestAdvancedGameSample,
        TestAdvancedMapLoader,
        TestAdvancedTextInterface
    ]
    master = TestMaster(max_diff=None,
                        suppress_stdout=True,
                        timeout=1,
                        include_no_print=True,
                        scripts=[
                            ('a2', 'a2.py'),
                            ('a2_support', 'a2_support.py')
                        ])
    result = master.run(test_cases)


if __name__ == '__main__':
    main()
