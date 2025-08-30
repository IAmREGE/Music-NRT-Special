from sys import stderr
from time import monotonic, sleep
import argparse

try:
    from colorama import Fore, Back, init
    init(autoreset=True)
    del init
except ImportError:
    class Fore:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        RESET = "\033[39m"
        LIGHTYELLOW_EX = "\033[93m"

    class Back:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"
        RESET = "\033[49m"
        LIGHTYELLOW_EX = "\033[103m"


FORE_COLOR_MAP = (Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
                  Fore.MAGENTA, Fore.CYAN, Fore.WHITE, "", Fore.RESET, "", "",
                  "", Fore.LIGHTYELLOW_EX)
BACK_COLOR_MAP = (Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE,
                  Back.MAGENTA, Back.CYAN, Back.WHITE, "", Back.RESET, "", "",
                  "", Back.LIGHTYELLOW_EX)


class FrameUnit:
    def __init__(self, char=" ", fore=9, back=9):
        self.char = char
        self.fore = fore
        self.back = back

    def copy(self):
        return type(self)(self.char, self.fore, self.back)


class Frame:
    WIDTH = 79
    HEIGHT = 24

    def __init__(self):
        self.units = [[FrameUnit() for _ in range(self.WIDTH)]
                      for _ in range(self.HEIGHT)]

    def fill_units(self, text, x=0, y=0, fore=None, back=None):
        if y >= self.HEIGHT:
            return None
        head_x = x
        for char in text:
            if char == "\n":
                y += 1
                if y >= self.HEIGHT:
                    return None
                x = head_x
            elif char == "\r":
                x = 0
            elif char == "\b":
                if x > 0:
                    x -= 1
            elif x < self.WIDTH:
                unit = self.units[y][x]
                unit.char = char
                if fore is not None:
                    unit.fore = fore
                if back is not None:
                    unit.back = back
                x += 1

    def fill_style(self, text, mapper, x=0, y=0):
        if y >= self.HEIGHT:
            return None
        head_x = x
        for char in text:
            if char == "\n":
                y += 1
                if y >= self.HEIGHT:
                    return None
                x = head_x
            elif char == "\r":
                x = 0
            elif char == "\b":
                if x > 0:
                    x -= 1
            elif x < self.WIDTH:
                if char in mapper:
                    unit = self.units[y][x]
                    style = mapper[char]
                    if style[0] is not None:
                        unit.fore = style[0]
                    if style[1] is not None:
                        unit.back = style[1]
                x += 1

    def get_string(self):
        last_fore = last_back = None
        prelis = []
        for line in self.units:
            if prelis:
                prelis.append("\r\n")
            for unit in line:
                if unit.fore != last_fore:
                    last_fore = unit.fore
                    prelis.append(FORE_COLOR_MAP[last_fore])
                if unit.back != last_back:
                    last_back = unit.back
                    prelis.append(BACK_COLOR_MAP[last_back])
                prelis.append(unit.char)
        return "".join(prelis)

    def copy(self):
        copied = type(self)()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                copied.units[y][x] = self.units[y][x].copy()
        return copied

FPS = 4.0

FRAME_STRS = []

FRAME_BASE = Frame()
FRAME_BASE.fill_units("Music", 2, 1, 1)
FRAME_BASE.fill_units("Vocal", 2, 3, 3)
FRAME_BASE.fill_units("Music", 2, 7, 2)

FRAME_INTRO = FRAME_BASE.copy()
FRAME_INTRO.fill_units("TITLE: Alphabet", 14, 18, 7)
FRAME_INTRO.fill_units("COMPOSER: Wolfgang Amadeus Mozart", 32, 18, 2)
FRAME_INTRO.fill_units("VOCAL: ", 14, 20, 5)
FRAME_INTRO.fill_units("Luo Tianyi", 21, 20, 6)
FRAME_INTRO.fill_units(", ", 31, 20, 5)
FRAME_INTRO.fill_units("Yuezheng Ling", 33, 20, 1)
FRAME_INTRO.fill_units(", ", 46, 20, 5)
FRAME_INTRO.fill_units("Shian", 48, 20, 13)
FRAME_INTRO.fill_units("PV: REGE", 57, 20, 4)
FRAME_INTRO_V1 = FRAME_INTRO.copy()
FRAME_INTRO_V2 = FRAME_INTRO.copy()
FRAME_INTRO_V3 = FRAME_INTRO.copy()
for k, v in (
    (FRAME_INTRO,    {"A": (None, 6), "B": (None, 1), "C": (None, 13)}),
    (FRAME_INTRO_V1, {"A": (None, 9), "B": (None, 1), "C": (None, 13)}),
    (FRAME_INTRO_V2, {"A": (None, 6), "B": (None, 9), "C": (None, 13)}),
    (FRAME_INTRO_V3, {"A": (None, 6), "B": (None, 1), "C": (None, 9)})
):
    k.fill_style("""\
   AAA     BBBBBBB       CCCCC
  AA AA    BB    BB    CCC   CC
 AA   AA   BB   BB    CC
AA     AA  BBBBBB     CC              AAA   AAA   AAAB    BBB
AAAAAAAAA  BB   BBB   CC             A     A   A  A   B  B   B
AA     AA  BB     BB  CC              AC   A   C  C   C  B   B
AA     AA  BB    BB    CCC   CC         C  C   C  C   C   BCCC
AA     AA  BBBBBBB       CCCCC       CCC    CCC   C   C      C
                                                         CCCC""", v, 9, 9)
MUSIC_HI_NOTES = (
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, 5, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, 3, 1, None, None, None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, 5, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, 3, 1, None, None, None,
    5, None, 5, None, 4, None, 4, None, 3, None, 3, None, 2, None, 2, None,
    5, None, 5, None, 4, None, 4, None, 3, None, 3, 4, 3, None, 2, None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, 5, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, 3, 1, None, None, None
)
MUSIC_LO_NOTES = (
    1, None, 8, None, 10, None, 8, None, 11, None, 8, None, 10, None, 8, None,
    9, None, 7, None, 8, None, 6, None, 4, None, 5, None, 1, None, None, None,
    1, None, 8, None, 10, None, 8, None, 11, None, 8, None, 10, None, 8, None,
    9, None, 7, None, 8, None, 6, None, 4, None, 5, None, 1, None, None, None,
    10, None, 5, None, 9, None, 5, None, 8, None, 5, None, 7, None, 5, None,
    10, None, 5, None, 9, None, 5, None, 8, None, 8, 9, 8, None, 7, None,
    1, None, 8, None, 10, None, 8, None, 11, None, 8, None, 10, None, 8, None,
    9, None, 7, None, 8, None, 6, None, 4, None, 5, None, 1, None, None, None,
)
VOCAL_PT1_NOTES = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, None, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, None, 1, None, None, None,
    5, None, 5, None, 4, None, None, None, 3, None, 3, None, 2,None,None,None,
    5, None, 5, None, 4, None, 4, None, 3, None, 3, None, 2, None, None, None,
    1, None, 1, None, 5, None, None, None, 6, None, 8, None, 5,None,None,None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, None, 1, None, None, None
)
VOCAL_PT2_NOTES = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, None, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, None, 1, None, None, None,
    5, None, 5, None, 4, None, 4, None, 3, None, 3, None, 2, None, None, None,
    5, None, 5, None, 4, None, 4, None, 3, None, 3, None, 2, None, None, None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, None, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, None, 1, None, None, None
)
VOCAL_PT3_NOTES = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, None, None,
    4, None, 4, None, 3, None, 3, None, 2, 2, 2, 2, 1, None, None, None,
    5, None, 5, None, 4, None, None, None, 3, None, 3, None, 2,None,None,None,
    5, None, 5, None, 4, None, None, None, 3, None, 3, None, 2,None,None,None,
    1, None, 1, None, 5, None, 5, None, 6, None, 6, None, 5, None, None, None,
    4, None, 4, None, 3, None, 3, None, 2, None, 2, None, 1, None, None, None
)
NOTE_TO_SAYING = ("ti", "do", "re", "mi", "fa", "sol", "la")
NOTE_TO_KEY = ("C3", "D3", "E3", "F3", "G3", "A3", "B3",
               "C4", "D4", "E4", "F4", "G4", "A4", "B4",
               "C5", "D5", "E5", "F5", "G5", "A5")
VOCAL_PT1_LYRICS = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, "A", None, "B", None, "C",
    None, "D", None, "E", None, "F", None, "G", None, None, None, "H", None,
    "I", None, "J", None, "K", None, "L", None, "M", None, "N", None, None,
    None, "O", None, "P", None, "Q", None, None, None, "R", None, "S", None,
    "T", None, None, None, "U", None, "V", None, "W", None, None, None, "X",
    None, "Y", None, "Z", None, None, None, "X", None, "Y", None, "Z", None,
    None, None, "Now", None, "you", None, "see", None, None, None, "I", None,
    "can", None, "say", None, "my", None, "A", None, "B", None, "C", None,
    None, None
)
VOCAL_PT2_LYRICS = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, "A", None, "B", None, "C",
    None, "D", None, "E", None, "F", None, "G", None, None, None, "H", None,
    "I", None, "J", None, "K", None, "L", None, "M", None, "N", None, None,
    None, "O", None, "P", None, "Q", None, "R", None, "S", None, "T", None,
    "U", None, None, None, "V", None, None, None, "W", None, None, None, "X",
    None, "Y", None, "Z", None, None, None, "Now", None, "you", None, "know",
    None, "your", None, "A", None, "B", None, "C", None, None, None, "E",
    None, "-very", None, "-bo", None, "-dy", None, "sing", None, "with", None,
    "me", None, None, None
)
VOCAL_PT3_LYRICS = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, "A", None, "B", None, "C",
    None, "D", None, "E", None, "F", None, "G", None, None, None, "H", None,
    "I", None, "J", None, "K", None, "L", "M", "N", "O", "P", None, None,
    None, "Q", None, "R", None, "S", None, None, None, "T", None, "U", None,
    "V", None, None, None, "W", None, None, None, "X", None, None, None, "Y",
    None, "and", None, "Z", None, None, None, "Now", None, "I", None, "know",
    None, "my", None, "A", None, "B", None, "C", None, None, None, "Next",
    None, "time", None, "won't", None, "you", None, "sing", None, "with",
    None, "me", None, None, None
)
VOCAL_PT4_1_LYRICS = (
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, "A", None, "B", None, "C",
    None, "D", None, "E", None, "F", None, "G", None, None, None, "H", None,
    "I", None, "J", None, "K", None, "L", "M", "N", "O", "P", None, None,
    None, "Q", None, "R", None, "S", None, None, None, "T", None, "U", None,
    "V", None, None, None, "W", None, None, None, "X", None, None, None, "Y",
    None, "and", None, "Z", None, None, None, "Now", None, "you", None,
    "know", None, "your", None, "A", None, "B", None, "C", None, None, None,
    "Next", None, "time", None, "would", None, "you", None, "sing", None,
    "with", None, "me", None, None, None
)
this_frame = FRAME_INTRO
note_x = 9
for sec in range(1, 9):
    for half in range(2):
        for quarter in range(2):
            this_frame = FRAME_INTRO
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1), note_x, 1,
                                          1)
                if this_lo_note is not None:
                    this_frame.fill_units(str((this_lo_note-1)%7+1), note_x, 7,
                                          2)
                    if this_lo_note > 7:
                        this_frame.fill_units(".", note_x, 6, 2)
                note_x += 2
            if sec == 3:
                if not quarter:
                    this_frame = FRAME_INTRO_V2 if half else FRAME_INTRO_V1
            elif sec == 4:
                if not half:
                    this_frame = FRAME_INTRO_V3
            elif sec == 7:
                if half:
                    this_frame.fill_style("""\
 2222222X
22     22
      22X
    222 X
  222   X
 22     X
22      X
222222222""", {"2": (None, 1), " ": (None, 9), "X": (None, 9)}, 20, 9)
                else:
                    this_frame.fill_style("""\
 3333333X
33     33
      33X
   3333 X
      33X
       33
33    33X
 333333 X""", {"3": (None, 6), " ": (None, 9), "X": (None, 9)}, 9, 9)
            elif sec == 8:
                if half:
                    this_frame.fill_style("""\
 BBB    AAA    CC  CC  CC
B   B  A   A   CC  CC  CC
B   B  A   C   CC  CC  CC
 BCCC  C   C   CC  CC  CC
    C   CCC             X
CCCC           CC  CC  CC""", {
    "A": (None, 6), "B": (None, 1), "C": (None, 13), " ": (None, 9),
    "X": (None, 9)
}, 46, 12)
                else:
                    this_frame.fill_style("""\
   11   X
 11 1   X
1   1   X
    1   X
    1   X
    1   X
    1   X
111111111""", {"1": (None, 13), " ": (None, 9), "X": (None, 9)}, 31, 9)
            this_frame.fill_units("{0}.{1}".format(sec, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT1_PH1 = FRAME_BASE.copy()
this_frame = FRAME_PT1_PH1
note_x = 9
for sec in range(9, 25):
    for half in range(2):
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT1_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT1_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1), note_x, 1,
                                          1)
                if this_vocal_note is not None:
                    this_frame.fill_units(str((this_vocal_note-1)%7+1), note_x,
                                          3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 6)
                if this_lo_note is not None:
                    this_frame.fill_units(str((this_lo_note-1)%7+1), note_x, 7,
                                          2)
                    if this_lo_note > 7:
                        this_frame.fill_units(".", note_x, 6, 2)
                note_x += 2 if this_vocal_lyrics is None else \
                    max(1, len(this_vocal_lyrics)) + 1
            this_frame.fill_units("{0}.{1}".format(sec, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT1_PH2 = FRAME_BASE.copy()
this_frame = FRAME_PT1_PH2
note_x = 9
for sec in range(25, 33):
    for half in range(2):
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT1_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT1_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1), note_x, 1,
                                          1)
                if this_vocal_note is not None:
                    this_frame.fill_units(str((this_vocal_note-1)%7+1), note_x,
                                          3, 3)
                    if this_vocal_note > 7:
                        this_frame.fill_units(".", note_x, 2, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 6)
                if this_lo_note is not None:
                    this_frame.fill_units(str((this_lo_note-1)%7+1), note_x, 7,
                                          2)
                    if this_lo_note > 7:
                        this_frame.fill_units(".", note_x, 6, 2)
                note_x += 2 if this_vocal_lyrics is None else \
                    max(1, len(this_vocal_lyrics)) + 1
            this_frame.fill_units("{0}.{1}".format(sec, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT2_BREAK = FRAME_BASE.copy()
FRAME_PT2_ANIMS = (
    ("Password: A|", 28, 12, 7, 0),
    ("*b|", 38, 12, 7, 0),
    ("*C|", 39, 12, 7, 0),
    ("*d|", 40, 12, 7, 0),
    ("*E|", 41, 12, 7, 0),
    ("*f|", 42, 12, 7, 0),
    ("*G|", 43, 12, 7, 0),
    ("*", 44, 12, 7, 0),
    ("*H|", 44, 12, 7, 0),
    ("*i|", 45, 12, 7, 0),
    ("*J|", 46, 12, 7, 0),
    ("*k|", 47, 12, 7, 0),
    ("*L|", 48, 12, 7, 0),
    ("*m|", 49, 12, 7, 0),
    ("*N|", 50, 12, 7, 0),
    ("Authentication passed.", 38, 12, 2, 7)
)
this_frame = FRAME_PT2_BREAK
note_x = 9
for sec in range(1, 9):
    for half in range(2):
        this_frame.fill_units(*FRAME_PT2_ANIMS[((sec-1)<<1)|half])
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_hi_note%7],
                                          note_x, 1, 1)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_lo_note%7],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_SAYING[this_hi_note%7]),
                              0 if this_lo_note is None
                              else len(NOTE_TO_SAYING[this_lo_note%7])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+32, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT2_PH1 = FRAME_BASE.copy()
this_frame = FRAME_PT2_PH1
note_x = 9
for sec in range(9, 17):
    for half in range(2):
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT2_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT2_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_hi_note%7],
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_vocal_note%7],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 1)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_lo_note%7],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_SAYING[this_hi_note%7]),
                              0 if this_vocal_note is None
                              else len(NOTE_TO_SAYING[this_vocal_note%7]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_SAYING[this_lo_note%7])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+32, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT2_PH2 = FRAME_BASE.copy()
this_frame = FRAME_PT2_PH2
note_x = 9
for sec in range(17, 25):
    for half in range(2):
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT2_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT2_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_hi_note%7],
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_vocal_note%7],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 1)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_lo_note%7],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_SAYING[this_hi_note%7]),
                              0 if this_vocal_note is None
                              else len(NOTE_TO_SAYING[this_vocal_note%7]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_SAYING[this_lo_note%7])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+32, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT2_PH3 = FRAME_BASE.copy()
this_frame = FRAME_PT2_PH3
note_x = 9
for sec in range(25, 33):
    for half in range(2):
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT2_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT2_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_hi_note%7],
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_vocal_note%7],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 1)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_lo_note%7],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_SAYING[this_hi_note%7]),
                              0 if this_vocal_note is None
                              else len(NOTE_TO_SAYING[this_vocal_note%7]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_SAYING[this_lo_note%7])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+32, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT3_BREAK = FRAME_BASE.copy()
this_frame = FRAME_PT3_BREAK
note_x = 9
for sec in range(1, 9):
    for half in range(2):
        for quarter in range(2):
            if half and not quarter:
                if sec == 1:
                    this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQ RST\nUVW XYZ",
                                          10, 12, 4)
                elif sec == 5:
                    this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
                    this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQRSTU\nV W XYZ",
                                          20, 12, 2)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_hi_note+13],
                                          note_x, 1, 1)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_KEY[this_hi_note+13]),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+64, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT3_PH1 = FRAME_BASE.copy()
FRAME_PT3_PH1_ANIMS = (
    ("A", 30, 12, 3), None,
    ("B", 31, 12, 3), ("|\n|\n|\n|", 28, 12, 7),
    ("C", 32, 12, 3), None,
    ("D", 33, 12, 3), None,
    ("E", 34, 12, 3), None,
    ("F", 36, 12, 3), None,
    ("G", 38, 12, 3), None, None, None,
    ("H", 30, 13, 3), None,
    ("I", 31, 13, 3), None,
    ("J", 32, 13, 3), None,
    ("K", 33, 13, 3), None,
    ("L", 34, 13, 3),
    ("M", 35, 13, 3),
    ("N", 36, 13, 3),
    ("O", 37, 13, 3),
    ("P", 38, 13, 3), None, None, None
)
this_frame = FRAME_PT3_PH1
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQ RST\nUVW XYZ", 10, 12, 4)
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQRSTU\nV W XYZ", 20, 12, 2)
note_x = 9
for sec in range(9, 17):
    for half in range(2):
        for quarter in range(2):
            anim = FRAME_PT3_PH1_ANIMS[((sec-9)<<2)|(half<<1)|quarter]
            if anim is not None:
                this_frame.fill_units(*anim)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT3_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT3_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_hi_note+13],
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_vocal_note+6],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 13)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_KEY[this_hi_note+13]),
                              0 if this_vocal_note is None
                              else len(NOTE_TO_KEY[this_vocal_note+6]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+64, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT3_PH2 = FRAME_BASE.copy()
FRAME_PT3_PH2_ANIMS = (
    ("Q", 30, 14, 3), None,
    ("R", 31, 14, 3), None,
    ("S", 32, 14, 3), None, None, None,
    ("T", 34, 14, 3), None,
    ("U", 36, 14, 3), None,
    ("V", 38, 14, 3), None, None, None,
    ("W", 30, 15, 3), None, None, None,
    ("X", 32, 15, 3), None, None, None,
    ("Y", 34, 15, 3), None, None, None,
    ("Z", 38, 15, 3), None, None, None
)
this_frame = FRAME_PT3_PH2
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQ RST\nUVW XYZ", 10, 12, 4)
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQRSTU\nV W XYZ", 20, 12, 2)
this_frame.fill_units("|\n|\n|\n|", 28, 12, 7)
this_frame.fill_units("ABCDE F G\nHIJKLMNOP", 30, 12, 3)
note_x = 9
for sec in range(17, 25):
    for half in range(2):
        for quarter in range(2):
            anim = FRAME_PT3_PH2_ANIMS[((sec-17)<<2)|(half<<1)|quarter]
            if anim is not None:
                this_frame.fill_units(*anim)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT3_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT3_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_hi_note+13],
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_vocal_note+6],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 13)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_KEY[this_hi_note+13]),
                              0 if this_vocal_note is None
                              else len(NOTE_TO_KEY[this_vocal_note+6]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+64, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT3_PH3 = FRAME_BASE.copy()
this_frame = FRAME_PT3_PH3
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQ RST\nUVW XYZ", 10, 12, 4)
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQRSTU\nV W XYZ", 20, 12, 2)
this_frame.fill_units("|\n|\n|\n|", 28, 12, 7)
this_frame.fill_units("ABCDE F G\nHIJKLMNOP\nQRS T U V\nW X Y   Z", 30, 12, 3)
note_x = 9
for sec in range(25, 33):
    for half in range(2):
        for quarter in range(2):
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT3_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT3_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_hi_note+13],
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_vocal_note+6],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 13)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None
                              else len(NOTE_TO_KEY[this_hi_note+13]),
                              0 if this_vocal_note is None
                              else len(NOTE_TO_KEY[this_vocal_note+6]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+64, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT3_BREAK = FRAME_BASE.copy()
this_frame = FRAME_PT3_BREAK
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQ RST\nUVW XYZ", 10, 12, 4)
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQRSTU\nV W XYZ", 20, 12, 2)
this_frame.fill_units("|\n|\n|\n|", 28, 12, 7)
this_frame.fill_units("ABCDE F G\nHIJKLMNOP\nQRS T U V\nW X Y   Z", 30, 12, 3)
note_x = 9
for sec in range(1, 9):
    for half in range(2):
        for quarter in range(2):
            if not quarter:
                if sec == 1:
                    if half:
                        this_frame.fill_units("you", 50, 14, 1)
                    else:
                        this_frame.fill_units("Are", 46, 14, 1)
                elif sec == 2:
                    if half:
                        this_frame.fill_units("dy?", 57, 14, 1)
                    else:
                        this_frame.fill_units("rea", 54, 14, 1)
                elif sec == 7:
                    if half:
                        this_frame.fill_units("'s", 49, 15, 1)
                    else:
                        this_frame.fill_units("Let", 46, 15, 1)
                elif sec == 8:
                    if not half:
                        this_frame.fill_units("START!", 52, 15, 1)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1),
                                          note_x, 1, 1)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None else 1,
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+96, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT4_PH1 = FRAME_BASE.copy()
FRAME_PT4_PH1_ANIMS = (
    ((" ", 10, 12, 9), (" ", 20, 12, 9), (" ", 30, 12, 9)), (),
    ((" ", 11, 12, 9), (" ", 21, 12, 9), (" ", 31, 12, 9)), (),
    ((" ", 12, 12, 9), (" ", 22, 12, 9), (" ", 32, 12, 9)), (),
    ((" ", 13, 12, 9), (" ", 23, 12, 9), (" ", 33, 12, 9)), (),
    ((" ", 14, 12, 9), (" ", 24, 12, 9), (" ", 34, 12, 9)), (),
    ((" ", 15, 12, 9), (" ", 25, 12, 9), (" ", 36, 12, 9)), (),
    ((" ", 16, 12, 9), (" ", 26, 12, 9), (" ", 38, 12, 9)), (), (), (),
    ((" ", 10, 13, 9), (" ", 20, 13, 9), (" ", 30, 13, 9)), (),
    ((" ", 11, 13, 9), (" ", 21, 13, 9), (" ", 31, 13, 9)), (),
    ((" ", 12, 13, 9), (" ", 22, 13, 9), (" ", 32, 13, 9)), (),
    ((" ", 13, 13, 9), (" ", 23, 13, 9), (" ", 33, 13, 9)), (),
    ((" ", 14, 13, 9), (" ", 24, 13, 9), (" ", 34, 13, 9)),
    ((" ", 15, 13, 9), (" ", 25, 13, 9), (" ", 35, 13, 9)),
    ((" ", 16, 13, 9), (" ", 26, 13, 9), (" ", 36, 13, 9)),
    ((" ", 10, 14, 9), (" ", 20, 14, 9), (" ", 37, 13, 9)),
    ((" ", 11, 14, 9), (" ", 21, 14, 9), (" ", 38, 13, 9)), (), (), ()
)
this_frame = FRAME_PT4_PH1
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQ RST\nUVW XYZ", 10, 12, 4)
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("ABCDEFG\nHIJKLMN\nOPQRSTU\nV W XYZ", 20, 12, 2)
this_frame.fill_units("|\n|\n|\n|", 28, 12, 7)
this_frame.fill_units("ABCDE F G\nHIJKLMNOP\nQRS T U V\nW X Y   Z", 30, 12, 3)
note_x = 9
for sec in range(9, 17):
    for half in range(2):
        for quarter in range(2):
            for anim in FRAME_PT4_PH1_ANIMS[((sec-9)<<2)|(half<<1)|quarter]:
                this_frame.fill_units(*anim)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT3_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT3_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1),
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_vocal_note%7],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 6)
                    this_frame.fill_units(this_vocal_lyrics, note_x, 5, 13)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None else 1,
                              0 if this_vocal_note is None
                              else len(NOTE_TO_SAYING[this_vocal_note%7]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+96, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT4_PH2 = FRAME_BASE.copy()
FRAME_PT4_PH2_ANIMS = (
    (("    ", 10, 14, 9), ("   ", 20, 14, 9), (" ",    30, 14, 9)), (),
    ((" ",    14, 14, 9), (" ",   23, 14, 9), (" ",    31, 14, 9)), (),
    ((" ",    15, 14, 9), (" ",   24, 14, 9), ("  ",   32, 14, 9)), (), (), (),
    ((" ",    16, 14, 9), (" ",   25, 14, 9), ("  ",   34, 14, 9)), (),
    ((" ",    10, 15, 9), (" ",   26, 14, 9), ("  ",   36, 14, 9)), (),
    ((" ",    11, 15, 9), ("  ",  20, 15, 9), (" ",    38, 14, 9)), (), (), (),
    (("  ",   12, 15, 9), ("  ",  22, 15, 9), ("  ",   30, 15, 9)), (), (), (),
    ((" ",    14, 15, 9), (" ",   24, 15, 9), ("  ",   32, 15, 9)), (), (), (),
    ((" ",    15, 15, 9), (" ",   25, 15, 9), ("    ", 34, 15, 9)), (), (), (),
    ((" ",    16, 15, 9), (" ",   26, 15, 9), (" ",    38, 15, 9)), (), (), ()
)
this_frame = FRAME_PT4_PH2
this_frame.fill_units("  Q RST\nUVW XYZ", 10, 14, 4)
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("  QRSTU\nV W XYZ", 20, 14, 2)
this_frame.fill_units("|\n|\n|\n|", 28, 12, 7)
this_frame.fill_units("QRS T U V\nW X Y   Z", 30, 14, 3)
note_x = 9
for sec in range(17, 25):
    for half in range(2):
        for quarter in range(2):
            for anim in FRAME_PT4_PH2_ANIMS[((sec-17)<<2)|(half<<1)|quarter]:
                this_frame.fill_units(*anim)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT3_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics = VOCAL_PT3_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1),
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_vocal_note%7],
                                          note_x, 3, 3)
                if this_vocal_lyrics is not None:
                    this_frame.fill_units(this_vocal_lyrics, note_x, 4, 6)
                    this_frame.fill_units(this_vocal_lyrics, note_x, 5, 13)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None else 1,
                              0 if this_vocal_note is None
                              else len(NOTE_TO_SAYING[this_vocal_note%7]),
                              0 if this_vocal_lyrics is None
                              else len(this_vocal_lyrics),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+96, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
FRAME_PT4_PH3 = FRAME_BASE.copy()
this_frame = FRAME_PT4_PH3
this_frame.fill_units("|\n|\n|\n|", 18, 12, 7)
this_frame.fill_units("|\n|\n|\n|", 28, 12, 7)
note_x = 9
for sec in range(25, 33):
    for half in range(2):
        for quarter in range(2):
            if sec == 32 and half and not quarter:
                this_frame.fill_units("FULL COMBO!", 18, 13, 4, 7)
            this_hi_note = MUSIC_HI_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_note = VOCAL_PT3_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics_1 = \
                VOCAL_PT4_1_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_vocal_lyrics_2 = \
                VOCAL_PT3_LYRICS[((sec-1)<<2)|(half<<1)|quarter]
            this_lo_note = MUSIC_LO_NOTES[((sec-1)<<2)|(half<<1)|quarter]
            if this_hi_note is not None or this_vocal_note is not None or \
                this_vocal_lyrics is not None or this_lo_note is not None:
                if this_hi_note is not None:
                    this_frame.fill_units(str((this_hi_note-1)%7+1),
                                          note_x, 1, 1)
                if this_vocal_note is not None:
                    this_frame.fill_units(NOTE_TO_SAYING[this_vocal_note%7],
                                          note_x, 3, 3)
                if this_vocal_lyrics_1 is not None:
                    this_frame.fill_units(this_vocal_lyrics_1, note_x, 4, 1)
                if this_vocal_lyrics_2 is not None:
                    this_frame.fill_units(this_vocal_lyrics_2, note_x, 5, 13)
                if this_lo_note is not None:
                    this_frame.fill_units(NOTE_TO_KEY[this_lo_note-1],
                                          note_x, 7, 2)
                note_x += max(0 if this_hi_note is None else 1,
                              0 if this_vocal_note is None
                              else len(NOTE_TO_SAYING[this_vocal_note%7]),
                              0 if this_vocal_lyrics_1 is None
                              else len(this_vocal_lyrics_1),
                              0 if this_vocal_lyrics_2 is None
                              else len(this_vocal_lyrics_2),
                              0 if this_lo_note is None
                              else len(NOTE_TO_KEY[this_lo_note-1])) + 1
            this_frame.fill_units("{0}.{1}".format(sec+96, half+1).rjust(5),
                                  72, 22, 1)
            FRAME_STRS.append(this_frame.get_string())
this_frame.fill_units("Fine.", 72, 22, 1)
FRAME_STRS.append(this_frame.get_string())

parser = argparse.ArgumentParser(
    prog="PV of Alphabet",
    description="This program outputs the frames of the PV of the song."
)
parser.add_argument(
    "-s", "--skip-frames", help="Skip foremost N frames", type=int
)
parser.add_argument(
    "-f", "--fps", help="Override the FPS (default: {0})".format(FPS),
    type=float
)
parser.add_argument(
    "-V", "--version", help="Show version info of this program",
    action="store_true"
)

args = parser.parse_args()

if args.version:
    print("""\
PV of Alphabet
Program: REGE (GitHub: IAmREGE  bilibili: 523423693)""")
    from sys import exit
    exit(0)

if args.skip_frames:
    del FRAME_STRS[:args.skip_frames]

SPF = 1. / (FPS if args.fps is None else args.fps)
start_time = monotonic()
count = 0
try:
    for count, body in enumerate(FRAME_STRS, start=1):
        print("\033[H", end=body, flush=True)
        while monotonic() - start_time < SPF * count:
            sleep(0.001)
except KeyboardInterrupt:
    print("1 frame presented" if count == 1
          else "{0} frames presented".format(count), file=stderr)