#coding: utf-8
import random
from zombsole.core import Thing, FightingThing, ComplexThingBuilder, Weapon
from zombsole.utils import closest, distance, possible_moves


class Box(Thing):
    '''Solid box.'''
    MAX_LIFE = 10

    def __init__(self, position):
        super(Box, self).__init__(u'box', u'\u25A4', 'yellow',
                                  Box.MAX_LIFE,
                                  position)


class DeadBody(Thing):
    '''Dead body.'''
    MAX_LIFE = 50

    def __init__(self, name, color, position):
        super(DeadBody, self).__init__(name, u'\u2620', color,
                                       DeadBody.MAX_LIFE,
                                       position)


class Wall(Thing):
    '''Solid section of wall.'''
    MAX_LIFE = 200

    def __init__(self, position):
        super(Wall, self).__init__(u'wall', u'\u2593', 'white',
                                   Wall.MAX_LIFE,
                                   position)


class Building(ComplexThingBuilder):
    '''Building builder.'''
    def __init__(self, position, size, doors=2):
        self.position = position
        self.size = size
        self.doors = doors

    def create_parts(self):
        '''Create parts for a building of the given size.'''
        start_x, start_y = self.position
        end_x = start_x + self.size[0]
        end_y = start_y + self.size[1]

        # building walls
        top = [Wall((x, start_y)) for x in range(start_x, end_x + 1)]
        bottom = [Wall((x, end_y)) for x in range(start_x, end_x + 1)]
        left = [Wall((start_x, y)) for y in range(start_y + 1, end_y)]
        right = [Wall((end_x, y)) for y in range(start_y + 1, end_y)]

        walls = top + bottom + left + right

        # create doors by removing random wall segments
        random.shuffle(walls)
        walls = walls[self.doors:]

        return walls


def _new_weapon_class(name, max_range, damage_range):
    '''Create new weapon class.'''
    class NewWeapon(Weapon):
        def __init__(self):
            super(NewWeapon, self).__init__(name,
                                            max_range,
                                            damage_range)

    NewWeapon.__name__ = name
    return NewWeapon


ZombieClaws = _new_weapon_class('ZombieClaws', 1.5, (5, 10))
Gun = _new_weapon_class('Gun', 10, (10, 50))
Shotgun = _new_weapon_class('Shotgun', 6, (75, 100))
Rifle = _new_weapon_class('Rifle', 15, (25, 50))
Knife = _new_weapon_class('Knife', 1.5, (5, 10))
Axe = _new_weapon_class('Axe', 2, (75, 100))


class Zombie(FightingThing):
    MAX_LIFE = 100

    def __init__(self, position, life=None):
        if life is None:
            life = random.randint(Zombie.MAX_LIFE / 2, Zombie.MAX_LIFE)

        remains = DeadBody('zombie remains', 'green', None)

        super(Zombie, self).__init__(u'zombie', u'\u2A30', 'green',
                                     life,
                                     position,
                                     ZombieClaws(),
                                     remains)

    def next_step(self, things):
        action = None

        humans = [thing for thing in things.values()
                  if isinstance(thing, Human)]
        positions = possible_moves(self.position, things)

        if humans:
            target = closest(self, humans)

            if distance(self.position, target.position) < self.weapon.max_range:
                action = 'attack', target
            else:
                if positions:
                    best_position = sorted(positions, key=lambda position: distance(target.position, position))[0]
                    action = 'move', best_position
        else:
            if positions:
                action = 'move', random.choice(positions)

        return action


class Human(FightingThing):
    MAX_LIFE = 100

    def __init__(self, name, color, position, weapon=None):
        if weapon is None:
            weapon = random.choice([Gun, Shotgun, Rifle, Knife, Axe])()

        remains = DeadBody('dead ' + name, color, None)

        super(Human, self).__init__(name, u'\u2A30', color,
                                    Human.MAX_LIFE,
                                    position,
                                    weapon,
                                    remains)
