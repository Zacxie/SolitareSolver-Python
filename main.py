import sys
import stateRecognizer

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


def main():
    #constants
    noneMSG = 'NONE'

    sg.ChangeLookAndFeel('LightGreen')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Text('Your moves', size=(40, 1), justification='left', font='Helvetica 14')],
              [sg.Multiline(size=(30, 30),disabled=True, key='textbox',justification='top'),sg.Image(filename='', key='image')],
              [sg.ReadButton('Exit', size=(10, 1), pad=((200, 0), 3), font='Helvetica 14'),
               sg.RButton('Start Capture', size=(10, 1), font='Any 14'),
               sg.RButton('End Capture', size=(10, 1), font='Any 14'),
               sg.RButton('New Game', size=(10, 1), font='Any 14')]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       location=(800, 400))
    window.Layout(layout).Finalize()



    #Initialize video capture and dimensions
    cap = cv.VideoCapture(1)
    _, frame = cap.read()  #
    height, width, _ = frame.shape

    #Init the stateRecognizer
    recognizer = stateRecognizer.StateRecognizer(width, height)

    #State parameters
    analyzing = False
    firstRound = True
    moveList = ''
    unknownCard = True
    newCards = noneMSG
    numOfExpectedCards = 7



    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    while True:

        # Configure buttons
        if not recognizer.isReady(numOfExpectedCards):
            window['End Capture'].update(disabled=True)
        elif analyzing:
            window['End Capture'].update(disabled=False)

        button, values = window.read(timeout=0)

        #Button choice
        if button == 'Exit' or values is None:
            sys.exit(0)

        elif button == 'Start Capture':
            analyzing = True
            recognizer.resetTurn()

        elif button == 'New Game':

            recognizer.reset()
            moveList = ''
            window['textbox'].update(moveList)
            firstRound=True
            numOfExpectedCards = 7

        elif button == 'End Capture':
            newCards = noneMSG
            answer = "Yes"
            analyzing = False
            window['End Capture'].update(disabled=True)

            if firstRound:
                newCards = recognizer.evaluateFirstRound()
                firstRound=False
                answer = sg.popup_yes_no('Confirming state',
                                         'New cards this round were: ' + str(newCards),
                                         'Are you satisfied with the current state recognized?',
                                         keep_on_top=True)

            elif unknownCard:
                #Only look for new card if unkownCard is true
                newCards = recognizer.evaluate()
                numOfExpectedCards = numOfExpectedCards + 1

                answer = sg.popup_yes_no('Confirming state',
                                         'New card this round was: ' + str(newCards),
                                         'Are you satisfied with the current state recognized?',
                                         keep_on_top=True)

            if (answer=="Yes"):
                client.send(newCards)
                msg = client.recieve()
                msgItems = msg.split(";")

                #1st item is description of move

                moveList = "Turn: "+msgItems[3]+""+msgItems[0] + '\n\n' + moveList
                window['textbox'].update(moveList)


                #2nd item is true/false describing if a new card is revealed
                if msgItems[1] == 'true' or msgItems[1] == 'True':
                    unknownCard = True
                else:
                    unknownCard = False

                #3rd item is either GAME_WON, GAME_LOST or empty


            elif (answer=="No"):
                recognizer.resetTurn()
                window['End Capture'].update(disabled=True)

        # Capture frame-by-frame
        ret, frame = cap.read()

        if (analyzing):
            # Get OpenCV to recognize
            frame = analyze(cap, recognizer, numOfExpectedCards)

        # Display the resulting frame
        # cv.imshow('frame', frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # let img be the PIL image
        img = Image.fromarray(gray)  # create PIL image from frame

        bio = io.BytesIO()  # a binary memory resident stream
        img.save(bio, format='PNG')  # save image as png to it
        imgbytes = bio.getvalue()  # this can be used by OpenCV hopefully
        window.FindElement('image').Update(data=imgbytes)

main()


