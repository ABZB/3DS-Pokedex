from tkinter import *
from tkinter.filedialog import askopenfilename
from utilities import *
from dex_exporter_class import *
from dex_exporter_functions import *


exporter = Dex_exportation_thing()

root = Tk()
root.title('Pokedex Exporter V.' + str(exporter.version_major) + '.' + str(exporter.version_minor))

for x in range(2):
    root.columnconfigure(x, weight = 1)
for x in range(2):
    root.rowconfigure(x, weight = 1)

#load/save config
cfg_load = Button(root, text = 'Load Pokedex Database', command = lambda: load_database(exporter), height = 2, width = 22, pady = 5, padx = 7)
cfg_load.grid(row = 0, column = 0, sticky="ew")


cfg_save = Button(root, text = 'Export Pokemon Information', command = lambda: export_pokemon_information(exporter), height = 2, width = 22, pady = 5, padx = 7)
cfg_save.grid(row = 0, column = 1, sticky="ew")



root.mainloop()