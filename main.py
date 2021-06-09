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


    sg.ChangeLookAndFeel('LightGreen')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Text('Your moves', size=(40, 1), justification='left', font='Helvetica 14')],
              [sg.Multiline(size=(30, 30), disabled=True, key='textbox', justification='top'),
               sg.Image(filename='', key='image')],
              [sg.ReadButton('Exit', size=(10, 1), pad=((200, 0), 3), font='Helvetica 14'),
               sg.RButton('Start Capture', size=(10, 1), font='Any 14'),
               sg.RButton('End Capture', size=(10, 1), font='Any 14'),
               sg.RButton('New Game', size=(10, 1), font='Any 14')]]
    # Initialize video capture and dimensions
    cap = cv.VideoCapture(0)
    _, frame = cap.read()  #
    height, width, _ = frame.shape

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       location=(800, 400))
    window.Layout(layout).Finalize()

    gs = GUIState.GUIState(stateRecognizer.StateRecognizer(width, height), window)


    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    while True:
        # Configure buttons
        if not gs.recognizer.isReady(gs.numOfExpectedCards):
            gs.window['End Capture'].update(disabled=True)
        elif gs.analyzing:
            gs.window['End Capture'].update(disabled=False)

        button, values = gs.window.read(timeout=0)

        #Button choice
        if button == 'Exit' or values is None:
            sys.exit(0)

        elif button == 'Start Capture':
            gs.analyzing = True

        elif button == 'New Game':
            newGame(gs)

        elif button == 'End Capture':
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
    sg.popup_yes_no('Congrats', keep_on_top=True)

def gameLost(gs):
    gs.window['End Capture'].update(disabled=True)
    gs.window['Start Capture'].update(disabled=True)
    sg.popup_yes_no('You suck', keep_on_top=True)

def newGame(gs):
    gs.window['Start Capture'].update(disabled=False)
    gs.recognizer.reset()
    gs.moveList = ''
    gs.window['textbox'].update(gs.moveList)
    gs.firstRound = True
    gs.numOfExpectedCards = 7


def confirmFirstRound(gs):
    printarray = []
    newCards = gs.recognizer.evaluateFirstRound()
    conversion.convertCards(newCards, printarray)
    return sg.popup_yes_no('Confirming state',
                             'New cards this round were: ' + str(printarray),
                             'Are you satisfied with the current state recognized?',
                             keep_on_top=True)


def confirmOtherRounds(gs):
    printarray = []
    # Only look for new card if unkownCard is true
    newCards = gs.recognizer.evaluate()
    conversion.convertSingle(newCards, printarray)
    gs.numOfExpectedCards = gs.numOfExpectedCards + 1

    return sg.popup_yes_no('Confirming state',
                             'New card this round was: ' + str(printarray),
                             'Are you satisfied with the current state recognized?',
                             keep_on_top=True)


def onConfirmCards(gs, newCards):
    gs.recognizer.markAllAsProcessed()
    # It is no longer first round
    firstRound = False

    client.send(newCards)
    msg = client.recieve()
    msgItems = msg.split(";")

    # 1st item is description of move

    gs.moveList = "Processed cards: " + gs.recognizer.getAllProcessedLabels() + "\nTurn: " + msgItems[3] + "" + \
                  msgItems[0] + '\n\n' + gs.moveList
    gs.window['textbox'].update(gs.moveList)

    # 2nd item is true/false describing if a new card is revealed
    if msgItems[1] == 'true' or msgItems[1] == 'True':
        gs.unknownCard = True
    else:
        gs.unknownCard = False

    # 3rd item is either GAME_WON, GAME_LOST or empty
    if msgItems[2] == "GAME_WON":
        gameWon(gs)
    elif msgItems[2] == "GAME_LOST":
        gameLost(gs)


def endCapture(gs):
    newCards = noneMSG
    answer = "Yes"
    gs.analyzing = False
    gs.window['End Capture'].update(disabled=True)

    if gs.firstRound:
       answer = confirmFirstRound(gs)

    elif gs.unknownCard:
       answer = confirmOtherRounds(gs)

    if (answer == "Yes"):
        onConfirmCards(gs, newCards)

    elif (answer == "No"):
        gs.recognizer.resetTurn()
        gs.window['End Capture'].update(disabled=True)


main()


