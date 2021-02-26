import hangman


class GameManager:
    def __init__(self):
        self.games = {}
        self.next_game_id = 1

    def create_game(self):
        game = hangman.create_hangman_game()
        game_id = self.next_game_id
        self.games[game_id] = game
        self.next_game_id += 1

        return game_id, game

    def get_game(self, game_id):
        return self.games.get(game_id, None)

