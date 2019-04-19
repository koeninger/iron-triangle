import iron_triangle as it
import matplotlib.pyplot as plt
import numpy as np


def plotAllDisad():
    actions = it.all_actions
    elems = it.all_elements
    subplotrow = len(it.all_action_types)
    subplotcol = len(elems)
    subplotindex = 0
    for (name, typ) in it.all_action_types:
        for (elem_name, elem) in elems:
            subplotindex = subplotindex + 1
            plt.subplot(subplotrow, subplotcol, subplotindex)
            plt.title("Disad %s %s" %(name, elem_name))
            for amt in range(0,3):
                xs = range(0,7)
                for (name2, typ2) in it.all_action_types:
                    color = 'k:' if name2 == 'Attack' else 'b--' if name2 == 'Grapple' else 'y-'
                    ys = [it.payoff_eval(actions = actions, p2_disadvantage = it.Disadvantage(typ, elem, amt), p1_stance = it.Stance(typ2, amt2))[1][0] for amt2 in xs]
                    plt.plot(xs, ys, color, label = "Disad %s Stance %s" %(amt, name2))

    plt.show()

                
if __name__ == '__main__':
    plotAllDisad()
    
                    
