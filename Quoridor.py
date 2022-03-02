# Author: Xiao Yu Chen
# Date: 8/12/12
# Description: Set up and play a 2-player board game called Quoridor.

class QuoridorGame:
    """
    Represents one match of Quoridor. This class is responsible for setting up the game board and running through
    player actions from setup through the end of the game. The game starts with both players pawns facing each other at
    their respective baselines and ends when one player's pawn reaches the opponent's baseline. QuoridorGame interacts
    with the Fence class to block pawn movements.
    """

    def __init__(self):
        """
        Initializes a 9 x 9 game board with two pawns placed on the 5th column of the baseline. The edges of the game
        board are initialized as fences. Each player is assigned 10 fences to be used. The game starts on player 1's
        turn and ends when a winner is set.
        """
        # Sets up 100 coordinates, 81 of which are used for the game and the remaining are used for edge fences.
        self._board = [[[None for x in range(3)] for y in range(10)] for z in range(10)]

        # Sets up the pawns at the baselines.
        self._board[0][4][0] = 1
        self._board[8][4][0] = 2

        # Each player starts with 10 fences in reserve.
        self._p1_fence_count = 10
        self._p2_fence_count = 10

        # The game starts with player 1.
        self._current_player = 1
        self._winner = None

        # Sets up the fences along the edges of the board.
        for column in range(10):
            for row in range(10):
                if column == 0 or column == 9:
                    self.place_fence(None, "v", (column, row))
                if row == 0 or row == 9:
                    self.place_fence(None, "h", (column, row))

    def move_pawn(self, player, coord):
        """
        Attempts to move the current player's (first parameter) pawn to the passed coordinate (second parameter).
        Returns True if the move is successful or makes the player win. Returns False if the move illegal or blocked
        by a fence or if the game is already won.
        """
        # Invalid conditions including out-of-bound coordinates, out-of-turn moves, or game over.
        if coord[1] < 0 or coord[1] > 8 or coord[0] < 0 or coord[1] > 8 or \
                self._winner is not None or player != self._current_player:
            return False
        # Cases where the player has a valid move to an adjacent coordinate.
        elif self._board[coord[1] - 1][coord[0]][0] == player and self._board[coord[1]][coord[0]][1] is None:
            return self.move_pawn_success(player, (coord[0], coord[1] - 1), coord)
        elif self._board[coord[1] + 1][coord[0]][0] == player and self._board[coord[1] + 1][coord[0]][1] is None:
            return self.move_pawn_success(player, (coord[0], coord[1] + 1), coord)
        elif self._board[coord[1]][coord[0] - 1][0] == player and self._board[coord[1]][coord[0]][2] is None:
            return self.move_pawn_success(player, (coord[0] - 1, coord[1]), coord)
        elif self._board[coord[1]][coord[0] + 1][0] == player and self._board[coord[1]][coord[0] + 1][2] is None:
            return self.move_pawn_success(player, (coord[0] + 1, coord[1]), coord)
        # Edge cases such as the player's pawn already being in the given coordinate.
        else:
            return False

    def move_pawn_success(self, player, prev, current):
        """
        Helper function only called when pawn movement is valid. Checks if the move would cause the player to win.
        Changes the current player turn. Returns True.
        """
        # Moves the current player's pawn into the given coordinate.
        self._board[current[1]][current[0]][0] = player
        # Removes the player's pawn from the previous coordinate.
        self._board[prev[1]][prev[0]][0] = None
        if player == 1:
            # Checks if player 1 reached player 2's baseline.
            if current[0] == 8:
                self._winner = 1
            self._current_player = 2
        elif player == 2:
            # Checks if player 2 reached player 1's baseline.
            if current[0] == 0:
                self._winner = 0
            self._current_player = 1
        return True

    def place_fence(self, player, orient, coord):
        """
        Attempts to place a fence belonging to the current player (first parameter) in a given orientation
        (second parameter) to the given position (third parameter). Returns True if the fence can be placed. Returns
        False if the player if the given position is illegal (out of bounds or if it would overlap with an existing
        fence) or if the player has no remaining fences, or if it breaks the fair play rule or the game is already won.
        """
        # Invalid conditions including out-of-bound coordinates, out-of-turn placements, or game over.
        if coord[1] < 0 or coord[1] > 8 or coord[0] < 0 or coord[1] > 8 or \
                self._winner is not None or (player is not None and player != self._current_player):
            return False
        # Condition where the current player is out of fences to place.
        elif (player == 1 and self._p1_fence_count == 0) or (player == 2 and self._p2_fence_count == 0):
            return False
        # Valid horizontal fence placement by the current player.
        elif orient == "h" and self._board[coord[1]][coord[0]][1] is None:
            self._board[coord[1]][coord[0]][1] = Fence(orient)
            return self.fence_placed_success(player)
        # Valid vertical fence placement by the current player.
        elif orient == "v" and self._board[coord[1]][coord[0]][2] is None:
            self._board[coord[1]][coord[0]][2] = Fence(orient)
            return self.fence_placed_success(player)
        else:
            return False

    def fence_placed_success(self, player):
        """
        Helper function only called when fence placement is valid. Changes player turn. Returns True when fences are
        placed outside of the setup.
        """
        if player == 1:
            self._p1_fence_count -= 1
            self._current_player = 2
        elif player == 2:
            self._p2_fence_count -= 1
            self._current_player = 1
        if player is not None:
            return True

    def is_winner(self, player):
        """Returns True if the passed player has won. Return False if not."""
        if self._winner == player:
            return True
        return False

    def print_board(self):
        """Prints the current state of the game board."""
        for sublist in self._board:
            for element in sublist:
                if element[1] is not None and element is not sublist[9]:
                    print("  _", end=" ")
                elif element[1] is None and element is not sublist[9]:
                    print("   ", end=" ")
            print()
            for element in sublist:
                if element[2] is None and sublist is not self._board[9]:
                    print(" ", end="")
                elif element[2] is not None and sublist is not self._board[9]:
                    print("|", end="")

                if element[0] is None and element is not sublist[9] and sublist is not self._board[9]:
                    print("[ ]", end="")
                elif element[0] is not None and element is not sublist[9] and sublist is not self._board[9]:
                    print("[" + str(element[0]) + "]", end="")

            print()


class Fence:
    """
    Represents a fence of one player. A fence object has an orientation with a getter.
    Fences are used by each player (up to 10) in QuoridorGame as blocking pieces for pawns.
    """

    def __init__(self, orientation):
        """Initializes the fence's orientation."""
        self._orientation = orientation

    def get_orientation(self):
        """Returns the fence's orientation."""
        return self._orientation
