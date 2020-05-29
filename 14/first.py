#!/usr/bin/env python

from textwrap import dedent
from collections import defaultdict

class Quantity:
    def __init__(self, amount, chemical):
        self.amount = amount
        self.chemical = chemical
    
    @classmethod
    def parse(cls, str):
        amount, chemical = str.split(' ')
        amount = int(amount)
        return Quantity(amount, chemical)
    
    def __repr__(self):
        return f'{self.amount} {self.chemical}'
    

class Reaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
    
    def __repr__(self):
        return f'{", ".join(map(str, self.inputs))} => {", ".join(map(str, self.outputs))}'

class Reactions:
    def __init__(self, reactions):
        self.reactions = reactions
    
    @classmethod
    def parse(cls, lines):
        """
        >>> inp = r'''
        ... 9 ORE => 2 A
        ... 8 ORE => 3 B
        ... 7 ORE => 5 C
        ... 3 A, 4 B => 1 AB
        ... 5 B, 7 C => 1 BC
        ... 4 C, 1 A => 1 CA
        ... 2 AB, 3 BC, 4 CA => 1 FUEL
        ... '''
        >>> r = Reactions.parse(dedent(inp).strip().split('\\n'))
        >>> r
        9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL
        >>> r.dot(open('/tmp/asdf.dot', 'w'))
        """
        reactions = []
        for l in lines:
            reactants, output = l.strip().split(' => ')
            output = Quantity.parse(output)
            reactants = [Quantity.parse(q) for q in reactants.split(', ')]
            reactions.append(Reaction(reactants, [output]))

        return Reactions(reactions)
        
    def dot(self, out):
        with(out):
            out.write('digraph g {\n')
            
            for reaction in self.reactions:
                output = reaction.outputs[0]
                for input in reaction.inputs:
                    out.write(f'\t{input.chemical} -> {output.chemical} [headlabel={output.amount}, taillabel={input.amount}]\n')
            out.write('}\n')
    
    def __repr__(self):
        return '\n'.join(map(str, self.reactions))

def all_paths(graph, start, target):
    paths = []
    Q = [[start]]
    # discovered = set(start)
    while len(Q) > 0:
        path = Q.pop(0)
        if path[-1] == target:
            paths.append(path)
        
        for w in graph[path[-1]]:
            newpath = path[:] + [w]
            Q.append(newpath)
    
    return paths  
    

def solve(reactions):
    """
    >>> inp = r'''
    ... 9 ORE => 2 A
    ... 8 ORE => 3 B
    ... 7 ORE => 5 C
    ... 3 A, 4 B => 1 AB
    ... 5 B, 7 C => 1 BC
    ... 4 C, 1 A => 1 CA
    ... 2 AB, 3 BC, 4 CA => 1 FUEL
    ... '''
    >>> r = Reactions.parse(dedent(inp).strip().split('\\n'))
    >>> solve(r)
    165
    """
    
    
    # backwards = {'FUEL': ['AB', 'BC', 'CA'], 'AB': ['B', 'A'], 'BC': ['B', 'C'], 'CA': ['C', 'A'], 'B': ['ORE'], 'A': ['ORE'], 'C': ['ORE']}
    # forwards = [('ORE', 'A'): (9, 2), ('ORE', 'B'): (8, 3), ('ORE', 'C'): (7, 5), ()]
    
    paths = []
    
    
    
    
    
    
    # forwards = {'ORE': (1, [])}
    # quantities = {'FUEL': 1}
    # while True:
    #     after = {}
    #     for chemical, amount in quantities.items():
            


    pass
    

if __name__ == "__main__":
    backwards = defaultdict(lambda: [])
    backwards['FUEL'].append('AB')
    backwards['FUEL'].append('BC')
    backwards['FUEL'].append('CA')
    backwards['AB'].append('A')
    backwards['AB'].append('B')
    backwards['BC'].append('B')
    backwards['BC'].append('C')
    backwards['CA'].append('C')
    backwards['CA'].append('A')
    backwards['A'].append('ORE')
    backwards['B'].append('ORE')
    backwards['C'].append('ORE')
    
    paths = all_paths(backwards, 'FUEL', 'ORE')
    for p in paths:
        print(p)
    
    
    
    
    # import sys
    # r = Reactions.parse(sys.stdin.readlines())
    # r.dot(open('/tmp/asdf.dot', 'w'))
    # solve(r)