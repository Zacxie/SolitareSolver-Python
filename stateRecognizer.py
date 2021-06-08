import math


class StateRecognizer(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x_pile_witdh = int(width / 7)
        self.y_buffer_top = int(height * 0.30)
        self.y_buffer_bottom = int(height * 0.35)
        self.acceptance_radius = self.x_pile_witdh
        self.itemLabels = []
        self.processed = []
        self.x = []
        self.y = []
        self.count = []
        self.ready = False



    def reset(self):
        self.itemLabels = []
        self.processed = []
        self.x = []
        self.y = []
        self.count = []
        self.ready = False

    def resetTurn(self):
        # Remove all unprocessed items
        self.ready = False
        newItemLabels = []
        newX = []
        newY = []
        for i in range(len(self.itemLabels)):
            if self.processed[i]:
                newItemLabels.append(self.itemLabels[i])
                newX.append(self.x[i])
                newY.append(self.y[i])

        self.itemLabels = newItemLabels
        self.x = newX
        self.y = newY
        self.processed = []
        # Mark all the remaining items as processed
        for i in range(len(self.itemLabels)):
            self.processed.append(True)
            #self.processed[i] = True

    def addItem(self, label, x, y):
        is_contained = False
        for i in range(len(self.itemLabels)):
            # If card is already recognized.
            if self.itemLabels[i] == label:
                self.x[i] = x
                self.y[i] = y
                self.count[i] = self.count[i] + 1
                is_contained = True

        if not is_contained:
            # If the card is new and not have been recognized before
            self.itemLabels.append(label)
            self.processed.append(False)
            self.x.append(x)
            self.y.append(y)
            self.count.append(1)



    def evaluateFirstRound(self):
        # In the first round - we assume, that it has recognized 7 cards and we want these sorted with regards to x-value
        if len(self.itemLabels) < 7:
            return "ERROR - LESS THAN 7 CARDS"

        # Sort after count
        _, sorted_labels = zip(*sorted(zip(self.count, self.itemLabels)))

        # Take 7 most counted cards
        sorted_labels = reverse(sorted_labels)[0:7]

        # Create new x vector - only with cards in sorted_labels
        newX = []
        for i in range(len(sorted_labels)):
            index = self.itemLabels.index(sorted_labels[i])
            newX.append(self.x[index])

        # Sort after x value
        _, sorted_labels = zip(*sorted(zip(newX, sorted_labels)))

        # Go through items. Set count to 0 if card was an error. Otherwise mark as processed.
        for i in range(len(self.itemLabels)):
            if self.itemLabels[i] not in sorted_labels:
                self.count[i] = 0
            else:
                self.processed[i] = True

        # Return 7 most counted cards sorted after x value
        return sorted_labels

    def evaluate(self):
        # To be called if a new card was revealed to figure out which card it was
        # Looks at all recognized cards - finds the one that was not known in previous round and also have been recognized the most times
        # The remaining cards that hasn't been recognized will there count be set to 0.

        maxCount = 0
        index = None

        # Find the card with the highest count (recognized most times)
        for i in range(len(self.processed)):
            if not self.processed[i]:

                if maxCount < self.count[i]:
                    maxCount = self.count[i]
                    index = i

        self.processed[index] = True

        # Sets the count for all the cards that hasn't been processed to 0 (The cards that most likely are errors)
        for i in range(len(self.processed)):
            if not self.processed[i]:
                self.count[i] = 0

        return self.itemLabels[index]

    def isReady(self, expected):
        return len(self.itemLabels) >= expected


def reverse(lst):
    return [ele for ele in reversed(lst)]


