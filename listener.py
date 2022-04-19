import pynput,time,threading
from enum import IntEnum
from chords import COMBINATIONS

DWELL_TIME = 0.6
CURRENT = dict()
CONDITION = threading.Condition()

def key_number(key):
    if type(key) is pynput.keyboard.KeyCode:
        return hash(key.char)
    else:
        return hash(key.value)

def add_key(key):
    n = key_number(key)
    CURRENT.setdefault(n, 0)
    CURRENT[n]+=1

def on_press(key):
    add_key(key)
    with CONDITION:
        CONDITION.notify_all()

def on_release(key):
    n = key_number(key)
    if n in CURRENT:
        v = CURRENT[n]-1
        if v <= 0:
            del CURRENT[n]
        else:
            CURRENT[n] = v

def key_tuple(keys):
    return tuple(sorted(key_number(key) for key in keys))

listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

class InputGroup():
    def __init__(self, chords, index):
        next_chords = {}
        self.action = None
        for chord in chords:
            chord_length = len(chord[0])
            if index < chord_length:
                keys = key_tuple(chord[0][index])
                n = next_chords.get(keys, [])
                n.append(chord)
                next_chords[keys] = n
            else:
                self.action = chord[1]
        self.nexts = {}
        for combo,chords in next_chords.items():
            self.nexts[combo] = InputGroup(chords, index+1)

    def launch(self):
        if len(self.nexts) == 0 and self.action != None:
            self.action()
            return
        elapsed_time = 0.0
        start_time = time.clock_gettime(time.CLOCK_REALTIME)
        hit_anything = False
        while elapsed_time + 0.01 < DWELL_TIME:
            with CONDITION:
                activated = CONDITION.wait(DWELL_TIME-elapsed_time)
            elapsed_time = time.clock_gettime(time.CLOCK_REALTIME)-start_time
            if activated:
                hit_anything = True
                try:
                    key = tuple(sorted(CURRENT))
                    operation = self.nexts[key]
                    return operation.launch()
                except KeyError:
                    pass
            else:
                if self.action != None and not hit_anything:
                    self.action()
                return

MAIN_GROUP=InputGroup(COMBINATIONS, 0)

while True:
    if len(CURRENT) == 0:
        with CONDITION:
            CONDITION.wait()
    else:
        try:
            MAIN_GROUP.launch()
        except KeyError:
            time.sleep(0.2)
