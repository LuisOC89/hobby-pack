import datetime

#To fix times like 1:3, to make it look like 01:03, or dates like 4/8/2018, to make it look like 04/08/2018
def filling(number):
    if (number < 10):
        if (number == 0):
            return "00"
        else:
            return("0"+str(number))
    else:
        return(str(number))

#To get current date and time
def now1():
    return datetime.datetime.now()