import iron_triangle as it
import matplotlib.pyplot as plt
import numpy as np


def plotAllDisad():
    actions = it.all_actions
    locs = it.all_locations
    subplotrow = len(it.all_action_types)
    subplotcol = len(locs)
    subplotindex = 0
    for (name, typ) in it.all_action_types:
        for (loc_name, loc) in locs:
            subplotindex = subplotindex + 1
            plt.subplot(subplotrow, subplotcol, subplotindex)
            plt.title("Disad %s %s" %(name, loc_name))
            for amt in range(0,3):
                xs = range(0,7)
                for (name2, typ2) in it.all_action_types:
                    color = 'k:' if name2 == 'Attack' else 'b--' if name2 == 'Grapple' else 'y-'
                    ys = [it.payoff_eval(actions = actions, p2_disadvantage = it.Disadvantage(typ, loc, amt), p1_stance = it.Stance(typ2, amt2))[1][0] for amt2 in xs]
                    plt.plot(xs, ys, color, label = "Disad %s Stance %s" %(amt, name2))

    plt.show()

# assumes counteracting combo is the best    
def plotComboDisad():
    actions = it.all_actions
    locs = it.all_locations
    subplotrow = len(it.all_action_types)
    subplotcol = len(locs)
    subplotindex = 0
    for (name, typ) in it.all_action_types:
        for (loc_name, loc) in locs:
            subplotindex = subplotindex + 1
            plt.subplot(subplotrow, subplotcol, subplotindex)
            plt.title("Disad %s %s" %(name, loc_name))
            for amt in range(0,3):
                xs = range(0,7)
                [ca1, ca2] = (it.attacks if typ == it.DEFEND else it.grapples if typ == it.ATTACK else it.defenses)[0:2] 
                combo = it.Combo(amt + 1, ca1, ca2)
                color = 'r--'
                ys = [it.payoff_eval(actions = actions, p1_combo = combo, p2_disadvantage = it.Disadvantage(typ, loc, amt), p1_stance = it.Stance(combo.action1.type, amt2))[1][0] for amt2 in xs]
                plt.plot(xs, ys, color, label = "Disad %s Stance %s Combo %s" %(amt, combo.action1.type, combo.amount))
                for (name2, typ2) in it.all_action_types:
                    color = 'k:' if typ2 == it.ATTACK else 'b--' if typ2 == it.GRAPPLE else 'y-'
                    ys = [it.payoff_eval(actions = actions, p2_disadvantage = it.Disadvantage(typ, loc, amt), p1_stance = it.Stance(typ2, amt2))[1][0] for amt2 in xs]
                    plt.plot(xs, ys, color, label = "Disad %s Stance %s" %(amt, name2))

    plt.show()

    
if __name__ == '__main__':
    plotComboDisad()
    
                    
