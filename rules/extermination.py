# coding: utf-8
from game import Rules
from things import Zombie


class ExterminationRules(Rules):
    '''A kind of game where players must exterminate all zombies.

       Team wins when all zombies are dead.
    '''
    def zombies_alive(self):
        zombies = [thing for thing in self.game.world.things.values()
                    if isinstance(thing, Zombie) and thing.life > 0]
        return bool(zombies)

    def game_ended(self):
        if self.players_alive():
            return not self.zombies_alive()
        else:
            return True

    def game_woRules(self):
        if self.players_alive():
            return True, 'zombies exterminated! :)'
        else:
            return False, 'players exterminated! :('


def create(game):
    return ExterminationRules(game)