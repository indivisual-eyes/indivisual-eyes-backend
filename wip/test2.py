class Solution:

    def predictPartyVictory(self, senate: str) -> str:
       
        senate = []
        for senator in senate:
            senate.append(senator)
        # Base Case
        if 'D' not in senate:
            return 'Radiant'
        if 'R' not in senate:
            return 'Dire'
    

        for senator in range(len(senate)):

            if senate[senator] == 'R':
                senate = self.optimal_remove(senate, 'D', senator)
            elif senator[senator] == 'D':
                senate[senator] = self.optimal_remove(senate, 'R', senator)

        # New senate
        ns = ''
        for s in senate:
            if s != 'B':
                ns += s
        print(ns)
        return self.predictPartyVictory(ns)
    
    def optimal_remove(self,cycle: list, blocked: str, index: int):
        newsenate = cycle
        cur = index 
        max_index = len(newsenate)
        while cur != max_index:
            if newsenate[cur] == blocked:
                newsenate[cur] = 'B'
                return newsenate
            cur += 1

        return self.replace_first_instance(newsenate, blocked, 'B')
    
    def replace_first_instance(lst, target, replacement):
        for i, item in enumerate(lst):
            if item == target:
                lst[i] = replacement
                break  # Exit the loop after the first replacement
        return lst

Solution.predictPartyVictory("RDD")