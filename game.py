import tkinter as tk
from logic import GameState


class LightsOutApp:
    BG_COLOR = "#000000"
    TEXT_COLOR = "#F8FAFC"
    ACCENT_COLOR = "#F59E0B"
    TILE_OFF = "#334155"
    TILE_HINT = "#38BDF8"

    def __init__(self, root):
        self.root = root
        self.root.title("Lights Out")
        self.root.configure(bg=self.BG_COLOR)
        self.root.geometry("500x580")
        self.root.resizable(False, False)

        self.selected_size = 5
        self.game = GameState(self.selected_size)
        self.hints_used = 0
        self.current_hint = None
        self.buttons = []
        self.size_buttons = {}
        self.victory_frame = None

        self.instruction_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=40, pady=40)
        self.game_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=30, pady=25)

        self.build_instruction_screen()
        self.build_game_screen()

        self.instruction_frame.pack(expand=True, fill="both")

    def make_button(self, parent, text, command, width=8):
        return tk.Button(
            parent,
            text=text,
            font=("Times New Roman", 11, "bold"),
            fg=self.BG_COLOR,
            bg=self.ACCENT_COLOR,
            activebackground=self.ACCENT_COLOR,
            activeforeground=self.BG_COLOR,
            relief="flat",
            cursor="hand2",
            width=width,
            pady=10,
            command=command
        )

    # Instruction screen
    def build_instruction_screen(self):
        tk.Label(
            self.instruction_frame,
            text="LIGHTS OUT",
            font=("Times New Roman", 28, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        ).pack(pady=(10, 5))

        tk.Label(
            self.instruction_frame,
            text="Team 3: Asad, Seyjon",
            font=("Times New Roman", 12, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        ).pack(pady=(0, 30))

        tk.Label(
            self.instruction_frame,
            text="HOW TO PLAY",
            font=("Times New Roman", 13, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        rules = (
            "Turn off all the lights.\n\n"
            "Clicking any tile toggles itself and its horizontal and\n"
            "vertical neighbors.\n\n"
            "Use hints if you are stuck."
        )
        tk.Label(
            self.instruction_frame,
            text=rules,
            font=("Times New Roman", 11),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
            justify="left",
            anchor="w"
        ).pack(fill="x")

        start_btn = self.make_button(self.instruction_frame, "START GAME", self.start_game, width=15)
        start_btn.pack(side="bottom", pady=15)

    def select_board_size(self, size):
        if size != self.selected_size:
            self.selected_size = size
            self.update_size_buttons()
            self.game = GameState(size)
            self.rebuild_board()
            self.setup_board(new_puzzle=True)

    def update_size_buttons(self):
        for size in self.size_buttons:
            if size == self.selected_size:
                button_color = self.ACCENT_COLOR
                text_color = self.BG_COLOR
            else:
                button_color = self.TILE_OFF
                text_color = self.TEXT_COLOR

            self.size_buttons[size].config(
                bg=button_color,
                fg=text_color,
                activebackground=button_color,
                activeforeground=text_color
            )

    def start_game(self):
        self.game = GameState(self.selected_size)
        self.instruction_frame.pack_forget()
        self.game_frame.pack(expand=True, fill="both")
        self.rebuild_board()
        self.setup_board(new_puzzle=True)

    # Game screen
    def build_game_screen(self):
        stats_frame = tk.Frame(self.game_frame, bg=self.BG_COLOR)
        stats_frame.pack(fill="x", pady=(0, 20))

        self.moves_label = tk.Label(
            stats_frame, text="Moves: 0", font=("Times New Roman", 13, "bold"),
            fg=self.TEXT_COLOR, bg=self.BG_COLOR
        )
        self.moves_label.pack(side="left")

        self.hints_label = tk.Label(
            stats_frame, text="Hints Used: 0", font=("Times New Roman", 13, "bold"),
            fg=self.TEXT_COLOR, bg=self.BG_COLOR
        )
        self.hints_label.pack(side="right")

        size_frame = tk.Frame(self.game_frame, bg=self.BG_COLOR)
        size_frame.pack(fill="x", pady=(0, 10))

        size_button_frame = tk.Frame(size_frame, bg=self.BG_COLOR)
        size_button_frame.pack(anchor="center")

        for size in (3, 5, 7):
            button = tk.Button(
                size_button_frame,
                text=str(size) + "x" + str(size),
                font=("Times New Roman", 10, "bold"),
                width=5,
                pady=4,
                relief="flat",
                cursor="hand2",
                command=lambda board_size=size: self.select_board_size(board_size)
            )
            button.pack(side="left", padx=4)
            self.size_buttons[size] = button

        self.update_size_buttons()

        self.board_frame = tk.Frame(self.game_frame, bg=self.BG_COLOR)
        self.board_frame.pack(pady=10)

        controls_frame = tk.Frame(self.game_frame, bg=self.BG_COLOR)
        controls_frame.pack(fill="x", pady=(25, 0))

        self.make_button(controls_frame, "Undo", self.undo_move).pack(side="left", expand=True)
        self.make_button(controls_frame, "Hint", self.use_hint).pack(side="left", expand=True)
        self.make_button(controls_frame, "Reset", lambda: self.setup_board(new_puzzle=False)).pack(side="left", expand=True)
        self.make_button(controls_frame, "New Game", lambda: self.setup_board(new_puzzle=True)).pack(side="left", expand=True)

    def rebuild_board(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.destroy()

        self.buttons = []

        if self.game.size == 3:
            button_width = 8
            button_height = 4
        elif self.game.size == 5:
            button_width = 6
            button_height = 3
        else:
            button_width = 4
            button_height = 2

        for row in range(self.game.size):
            row_buttons = []
            for col in range(self.game.size):
                button = tk.Button(
                    self.board_frame,
                    width=button_width,
                    height=button_height,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda selected_row=row, selected_col=col: self.on_tile_click(
                        selected_row, selected_col
                    )
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    # Gameplay and display updates
    def setup_board(self, new_puzzle):
        if self.victory_frame is not None:
            self.victory_frame.destroy()
            self.victory_frame = None

        if new_puzzle:
            self.game.generate_board()
        else:
            self.game.reset_puzzle()

        self.hints_used = 0
        self.current_hint = None
        self.set_board_enabled(True)
        self.update_display()

    def on_tile_click(self, row, col):
        self.game.press(row, col)
        self.current_hint = None
        self.update_display()

        if self.game.is_solved():
            self.set_board_enabled(False)
            self.show_victory_message()

    def undo_move(self):
        had_move = len(self.game.move_history) > 0
        self.game.undo()
        self.current_hint = None

        if had_move:
            if self.victory_frame is not None:
                self.victory_frame.destroy()
                self.victory_frame = None
            self.set_board_enabled(True)

        self.update_display()

    def use_hint(self):
        if not self.game.is_solved():
            suggested_move = self.game.hint()
            if suggested_move is not None:
                self.current_hint = suggested_move
                self.hints_used += 1
                self.update_display()

    def update_display(self):
        self.moves_label.config(text=f"Moves: {self.game.moves_made}")
        self.hints_label.config(text=f"Hints Used: {self.hints_used}")

        for r in range(self.game.size):
            for c in range(self.game.size):
                if self.current_hint == (r, c):
                    color = self.TILE_HINT
                elif self.game.grid[r][c]:
                    color = self.ACCENT_COLOR
                else:
                    color = self.TILE_OFF

                self.buttons[r][c].config(bg=color, activebackground=color)

    def set_board_enabled(self, enabled):
        if enabled:
            state = "normal"
        else:
            state = "disabled"

        for r in range(self.game.size):
            for c in range(self.game.size):
                self.buttons[r][c].config(state=state)

    # Victory overlay
    def show_victory_message(self):
        self.victory_frame = tk.Frame(
            self.board_frame,
            bg=self.BG_COLOR,
            highlightbackground=self.ACCENT_COLOR,
            highlightthickness=3,
            padx=28,
            pady=22
        )
        self.victory_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.victory_frame, text="BOARD SOLVED!",
            font=("Times New Roman", 18, "bold"), fg=self.ACCENT_COLOR, bg=self.BG_COLOR
        ).pack(pady=(0, 8))

        tk.Label(
            self.victory_frame,
            text=f"Total Moves: {self.game.moves_made}\nHints Used: {self.hints_used}",
            font=("Times New Roman", 12, "bold"), fg=self.TEXT_COLOR, bg=self.BG_COLOR
        ).pack(pady=(0, 16))

        self.make_button(
            self.victory_frame, "Play New Puzzle",
            lambda: self.setup_board(new_puzzle=True), width=15
        ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = LightsOutApp(root)
    root.mainloop()