
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
