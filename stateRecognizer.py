
### Gruppe 12 ###
#Christian Kyed - s184210
#Ida Schrader - s195483
#Mads Storgaard-Nielsen - s180076
#Marie Seindal - s185363
#Peter Revsbech - s183760
#Sebastian Bjerre - s163526

import math

noneMSG = 'NONE'
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
        deletionList = []
        for key in self.processed.keys():
            if not self.processed[key]:
                deletionList.append(key)
                del self.count[key]
                del self.x[key]
                del self.y[key]

        for key in deletionList:
            del self.processed[key]

    def markAllAsProcessed(self):
        for key in self.processed.keys():
            self.processed[key] = True

        for key in self.processed:
            if not self.processed[key]:
                self.count[key] = 0

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
        deletionList = []

        for key in self.processed.keys():
            # If not previously processed or the newly found max key - delete it
            if key not in keys:
                del self.count[key]
                del self.x[key]
                del self.y[key]
                deletionList.append(key)

        for key in deletionList:
            del self.processed[key]

        return labels

    def evaluate(self):
        # To be called if a new card was revealed to figure out which card it was
        # Looks at all recognized cards - finds the one that was not known in previous round and also have been recognized the most times
        # The counts of the remaining cards will be set to 0.

        maxCount = 0
        maxKey = noneMSG

        for key,value in self.count.items():
            # Find most counted unprocessed card
            if value > maxCount and not self.processed[key]:
                maxCount = value
                maxKey = key

        deletionList = []

        # Delete all unrecognized cards
        for key in self.processed.keys():
            # If not previously processed or the newly found max key - delete it
            if key != maxKey and not self.processed[key]:
                del self.count[key]
                del self.x[key]
                del self.y[key]
                deletionList.append(key)

        for key in deletionList:
            del self.processed[key]

        return maxKey

    def isReady(self, expected):
        return len(self.processed.keys()) >= expected

    def getAllProcessedLabels(self):
        resultString = ''
        for key in self.processed.keys():
            resultString = resultString + " " +key
        return resultString

    def getNumOfProcessedCards(self):
        count = 0
        for key in self.processed.keys():
            if self.processed[key]:
                count = count + 1
        return count


def reverse(lst):
    return [ele for ele in reversed(lst)]




