import pyautogui
from python_imagesearch.imagesearch import imagesearch
import time
import subprocess
import configparser

pyautogui.FAILSAFE = False
TIMELAPSE = 0.1

acceptButtonImg = './sample.png'
acceptedButtonImg = './sample-accepted.png'
championSelectionImg_flash = './flash-icon.png'
championSelectionImg_emote = './emote-icon.png'
playButtonImg = './play-button.png'
configDir = './config.ini'

wOffset = 0
parser = configparser.ConfigParser()
parser.read(configDir)
config = parser.sections()
if int(parser.get('Monitors', 'nrOfMonitors')) == 1:
    wOffset = 0
elif int(parser.get('Monitors', 'nrOfMonitors')) >= 2:
    wOffset = 1920

def checkGameAvailableLoop():
    print('Checking...')
    while True:
        pos = imagesearch(acceptButtonImg, 0.85)
        if pos[0] != -1:
            pyautogui.click((pos[0] - wOffset)+ 89, pos[1] + 31)
            print("Game accepted!")
            time.sleep(10.5)
            break
        
        time.sleep(TIMELAPSE)
    

def checkChampionSelection():
    flash = imagesearch(championSelectionImg_flash, 0.9)
    emote = imagesearch(championSelectionImg_emote, 0.9)

    if emote[0] != -1 or flash[0] != -1:
        return True
    else:
        return False

def checkGameCancelled():
    accepted = imagesearch(acceptedButtonImg)
    play = imagesearch(playButtonImg)

    if accepted[0] == -1 and play[0] != -1:
        return True
    else:
        return False

def isLeagueRunning():
    tasklist = str(subprocess.check_output('tasklist', shell=True))
    result = tasklist.find('League of Legends.exe')
    return result


def main():
    active = True
    leagueRunning = False
    while active:
        checkGameAvailableLoop()
        time.sleep(TIMELAPSE)
    
        cancelled = checkGameCancelled()
        if cancelled is True:
            print("Game has been cancelled, waiting...")
            
        csResult = checkChampionSelection()
        if csResult is True:
            print("Champion selection! Good Luck :D")
            
            while leagueRunning == False:
                cancelled = checkGameCancelled()
                if cancelled is True:
                    print("Game has been cancelled, waiting...")
                    break
                leagueStatus = isLeagueRunning()
                if leagueStatus > 0:
                    leagueRunning = True
            

        if leagueRunning == True:
            print("--------------------------------")
            print('Paused while League of Legends is running')
            print("--------------------------------")
            while leagueRunning == True:
                leagueStatus = isLeagueRunning()
                if leagueStatus == -1:
                    leagueRunning = False
        time.sleep(TIMELAPSE)
        

if __name__ == '__main__':
    main()