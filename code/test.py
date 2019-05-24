import unittest
from iron_triangle import *

class TestIronTriangle(unittest.TestCase):    
    def testBasicActions(self):
        """basic triangle of defense beats attack beats grapple beats defense"""
        atk = attacks[0]
        dfn = defenses[0]
        grp = grapples[0]
        self.assertEqual(payoff(atk, atk), 0)
        self.assertEqual(payoff(atk, atk), 0)
        self.assertEqual(payoff(dfn, dfn), 0)
        self.assertTrue(payoff(atk, grp) > 0)
        self.assertTrue(payoff(grp, dfn) > 0)
        self.assertTrue(payoff(dfn, atk) > 0)
        self.assertTrue(payoff(atk, dfn) < 0)
        self.assertTrue(payoff(dfn, grp) < 0)
        self.assertTrue(payoff(grp, atk) < 0)
        
    def testEquilibrium(self):
        """at neutral there should be equal value for both players, and no dominated strategies"""
        eql, val = payoff_eval()
        self.assertEqual(val[0], 0)
        self.assertEqual(val[1], 0)
        dominated = [p for p in eql if p == 0]
        self.assertEqual(len(dominated), 0)

    def testDisadvantage(self):
        """disadvantage should make things worse for you"""
        p2 = [payoff_eval(p2_disadvantage = Disadvantage(act, elem, 1)) for act in [ATTACK, DEFEND, GRAPPLE] for (n, elem) in all_elements]
        for (e, v) in p2:
            self.assertTrue(v[0] > 0)
            self.assertTrue(v[1] < 0)
        p1 = [payoff_eval(p1_disadvantage = Disadvantage(act, elem, 1)) for act in [ATTACK, DEFEND, GRAPPLE] for (n, elem) in all_elements]
        for (e, v) in p1:
            self.assertTrue(v[0] < 0)
            self.assertTrue(v[1] > 0)

    def testStance(self):
        for typ in [ATTACK, DEFEND, GRAPPLE]:
            stance = Stance(typ, 1)
            for p1 in all_actions:
                for p2 in all_actions:
                    pay = payoff(p1, p2)
                    pay_stance = payoff(p1, p2, p1_stance = stance)
                    if stance.type != p1.type or p1 == p2:
                        # stances shouldn't have an effect if you don't choose a matching type of action
                        self.assertEqual(pay, pay_stance)
                    elif pay > 0:
                        # stances should help if you're right
                        self.assertTrue(pay_stance > pay)
                    else:
                        # stances should hurt if you're wrong
                        self.assertTrue(pay_stance < pay)

    def testCombatExample(self):
        pay = payoff(
            Action(GRAPPLE, HEAVEN, 4, 3),
            Action(DEFEND, EARTH, 2, 1),
            p1_stance = Stance(GRAPPLE, 2),
            p2_stance = Stance(DEFEND, 1),
            p2_disadvantage = Disadvantage(ATTACK, EARTH, 1),
            p1_combo = Combo(1, Action(GRAPPLE, HEAVEN, 4, 3), Action(GRAPPLE, YINYANG, 4, 3)))
        self.assertEqual(pay, 13) 

if __name__ == '__main__':
    unittest.main()
