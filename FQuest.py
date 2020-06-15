from tkinter import *
from tkinter.filedialog import *


class NpcConfig:

    def __init__(self, fileIO):
        self._name = "Name"
        self._id = 10
        self._worldServer = "WS00"
        self._luaScript = ""

        # Position relative to the WorldServer
        self._position_x = 0.0
        self._position_y = 0.0

        self._devNotes = ""
        self._npcRelations = {}

        self._isMerchant = False

        pass


def retrieveNpcConfigInformations():
    filename = askopenfilename(title="Open config file", filetypes=[('config files', '.xml'), ('all files', '.*')])
    fichier = open(filename, "r")
    content = fichier.read()
    fichier.close()


fenetre = Tk()
firstFrame = Frame(fenetre, borderwidth=2, relief=GROOVE)
firstFrame.pack(side=LEFT, padx=10, pady=10)

Label(firstFrame, text="Existing NPCs").pack(padx=10, pady=10)

# liste
list = Listbox(fenetre)
list.insert(1, "Python")
list.insert(2, "PHP")
list.insert(3, "jQuery")
list.insert(4, "CSS")
list.insert(5, "Javascript")
list.pack()

Button(firstFrame, text='Add NPC in list', command=retrieveNpcConfigInformations).pack()

secondFrame = Frame(fenetre, borderwidth=2, relief=GROOVE)
secondFrame.pack(side=RIGHT, padx=10, pady=10)

Label(secondFrame, text="Current NPC").pack(padx=10, pady=10)

fenetre.mainloop()
