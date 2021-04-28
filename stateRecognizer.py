import math

class StateRecognizer(object):


    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.x_pile_witdh=int(width/7)
        self.y_buffer_top = int(height * 0.30)
        self.y_buffer_bottom = int(height * 0.35)
        self.acceptance_radius = self.x_pile_witdh
        self.itemLabels = []
        self.processed = []


    def reset(self):
        #Remove all unprocessed items
        newItemLabels = []
        for i in self.itemLabels:
            if self.processed[i]:
                newItemLabels.append(self.itemLabels[i])

        self.itemLabels = newItemLabels

        # Mark all the reamaining items as processed
        for i in self.processed:
            self.processed[i] = True


    def addItem(self, label):
        is_contained = False
        for i in range(len(self.itemLabels)):
            if self.itemLabels[i] == label:

                is_contained = True

        if not is_contained:
            self.itemLabels.append(label)
            self.processed.append(False)

    def evaluateFirstRound(self):
        #In the first round - we assume, that it has recognized 7 cards and we want these sorted with regards to x-value
        if len(self.itemLabels) != 7:
            return None
        sorted_x, sorted_labels = zip(*sorted(zip(self.x, self.itemLabels)))

        #Mark all the 7 items as processed
        for i in self.processed:
            self.processed[i] = True

        return sorted_labels


    def evaluate(self):
        #To be called if a new card was revealed to figure out which card it was
        #Looks at all recognized cards - finds the one that was not known in previous round

        resultCard = None

        for i in self.processed:
            if not self.processed[i]:
                if not resultCard == None:
                    print('Error - more that one new card this round!')
                    return "ERROR - MORE THAN ONE CARD"
                # This is the new card that was revealed
                resultCard = self.itemLabels[i]
                self.processed[i] = True

        return resultCard



    def closestObject(self, x_exp, y_exp):
        closest = None
        min_dist = 10000
        for i in range(len(self.itemLabels)):
            x_dist = self.x[i] - x_exp
            y_dist = self.y[i] - y_exp
            dist = math.sqrt(x_dist*x_dist + y_dist*y_dist)
            if (dist < min_dist):
                closest = self.itemLabels[i]
                min_dist = dist
        return closest