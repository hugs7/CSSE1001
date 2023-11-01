# Imports
from a2_solution import *
from task1 import AbstractGrid, InventoryView
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # For images, formatting and resizing
import os                       # For creating directories (part of save game)
from datetime import datetime   # For save files
from ast import literal_eval    # Used for converting string rep of dict to dict

# Globals
global current_file     # Stores info for restarting game.
global wait             # tkinter .after() command is set to this. Allows usage
#                         of .after_cancel() for a new instance of game so as
#                         not to cause an error.

# Classes


class StatusBar(tk.Frame):
    """
    The status bar displays extra information to the player in a frame at the
    bottom of the game window. Data includes steps made, a timer, as well as
    restart and quit buttons.
    """

    def __init__(self, master: tk.Tk, restart, **kwargs):
        """
        Constructor for the status bar frame.
        @param master: Frame that status bar is placed in.
        @param restart: Restart function for game.
        @param kwargs: Extra tkinter arguments.
        """

        super(StatusBar, self).__init__(master, **kwargs)

        # Left Image
        self._lft_img = Image.open("images/chaser.png")
        self._lft = ImageTk.PhotoImage(self._lft_img)

        self._chaser = tk.Label(master, image=self._lft)
        self._chaser.pack(side="left", expand=True)

        # Timer
        self._t_frame = tk.Frame(master)
        self._t_frame.pack(side="left", expand=True)

        self._time_title = tk.Label(self._t_frame, text="Timer")
        self._time_title.pack(side="top")

        self._time = tk.Label(self._t_frame, text="0 seconds")
        self._time.pack(side="bottom")

        # Moves made
        self._m_frame = tk.Frame(master)
        self._m_frame.pack(side="left", expand=True)

        self._moves_title = tk.Label(self._m_frame, text="Moves made")
        self._moves_title.pack(side="top")

        self._moves = tk.Label(self._m_frame, text="0 moves")
        self._moves.pack(side="bottom")

        # Buttons
        def restart_bind():
            restart()

        def exit_bind():
            quit()

        self._btn_frame = tk.Frame(master)
        self._btn_frame.pack(side="left", expand=True)

        self._restart = tk.Button(self._btn_frame, text="Restart",
                                  command=restart_bind)
        self._restart.pack(side="top")

        self._quit = tk.Button(self._btn_frame, text="Quit", command=exit_bind)
        self._quit.pack(side="bottom")

        # Right Image
        self._rgt_img = Image.open("images/chasee.png")
        self._rgt = ImageTk.PhotoImage(self._rgt_img)

        self._chasee = tk.Label(master, image=self._rgt)
        self._chasee.pack(side="left", expand=True)

    def update_timer(self, time: int) -> None:
        """
        Updates the view of the game timer
        @param time: Time elapsed in game.
        @return: None.
        """

        timer_text = str(time) + " seconds"

        self._time.config(text=timer_text)

    def update_moves(self, steps: int) -> None:
        """
        Updates the view of the number of moves made.
        @param steps: Steps made by player in game.
        @return: None.
        """

        moves = str(steps) + " moves"

        self._moves.config(text=moves)


class ImageMap(AbstractGrid):
    """
    Behaves similarly to BasicMap class, except that images are used to display
    entities rather than labelled rectangles.
    """

    def __init__(self, master: tk.Tk, size: int, **kwargs):
        """
        Constructor for the ImageMap class.
        @param master: Frame that ImageMap is created on.
        @param size: Size of canvas to be created.
        @param kwargs: Extra tkinter arguments.
        """

        height = width = CELL_SIZE * size

        super(ImageMap, self).__init__(master, size, size, height, width,
                                       **kwargs)

        self._master = master
        self._size = size

        self._entity_imgs = []

    def draw_entity(self, position: Position, tile_type: str) -> None:
        """
        Draws the entities on the map. However, this time they are drawn with
        graphics, instead of the more basic rectangles.
        @param position: Position to draw the entity at.
        @param tile_type: Type of entity to draw as display format.
        @return: None.
        """

        # Add entity image instances to list of images to be used in the grid.
        self._entity_imgs.append(tk.PhotoImage(file=IMAGES.get(tile_type)))

        centre_pos = self.get_position_centre(position)

        # Offset of +2.5 helps images look more centred on tile (don't know why)
        x, y = centre_pos.get_x() + 2.5, centre_pos.get_y() + 2.5

        self.create_image(x, y, image=self._entity_imgs[-1])


class ImageGraphicalInterface:
    """
    The AdvancedGraphicalInterface class builds on the BasicGraphicalInterface
    class to add functionality including textures, higher quality graphics and
    a more functional HUD.
    """

    def __init__(self, root: tk.Tk, size: int):
        """
        Constructor for the AdvancedGraphicalInterface.
        @param root: Root element for tkinter.
        @param size: Size of the game map.
        """

        global current_file

        current_file = ""

        # Game variables
        self._root = root   # Window
        self._size = size   # Game size

        self._game_over = False
        self._game = None   # Gets set in ImageGraphicalInterface.play()
        self._paused = False

        self._time = 0
        self._steps = 0

        # Win/lose
        self._name = None
        self._button_pressed = 0
        self._play_again = None

        # Background tiles
        self._bgs = [[None] * size for _ in range(size)]
        self._bg = None

        # Graphics settings
        root.resizable(False, False)

        # Frames
        # Bottom Frame
        self._bottom_frame = tk.Frame(root)
        self._bottom_frame.pack(side="bottom", fill="both", padx=20, pady=5)

        # Top banner
        self._top_banner = tk.Label(root)
        self._top_banner.pack(side="top", fill="x")

        # Game square
        self._bmap = ImageMap(root, size)
        self._bmap.pack(
            side="left",
            fill="both",
            padx=(5, 0)
        )

        # Inventory
        self._inv = InventoryView(root, size, background="#E9E6F0")
        self._inv.pack(side="right", fill="both", pady=(0, 9))

        # Banner image
        # Must go here so sizing is correct
        self._bnr_img = Image.open("images/banner.png")
        root.update()
        window_width = root.winfo_width()

        self._bnr_img = self._bnr_img.resize((window_width, window_width // 6))
        self._photo_img = ImageTk.PhotoImage(self._bnr_img)

        self._top_banner.config(image=self._photo_img)

        # Menu
        def load_game():
            global current_file

            self.toggle_pause()

            allowed_filetypes = [('text files', '.txt')]

            file_select = filedialog.askopenfilename(
                parent=root,
                initialdir=os.getcwd(),
                title="Please select a savegame",
                filetypes=allowed_filetypes
            )

            if file_select != "":
                current_file = file_select

                # Close current game and create new one
                root.destroy()
                self._root.after_cancel(wait)
                start_game()
            else:
                self.toggle_pause()

        def save_game():
            self.toggle_pause()

            # Make save directory if doesn't already exist
            if not os.path.exists("savegames"):
                os.makedirs("savegames")

            # Set filename to function of current time (to ensure no overwrites)
            now = datetime.now()
            dt_string = now.strftime("%d.%m.%Y.%H.%M.%S")
            save_name = "endOfDayz save - " + str(dt_string) + ".txt"

            # Write to file
            save_file = open("savegames/"+save_name, "a")

            current_mapping = self._game.get_grid().serialize()

            save_file.write(str(current_mapping))
            save_file.write("\n")
            save_file.write(str(self._game.get_grid().get_size()))
            save_file.write("\n")
            player = self._game.get_player()
            if isinstance(player, HoldingPlayer):
                save_file.write(str(player.get_inventory().get_items()))
            save_file.write("\n")
            save_file.write(str(self._time) + "\n" + str(self._steps))

            save_file.close()

            db = "Saved game at:\n'savegames/"+save_name+"'."
            tk.messagebox.showinfo("Save game file", db)

            self.toggle_pause()

        def open_high_scores():
            self.toggle_pause()

            def close_hs():
                self.toggle_pause()
                hs.destroy()

            hs = tk.Toplevel()
            hs.title("High Scores")

            hs.protocol("WM_DELETE_WINDOW", close_hs)

            title = tk.Label(
                hs,
                text="High Scores",
                bg=DARK_PURPLE,
                fg="white",
                font=("Myriad Pro", 44)
            )
            title.pack(side="top")

            with open(HIGH_SCORES_FILE, "r") as hs_file:
                scores = hs_file.read()

            score_label = tk.Label(hs, text=scores)
            score_label.pack(side="top")

            done_btn = tk.Button(hs, text="Done", command=close_hs)
            done_btn.pack(side="bottom", pady=2.5)

            # Set dialog window geometry to centre of root window
            root.update_idletasks()
            x, y = self._root.winfo_rootx(), self._root.winfo_rooty()
            w, h = self._root.winfo_width(), self._root.winfo_height()
            hsw, hsh = hs.winfo_width(), hs.winfo_height()

            dx, dy = (w - hsw) // 2, (h - hsh) // 2
            hs.geometry("+%d+%d" % (x + dx, y + dy))

        def quit_game():
            self.toggle_pause()
            quit_dialog = tk.messagebox.askyesno(
                title="Quit dialog",
                message="Are you sure you want to quit?",
                parent=root
            )

            if quit_dialog:
                quit()
            else:
                self.toggle_pause()

        menu_bar = tk.Menu(root)
        file = tk.Menu(menu_bar, tearoff=0)

        # Menu bar items
        file.add_command(label="Load game", command=load_game)
        file.add_command(label="Save game", command=save_game)
        file.add_separator()
        file.add_command(label="High Scores", command=open_high_scores)
        file.add_separator()
        file.add_command(label="Restart", command=self.restart)
        file.add_command(label="Quit", command=quit_game)
        menu_bar.add_cascade(label="File", menu=file)

        root.config(menu=menu_bar)

        # Status Bar
        self._status_bar = StatusBar(self._bottom_frame, self.restart)
        self._status_bar.pack(side="bottom")

    def toggle_pause(self) -> None:
        """
        Toggles the pause state of the game.
        @return: None.
        """

        def local_step():
            self._step(self._game)

        self._paused = not self._paused

        if not self._paused:
            self._root.after(500, local_step)
            self._root.title("EndOfDayz")
        elif self._paused:
            self._root.title("EndOfDayz (paused)")

    def restart(self) -> None:
        """
        Restarts game.
        @return: None.
        """

        self._root.destroy()
        self._root.after_cancel(wait)
        start_game()

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

        if y < len(inventory_items) and len(inventory_items) > 0:
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

            # Game square background
            size = game.get_grid().get_size()

            for col in range(size):
                for row in range(size):
                    grid_pos = Position(col, row)
                    centre_pos = self._bmap.get_position_centre(grid_pos)
                    x, y = centre_pos.get_x(), centre_pos.get_y()

                    self._bg = Image.open(IMAGES.get(BACK_GROUND))
                    # noinspection PyTypeChecker
                    self._bgs[col][row] = ImageTk.PhotoImage(self._bg)
                    self._bmap.create_image((x, y), image=self._bgs[col][row])

            # Draw entities
            grid_mapping = game.get_grid().get_mapping()

            for position, entity in grid_mapping.items():
                self._bmap.draw_entity(position, entity.display())

            # Draw inventory
            player = game.get_player()
            if isinstance(player, HoldingPlayer):
                self._inv.draw(player.get_inventory())

            # Draw status bar
            self._status_bar.update_timer(self._time)
            self._status_bar.update_moves(self._steps)

            # Win/lose
            # Check for game win or game lose, else continue with loop.
            title = "Game Over!"
            if game.has_won():
                self._game_over = True

                # Get existing leaderboard names (to ensure no duplicates)
                with open(HIGH_SCORES_FILE, "r") as hs_file:
                    scores = hs_file.readlines()

                names = []

                for score in scores:
                    colon_index = []
                    for index, character in enumerate(score):
                        if character == ":":
                            colon_index.append(index)
                            name = score[0:colon_index[-1]]
                            names.append(name)

                # Dialog box for winning
                message = WIN_MESSAGE + " . Your time was " + str(self._time) \
                    + " seconds.\nPlease enter your name for the leaderboard:"

                def disable_event():
                    pass

                dia_win = tk.Toplevel()
                dia_win.title(title)
                dia_win.protocol("WM_DELETE_WINDOW", disable_event)

                # Message
                lbl = tk.Label(dia_win, text=message)
                lbl.pack(pady=2)

                # User entry
                def edit(txt_fld):
                    if txt_fld.get() in names:
                        btn_one.config(state="disabled")
                        btn_two.config(state="disabled")
                    elif txt_fld.get() not in names and txt_fld.get() != "":
                        btn_one.config(state="normal")
                        btn_two.config(state="normal")

                # String var is updated when user makes change to entry field
                s_var = tk.StringVar()
                s_var.trace("w", lambda txt, i, mode, sv=s_var: edit(s_var))
                name_entry = tk.Entry(dia_win, textvariable=s_var)
                name_entry.pack(pady=2)

                # Buttons
                def btn_one():
                    self._button_pressed = 1
                    self._name = name_entry.get()

                    dia_win.destroy()

                def btn_two():
                    self._button_pressed = 2
                    self._name = name_entry.get()

                    dia_win.destroy()

                btn1 = "Enter"
                btn2 = "Enter and play again"

                btn_frame = tk.Frame(dia_win)
                btn_frame.pack(side="bottom", pady=5)

                btn_one = tk.Button(
                    btn_frame,
                    state="disabled",
                    text=btn1,
                    command=btn_one
                )
                btn_one.pack(side="left", padx=10)

                btn_two = tk.Button(
                    btn_frame,
                    state="disabled",
                    text=btn2,
                    command=btn_two
                )
                btn_two.pack(side="right", padx=00)

                # Set dialog window geometry to centre of root window
                self._root.update_idletasks()
                x, y = self._root.winfo_rootx(), self._root.winfo_rooty()
                w, h = self._root.winfo_width(), self._root.winfo_height()
                dww, dwh = dia_win.winfo_width(), dia_win.winfo_height()
                dx, dy = (w - dww) // 2, (h - dwh) // 2

                dia_win.geometry("+%d+%d" % (x + dx, y + dy))

                name_entry.focus_force()
                self._root.wait_window(dia_win)

                # This is now after dialog has closed
                # Get scores and store in list
                score_list = []

                for score in scores:
                    colon_index = []
                    for index, character in enumerate(score):
                        if character == ":":
                            colon_index.append(index)
                            name = score[0:colon_index[-1]]
                            # x seconds
                            # 987654321
                            time = int(score[colon_index[-1] + 2:-9])
                            score_list.append((name, time))

                # Add new score to scores
                score_list.append((self._name, self._time))

                # Sort scores, take MAX_ALLOWED_HIGH_SCORES and overwrite file.
                sorted_scores = sorted(score_list, key=lambda tup: tup[1])

                while len(sorted_scores) > MAX_ALLOWED_HIGH_SCORES:
                    sorted_scores.pop()

                leaderboard_file = open(HIGH_SCORES_FILE, "w")

                for line in sorted_scores:
                    leaderboard_file.write(line[0] + ": " + str(line[1]) +
                                           " seconds\n")

                leaderboard_file.close()

                # Return user to final state or restart game from input.
                if self._button_pressed == 1:
                    self._root.title("EndOfDayz (paused)")
                elif self._button_pressed == 2:
                    self.restart()      # Restart game
            elif game.has_lost():
                self._game_over = True
                message = LOSE_MESSAGE + " Do you want to play again?"
                lose_dialog = tk.messagebox.askyesno(
                    title=title,
                    message=message,
                    parent=self._root
                )

                # If player wants to play again, call restart method.
                if lose_dialog:
                    self.restart()
                elif not lose_dialog:
                    self._root.title("EndOfDayz (paused)")

    def _handle_input(self, event: tk.Event, game: AdvancedGame) -> None:
        """
        Handles all keyboard inputs from the user.
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

        if keycode in moves.keys():  # Moving input
            direction = game.direction_to_offset(moves.get(keycode))
            if direction:
                self._move(game, direction)
        elif isinstance(player, HoldingPlayer) and keycode in fires.keys():
            if player.get_inventory().has_active(CROSSBOW):
                # Fire the weapon in the indicated direction.
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
        self._steps += 1
        self.draw(game)

    def _step(self, game: AdvancedGame) -> None:
        """
        The _step method is called every second. This method triggers the step
        method for the game and updates the view accordingly.
        @param game: The current game as an AdvancedGame object.
        @return: None.
        """

        global wait

        root = self._root

        def call_step():
            if not self._paused:
                self._step(game)

        # Delay of 1000ms before each step.
        wait = root.after(1000, call_step)

        game.step()         # Step game in model
        self._time += 1     # Increment game timer
        self.draw(game)     # Draw game

    def play(self, game: AdvancedGame) -> None:
        """
        Binds events and initialises gameplay. This method will need to be
        called on the instantiated BasicGraphicalInterface in main to commence
        gameplay.
        @param game:
        @return: None.
        """

        root = self._root

        self._game = game   # Update private game

        # Initial draw of game
        self.draw(game)

        # Create leaderboard file (if doesn't already exist)
        open(HIGH_SCORES_FILE, "a+")

        # Move and fire inputs
        def event_parameters(event: tk.Event):
            if not self._paused and not self._game_over:
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
            if not self._paused:
                self._step(game)

        root.after(0, call_step)
        root.mainloop()

# Misc functions


def start_game():
    """
    Starts the game. This standalone function is used for restarts. It will
    restart a loaded game if one has been loaded. Otherwise, it will restart
    the default game. This class has its own map loader instance which adds
    entities to a newly instantiated grid. That grid is then passed into a new
    game instance to then be displayed by the view — ImageGraphicalInterface.
    """

    # If the user has loaded a map.
    if current_file != "":
        # Read loaded map save file.
        with open(current_file, "r") as save_game:
            save_data = save_game.readlines()

        # Instantiate AdvancedMapLoader and Grid.
        aml = AdvancedMapLoader()
        grid = Grid(int(save_data[1]))

        # Convert grid data (as grid.serialize() from save_game())
        grid_data = literal_eval(save_data[0])

        # Add entities to grid
        for xy, token in grid_data.items():
            x, y = xy
            position = Position(x, y)
            entity = aml.create_entity(token)
            grid.add_entity(position, entity)

        # Instantiate game
        game = AdvancedGame(grid)

        # If HoldingPlayer, add items to inventory
        player = game.get_player()
        if isinstance(player, HoldingPlayer):
            inventory_data = save_data[2].strip('][').split(', ')
            for pickup in inventory_data:
                token = pickup[0]
                # Find brackets in pickup
                bracket_index = []
                for index, character in enumerate(pickup):
                    if character == "(":
                        bracket_index.append(index)
                    elif character == ")":
                        bracket_index.append(index)
                try:
                    pickup_instance = aml.create_entity(token)
                except ValueError:
                    break
                health = int(pickup[bracket_index[0] + 1: bracket_index[1]])

                if isinstance(pickup_instance, (Garlic, Crossbow)):
                    pickup_instance._lifetime = health
                    player.get_inventory().add_item(pickup_instance)

        set_time_steps = True
    else:
        game = advanced_game(MAP_FILE)
        set_time_steps = False

    # Instantiate new window, gui, and then begin play loop.
    root = tk.Tk()
    root.title("EndOfDayz")
    app = ImageGraphicalInterface(root, game.get_grid().get_size())
    if set_time_steps:
        app._time = int(save_data[3])
        app._steps = int(save_data[4])
    app.play(game)
