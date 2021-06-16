
### Gruppe 12 ###
#Christian Kyed - s184210
#Ida Schrader - s195483
#Mads Storgaard-Nielsen - s180076
#Marie Seindal - s185363
#Peter Revsbech - s183760
#Sebastian Bjerre - s163526

class GUIState():
    def __init__(self, recognizer, window):
        self.newCards = 'NONE'
        self.analyzing = False
        self.recognizer = recognizer
        self.moveList = ""
        self.window = window
        self.firstRound = True
        self.numOfExpectedCards = 7
        self.unknownCard = True
        self.newGamePressed = False
