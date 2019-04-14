from collections import namedtuple
import nashpy as nash
import numpy as np


# action types
ATTACK = 1
DEFEND = 2
GRAPPLE = 3

# risk types
EARTH = 0
WATER = 1
FIRE = 2
HEAVEN = 3

Stance = namedtuple('Stance', ['type', 'amount'])

Action = namedtuple('Action', ['name','vs_attack', 'vs_defend', 'vs_grapple', 'type', 'amount'])

Disadvantage = namedtuple('Disadvantage', ['type', 'amount'])

attacks = [
    Action("basic attack", FIRE, WATER, HEAVEN, ATTACK, 3)
]

defenses = [
    Action("basic defend", HEAVEN, FIRE, WATER, DEFEND, 2)
]

grapples = [
    Action("basic grapple", WATER, HEAVEN, FIRE, GRAPPLE, 4)
]

all_actions = [*attacks, *defenses, *grapples]

def better_type(p1, p2):
    return True if (p1.type == ATTACK and p2.type == GRAPPLE) else False if (p1.type == GRAPPLE and p2.type == ATTACK) else p1.type > p2.type
    
def better_risk(p1, p2):
    return True if (p1 == EARTH and p2 == HEAVEN) else False if (p1 == HEAVEN and p2 == EARTH) else p1 > p2
    
def same_type(a, b):
    return a is not None and b is not None and a.type == b.type

def bonus(stance_or_disadvantage, action):
    return stance_or_disadvantage.amount if same_type(stance_or_disadvantage, action) else 0

def payoff(p1_action, p2_action, p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None):
    """net damage done by player 1 to player 2"""
    assert p1_disadvantage is None or p2_disadvantage is None
    p1_risk = p1_action[p2_action.type]
    p2_risk = p2_action[p1_action.type]
    p1_win_damage = p1_action.amount + bonus(p1_stance, p1_action) + bonus(p2_stance, p2_action) + bonus(p2_disadvantage, p2_action)
    p2_win_damage = p2_action.amount + bonus(p2_stance, p2_action) + bonus(p1_stance, p1_action) + bonus(p1_disadvantage, p1_action)
    
    if better_risk(p1_risk, p2_risk):
        return p1_win_damage
    elif better_risk(p2_risk, p1_risk):
        return -1 * p2_win_damage
    elif better_type(p1_action, p2_action):
        return p1_win_damage
    elif better_type(p2_action, p1_action):
        return -1 * p2_win_damage
    elif same_type(p2_disadvantage, p2_action):
        return p1_win_damage
    elif same_type(p1_disadvantage, p1_action):
        return -1 * p2_win_damage
    else:
        return p1_win_damage - p2_win_damage

def payoff_matrix(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None):
    return [[payoff(p1_action = p1_action, p2_action = p2_action,
                    p1_stance = p1_stance, p2_stance = p2_stance,
                    p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage)
             for p2_action in all_actions] for p1_action in all_actions]

def print_payoff_matrix(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None):
    print([a.name for a in all_actions])
    for i in payoff_matrix(p1_stance = p1_stance, p2_stance = p2_stance,
                           p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage):
        print(i)
        
def equilibrium_value(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None):
    matrix = payoff_matrix(p1_stance = p1_stance, p2_stance = p2_stance,
                           p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage)
    game = nash.Game(np.array(matrix))
    eqls = list(game.support_enumeration())
    (p1val, p2val) = game[eqls[0][0], eqls[0][1]]
    return (eqls, [round(p1val, 2), round(p2val, 2)])
