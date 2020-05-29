#!/usr/bin/env python

from enum import Enum
from textwrap import dedent
from collections import defaultdict

class Tile(Enum):
    WALL = '#'
    PASSAGE = '.'
    KEY = '🔑'
    DOOR = '🚪'
 
def neighbors(loc):
    yield (loc[0], loc[1] - 1)
    yield (loc[0], loc[1] + 1)
    yield (loc[0] + 1, loc[1])
    yield (loc[0] - 1, loc[1])

   
class Security:
    def __init__(self, letter=None, key_loc=None, door_loc=None):
        self.letter = letter
        self.key_loc = key_loc
        self.door_loc = door_loc

class Map:
    def __init__(self, position, tiles, security, size):
        self.position = position
        self.tiles = tiles
        self.security = security
        self.size = size
    
    def __repr__(self):
        out = ''
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if (x,y) == self.position:
                    out += '@'
                elif self.tiles[(x,y)] in (Tile.WALL, Tile.PASSAGE):
                    out += self.tiles[(x,y)].value
                elif self.tiles[(x,y)] is Tile.KEY:
                    out += self.security[(x,y)].letter.lower()
                elif self.tiles[(x,y)] is Tile.DOOR:
                    out += self.security[(x,y)].letter.upper()
            out += '\n'
        return out[:-1]
                    
    def build_graph(self):
        edges = defaultdict(lambda: [])
        Q = [self.position]
        seen = set(self.position)
        while len(Q) > 0:
            loc = Q.pop(0)
            
            for n in neighbors(loc):
                if self.tiles(n) is Tile.WALL:
                    continue
                
    
    @classmethod
    def read_input(cls, lines):
        """
        >>> inp = r'''
        ... #########
        ... #b.A.@.a#
        ... #########
        ... '''
        >>> Map.read_input(dedent(inp).strip().split('\\n'))
        #########
        #b.A.@.a#
        #########
        """
        position = None
        tiles = {}
        security = defaultdict(lambda: Security())
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == Tile.WALL.value:
                    tiles[(x,y)] = Tile.WALL
                elif char == Tile.PASSAGE.value:
                    tiles[(x,y)] = Tile.PASSAGE
                elif char == '@':
                    position = (x,y)
                    tiles[(x,y)] = Tile.PASSAGE
                elif char.islower():
                    tiles[(x,y)] = Tile.KEY
                    security[(x,y)].letter = char.lower()
                    security[(x,y)].key_loc = (x,y)
                elif char.isupper():
                    tiles[(x,y)] = Tile.DOOR
                    security[(x,y)].letter = char.lower()
                    security[(x,y)].door_loc = (x,y)
                else:
                    raise Exception(f'Unknown character: {char}')
        return Map(position, tiles, security, (x+1, y+1))

if __name__ == "__main__":
    import sys
    lines = sys.stdin.readlines()
    program = Map.read_input(l.strip() for l in lines)
    print(program)