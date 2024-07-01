from tkinter import *
from tkinter.filedialog import askopenfilename
from utilities import *
from dex_exporter_class import *



def load_database():
    with open(askopenfilename(title='Select Dumped Game Text File', defaultextension='.pkwd', filetypes= [('Pokemon World Database','.db')]), 'b') as hexdata:
        exporter.datasource = hexdata.read()
        return(exporter)

def export_pokemon_information(exporter):
    
    #check versions
    if(exporter.version_major != exporter[0] or exporter.version_minor != exporter[1]):
        print('Warning, version mismatch. Database was created with version ' + str(exporter[0]) + '.' + str(exporter[1]) + ', and this program is version ' + str(exporter.version_major) + '.' + str(exporter.version_minor))
    
    #grab max personal index
    exporter.max_personal_index = int((int_frm_bytes(exporter.datasource, int_frm_bytes(exporter.datasource, 2), 3) - int_frm_bytes(exporter.datasource, 2))/3 - 1)
    

    #start from the pointer to Bulbasaur, go up by 3 bytes to next pointereach time we finish
    for x in range((int_frm_bytes(exporter.datasource, int_frm_bytes(exporter.datasource, 2), 3) - int_frm_bytes(exporter.datasource, 2)), exporter.max_personal_index, 3):
        


    

    exporter.max_nat_dex = 0
    exporter.max_personal_index = 0
	    
    exporter.pokemon_data
    exporter.move_data


    #name array variables
    exporter.pokemon_names = []
    exporter.forme_names = [] 
        
    exporter.type_names = []
        
    exporter.ability_names = []
    exporter.ability_descriptions = []
        
    exporter.dex_data = []
        
    exporter.item_names = []
    exporter.item_descriptions = []
        
    exporter.move_names = []
    exporter.move_descriptions = []
        
    exporter.trainer_classes = []
    exporter.trainer_names = []




exporter = Dex_exportation_thing()

root = Tk()
root.title('Pokedex Exporter V.' + str(exporter.version_major) + '.' + str(exporter.version_minor))

for x in range(2):
    root.columnconfigure(x, weight = 1)
for x in range(2):
    root.rowconfigure(x, weight = 1)

#load/save config
cfg_load = Button(root, text = 'Load Pokedex Database', command = lambda: load_database(), height = 2, width = 22, pady = 5, padx = 7)
cfg_load.grid(row = 0, column = 0, sticky="ew")


cfg_save = Button(root, text = 'Export Pokemon Information', command = export_pokemon_information(exporter), height = 2, width = 22, pady = 5, padx = 7)
cfg_save.grid(row = 0, column = 1, sticky="ew")

root.mainloop()