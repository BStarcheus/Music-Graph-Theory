from Triad import *
import time
from pyo import *


def startNote(note):
    return Sine(freq=note.freq, mul=0.01).out()

def startChord(triad):
    playedNotes = []
    for note in triad.notes:
        x = startNote(note)
        playedNotes.append(x)
    return playedNotes

def stopNotes(notes):
    for x in notes:
        x.stop()

def playNote(note, dur=0.5):
    playNotes = startNote(note)
    time.sleep(dur)
    stopNotes(playNotes)

def playChord(triad, dur=0.5):
    playNotes = startChord(triad)
    time.sleep(dur)
    stopNotes(playNotes)


s = Server().boot()
s.start()
#s.gui(locals())


"""
# Testing chord progression
currNode = "CbM"

for _ in  range(15):
    print(currNode)
    playNotes = playChord(chords[currNode][1])
    time.sleep(0.5)
    stopNotes(playNotes)
    currNode = str(chords[currNode][5])
"""

start = "Fm"
end = "Edim"

# Depth first search

path = dfsPath(start, end)
print("Depth first search path for", start, "to", end)
print(path)
path = [Triad(x) for x in path]
for tr in path:
    print(tr)
    playChord(tr)


# Breadth first search

path = bfsPath(start, end)
path = [Triad(x) for x in path]
print("Breadth first search path for", start, "to", end)
print(path)
for tr in path:
    print(tr)
    playChord(tr)


s.stop()
s.shutdown()
