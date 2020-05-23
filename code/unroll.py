from __future__ import print_function
from collections import namedtuple
import numpy as np
import gambit

# action types
ATTACK = 1
DEFEND = 2
GRAPPLE = 3
all_action_types = [('Attack', ATTACK), ('Defend', DEFEND), ('Grapple', GRAPPLE)]

# locations
HIGH = 1
LOW = 2
MID = 3
all_locations = [('High', HIGH), ('Low', LOW), ('Mid', MID)]

Stance = namedtuple('Stance', ['type', 'amount'])

Action = namedtuple('Action', ['type','location', 'amount', 'multiplier'])

Disadvantage = namedtuple('Disadvantage', ['type', 'location', 'amount'])

Combo = namedtuple('Combo', ['amount', 'action1', 'action2'])

attacks = [
    Action(ATTACK, HIGH, 3, 2),
    Action(ATTACK, LOW, 3, 2),
    Action(ATTACK, MID, 3, 2),
]

defenses = [
    Action(DEFEND, HIGH, 2, 1),
    Action(DEFEND, LOW, 2, 1),
    Action(DEFEND, MID, 2, 1),
]

grapples = [
    Action(GRAPPLE, HIGH, 4, 2),
    Action(GRAPPLE, LOW, 4, 2),
    Action(GRAPPLE, MID, 4, 2),
]

all_actions = attacks + defenses + grapples


#test_p2_disadvantage = Disadvantage(ATTACK, HIGH , 1)
test_p2_disadvantage = None

#test_p1_stance = Stance(ATTACK, 10)
test_p1_stance = None

test_actions = all_actions


def better_type(p1, p2):
    t1, t2 = (p1.type, p2.type)
    return ((t1 == ATTACK and t2 == GRAPPLE) or
            (t1 == GRAPPLE and t2 == DEFEND) or
            (t1 == DEFEND and t2 == ATTACK))

def better_location(p1, p2):
    e1, e2 = (p1.location, p2.location)
    return ((e1 == LOW and e2 == HIGH) or
            (e1 == MID and e2 == LOW) or
            (e1 == HIGH and e2 == MID))

def same_type(a, b):
    return a is not None and b is not None and a.type == b.type

def same_location(a, b):
    return a is not None and b is not None and a.location == b.location

def stance_loss(stance, action):
    return stance.amount if same_type(stance, action) else 0

def bonus(stance, action, combo = None):
    combo_bonus = combo.amount if combo is not None and (combo.action1 == action or combo.action2 == action) else 0
    stance_bonus = stance_loss(stance, action)
    
    return combo_bonus + round(stance_bonus * action.multiplier)

def disad_loss(disad, action):
    return disad.amount if (same_type(disad, action) or same_location(disad, action)) else 0

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
    elif better_location(p1_action, p2_action):
        return p1_win_amt
    elif better_location(p2_action, p1_action):
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
        print(" ".join(['{:+2}'.format(0.0 if x == 0 else x) for x in line]))

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
    print("""NFG 1 R "unroll" """)
    print("""{"Player 1" "Player 2" } { %s %s }""" %(len(actions), len(actions)))
    for line in payoffs:
        for p in line:
            print(p, -p, end=" ")
    print()

                
if __name__ == '__main__':
    print_nfg(p1_stance = test_p1_stance, p2_disadvantage = test_p2_disadvantage, actions = test_actions)
    
