class Player:
    """Class that represents a player in a mancala game"""
    def __init__(self, name):
        """
        Constructor for player class, initializes required data members.
        All data members are private.

        Args:
            name (str): name of a player
        """
        self._name = name
    
    def get_name(self):
        """
        Method that returns the name of a player. Takes no parameters.
        
        Returns:
            self._name (str): name of the player
        """
        return self._name

class Mancala:
    """Class that represents a mancala game"""
    def __init__(self):
        """
        Constructor for mancala class, initializes required data members.
        All data members are private. Takes no arguments.
        """
        self._player1 = None
        self._player2 = None
        self._board = {
            1 : 4, 2 : 4, 3 : 4, 4 : 4, 5 : 4, 6 : 4, 7 : 0,
            8 : 4, 9 : 4, 10 : 4, 11 : 4, 12 : 4, 13 : 4, 14 : 0
        }
    
    def create_player(self, player_name):
        """
        Method that creates a player and prints a warning if
        more than two players want to play a game.

        Args:
            player_name (str): name of the player

        Returns:
            Player(player_name) (obj): registers the player name
                in the Player class.
        """
        if self._player1 is None:
            self._player1 = player_name
        elif self._player1 is not None and self._player2 is None:
            self._player2 = player_name
        elif self._player1 is not None and self._player2 is not None:
             return print('Only two players can play this game at the same time')
        return Player(player_name)

    def check_for_opposite_pit(self, player, pit):
        """
        Method that checks the pit opposite to the one 
        the player ends in and transfers all the seeds
        in the opposite pit to the player's pit.

        Args:
            player (int): player that moved
            pit (int): pit the player ends in
        """
        opposite_dict = {
            1 : 13, 2 : 12, 3 : 11, 4 : 10, 5 : 9, 6 : 8,
            13 : 1, 12 : 2, 11 : 3, 10 : 4, 9 : 5, 8 : 6
        }
        
        opposite_pit = opposite_dict[pit]
        self._board[pit] += self._board[opposite_pit]
        self._board[opposite_pit] = 0

        if player == 1:
            self._board[7] += self._board[pit]
            self._board[pit] = 0

    def play_game(self, player, pit):
        """
        Method that represents a player turn. Allows the
        player to choose a pit.

        Args:
            player (int): number assignated to a player,
                either 1 or 2
            pit (int): pit number the player chooses to
                play

        Returns:
            list(self._board.values()) (list): shows the
                state of the board after the player's move.
        """
        if pit > 6 or pit <= 0:
            return print('Invalid number for pit index')

        if self.game_ended() == True:
            self.return_winner()
            return print('Game is ended')
        
        if player == 2:
            pit += 7

        seed_num = self._board[pit]
        self._board[pit] = 0

        self.move_seed(player, pit, seed_num)

        return list(self._board.values())
    
    def move_seed(self, player, start_pit, seeds):
        """
        Method that represents the seed movement on the board.

        Args:
            player (int): number assignated to a player,
                either 1 or 2
            start_pit (int): pit player chose initially.
            seeds (int): number of seeds to move.
        """
        next_pit_dict = {
            1 : 2, 2 : 3, 3 : 4, 4 : 5, 5 : 6, 6 : 7, 7 : 8,
            8 : 9, 9 : 10, 10 : 11, 11 : 12, 12 : 13, 13 : 14, 14 : 1
        }

        new_pit = next_pit_dict[start_pit]

        if player == 1 and new_pit == 14:
            new_pit = next_pit_dict[14]
        if player == 2 and new_pit == 7:
            new_pit = next_pit_dict[7]

        if seeds > 0:
            self._board[new_pit] += 1
            self.move_seed(player, new_pit, seeds - 1)
        
        if seeds == 0 and self._board[start_pit] == 1:
            if start_pit != 7 and start_pit != 14:
                if player == 1 and start_pit in self.p1_pits():
                    self.check_for_opposite_pit(player, start_pit)
                if player == 2 and start_pit in self.p2_pits():
                    self.check_for_opposite_pit(player, start_pit)
        
        if seeds == 0:
            if player == 1 and start_pit == 7:
                return print('player 1 take another turn')
        
            if player == 2 and start_pit == 14:
                return print('player 2 take another turn')
    
    def p1_pits(self):
        """
        Creates a list with the seeds in each pit for player 1.

        Returns:
            p1_pits (list): list showing the amount of seeds in
                each pit for player 1. The list shows pits 
                in ascending order.
        """
        p1_pits = [self._board[1], self._board[2], self._board[3], self._board[4], self._board[5], self._board[6]]
        return p1_pits
    
    def p2_pits(self):
        """
        Creates a list with the seeds in each pit for player 2.

        Returns:
            p2_pits (list): list showing the amount of seeds in
                each pit for player 2. The list shows pits 
                in ascending order.
        """
        p2_pits = [self._board[8], self._board[9], self._board[10], self._board[11], self._board[12], self._board[13]]
        return p2_pits

    def print_board(self):
        """
        Method that prints the state of the board in the
        following format:

        player1:
        store: number of seeds in player 1's store
        player 1 seeds number from pit 1 to 6 in a list
        player2:
        store: number of seeds in player 2's store
        player 2 seeds number from pit 1 to 6 in a list 

        Takes no parameters.
        """
        p1_store_seeds = self._board[7]
        p2_store_seeds = self._board[14]

        print(
            f'player1:\nstore: {p1_store_seeds}\n{self.p1_pits()}\nplayer2:\nstore: {p2_store_seeds}\n{self.p2_pits()}'
        )

    def game_ended(self):
        """
        Method that checks if the game has ended by counting
        seed number in each player's side of the board.
        Takes no parameters.

        Returns:
            True (bool): game has ended.
        """
        if sum(self.p1_pits()) == 0:
            return True
        
        elif sum(self.p2_pits()) == 0:
            return True

    def return_winner(self):
        """
        Method that, if the game has ended, finishes the game
        by moving all remaining pits to their side's store and
        calculates who the winner is by comparing seed number 
        in both player's stores. If the game has not ended prints
        a warning.

        Returns:
            print(f'Winner is player 1: {self._player1}') (str):
                player 1 wins.
            print("It's a tie") (str): game ends in a tie.
            print(f'Winner is player 2: {self._player2}') (str):
                player 2 wins.
            print('Game has not ended') (str): end condition not met.
        """
        if self.game_ended() == True:
            if sum(self.p1_pits()) != 0 or sum(self.p2_pits()) != 0: 
                if sum(self.p1_pits()) == 0:
                    self._board[14] += sum(self.p2_pits())
                    for numbers in range(8,14):
                        self._board[numbers] = 0
                
                elif sum(self.p2_pits()) == 0:
                    self._board[7] += sum(self.p1_pits())
                    for numbers in range(1,7):
                        self._board[numbers] = 0

            result = self._board[7]/self._board[14]

            if result > 1:
                return print(f'Winner is player 1: {self._player1}')
            
            if result == 1:
                return print("It's a tie")
            
            if result < 1:
                return print(f'Winner is player 2: {self._player2}')
        
        if self.game_ended() != True:
            return print('Game has not ended')
            



game = Mancala()
player1 = game.create_player('Lily')
player2 = game.create_player("Lucy")
game.play_game(1, 1)
game.play_game(1, 2)
game.play_game(1, 3)
game.play_game(1, 4)
game.play_game(1, 5)
game.play_game(1, 6)
# game.play_game(1, 5)
# game.print_board()
game.return_winner()
game.print_board()
game.return_winner()
game.print_board()
