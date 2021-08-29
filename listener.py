import pynput,time,threading
from chords import COMBINATIONS

DWELL_TIME = 0.5
CURRENT = set()
CONDITION = threading.Condition()

def on_press(key):
    if type(key) is pynput.keyboard.KeyCode:
        CURRENT.add(key.char)
    else:
        CURRENT.add(key)
    with CONDITION:
        CONDITION.notifyAll()

def on_release(key):
    try:
        if type(key) is pynput.keyboard.KeyCode:
            CURRENT.remove(key.char)
        else:
            CURRENT.remove(key)
    except KeyError:
        pass

listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

class InputGroup():
    def __init__(self, chords, index):
        next_chords = {}
        self.action = None
        for chord in chords:
            chord_length = len(chord[0])
            if index < chord_length:
                n = next_chords.get(chord[0][index], [])
                n.append(chord)
                next_chords[chord[0][index]] = n
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
        while elapsed_time + 0.01 < DWELL_TIME:
            with CONDITION:
                activated = CONDITION.wait(DWELL_TIME-elapsed_time)
            elapsed_time = time.clock_gettime(time.CLOCK_REALTIME)-start_time
            if activated:
                try:
                    key = tuple(sorted(hash(o) for o in CURRENT))
                    operation = self.nexts[key]
                    operation.launch()
                    return
                except KeyError:
                    pass
            else:
                if self.action != None:
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
