
__author__ = "Dustin Martin"
__version__ = "1.0"
__email__ = "dusmar6@gmail.com"

"""
Version 1.0 of the Radio Big project

Essentially just an inefficient, hastily thrown together proof-of-concept

"""


from configparser import SafeConfigParser
import os.path
import random
import time
import pygame
import playsound
import os
from tinytag import TinyTag


class Song:

    def __init__(self, titleIn, artistIn, lengthIn, fileLocIn, dirIn):
        self.title = titleIn
        self.artist = artistIn
        self.length = lengthIn  #in seconds
        self.fileLoc = fileLocIn
        self.directory = dirIn


    def getTitle(self):
        return self.title
    def getArtist(self):
        return self.artist
    def getLength(self):
        return self.length
    def getFileLoc(self):
        return self.fileLoc
    def getDirectory(self):
        return self.directory
    def getSinceLast(self):
        return self.sinceLast

class DJ:

    def __init__(self, lengthin, filelocin, dirin, artistin=None):
        self.artist = artistin
        self.fileLoc = filelocin
        self.length = lengthin
        self.directory = dirin


    def getartist(self):
        return self.artist

    def getlength(self):
        return self.length

    def getfileloc(self):
        return self.fileLoc

    def getdirectory(self):
        return self.directory


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

SONG_DIR = os.path.join(ROOT_DIR, 'songs\\normal')
INST_DIR = os.path.join(ROOT_DIR, 'songs\\instrumentals')

ARTIST_INTRO_DIR = os.path.join(ROOT_DIR, 'dj\\artist intros')
GEN_SONG_INTRO_DIR = os.path.join(ROOT_DIR, 'dj\\generic song intros')
INTRO_DIR = os.path.join(ROOT_DIR, 'dj\\intros')
INTRO_SFX_DIR = os.path.join(ROOT_DIR, 'dj\\introsSFX')
LOCAL_STORIES_DIR = os.path.join(ROOT_DIR, 'dj\\local stories')
OUTROS_DIR = os.path.join(ROOT_DIR, 'dj\\outros')
WEATHER_EVENTS_DIR = os.path.join(ROOT_DIR, 'dj\\weather events')

def getMetaTitle(directory):  # retrieves title from metadata of directory.
    tag = TinyTag.get(directory)
    return tag.title

def getMetaArtist(directory):  # retrieves artist name from metadata
    tag = TinyTag.get(directory)
    return tag.artist

def getMP3Length(directory):  # retrieves length of mp3
    tag = TinyTag.get(directory)
    return int(tag.duration)

def getWAVLength(directory, filename):
    os.chdir(directory)  # Get into the dir with sound
    statbuf = os.stat(filename)
    mbytes = statbuf.st_size / 1024
    duration = mbytes / 200
    return int(duration)

def discoverSongs(dir):
    temp = []
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            path = os.path.join(dir, filename)
            artist = getMetaArtist(path)
            length = getMP3Length(path)
            title = getMetaTitle(path)
            temp.append(Song(title, artist, length, path, dir))
    return temp

def discoverDJ(dir):
    temp = []
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            path = os.path.join(dir, filename)
            length = getMP3Length(path)
            if dir == ARTIST_INTRO_DIR:
                artist = getMetaArtist(path)
                temp.append(DJ(length, path, dir, artist))
            else:
                temp.append(DJ(length, path, dir))
    return temp

class dirClass:

    def __init__(self):

        self.songs = discoverSongs(SONG_DIR)
        self.instrumentals = discoverSongs(INST_DIR)

        self.artistIntros = discoverDJ(ARTIST_INTRO_DIR)
        self.songIntros = discoverDJ(GEN_SONG_INTRO_DIR)
        self.intros = discoverDJ(INTRO_DIR)
        self.introsSFX = discoverDJ(INTRO_SFX_DIR)
        self.localStories = discoverDJ(LOCAL_STORIES_DIR)
        self.outros = discoverDJ(OUTROS_DIR)
        self.weatherEvents = discoverDJ(WEATHER_EVENTS_DIR)

mp3Arrays = dirClass()

pygame.mixer.init()

songQuar = []
introQuar = []
intermissionQuar = []
eventQuar = []

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
gameArtists  = ["Yellowcard", "Alpinestars", "Andyhunter", "Aphrodite", "Audio Bullys", "Autopilot Off", "Basement Jaxx", "Chaos",
                    "Dan the Automator", " DeepSky", "Dilated Peoples", "Fatboy Slim", "Felix da Housecat", "Finger Eleven",
                    "Fischerspooner", "Ima Robot","Jane's Addiction","Johnny Morgan","Kinky","N.E.R.D",
                    "Overseer","Placebo", "Queens of the Stone Age","Red Hot Chili Peppers",
                    "The Caesars","Swollen Members","Swollen Members","The Black Eyed Peas","The Chemical Brothers",
                    "Thrice","The X-Ecutioners"]


def writeDefaultConfig():
    config = SafeConfigParser()
    config.read(ROOT_DIR+'\\config.ini')
    config.add_section('number of songs between intermissions')
    config.set('number of songs between intermissions', 'at least', '1')
    config.set('number of songs between intermissions', 'at most', '2')
    with open('config.ini', 'w') as f:
        config.write(f)


def getConfig():
    config = SafeConfigParser()
    config.read(ROOT_DIR+'\\config.ini')
    return config


def intermissionCheck(streak, interFreq):
    if streak >= interFreq:
        return True
    else:
        return False


def playIntermission():
    current = mp3Arrays.instrumentals[random.randint(0, len(mp3Arrays.instrumentals)-1)]
    while current in intermissionQuar:
        current = mp3Arrays.instrumentals[random.randint(0, len(mp3Arrays.instrumentals)-1)]
    pygame.mixer.music.load(current.fileLoc)
    pygame.mixer.music.play()

    if len(intermissionQuar) > 2:
        del intermissionQuar[:-1]
    intermissionQuar.insert(0, current)
    return current


def playSong():
    s = mp3Arrays.songs[random.randint(0, len(mp3Arrays.songs)-1)]
    while s in songQuar:
        s = mp3Arrays.songs[random.randint(0, len(mp3Arrays.songs)-1)]
    pygame.mixer.music.load(s.fileLoc)
    pygame.mixer.music.play()
    if len(songQuar)> 7:
        del songQuar[:-1]
    songQuar.insert(0, s)
    return s


def playWeather():
    w = mp3Arrays.weatherEvents[random.randint(0, len(mp3Arrays.weatherEvents)-1)]
    while w in eventQuar:
        w = mp3Arrays.weatherEvents[random.randint(0, len(mp3Arrays.weatherEvents)-1)]
    playsound.playsound(w.fileLoc, False)

    if len(eventQuar) > 19:
        del eventQuar[:-1]
    eventQuar.insert(0, w)
    return w

def playEvent():
    e = mp3Arrays.localStories[random.randint(0, len(mp3Arrays.localStories)-1)]
    while e in eventQuar:
        e = mp3Arrays.localStories[random.randint(0, len(mp3Arrays.localStories)-1)]
    playsound.playsound(e.fileLoc, False)

    if len(eventQuar) > 19:
        del eventQuar[:-1]
    eventQuar.insert(0, e)
    return e


def playIntro(song):
    temp=[]
    if song.getArtist() in gameArtists:
        for x in mp3Arrays.artistIntros:
            if song.getArtist() == x.getartist():
                introtemp = x
                temp.append(introtemp)
        i = temp[random.randint(0, len(temp)-1)]
        while i in introQuar:
            i = temp[random.randint(0, len(temp)-1)]
        playsound.playsound(i.fileLoc, False)

        if len(introQuar) > 6:
            del introQuar[:-1]
        introQuar.insert(0, i)

    else:
        i = mp3Arrays.songIntros[random.randint(0,len(mp3Arrays.songIntros)-1)]
        while i in introQuar:
            i = mp3Arrays.songIntros[random.randint(0,len(mp3Arrays.songIntros)-1)]
        playsound.playsound(i.fileLoc, False)

        if len(introQuar) > 6:
            del introQuar[:-1]
        introQuar.insert(0, i)

def playSFXIntro():
    i = mp3Arrays.introsSFX[random.randint(0,len(mp3Arrays.introsSFX)-1)]
    while i in introQuar:
        i = mp3Arrays.introsSFX[random.randint(0,len(mp3Arrays.introsSFX)-1)]
    playsound.playsound(i.fileLoc, False)

    if len(introQuar) > 6:
        del introQuar[:-1]
    introQuar.insert(0, i)

    return i

def playOutro():
    o = mp3Arrays.outros[random.randint(0, len(mp3Arrays.outros)-1)]
    while o in introQuar:
        o = mp3Arrays.outros[random.randint(0, len(mp3Arrays.outros)-1)]
    playsound.playsound(o.fileLoc, False)

    if len(introQuar) > 6:
        del introQuar[:-1]
    introQuar.insert(0, o)

def main():
    try:
        try:
            config = getConfig()
            configAtLeast = int(config.get('number of songs between intermissions', 'at least'))
            configAtMost = int(config.get('number of songs between intermissions', 'at most'))
        except:
            writeDefaultConfig()
            config = getConfig()
            configAtLeast = int(config.get('number of songs between intermissions', 'at least'))
            configAtMost = int(config.get('number of songs between intermissions', 'at most'))
    except:
        print("Config Error")
        configAtLeast = 1
        configAtMost = 2


    interFreq = random.randint(configAtLeast, configAtMost)

    songStreak = 0
    isAfterInter = False


    while True:

        currentSong = playSong()
        songStreak+=1

        if isAfterInter:
            time.sleep(2)
        time.sleep(random.randint(2, 4))
        playIntro(currentSong)
        time.sleep(currentSong.getLength()-4)

        if intermissionCheck(songStreak, interFreq):
            currentSFXIntro = playSFXIntro()
            time.sleep(.3)
            pygame.mixer.music.stop()
            time.sleep(2)
            currentInter = playIntermission()

            time.sleep(0.7) #sfxintro finishes
            time.sleep(1.5) #adjust gap

            currentWeather = playWeather()
            time.sleep(currentWeather.getlength())

            time.sleep(random.randint(2, 3))
            times = random.randint(2,4)

            for x in range(times):
                currentEvent = playEvent()
                time.sleep(currentEvent.getlength())
                time.sleep(random.randint(2,3))

            playOutro()
            time.sleep(random.randint(6,8))

            playSFXIntro()
            time.sleep(.65)
            pygame.mixer.music.stop()

            songStreak=0
            interFreq = random.randint(configAtLeast, configAtMost)
            time.sleep(1)
        else:
            while pygame.mixer.get_busy():
                time.sleep(.01)

main()
