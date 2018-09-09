''' Unit testing for the optimalChange method '''
import unittest # Note : An alternative Python test suite is 'pytest'
import rendu_simple

class TestRendu(unittest.TestCase):
    def loop_assertEqual(self, inputs_outputs):
        for i, o in inputs_outputs.items():
            with self.subTest(name=i):
                res = rendu_simple.optimalChange(i)
                self.assertIsInstance(res, rendu_simple.Change)
                self.assertEqual([res.coin2, res.bill5, res.bill10], o)

    def loop_assertRaises(self, inputs, exception, msg_regex):
        for i in inputs:
            with self.subTest(name=i):
                with self.assertRaisesRegex(exception, msg_regex):
                    rendu_simple.optimalChange(i)

    def test_optimal_simple(self):
        ''' 
            Checks that the method works with 'simple' inputs 
            'simple' inputs : Inputs for which a greedy algorithm can find a [optimal] solution .
            -> Numbers ending in : [0,2,4,5,7,9]
        '''

        # Output denominations : [2,5,10]
        inputs_outputs = {2:[1,0,0],
                          4:[2,0,0],
                          5:[0,1,0],
                          7:[1,1,0],
                          9:[2,1,0],
                         12:[1,0,1],
                         17:[1,1,1],
                         29:[2,1,2],
                         47:[1,1,4],
                        109:[2,1,10],
                        525:[0,1,52],
                     123454:[2,0,12345]}

        self.loop_assertEqual(inputs_outputs)
        
    def test_optimal_complex(self):
        ''' 
            Checks that the method works with 'complex' inputs 
            'complex' inputs : Inputs for which a greedy algorithm cannot find the optimal solution - or any at all.
            -> Numbers ending in : [1,3,6,8] except for numbers [1,3] which are impossible to solve for using the given denominations list.
            
            For example : - Making change for 6€ is possible using 2+2+2, but the greedy algorithm would pick 1 bill of 5 then be stuck with 1€ left -> Failure. 
                          - Alternatively, using denominations [3,2], the greedy algorithm would pick '2+2+2' while the optimal result is 3+3. 
                                -> The full version of this program remains optimal even in this case :).

            A non-proven solution, but passing all current tests (even with arbitrary denominations) is to take back 1 unit of the current denomination if none of 
            the remaining denominations are not smaller (or equal) and not of the same parity as the remaining change to make.
            
            A more generic and robust solution would be to compute the combinations of all smaller values that would sum to the remaining change value {r} or using 
            a probabilistic convolution tree (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0091507). However, both are more complex and / or slower.
        '''

        # Output denominations values : [2,5,10]
        inputs_outputs = {6:[3,0,0],
                          8:[4,0,0],
                         11:[3,1,0],
                         13:[4,1,0],
                         16:[3,0,1],
                         18:[4,0,1],
                         36:[3,0,3],
                         43:[4,1,3],
                         56:[3,0,5],
                         61:[3,1,5],
                         78:[4,0,7],
                        111:[3,1,10],
                      58946:[3,0,5894]}

        self.loop_assertEqual(inputs_outputs)


    def test_bad_inputs(self):
        ''' Checks that the method corretly discards invalid inputs '''

        # Test invalid types
        self.loop_assertRaises([12.0, "what is this", []], TypeError, "Can only compute the optimalChange for an positive integer amount.")

        # Test invalid values
        self.loop_assertRaises([0, -12], ValueError, "Can only compute the optimalChange for an positive integer amount.")


    def test_possible(self):
        ''' 
            Checks that the algorithm can find a Change for many values but doesn't check optimality 
            Note : Change may be found for some combination of input values and denominations list, in our case : 1 and 3.
        '''
        for i in range(4,10000):
            with self.subTest(name=i):
                res = rendu_simple.optimalChange(i)
                self.assertIsInstance(res, rendu_simple.Change)

    def test_impossible(self):
        ''' Using the given denomination set [10,5,2], making the change for 1€ or 3€ is impossible'''
        for i in [1,3]:
            res = rendu_simple.optimalChange(i)
            self.assertIsNone(res)


if __name__ == '__main__':
    unittest.main(exit=False)