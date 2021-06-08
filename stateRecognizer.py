import math


class StateRecognizer(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x_pile_witdh = int(width / 7)
        self.y_buffer_top = int(height * 0.30)
        self.y_buffer_bottom = int(height * 0.35)
        self.acceptance_radius = self.x_pile_witdh
        self.processed = {}
        self.x = {}
        self.y = {}
        self.count = {}
        self.ready = False

    def reset(self):
        self.processed = {}
        self.x = {}
        self.y = {}
        self.count = {}
        self.ready = False

    def resetTurn(self):
        for key in self.processed.items():
            self.processed[key] = True

    def addItem(self, label, x, y):
        if label in self.processed.keys():
            #Increment it's counter and update coordinates
            self.count[label] = self.count[label] + 1
            self.x[label] = x
            self.y[label] = y
        else:
            #Add entry to all hashmaps
            self.count[label] = 1
            self.x[label] = x
            self.y[label] = y
            self.processed[label] = False


    def evaluateFirstRound(self):
        # In the first round - we assume, that it has recognized 7 cards and we want these sorted with regards to x-value
        if len(self.processed.keys()) < 7:
            return "ERROR - LESS THAN 7 CARDS"

        #Find keys of 7 highest counts
        keys = sorted(self.count, key=self.count.get, reverse=True)[:7]

        xvals = []
        labels = []
        for key in keys:
            xvals.append(self.x[key])
            labels.append(key)

        # Sort after x value
        _, labels = zip(*sorted(zip(xvals, labels)))

        # Delete all unrecognized cards
        for key in self.processed.keys():
            if key not in labels:
                self.count[key] = 0

        return labels

    def evaluate(self):
        # To be called if a new card was revealed to figure out which card it was
        # Looks at all recognized cards - finds the one that was not known in previous round and also have been recognized the most times
        # The counts of the remaining cards will be set to 0.

        maxCount = 0
        maxKey = None

        for key,value in self.count.items():
            # Find most counted unprocessed card
            if value > maxCount and not self.processed[key]:
                maxCount = value
                maxKey = key

        # Delete all unrecognized cards
        for key in self.processed.keys():
            # If not previously processed or the newly found max key - delete it
            if key != maxKey or not self.processed[key]:
                del self.count[key]
                del self.processed[key]
                del self.x[key]
                del self.y[key]

        return maxKey

    def isReady(self, expected):
        return len(self.processed.keys()) >= expected


def reverse(lst):
    return [ele for ele in reversed(lst)]

