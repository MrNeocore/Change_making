import warnings
from collections import OrderedDict

class Change:
    # When more than {print_expand_threshold} unit of the same denomination (e.g. 2€ coins) are used, do not expand (i.e. 2+2+2+2) but display "{denomination}*{count}"" instead.
    print_expand_threshold = 5

    def __init__(self, bill10, bill5, coin2):
        self.bill10 = bill10
        self.bill5  = bill5
        self.coin2  = coin2

    def __str__(self):
        out = []
        # Construct the output string by either expanding the count / value pairs or showing a simple product sign (see {print_expand_threshold} class variable comment).
        for value, count in zip([10,5,2], [self.bill10, self.bill5, self.coin2]):
            if count <= Change.print_expand_threshold:
                out.extend([str(value)] * count)
            else:
                out.append(f"{count}*{value}")

        return ' + '.join(out)
        #return ' + '.join(['10'] * self.bill10 + ['5'] * self.bill5 + ['2'] * self.coin2) # Simpler print method, always expanding value / count. 

def optimalChange(s, verbose=0):
    # Checks that the input amount is an integer
    if not isinstance(s, int):
        raise TypeError("Can only compute the optimalChange for an positive integer amount.")
    
    # Checks that the input amount is a strictly positive number
    if s <= 0:
        raise ValueError("Can only compute the optimalChange for an positive integer amount.")

    # Order must match in Change constructor.
    denominations = [10,5,2]
    money_bag = OrderedDict({k:0 for k in denominations})
    l = len(money_bag)

    # Working variable : Remaining change to find
    r = s

    # Algorithm logic
    # Take from the remaining amount as many units of the current denomination - which are sorted in descending order.descending
    # If the remaining amount is smaller than any of the remaining denominations or if none of the denominations has the same parity as the remaining amount :
        # Take one unit back of the current denomination.
    # While not proven, tests indicate that this method ensures optimality (and feasability), even when using arbitrary denominations list.
    for i, x in enumerate(denominations):
        money_bag[x], r = divmod(r, x)
        
        if r == 0: 
            break

        # If none of the remaining denominations are not smaller (or equal) and not of the same parity as the remaining change to make, we take back 'one' of the current denomination.
        if (i+1 < l and not any([(x <= r) and x%2 == r%2 for x in denominations[i+1:]])) and money_bag[x] > 0:
            money_bag[x] -= 1
            r += x

    # We couldn't get the correct change, warn the user (if verbose) and return None
    if r != 0:
        if verbose: 
            warnings.warn("Could not find the correct change for {0} ! Remaining is : {1:.2f} €".format(s, r))
        
        return None 

    # Exact change found, return Change instance
    return Change(*money_bag.values())

if __name__ == '__main__':
    print(optimalChange(12))