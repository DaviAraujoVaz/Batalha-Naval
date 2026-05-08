import random

class GameLogic:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(10)]
        self.hits_received = 0  # Total ship parts hit by opponent. If 10, I lose.
        self.total_ship_parts = 10
        self.place_ships()

    def reset(self):
        self.board = [[0 for _ in range(10)] for _ in range(10)]
        self.hits_received = 0
        self.place_ships()

    def place_ships(self):
        # 3 submarines (1x1)
        # 2 cruisers (1x2 or 2x1)
        # 1 aircraft carrier (1x3 or 3x1)
        ships_to_place = [
            ("Carrier", 3),
            ("Cruiser", 2),
            ("Cruiser", 2),
            ("Submarine", 1),
            ("Submarine", 1),
            ("Submarine", 1)
        ]

        for name, size in ships_to_place:
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                row = random.randint(0, 9)
                col = random.randint(0, 9)

                if self._can_place_ship(row, col, size, horizontal):
                    self._place_ship(row, col, size, horizontal)
                    placed = True

    def _can_place_ship(self, row, col, size, horizontal):
        if horizontal:
            if col + size > 10:
                return False
            for c in range(col, col + size):
                if not self._is_cell_and_neighbors_free(row, c):
                    return False
        else:
            if row + size > 10:
                return False
            for r in range(row, row + size):
                if not self._is_cell_and_neighbors_free(r, col):
                    return False
        return True

    def _is_cell_and_neighbors_free(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < 10 and 0 <= c < 10:
                    if self.board[r][c] != 0:
                        return False
        return True

    def _place_ship(self, row, col, size, horizontal):
        if horizontal:
            for c in range(col, col + size):
                self.board[row][c] = 1 # 1 represents ship
        else:
            for r in range(row, row + size):
                self.board[r][col] = 1

    def receive_shot(self, row, col):
        """Returns True if hit, False if miss"""
        if self.board[row][col] == 1:
            self.board[row][col] = -1 # -1 represents a hit ship
            self.hits_received += 1
            return True
        else:
            self.board[row][col] = -2 # -2 represents a missed shot in water
            return False

    def get_board_string(self):
        s = ""
        for row in self.board:
            for cell in row:
                s += "1" if abs(cell) == 1 else "0"
        return s

    def is_game_over(self):
        return self.hits_received >= self.total_ship_parts
