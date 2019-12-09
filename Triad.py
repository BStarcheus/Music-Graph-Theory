# This program contains notes for a single octave of the piano starting at middle C

# Frequencies for each piano key in single octave. 40 is middle C. 52 is C5
frequencies = {40:261.6256, 41:277.1826, 42:293.6648, 43:311.1270, 44:329.6276, 45:349.2282, 46:369.9944, 47:391.9954, 48:415.3047, 49:440, 50:466.1638, 51:493.8833, 52:523.2511}
# The piano key corresponding to each type of note
notes = {"C":40, "C#":41, "Db":41, "D":42, "D#":43, "Eb":43, "E":44, "Fb":44, "E#":45, "F":45, "F#":46, "Gb":46, "G":47, "G#":48, "Ab":48, "A":49, "A#":50, "Bb":50, "B":51, "Cb":51, "B#":52}
# The possible names for each piano key, ignoring double sharps and flats
keys = {40:["C", "B#"], 41:["C#","Db"], 42:["D"], 43:["D#","Eb"], 44:["E","Fb"], 45:["E#","F"], 46:["F#","Gb"], 47:["G"], 48:["G#","Ab"], 49:["A"], 50:["A#","Bb"], 51:["B","Cb"], 52:["B#"]}


class Note():
    """
    The note class represents a single musical note represented by
    a letter A - G and an accidental #, b, or neither (natural),
    and its frequency on the middle C octave.
    """
    def __init__(self, noteStr):
        if len(noteStr) == 1:
            # "C"
            self.letter = str(noteStr[0])
            self.acc = ""
        elif len(noteStr) == 2:
            # "C#" or "Cb"
            self.letter = str(noteStr[0])
            self.acc = str(noteStr[1])
        else:
            raise "Invalid string for note."

        self.freq = frequencies[notes[str(self.letter) + str(self.acc)]]
    def __repr__(self):
        return self.letter + self.acc


class Triad():
    """
    The triad class represents a single chord with the
    root, third, and fifth notes.
    Triads have a root note and a quality.
    Qualities are Major (M), minor (m), or diminished (dim).
    """
    def __init__(self, triadStr):
        if len(triadStr) == 2:
            # "CM"
            self.root = Note(triadStr[0])
            self.qual = triadStr[1]
        elif len(triadStr) == 3:
            # "CbM" "C#m"
            self.root = Note(triadStr[:2])
            self.qual = triadStr[2]
        elif len(triadStr) > 3 and len(triadStr) <= 5:
            dInd = triadStr.find("dim")
            if dInd == 1:
                # "Cdim"
                self.root = Note(triadStr[0])
                self.qual = triadStr[1:]
            elif dInd == 2:
                # "C#dim"
                self.root = Note(triadStr[:2])
                self.qual = triadStr[2:]
            else:
                raise "Invalid string for triad."
        else:
            raise "Invalid string for triad."

        self.notes = self.genNotes()

    def __repr__(self):
        return str(self.root) + self.qual
    def genNotes(self):
        """ Get the list of root, third and fifth as Note objects"""
        noteLst = [self.root]
        num = ord(self.root.letter) # ASCII value of the root letter

        step1 = 0
        stepinc = 0
        letStep = 2

        if self.qual == "M":
            step1 = 4 # W W
            stepinc = 3 # H W
        elif self.qual == "m":
            step1 = 3 # W H
            stepinc = 4 # W W
        elif self.qual == "dim":
            step1 = 3 # W H
            stepinc = 3 # W H
        else:
            raise "Not a valid triad type."

        for _ in range(2):
            # The new number of piano key of the next note in the chord
            newNum = (((notes[self.root.letter + self.root.acc] + step1) - 40) % 12) + 40
            # Look in the keys and try to find a match that is either 2 or 4 letters after the root EX: A -> C# -> E
            newLets = [x for x in keys[newNum] if ord(x[0]) == (((num + letStep) - 65) % 7) + 65]
            # There will only ever be one result
            newLet = newLets[0]
            # Take the letter
            newLetter = newLet[0]
            # Take the accidental if there is one
            try:
                newAcc = newLet[1]
            except:
                newAcc = ""
            noteLst.append(Note(newLetter + newAcc))

            step1 += stepinc
            letStep *= 2

        return noteLst


def getScale(root, qual):
    """
    Returns a list of Note objects in a scale, given a root note and
    quality of the scale (M, m, or dim)
    """
    sclNotes = [root]
    steps = []
    curLetNum = ord(root.letter)

    if qual == "M":
        steps = [2, 2, 1, 2, 2, 2, 1]
    elif qual == "m":
        steps = [2, 1, 2, 2, 1, 2, 2]
    elif qual == "dim":
        steps = [2, 1, 2, 1, 2, 1, 2, 1]
    else:
        raise "Not a valid scale type."

    newKeyNum = notes[root.letter + root.acc]

    for step in steps:
        # The ASCII number of the current letter
        curLetNum = (((curLetNum + 1) - 65) % 7) + 65
        # The piano key number for the next note
        newKeyNum = (((newKeyNum + step) - 40) % 12) + 40
        # Look in the keys and try to find a match to the current letter
        newLets = [x for x in keys[newKeyNum] if ord(x[0]) == curLetNum]
        # There will only ever be one result
        newLet = newLets[0]
        # Take the letter
        newLetter = newLet[0]
        # Take the accidental if there is one
        try:
            newAcc = newLet[1]
        except:
            newAcc = ""
        sclNotes.append(Note(newLetter + newAcc))

    return sclNotes


def generateRN(note, qual):
    """
    Returns a dictionary of Roman Numerals and their
    Triads for some root note and quality. EX: CM, G#m, etc.
    Does not accept diminshed quality. RN I must be M or m.
    """
    newD = {}
    sclNotes = getScale(note, qual)

    q = []
    # Lists of chord qualities for each Roman Numeral type
    if qual == "M":
        q = ["M", "m", "m", "M", "M", "m", "dim"]
    elif qual == "m":
        q = ["m", "dim", "M", "m", "m", "M", "M"]
    else:
        raise "Not a valid chord progression RN type."

    for i in range(1, 8):
        # For each Roman Numeral, store a Triad
        newD[i] = Triad(str(sclNotes[i - 1]) + str(q[i - 1]))

    return newD


# Unused chords in music. Many use double flats or sharps.
unused = ["G#M", "A#M", "D#M", "Cbm", "Dbm", "Gbm", "FbM", "Fbm", "E#M", "E#m", "B#M", "B#m"]

qualities = ["M","m"]

chords = {}
# Build the entire chords dictionary, excluding unused keys that would have double sharps or flats
for note in notes:
    for qual in qualities:
        if (note + qual) in unused:
            continue
        else:
            chords[note + qual] = generateRN(Note(note), qual)

# Example entry: "CM":{1: CM, 2: Dm, 3: Em, 4: FM, 5: GM, 6: Am, 7: Bdim}

# The chords dictionary represents chords using Graph Theory.
# The chord string, like "CM", is the node, and the edges are the Roman Numerals,
# leading to the connected chords. This creates a directed graph.

# Since diminished chords cannot generate Roman Numerals, they are a dead end in the graph.


def dfsPath(stNode, endNode, visited=[], path=[]):
    """
    Returns the first path found from a start to end node
    using depth first search in the the chords graph.
    """
    if stNode == endNode:
        visited.append(stNode)
        path.append(endNode)
        return path

    if stNode in unused or "dim" in stNode:
        return path
    if stNode in visited or stNode in path:
        return path

    visited.append(stNode)

    path += [stNode]

    for rn in chords[stNode]:
        node = str(chords[stNode][rn])

        if node not in visited:
            path = dfsPath(node, endNode, visited, path)

            if endNode in path:
                return path
    return path


def bfsPath(stNode, endNode):
    """
    Returns the first path found from a start to end node
    using breadth first search in the the chords graph.
    """
    visited = []
    path = []
    queue = []

    queue.append([stNode])
    visited.append(stNode)

    while queue:
        path = queue.pop(0)

        node = path[-1]

        if node == endNode:
            return path

        if node in unused or "dim" in node:
            continue

        for rn in chords[node]:
            newNode = str(chords[node][rn])

            if newNode not in visited:
                visited.append(newNode)
                newPath = list(path)
                newPath.append(newNode)
                queue.append(newPath)
    return path
