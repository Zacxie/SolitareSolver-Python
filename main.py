
### Gruppe 12 ###
#Christian Kyed - s184210
#Ida Schrader - s195483
#Mads Storgaard-Nielsen - s180076
#Marie Seindal - s185363
#Peter Revsbech - s183760
#Sebastian Bjerre - s163526

import sys
import stateRecognizer
import GUIState
import conversion

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import cv2 as cv
from PIL import Image
import io
from sys import exit as exit
from opencv import analyze
import client

"""
Demo program that displays a webcam using OpenCV
"""

# constants
noneMSG = 'NONE'


def main():
    sg.ChangeLookAndFeel('TealMono')

    # define the window layout
    layout = [[sg.Text('', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Text('Moves', size=(40, 1), justification='left', font='Helvetica 14')],
              [sg.Multiline(size=(30, 30), disabled=True, key='textbox', justification='top'),
               sg.Image(filename='', key='image')],
              [sg.RButton('Start Capture', size=(10, 1), pad=((247, 0), 3), font='Any 14'),
               sg.RButton('End Capture', size=(10, 1), font='Any 14'),
               sg.RButton('New Game', size=(10, 1), pad=((150, 0), 3), font='Any 14'),
               sg.ReadButton('Exit', size=(10, 1), font='Helvetica 14')]]
    # Initialize video capture and dimensions
    cap = cv.VideoCapture(0)
    _, frame = cap.read()  #
    height, width, _ = frame.shape

    # create the window and show it without the plot
    window = sg.Window('CDIO Gruppe 12',
                       location=(800, 400))
    window.Layout(layout).Finalize()

    gs = GUIState.GUIState(stateRecognizer.StateRecognizer(width, height), window)

    gs.window['New Game'].update(disabled=True)


    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    while True:
        # Configure buttons
        if not gs.recognizer.isReady(gs.numOfExpectedCards):
            gs.window['End Capture'].update(disabled=True)
        elif gs.analyzing:
            gs.window['End Capture'].update(disabled=False)

        button, values = gs.window.read(timeout=0)

        # Button choice
        if button == 'Exit' or values is None:
            client.send('EXIT')
            client.end_con()
            sys.exit(0)

        elif button == 'Start Capture':
            gs.window['Start Capture'].update(disabled=True)
            gs.window['New Game'].update(disabled=True)
            gs.analyzing = True

        elif button == 'New Game':
            newGame(gs)
            continue

        elif button == 'End Capture':
            print('NumOfExpected: '+ str(gs.numOfExpectedCards))
            print('Processed Cards: '+ str(gs.recognizer.getNumOfProcessedCards()))
            endCapture(gs)

        # Capture frame-by-frame
        ret, frame = cap.read()

        if (gs.analyzing):
            # Get OpenCV to recognize
            frame = analyze(cap, gs.recognizer, gs.numOfExpectedCards)

        # Display the resulting frame
        # cv.imshow('frame', frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # let img be the PIL image
        img = Image.fromarray(gray)  # create PIL image from frame

        bio = io.BytesIO()  # a binary memory resident stream
        img.save(bio, format='PNG')  # save image as png to it
        imgbytes = bio.getvalue()  # this can be used by OpenCV hopefully
        window.FindElement('image').Update(data=imgbytes)


def gameWon(gs):
    gs.window['End Capture'].update(disabled=True)
    gs.window['Start Capture'].update(disabled=True)
    sg.popup_ok('Congratulations, you won the game! You can start a new game by selecting New Game, '
                'or quit the game by selecting Exit. Thanks for playing!', keep_on_top=True)


def gameLost(gs):
    gs.window['End Capture'].update(disabled=True)
    gs.window['Start Capture'].update(disabled=True)
    sg.popup_ok('You lost! Better luck next time. You can start a new game by selecting New Game, '
                'or quit the game by selecting Exit. Thanks for playing!', keep_on_top=True)


def newGame(gs):
    gs.newGamePressed = True
    endCapture(gs)
    gs.window['Start Capture'].update(disabled=False)
    gs.recognizer.reset()
    gs.moveList = ''
    gs.window['textbox'].update(gs.moveList)
    gs.firstRound = True
    gs.numOfExpectedCards = 7
    client.send('END_GAME')



def confirmFirstRound(gs):
    printarray = []
    gs.newCards = gs.recognizer.evaluateFirstRound()
    conversion.convertCards(gs.newCards, printarray)
    return sg.popup_yes_no('', 'New cards: ' + str(printarray).replace('[', '').replace(']', '').replace('\'', ''),
                           'Correct?',
                           keep_on_top=True)


def confirmOtherRounds(gs):
    printarray = []
    # Only look for new card if unkownCard is true
    gs.newCards = gs.recognizer.evaluate()
    if (gs.newCards != noneMSG):
        conversion.convertSingle(gs.newCards, printarray)

        return sg.popup_yes_no('', 'New card: ' + str(printarray).replace('[', '').replace(']', '').replace('\'', ''),
                               'Correct?',
                               keep_on_top=True)
    elif gs.newCards == noneMSG:
        return sg.popup_ok('', 'No new card was found. Try moving either the cards or camera a bit.',
                           keep_on_top=True)


def onConfirmCards(gs):
    gs.recognizer.markAllAsProcessed()
    # It is no longer first round
    gs.firstRound = False

    client.send(gs.newCards)
    msg = client.recieve()
    msgItems = msg.split(";")

    msg0converted = []
    msg0 = msgItems[0].split()
    conversion.stringBuilder(msg0,msg0converted)
    text = msg0converted.__str__().replace("'", "")
    text = text.replace(",","")
    text = text.replace("[", "")
    text = text.replace("]", "")


    # 1st item is description of move
    # "Processed cards: " + gs.recognizer.getAllProcessedLabels() +
    gs.moveList = "\nTurn: " + msgItems[3] + "" + \
                  text + '\n\n' + gs.moveList
    gs.window['textbox'].update(gs.moveList)

    # 2nd item is true/false describing if a new card is revealed
    if msgItems[1] == 'true' or msgItems[1] == 'True':
        gs.unknownCard = True
        gs.numOfExpectedCards = gs.numOfExpectedCards +1
    else:
        gs.unknownCard = False

    # 3rd item is either GAME_WON, GAME_LOST or empty
    if msgItems[2] == "GAME_WON":
        gameWon(gs)
    elif msgItems[2] == "GAME_LOST":
        gameLost(gs)


def endCapture(gs):
    gs.newCards = noneMSG
    answer = "No"
    gs.analyzing = False
    gs.window['Start Capture'].update(disabled=False)
    gs.window['End Capture'].update(disabled=True)

    if not gs.newGamePressed:
        if gs.firstRound:
            answer = confirmFirstRound(gs)

        elif gs.unknownCard:
            answer = confirmOtherRounds(gs)

        if (answer == "Yes"):
            onConfirmCards(gs)
            gs.window['New Game'].update(disabled=False)

            gs.newCards = noneMSG



        elif (answer == "No"):
            gs.recognizer.resetTurn()
            gs.window['End Capture'].update(disabled=True)
            gs.newCards = noneMSG


    gs.newGamePressed = False


main()


