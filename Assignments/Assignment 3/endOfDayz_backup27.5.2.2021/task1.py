import tkinter as tk
from tkinter import messagebox
from a2_solution import *


class AbstractGrid(tk.Canvas):
    """
    AbstractGrid is an abstract view class which inherits from tk.Canvas and
    provide base functionality for other view classes. The AbstractGrid
    represents a grid with a set number of rows and columns. This allows the
    creation of information to be stored at a position in the grid.
    """

    def __init__(self, master: tk.Tk, rows: int, cols: int, width: int,
                 height: int, **kwargs):
        """
        Constructor for abstract grid.
        @param master: the root element.
        @param rows: rows in grid.
        @param cols: columns in grid.
        @param width: width of grid.
        @param height: height of grid.
        @param kwargs: Extra tkinter arguments.
        """

        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height

        super(AbstractGrid, self).__init__(width=self._width,
                                           height=self._height, **kwargs)

    def get_bbox(self, position: Position) -> tuple[int, int, int, int]:
        """
        Returns the bounding box for a (row, column) position as a tuple in the
        form (x_min, y_min, x_max, y_max).
        @param position: Position to get bounding box of.
        @return: Tuple containing the bounding box of the inputted position.
        """

        column, row = position.get_x(), position.get_y()

        x_min = int(column * (self._width / self._cols))
        x_max = int(x_min + (self._width / self._cols))

        y_min = int(row * (self._height / self._rows))
        y_max = int(y_min + (self._height / self._rows))

        return x_min, y_min, x_max, y_max

    def pixel_to_position(self, pixel: tuple) -> Position:
        """
        Converts the (x,y) pixel position (in graphics units) to a (row, column)
        position.
        @param pixel: Tuple containing x and y coordinate of a pixel.
        @return: Position instance of a row and column of the grid.
        """

        x, y = pixel

        column_size = self._width / self._cols
        row_size = self._height / self._rows

        return Position(int(x // column_size), int(y // row_size))

    def get_position_centre(self, position: Position) -> Position:
        """
        Gets the graphics coordinates for the centre of the cell at the given
        (row, column) position.
        @param position: Position from the grid.
        @return: Position containing the coordinates of the centre of input.
        """

        bbox = self.get_bbox(position)

        x_min, y_min, x_max, y_max = bbox

        x_centre = (x_min + x_max) // 2
        y_centre = (y_min + y_max) // 2

        return Position(x_centre, y_centre)

    def annotate_position(self, position: Position, text: str, **kwargs) -> \
            None:
        """
        Annotates the centre of the cell at the given (row, column) position
        with the provided text.
        @param position: Position to annotate at.
        @param text: Text as string to place at position.
        @return: None.
        """

        centre_pos = self.get_position_centre(position)

        x, y = centre_pos.get_x(), centre_pos.get_y()

        self.create_text((x, y), text=text, **kwargs)


class BasicMap(AbstractGrid):
    """
    BasicMap is a view class which inherits from AbstractGrid. Entities are
    drawn on the map using coloured rectangles at different (row, column)
    positions. They are then annotated with what they represent.
    """

    def __init__(self, master: tk.Tk, size: int, **kwargs):
        """
        Constructor for BasicMap.
        @param master: the root element.
        @param size: the size of the canvas to be created.
        @param kwargs: Extra tkinter arguments.
        """

        height = width = CELL_SIZE * size

        super(BasicMap, self).__init__(master, size, size, height, width,
                                       **kwargs)

        self._master = master
        self._size = size

    def draw_entity(self, position: Position, tile_type: str) -> None:
        """
        Draws the entities on the map. However, this time they are drawn with
        graphics, instead of the more basic rectangles.
        @param position: Position to draw the entity at.
        @param tile_type: Type of entity to draw as display format.
        @return: None.
        """

        bgcolour = ENTITY_COLOURS.get(tile_type)

        bbox = self.get_bbox(position)

        x_min, y_min, x_max, y_max = bbox

        self.create_rectangle(
            x_min, y_min, x_max, y_max,
            fill=bgcolour
        )

        if tile_type in [PLAYER, HOSPITAL]:
            fill = "white"
        else:
            fill = "black"

        self.annotate_position(position, tile_type, fill=fill)


class InventoryView(AbstractGrid):
    """
    InventoryView displays the items the player has in their inventory
    graphically on the right hand side of the game window. This class also
    provides a mechanism with which the player can activate items in their
    inventory before using them.
    """

    def __init__(self, master: tk.Tk, rows: int, **kwargs):
        """
        Constructor for InventoryView.
        @param master: the root element
        @param rows: number of rows in the game map.
        @param kwargs: Extra tkinter arguments.
        """

        height = CELL_SIZE * rows - 2

        super(InventoryView, self).__init__(master, rows, 2, INVENTORY_WIDTH,
                                            height, **kwargs)

        self._rows = rows

    def draw(self, inventory: Inventory) -> None:
        """
        Draws the inventory label and current items with their remaining
        lifetimes.
        @param inventory: The player's inventory as an inventory object.
        @return: None.
        """

        # Clear inventory
        self.delete("all")

        # Draw the title of the inventory.
        title_bbox = self.get_bbox(Position(0, 0))
        x_min, y_min, x_max, y_max = title_bbox

        # Inventory is 2 columns. Thus double x_max will make it 'merge' across
        x_max *= 2

        # Get centre of inventory and draw text.
        # Note I didn't use the AbstractGrid method because I wanted a custom x
        # and y centre position due to the 'merging' of columns.
        x_centre = (x_min + x_max) / 2
        y_centre = (y_min + y_max) / 2

        self.create_text(
            (x_centre, y_centre),
            font=("Arial", 20),
            text="Inventory",
            fill=DARK_PURPLE
        )

        # Draw inventory labels
        item_fulltext_lookup = {
            GARLIC: "Garlic",
            CROSSBOW: "Crossbow"
        }

        inv_items = inventory.get_items()

        # Loop through inventory items.
        for i, item in enumerate(inv_items):
            item_text = item.display()
            item_fulltext = item_fulltext_lookup.get(item_text)

            item_health = str(item.get_lifetime())

            # Active item
            text = "black"
            if item.is_active():
                # Highlight item
                text = "white"
                bbox = self.get_bbox(Position(0, i + 1))

                x_min, y_min, x_max, y_max = bbox

                self.create_rectangle(0, y_min, x_max * 2, y_max,
                                      fill=DARK_PURPLE)

            # Item text
            self.annotate_position(Position(0, i + 1), item_fulltext, fill=text)
            self.annotate_position(Position(1, i + 1), item_health, fill=text)

    def toggle_item_activation(self, pixel: tuple, inventory: Inventory) -> \
            None:
        """
        Activates or deactivates the item (if one exists) in the row containing
        the pixel.
        @param pixel: The x, y coordinate of the user's click in the inventory.
        @param inventory: The player's inventory as an Inventory object.
        @return: None.
        """

        # Gets position of click from pixel clicked.
        position = self.pixel_to_position(pixel)
        x, y = position.get_x(), position.get_y() - 1

        inventory_items = inventory.get_items()

        # Finds item in inventory and toggles its active state.
        if y in range(0, len(inventory_items)):
            inventory_items[y].toggle_active()


class BasicGraphicalInterface:
    """
    The BasicGraphicalInterface should manage the overall view (i.e.
    constructing the three major widgets) and event handling.
    """

    def __init__(self, root: tk.Tk, size: int):
        """
        Constructor for the BasicGraphicalInterface.
        @param root: Root element for tkinter.
        @param size: Size of the game map.
        """

        self._root = root
        self._size = size

        self._game_over = False

        root.resizable(False, False)

        # Top banner
        self._top_banner = tk.Label(
            root,
            text=TITLE,
            foreground="white",
            background=DARK_PURPLE
        )

        self._top_banner.config(
            font=("Myriad Pro", 30)
        )

        self._top_banner.pack(side="top", fill="x")

        # Game square
        self._bmap = BasicMap(root, size, background=MAP_BACKGROUND_COLOUR)

        self._bmap.pack(
            side="left",
            fill="both",
            padx=2.5,
            pady=2.5,
            ipadx=2.5,
            ipady=2.5
        )

        # Inventory
        self._inv = InventoryView(root, size, background="#E9E6F0")

        self._inv.pack(side="right", fill="both", padx=2.5, pady=2.5)

    def _inventory_click(self, event: tk.Event, inventory: Inventory) -> None:
        """
        This method is called when the user left clicks on inventory view. It
        handles activating or deactivating the clicked item (if one exists) and
        updating both the model and the view accordingly.
        @param event: Click event.
        @param inventory: Player's inventory as an Inventory object.
        @return: None.
        """

        pixel = (event.x, event.y)

        # Check if item clicked is already active
        position = self._inv.pixel_to_position(pixel)
        x, y = position.get_x(), position.get_y() - 1

        inventory_items = inventory.get_items()

        if y - 1 <= len(inventory_items):
            if not inventory_items[y].is_active():
                # Check for other active items
                inv_items = inventory.get_items()

                for i, item in enumerate(inv_items):
                    if item.is_active() and item:
                        # Deactivate active item
                        item.toggle_active()

            # Redraw inventory.
            self._inv.draw(inventory)

            # Toggle activation of item selected
            self._inv.toggle_item_activation(pixel, inventory)

            # Redraw inventory.
            self._inv.draw(inventory)

    def draw(self, game: AdvancedGame) -> None:
        """
        Clears and redraws the view based on the current game state.
        @param game: Current state of the game.
        @return: None.
        """

        if not self._game_over:
            # Clear and draw main game.
            self._bmap.delete("all")

            grid_mapping = game.get_grid().get_mapping()

            for position, entity in grid_mapping.items():
                self._bmap.draw_entity(position, entity.display())

            player = game.get_player()
            if isinstance(player, HoldingPlayer):
                self._inv.draw(player.get_inventory())

            # Check for game win or game lose
            if game.has_won():
                self._game_over = True
                messagebox.showinfo(title="Game Over", message=WIN_MESSAGE)
            elif game.has_lost():
                self._game_over = True
                messagebox.showinfo(title="Game Over", message=LOSE_MESSAGE)

    def _handle_input(self, event: tk.Event, game: AdvancedGame) -> None:
        """
        Handles the input from the user.
        @param event: Key press event.
        @param game: Instance of current game.
        @return: None.
        """

        # Maps keycodes to character presses. (for cross-platform support)
        moves = {
            65: "A",
            87: "W",
            68: "D",
            83: "S"
        }

        fires = {
            37: "A",    # Left
            38: "W",    # Up
            39: "D",    # Right
            40: "S"     # Down
        }

        keycode = event.keycode

        player = game.get_player()

        if keycode in moves.keys():    # Moving input
            direction = game.direction_to_offset(moves.get(keycode))
            if direction:
                self._move(game, direction)
        elif isinstance(player, HoldingPlayer):
            if player.get_inventory().has_active(CROSSBOW):
                # Fire the weapon in the indicated direction, if possible.
                if keycode in fires.keys():
                    start = game.get_grid().find_player()
                    offset = game.direction_to_offset(fires.get(keycode))

                    # Find the first entity in the direction player fired.
                    first = first_in_direction(game.get_grid(), start, offset)

                    # If the entity is a zombie, kill it.
                    if first is not None and first[1].display() in ZOMBIES:
                        position, entity = first
                        game.get_grid().remove_entity(position)

    def _move(self, game: AdvancedGame, direction: Position) -> None:
        """
        Handles moving the player and redrawing the game.
        @param game: The current game as an AdvancedGame object.
        @param direction: Direction to move player as a position object.
        @return: None.
        """

        # Draw game after player has moved.
        game.move_player(direction)
        self.draw(game)

    def _step(self, game: AdvancedGame) -> None:
        """
        The _step method is called every second. This method triggers the step
        method for the game and updates the view accordingly.
        @param game: The current game as an AdvancedGame object.
        @return: None.
        """

        root = self._root

        game.step()

        def call_step():
            self._step(game)

        # Draw game after zombies have moved.
        root.after(1000, call_step)
        self.draw(game)

    def play(self, game: AdvancedGame) -> None:
        """
        Binds events and initialises gameplay. This method will need to be
        called on the instantiated BasicGraphicalInterface in main to commence
        gameplay.
        @param game: Current state of the game.
        @return: None.
        """

        root = self._root

        # Initial draw of game
        self.draw(game)

        # Move and fire inputs
        def event_parameters(event: tk.Event):
            self._handle_input(event, game)

        root.bind_all("<Key>", event_parameters)

        # Click events
        def click(event: tk.Event):
            player = game.get_player()
            if isinstance(player, HoldingPlayer):
                self._inventory_click(event, player.get_inventory())

        self._inv.bind("<Button-1>", click)

        # Game step
        def call_step():
            self._step(game)

        root.after(0, call_step)
        root.mainloop()
