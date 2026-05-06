"""A tic-tac-toe game built with Python and Tkinter."""

import tkinter as tk
from itertools import cycle
from tkinter import font, messagebox
from typing import NamedTuple
import os

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="#1976D2"),
    Player(label="O", color="#388E3C"),
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self._create_menu()
        self._create_header()
        self._create_scoreboard()
        self._create_board_display()
        self._create_control_buttons()
        self._create_board_grid()
        self._setup_icon()

    def _setup_icon(self):
        # Set window icon using .ico in the same folder
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        try:
            self.iconbitmap(icon_path)
        except Exception:
            # Fallback to generic photo icon if icon not found
            try:
                icon = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "icon.png"))
                self.iconphoto(True, icon)
            except Exception:
                pass

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _exit(self):
        self.destroy()

    def _create_header(self):
        header_frame = tk.Frame(master=self)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.title_label = tk.Label(
            master=header_frame,
            text="Tic-Tac-Toe",
            font=font.Font(size=24, weight="bold"),
        )
        self.title_label.pack()

    def _create_scoreboard(self):
        sb = tk.Frame(master=self)
        sb.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(sb, text="Scoreboard", font=font.Font(size=14, weight="bold")).grid(row=0, column=0, columnspan=3)
        tk.Label(sb, text=f'X: {self.scores["X"]}', font=font.Font(size=12)).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        tk.Label(sb, text=f'O: {self.scores["O"]}', font=font.Font(size=12)).grid(row=1, column=1, padx=5, pady=2, sticky="w")
        tk.Label(sb, text=f'Ties: {self.scores["Ties"]}', font=font.Font(size=12)).grid(row=1, column=2, padx=5, pady=2, sticky="w")

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X, padx=10, pady=5)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=20, weight="bold"),
        )
        self.display.pack()

    def _create_control_buttons(self):
        btn_frame = tk.Frame(master=self)
        btn_frame.pack(pady=8)
        self.reset_game_btn = tk.Button(
            btn_frame,
            text="Reset Game",
            font=font.Font(size=12),
            command=self.reset_board,
            width=12,
        )
        self.reset_game_btn.grid(row=0, column=0, padx=5)
        self.reset_scores_btn = tk.Button(
            btn_frame,
            text="Reset Scores",
            font=font.Font(size=12),
            command=self.reset_scores,
            width=12,
        )
        self.reset_scores_btn.grid(row=0, column=1, padx=5)

    def reset_scores(self):
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self._update_scoreboard()

    def _update_scoreboard(self):
        # Rebuild scoreboard labels dynamically
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.cget("text").startswith(("X:", "O:", "Ties:")):
                        child.destroy()
        # Find scoreboard frame by title label "Scoreboard"
        scoreboard_frame = None
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.cget("text") == "Scoreboard":
                        scoreboard_frame = widget
                        break
        if not scoreboard_frame:
            return
        tk.Label(scoreboard_frame, text=f'X: {self.scores["X"]}', font=font.Font(size=12)).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        tk.Label(scoreboard_frame, text=f'O: {self.scores["O"]}', font=font.Font(size=12)).grid(row=1, column=1, padx=5, pady=2, sticky="w")
        tk.Label(scoreboard_frame, text=f'Ties: {self.scores["Ties"]}', font=font.Font(size=12)).grid(row=1, column=2, padx=5, pady=2, sticky="w")

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack(padx=10, pady=10)
        for row in range(self._game.board_size):
            self.rowconfigure(row + 3, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="#D32F2F")
                self.scores["Ties"] += 1
                self._update_scoreboard()
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
                self.scores[self._game.current_player.label] += 1
                self._update_scoreboard()
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="#E53935")

    def reset_board(self):
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()