
### Gruppe 12 ###
#Christian Kyed - s184210
#Ida Schrader - s195483
#Mads Storgaard-Nielsen - s180076
#Marie Seindal - s185363
#Peter Revsbech - s183760
#Sebastian Bjerre - s163526

def convertCards(newCards, printarray=[]):

    suit = ""
    number = ""

    for i in newCards:


        ### tjekker suit
        if (str(i).__contains__('H')):
            suit = "♥"
        elif (str(i).__contains__('D')):
            suit = '♦'
        elif (str(i).__contains__('C')):
            suit = '♣'
        elif (str(i).__contains__('S')):
            suit = '♠'
        else:
            continue

        ### tjekker tallet
        if (str(i).__contains__('A')):
            number = "A"
        elif (str(i).__contains__('2')):
            number = "2"
        elif (str(i).__contains__('3')):
            number = "3"
        elif (str(i).__contains__('4')):
            number = "4"
        elif (str(i).__contains__('5')):
            number = "5"
        elif (str(i).__contains__('6')):
            number = "6"
        elif (str(i).__contains__('7')):
            number = "7"
        elif (str(i).__contains__('8')):
            number = "8"
        elif (str(i).__contains__('9')):
            number = "9"
        elif (str(i).__contains__('10')):
            number = "10"
        elif (str(i).__contains__('J')):
            number = "J"
        elif (str(i).__contains__('Q')):
            number = "Q"
        elif (str(i).__contains__('K')):
            number = "K"
        else:
            continue
        printarray.append(number+suit)

def convertSingle(newCards, printarray=""):

    suit = ""
    number = ""

    ### tjekker suit
    if (newCards.__contains__('H')):
        suit = "♥"
    elif (newCards.__contains__('D')):
        suit = '♦'
    elif (newCards.__contains__('C')):
        suit = '♣'
    elif (newCards.__contains__('S')):
        suit = '♠'

    ### tjekker tallet
    if (newCards.__contains__('A')):
        number = "A"
    elif (newCards.__contains__('2')):
        number = "2"
    elif (newCards.__contains__('3')):
        number = "3"
    elif (newCards.__contains__('4')):
        number = "4"
    elif (newCards.__contains__('5')):
        number = "5"
    elif (newCards.__contains__('6')):
        number = "6"
    elif (newCards.__contains__('7')):
        number = "7"
    elif (newCards.__contains__('8')):
        number = "8"
    elif (newCards.__contains__('9')):
        number = "9"
    elif (newCards.__contains__('10')):
        number = "10"
    elif (newCards.__contains__('J')):
        number = "J"
    elif (newCards.__contains__('Q')):
        number = "Q"
    elif (newCards.__contains__('K')):
        number = "K"
    printarray.append(number+suit)

def stringBuilder (msg, returnmsg = []):
    suit = ""
    number = ""

    for i in msg:

        if (len(str(i)) == 2 or str(i).__contains__("10")):

            ### tjekker suit
            if (str(i).__contains__('H')):
                suit = "♥"
            elif (str(i).__contains__('D')):
                suit = "♦"
            elif (str(i).__contains__('C')):
                suit = "♣"
            elif (str(i).__contains__('S')):
                suit = "♠"
            else:
                suit = "no"


            ### tjekker tallet
            if (str(i).__contains__('A')):
                number = "A"
            elif (str(i).__contains__('2')):
                number = "2"
            elif (str(i).__contains__('3')):
                number = "3"
            elif (str(i).__contains__('4')):
                number = "4"
            elif (str(i).__contains__('5')):
                number = "5"
            elif (str(i).__contains__('6')):
                number = "6"
            elif (str(i).__contains__('7')):
                number = "7"
            elif (str(i).__contains__('8')):
                number = "8"
            elif (str(i).__contains__('9')):
                number = "9"
            elif (str(i).__contains__('10')):
                number = "10"
            elif (str(i).__contains__('J')):
                number = "J"
            elif (str(i).__contains__('Q')):
                number = "Q"
            elif (str(i).__contains__('K')):
                number = "K"
            else:
                number = "no"

            if (suit == "no" or number == "no"):
                returnmsg.append(i)
            else:
                returnmsg.append(number+suit)
            continue
        returnmsg.append(i)


