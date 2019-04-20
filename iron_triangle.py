from __future__ import print_function
from collections import namedtuple
import numpy as np
import gambit

# action types
ATTACK = 1
DEFEND = 2
GRAPPLE = 3
all_action_types = [('Attack', ATTACK), ('Defend', DEFEND), ('Grapple', GRAPPLE)]

# elements
YINYANG = 0
EARTH = 1
WATER = 2
FIRE = 3
HEAVEN = 4
all_elements = [('Yinyang', YINYANG), ('Earth', EARTH), ('Water', WATER), ('Fire', FIRE), ('Heaven', HEAVEN)]

#positional
BALANCED = 0
CROUCHING = 1
VERTICAL = 2
HORIZONTAL = 3
JUMPING = 4

Stance = namedtuple('Stance', ['type', 'amount'])

Action = namedtuple('Action', ['type','element', 'amount', 'multiplier'])

Disadvantage = namedtuple('Disadvantage', ['type', 'element', 'amount'])

Combo = namedtuple('Combo', ['amount', 'action1', 'action2'])

attacks = [
    Action(ATTACK, EARTH, 3, 2),
    Action(ATTACK, WATER, 3, 2),
    Action(ATTACK, FIRE, 3, 2),
    Action(ATTACK, HEAVEN, 3, 3),
    Action(ATTACK, YINYANG, 3, 3),
]

defenses = [
    Action(DEFEND, EARTH, 2, 1),
    Action(DEFEND, WATER, 2, 1),
    Action(DEFEND, FIRE, 2, 1),
]

grapples = [
    Action(GRAPPLE, EARTH, 4, 2),
    Action(GRAPPLE, WATER, 4, 2),
    Action(GRAPPLE, FIRE, 4, 2),
    Action(GRAPPLE, HEAVEN, 4, 3),
    Action(GRAPPLE, YINYANG, 4, 3),
]

beginner_actions = [attacks[0], defenses[0], grapples[0]]
basic_actions = attacks[0:3] + defenses[0:3] + grapples[0:3]
all_actions = attacks + defenses + grapples

test_p2_disadvantage = Disadvantage(ATTACK, EARTH , 1)
#test_p2_disadvantage = None

#test_p1_stance = Stance(ATTACK, 10)
test_p1_stance = None

test_actions = basic_actions
#test_actions = all_actions 



def better_type(p1, p2):
    t1, t2 = (p1.type, p2.type)
    return ((t1 == ATTACK and t2 == GRAPPLE) or
            (t1 == GRAPPLE and t2 == DEFEND) or
            (t1 == DEFEND and t2 == ATTACK))

def better_element(p1, p2):
    e1, e2 = (p1.element, p2.element)
    return ((e1 == YINYANG and (e2 == WATER or e2 == HEAVEN)) or
            (e1 == EARTH and (e2 == FIRE or e2 == YINYANG)) or
            (e1 == WATER and (e2 == EARTH or e2 == HEAVEN)) or
            (e1 == FIRE and (e2 == WATER or e2 == YINYANG)) or
            (e1 == HEAVEN and (e2 == EARTH or e2 == FIRE)))

def same_type(a, b):
    return a is not None and b is not None and a.type == b.type

def same_element(a, b):
    return a is not None and b is not None and a.element == b.element

def stance_loss(stance, action):
    return stance.amount if same_type(stance, action) else 0

def is_enlightened(x):
    return x is not None and (x.element == HEAVEN or x.element == YINYANG)

def bonus(stance, action, combo = None):
    combo_bonus = combo.amount if combo is not None and (combo.action1 == action or combo.action2 == action) else 0
    stance_bonus = stance_loss(stance, action)
    
    return combo_bonus + (stance_bonus * action.multiplier)

def disad_loss_act_elem(disad, action):
    return disad.amount if (same_type(disad, action) or same_element(disad, action)) else 0

def disad_loss_act(disad, action):
    return disad.amount if same_type(disad, action) else 0

def disad_loss_none(disad, action):
    return 0

# disad based on both seems best
disad_loss = disad_loss_act_elem

def payoff(p1_action, p2_action, p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, p1_combo = None):
    """net damage done by player 1 to player 2"""
    assert p1_disadvantage is None or p2_disadvantage is None

    p1_stance_loss = stance_loss(p1_stance, p1_action)
    p2_stance_loss = stance_loss(p2_stance, p2_action)

    p1_bonus = bonus(p1_stance, p1_action, p1_combo)
    p2_bonus = bonus(p2_stance, p2_action)

    p1_disad_loss = disad_loss(p1_disadvantage, p1_action)
    p2_disad_loss = disad_loss(p2_disadvantage, p2_action)
    
    p1_win_amt = p1_action.amount + p1_bonus + p2_stance_loss + p2_disad_loss
    p2_win_amt = p2_action.amount + p2_bonus + p1_stance_loss + p1_disad_loss

    if better_type(p1_action, p2_action):
        return p1_win_amt
    elif better_type(p2_action, p1_action):
        return -1 * p2_win_amt
    elif better_element(p1_action, p2_action):
        return p1_win_amt
    elif better_element(p2_action, p1_action):
        return -1 * p2_win_amt
    # disadvantage loses ties
    elif p2_disad_loss > 0:
        return p1_win_amt
    elif p1_disad_loss > 0:
        return -1 * p2_win_amt
    # real ties are just neutral, no stance, disad or combo damage, reset to neutral
    else:
        return p1_action.amount - p2_action.amount

def payoff_matrix(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, p1_combo = None, actions = all_actions):
    return [[payoff(p1_action = p1_action, p2_action = p2_action,
                    p1_stance = p1_stance, p2_stance = p2_stance,
                    p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage,
                    p1_combo = p1_combo)
             for p2_action in actions] for p1_action in actions]

def print_matrix(m):
    for line in m:
        print(" ".join(['{:>2}'.format(x) for x in line]))

def print_payoff_matrix(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, p1_combo = None, actions = all_actions):
    print_matrix(payoff_matrix(p1_stance = p1_stance, p2_stance = p2_stance,
                               p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage, p1_combo = p1_combo, actions = actions))
        
def payoff_eval(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, p1_combo = None, actions = all_actions):
    matrix = payoff_matrix(p1_stance = p1_stance, p2_stance = p2_stance,
                           p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage, p1_combo = p1_combo, actions = actions)
    return evaluate(matrix)
    
def evaluate(matrix):
    game = gambit.Game.new_table([len(matrix), len(matrix[0])])
    for p1 in range(0, len(matrix)):
        for p2 in range(0, len(matrix[0])) :
            game[p1,p2][0] = gambit.Decimal(matrix[p1][p2])
            game[p1,p2][1] = gambit.Decimal(-matrix[p1][p2])
            
    solver = gambit.nash.ExternalLCPSolver()
    eqls = solver.solve(game, use_strategic = True)
    #eqls = gambit.nash.lcp_solve(game, rational = False, use_strategic = True)
    eql = eqls[0]
    pay = eql.payoff()
    return [list(eql), [round(pay[0], 2), round(pay[1], 2)]] 
    
def stance_matrix(amount, p2_disadvantage = None, actions = all_action_types):
    return [[(payoff_eval(p1_stance = Stance(p1[1], amount), p2_stance = Stance(p2[1], amount), p2_disadvantage = p2_disadvantage)[1][0]) for p2 in actions] for p1 in actions]

def print_stance_matrix(amount, p2_disadvantage = None):
    print([n for (n, i) in all_action_types])
    print_matrix(stance_matrix(amount, p2_disadvantage))

def nfg_payoffs(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, actions = all_actions):
    return [[payoff(p1_action = p1_action, p2_action = p2_action,
                    p1_stance = p1_stance, p2_stance = p2_stance,
                    p1_disadvantage = p1_disadvantage, p2_disadvantage = p2_disadvantage)
             for p1_action in actions] for p2_action in actions]
    
def print_nfg(p1_stance = None, p2_stance = None, p1_disadvantage = None, p2_disadvantage = None, actions = all_actions):
    """format for gambit project files .nfg"""
    payoffs = nfg_payoffs(p1_stance, p2_stance, p1_disadvantage, p2_disadvantage, actions)
    print("""NFG 1 R "iron triangle" """)
    print("""{"Player 1" "Player 2" } { %s %s }""" %(len(actions), len(actions)))
    for line in payoffs:
        for p in line:
            print(p, -p, end=" ")
    print()

                
if __name__ == '__main__':
    print_nfg(p1_stance = test_p1_stance, p2_disadvantage = test_p2_disadvantage, actions = test_actions)
    
