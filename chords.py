from pynput.keyboard import Key,KeyCode,Controller
import unicodedata
import os

def open_app(argument):
    return lambda: os.system(argument + " &")

def run_many(*args):
    def result():
        for fun in args:
            fun()
    return result

def open_and_switch_desktop(argument, desktop):
    form1 = open_app(argument)
    form2 = run("qdbus org.kde.KWin /KWin setCurrentDesktop "+str(desktop))
    return run_many(form1, form2)

def run(argument):
    return lambda: os.system(argument)

def make_key(arguments):
    return arguments

def combination(*args):
    return [make_key(k) for k in args]

def yakuake():
    keyboard = Controller()
    keyboard.press(Key.f12)
    keyboard.release(Key.f12)

COMBINATIONS = [
    (combination([Key.cmd, Key.scroll_lock],[Key.cmd, Key.f6]), open_app("kronometer")),
    (combination([Key.cmd, Key.f6]), open_app("dolphin")),
    (combination([Key.cmd, Key.f11],[Key.cmd, Key.f11]), open_app("marble")),
    (combination([Key.cmd, Key.f11]), open_app("krunner")),
    (combination([Key.cmd, Key.f12]), open_app("konsole --workdir /home/shka/ -e ipython")),
    (combination([Key.cmd, Key.f12], [Key.cmd, Key.f12]), open_app("konsole --workdir /home/shka/ -e rlwrap sbcl --noinform --userinit /home/shka/.shclrc")),
    (combination([Key.cmd, Key.scroll_lock]), open_app("konsole --workdir=/home/shka/")),
    (combination([Key.cmd, Key.scroll_lock], [Key.scroll_lock, Key.cmd]), open_app("yakuake")),
    (combination([Key.cmd, Key.scroll_lock], [Key.cmd, Key.f7]), open_app("konsole --workdir=/home/shka/Repozytoria/")),
    (combination([Key.cmd, Key.scroll_lock], [Key.cmd, Key.f7], [Key.cmd, Key.f7]), open_app("konsole --workdir=/home/shka/quicklisp/local-projects/")),
    (combination([Key.cmd, Key.scroll_lock], [Key.cmd, Key.f10]), open_app("konsole --workdir=/home/shka/Pobrane/")),
    (combination([Key.cmd, Key.f11], [Key.cmd, Key.f7]), open_and_switch_desktop("firefox google.pl/maps/preview", 1)),
    (combination([Key.cmd, Key.f7]), open_and_switch_desktop("firefox --new-tab --url about:newtab", 1)),
    (combination([Key.cmd, Key.f7], [Key.cmd, Key.f2]), open_and_switch_desktop("firefox youtube.com", 1)),
    (combination([Key.cmd, Key.f7], [Key.cmd, Key.f3]), open_and_switch_desktop("firefox old.reddit.com/", 1)),
    (combination([Key.cmd, Key.f7], [Key.cmd, Key.f3], [Key.cmd, Key.f3]), open_and_switch_desktop("firefox old.reddit.com/r/Polska/", 1)),
    (combination([Key.cmd, Key.f7], [Key.cmd, Key.f3], [Key.cmd, Key.f2]), open_and_switch_desktop("firefox old.reddit.com/r/worldnews/", 1)),
    (combination([Key.cmd, Key.f7], [Key.cmd, Key.f6]), open_and_switch_desktop("firefox github.com", 1)),
    (combination([Key.cmd, Key.f7], [Key.cmd, Key.f7]), open_app("zeal")),
    (combination([Key.cmd, Key.f8]), open_app("ksysguard")),
    (combination([Key.cmd, Key.f8], [Key.cmd, Key.f8]), open_app("konsole -e htop")),
    (combination([Key.cmd, Key.f10]), open_app("chromium")),
    (combination([Key.cmd, Key.f10], [Key.cmd, Key.f10]), open_app("chromium --app=https://discord.com/")),
    (combination([Key.cmd, Key.f10], [Key.cmd, Key.f10], [Key.cmd, Key.f10]), open_app("chromium --app=https://facebook.com/")),
    (combination([Key.cmd, Key.f2]), open_app("kwrite")),
    (combination([Key.cmd, Key.f3]), open_app("spectacle")),
    (combination([Key.cmd, Key.f4]), open_app("systemsettings5")),
    (combination([Key.cmd, Key.f3], [Key.cmd, Key.f3]), open_app("spectacle -u")),
    (combination([Key.cmd, Key.f3], [Key.cmd, Key.f3], [Key.cmd, Key.f3]), open_app("spectacle -r")),
    (combination([Key.cmd, Key.pause], [Key.cmd, Key.f2]), open_app("soulseekqt")),
    (combination([Key.cmd, Key.pause], [Key.cmd, Key.pause]), open_app("ktorrent")),
    (combination([Key.cmd, Key.pause]), open_app("firedm")),
    (combination([Key.cmd, Key.f5]), open_app("kolourpaint")),
    (combination([Key.cmd, Key.f5], [Key.cmd, Key.f5]), open_app("gimp")),
    (combination([Key.cmd, Key.f5], [Key.cmd, Key.f5], [Key.cmd, Key.f5]), open_app("inkscape")),
    (combination([Key.cmd, Key.f2], [Key.cmd, Key.f2]), open_app("emacsclient -c -a 'emacs'")),
    (combination([Key.cmd, Key.f2], [Key.cmd, Key.f2], [Key.cmd, Key.f7]), open_app("emacsclient -c -a 'emacs' '/home/shka/Repozytoria/'")),
    (combination([Key.cmd, Key.f2], [Key.cmd, Key.f2], [Key.cmd, Key.f7], [Key.cmd, Key.f7]), open_app("emacsclient -c -a 'emacs' '/home/shka/quicklisp/local-projects/'")),
    (combination([Key.cmd, Key.f2], [Key.cmd, Key.f2], [Key.cmd, Key.f2]), open_app("okteta")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f10]), open_app("dolphin /home/shka/Pobrane/")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f3]), open_app("dolphin /home/shka/Wideo/")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f7]), open_app("dolphin /home/shka/Repozytoria/")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f7], [Key.cmd, Key.f7]), open_app("dolphin /home/shka/quicklisp/local-projects/")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f2]), open_app("dolphin /home/shka/Muzyka/")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f6], [Key.cmd, Key.f10]), open_app("krusader --left=/home/shka/Pobrane/ --right=/home/shka/")),
    (combination([Key.cmd, Key.f6], [Key.cmd, Key.f6]), open_app("krusader --left=/home/shka/ --right=/home/shka/"))
]
