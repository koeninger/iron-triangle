#!./venv/bin/python
import unittest
import iron_triangle as it

class TestIronTriangle(unittest.TestCase):
    def testBasicActions(self):
        """basic triangle of defense beats attack beats grapple beats defense"""
        atk = it.attacks[0]
        dfn = it.defenses[0]
        grp = it.grapples[0]
        self.assertEqual(it.payoff(atk, atk), 0)
        self.assertEqual(it.payoff(atk, atk), 0)
        self.assertEqual(it.payoff(dfn, dfn), 0)
        self.assertTrue(it.payoff(atk, grp) > 0)
        self.assertTrue(it.payoff(grp, dfn) > 0)
        self.assertTrue(it.payoff(dfn, atk) > 0)
        self.assertTrue(it.payoff(atk, dfn) < 0)
        self.assertTrue(it.payoff(dfn, grp) < 0)
        self.assertTrue(it.payoff(grp, atk) < 0)
        
    def testEquilibrium(self):
        """at neutral there should be equal value for both players, and no dominated strategies"""
        eql, val = it.payoff_eval()
        self.assertEqual(val[0], 0)
        self.assertEqual(val[1], 0)
        dominated = [p for p in eql if p == 0]
        self.assertEqual(len(dominated), 0)

    def testDisadvantage(self):
        """disadvantage should make things worse for you"""
        p2 = [it.payoff_eval(p2_disadvantage = it.Disadvantage(act, 1)) for act in [it.ATTACK, it.DEFEND, it.GRAPPLE]]
        for (e, v) in p2:
            self.assertTrue(v[0] > 0)
            self.assertTrue(v[1] < 0)
        p1 = [it.payoff_eval(p1_disadvantage = it.Disadvantage(act, 1)) for act in [it.ATTACK, it.DEFEND, it.GRAPPLE]]
        for (e, v) in p1:
            self.assertTrue(v[0] < 0)
            self.assertTrue(v[1] > 0)

    def testStance(self):
        for typ in [it.ATTACK, it.DEFEND, it.GRAPPLE]:
            stance = it.Stance(typ, 1)
            for p1 in it.all_actions:
                for p2 in it.all_actions:
                    pay = it.payoff(p1, p2)
                    pay_stance = it.payoff(p1, p2, p1_stance = stance)
                    if stance.type != p1.type or p1 == p2:
                        # stances shouldn't have an effect if you don't choose a matching type of action
                        self.assertEqual(pay, pay_stance)
                    elif pay > 0:
                        # stances should help if you're right
                        self.assertTrue(pay_stance > pay)
                    else:
                        # stances should hurt if you're wrong
                        self.assertTrue(pay_stance < pay)

    def testSanityCheck(self):
        for (name, typ) in it.all_action_types:
            for amt in range(1,3):
                print(
                    it.payoff_eval(p2_disadvantage = it.Disadvantage(typ, amt))[1][0],
                    name, "disad", amt)
                for amt2 in range(1,5):
                    for (name2, typ2) in it.all_action_types:
                        print(
                            it.payoff_eval(p2_disadvantage = it.Disadvantage(typ, amt), p1_stance = it.Stance(typ2, amt2))[1][0],
                            name, "disad", amt, name2, "stance", amt2)
            for amt in range(1,5):
                print(it.payoff_eval(p1_stance = it.Stance(typ, amt))[1][0], name, "stance", amt)
        for amt in range(1,5):
            print("overall stance ", amt, "\n", it.evaluate(it.stance_matrix(amt)))
                
if __name__ == '__main__':
    unittest.main()
