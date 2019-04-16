from collections import namedtuple
import nashpy as nash
import numpy as np


# action types
ATTACK = 1
DEFEND = 2
GRAPPLE = 3
all_action_types = [('Attack', ATTACK), ('Defend', DEFEND), ('Grapple', GRAPPLE)]

# elements
VOID = 0
EARTH = 1
WATER = 2
FIRE = 3
HEAVEN = 4

Stance = namedtuple('Stance', ['type', 'amount'])

Action = namedtuple('Action', ['type','element', 'amount'])

Disadvantage = namedtuple('Disadvantage', ['type', 'amount'])

attacks = [
    Action(ATTACK, EARTH, 3),
    Action(ATTACK, WATER, 3),
    Action(ATTACK, FIRE, 3),
#    Action(ATTACK, HEAVEN, 3),
]

defenses = [
    Action(DEFEND, EARTH, 2),
    Action(DEFEND, WATER, 2),
    Action(DEFEND, FIRE, 2),
]

grapples = [
    Action(GRAPPLE, EARTH, 4),
    Action(GRAPPLE, WATER, 4),
    Action(GRAPPLE, FIRE, 4),
#    Action(GRAPPLE, HEAVEN, 4),
]

all_actions = [*attacks, *defenses, *grapples]

test_p1_disadvantage = None #Disadvantage(GRAPPLE, 1)
test_actions = all_actions #[attacks[0], defenses[0], grapples[0]]

def better_type(p1, p2):
    return True if (p1.type == ATTACK and p2.type == GRAPPLE) else False if (p1.type == GRAPPLE and p2.type == ATTACK) else p1.type > p2.type
    
def better_element(p1, p2):
    return True if (p1.element == EARTH and p2.element == FIRE) else False if (p1.element == FIRE and p2.element == EARTH) else p1.element > p2.element
#    return True if (p1.element == EARTH and p2.element == HEAVEN) else False if (p1.element == HEAVEN and p2.element == EARTH) else p1.element > p2.element
    
def same_type(a, b):
    return a is not None and b is not None and a.type == b.type

def bonus(stance_or_disadvantage, action):
    return stance_or_disadvantage.amount if same_type(stance_or_disadvantage, action) else 0

def payoff(p1_action, p2_action, p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None):
    """net damage done by player 1 to player 2"""
    assert p1_disadvantage is None or p2_disadvantage is None

    # if you play action matching your stance and lose, you lose your stance energy
    p1_stance_loss = bonus(p1_stance, p1_action)
    p2_stance_loss = bonus(p2_stance, p2_action)
    # if you play stance and win, add your stance energy plus up to your base action damage
    p1_stance_gain = p1_stance_loss + min(p1_action.amount, p1_stance_loss)
    p2_stance_gain = p2_stance_loss + min(p2_action.amount, p2_stance_loss)
    
    p1_win_amt = p1_action.amount + p1_stance_gain + p2_stance_loss + bonus(p2_disadvantage, p2_action)
    p2_win_amt = p2_action.amount + p2_stance_gain + p1_stance_loss + bonus(p1_disadvantage, p1_action)

    if better_type(p1_action, p2_action):
        return p1_win_amt
    elif better_type(p2_action, p1_action):
        return -1 * p2_win_amt
    elif better_element(p1_action, p2_action):
        return p1_win_amt
    elif better_element(p2_action, p1_action):
        return -1 * p2_win_amt
    # disadvantage loses ties
    elif same_type(p2_disadvantage, p2_action):
        return p1_win_amt
    elif same_type(p1_disadvantage, p1_action):
        return -1 * p2_win_amt
    # real ties are just neutral, no stance, disad or combo damage, reset to neutral
    else:
        return p1_action.amount - p2_action.amount

def payoff_matrix(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, actions = all_actions):
    return [[payoff(p1_action = p1_action, p2_action = p2_action,
                    p1_stance = p1_stance, p2_stance = p2_stance,
                    p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage)
             for p2_action in actions] for p1_action in actions]

def print_matrix(m):
    for line in m:
        print(" ".join(['{:>2}'.format(x) for x in line]))

def print_payoff_matrix(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, actions = all_actions):
    print_matrix(payoff_matrix(p1_stance = p1_stance, p2_stance = p2_stance,
                               p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage, actions = actions))
        
def payoff_eval(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None):
    matrix = payoff_matrix(p1_stance = p1_stance, p2_stance = p2_stance,
                           p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage)
    return evaluate(matrix)
    
def evaluate(matrix):
    game = nash.Game(np.array(matrix))
    eqls = list(game.support_enumeration())
    (p1val, p2val) = game[eqls[0][0], eqls[0][1]]
    return (eqls, [round(p1val, 2), round(p2val, 2)])

def evaluate_lh(matrix):
    game = nash.Game(np.array(matrix))
    eqls = game.lemke_howson(initial_dropped_label=0)
    (p1val, p2val) = game[eqls[0], eqls[1]]
    return (eqls, [round(p1val, 2), round(p2val, 2)])


def stance_matrix(amount, p2_disadvantage = None):
    return [[(payoff_eval(p1_stance = Stance(p1[1], amount), p2_stance = Stance(p2[1], amount), p2_disadvantage = p2_disadvantage)[1][0]) for p2 in all_action_types] for p1 in all_action_types]

def print_stance_matrix(amount, p2_disadvantage = None):
    print([n for (n, i) in all_action_types])
    print_matrix(stance_matrix(amount, p2_disadvantage))

def print_nfg(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, actions = all_actions):
    """format for gambit project files .nfg"""
    payoffs = [[payoff(p1_action = p1_action, p2_action = p2_action,
                    p1_stance = p1_stance, p2_stance = p2_stance,
                    p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage)
             for p1_action in actions] for p2_action in actions]
    print("""NFG 1 R "iron triangle" """)
    print("""{"Player 1" "Player 2" } { %s %s }""" %(len(actions), len(actions)))
    for line in payoffs:
        for p in line:
            print(p, -p, end=" ")
    print()

                
if __name__ == '__main__':
    print_nfg(p1_disadvantage = test_p1_disadvantage, actions = test_actions)
    
