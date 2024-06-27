from tkinter import *
from dex_creator_file_loader import *
from dex_creator_class import *


def create_pokedex_database(dex_creation_data):
    print('All good so far I hope')








def set_checklists(gameinput, textoptioninput):
    games_temp.set(gameinput)
    name_text_options_temp.set(textoptioninput)

root = Tk()
root.title('Pokedex Builder V.1.0')
root.geometry('528x228')

dex_creation_data = Dex_creator()




#load/save config
cfg_load = Button(root, text = 'Load CFG', command = lambda: [load_dex_creator_cfg(dex_creation_data), set_checklists(dex_creation_data.game, dex_creation_data.game_text_path)], height = 2, width = 22, pady = 5, padx = 7)
cfg_load.grid(row = 0, column = 0, sticky="nsew")


cfg_save = Button(root, text = 'Save CFG', command = lambda: save_cfg(dex_creation_data, games_temp.get()), height = 2, width = 22, pady = 5, padx = 7)
cfg_save.grid(row = 0, column = 2, sticky="nsew")


#select game
games = ["XY", "ORAS", "SM", "USUM"]

games_temp = StringVar(root)
games_temp.set("Game")
game_select = OptionMenu(root, games_temp, *games)
game_select.grid(row = 2, column = 0, sticky="nsew")

#select game

   #     if(dex_creation_data.pokemon_name_loading_option == ''):
    #        dex_creation_data.insertion_output_list = cfg_array[4]
     #   elif(dex_creation_data.pokemon_name_loading_option == ''):


name_text_options = ['Forme Insertion CSV', 'User Text File','Default']

name_text_options_temp = StringVar(root)
name_text_options_temp.set("Source For Names")
name_text_options_select = OptionMenu(root, name_text_options_temp, *name_text_options)
name_text_options_select.grid(row = 2, column = 2, sticky="nsew")


#Grab extracted ROM folder path, this tells us where most of the stuff is
rom_folder_path_load = Button(root, text = 'Extracted ROM Folder', command = lambda: select_top_folder(dex_creation_data), height = 2, width = 22, pady = 5, padx = 7)
rom_folder_path_load.grid(row = 3, column = 0, sticky="nsew")

#Grab dumped game text file
game_text_file_load = Button(root, text = 'Dumped Game Text', command = lambda: select_game_text_file(dex_creation_data), height = 2, width = 22, pady = 5, padx = 7)
game_text_file_load.grid(row = 3, column = 2, sticky="nsew")


#Grab extracted ROM folder path, this tells us where most of the stuff is
name_source_folder_path_load = Button(root, text = 'Name Source', command = lambda: select_name_source_file(dex_creation_data, name_text_options_temp.get()), height = 2, width = 22, pady = 5, padx = 7)
name_source_folder_path_load.grid(row = 4, column = 0, sticky="nsew")

#Grab extracted Egg move folder in gen VI
extracted_egg_folder_load = Button(root, text = 'Extracted Egg Move Folder', command = lambda: select_egg_source_folder(dex_creation_data, games_temp.get()), height = 2, width = 22, pady = 5, padx = 7)
extracted_egg_folder_load.grid(row = 4, column = 2, sticky="nsew")




#Run Insertion
execute_button = Button(root, text = 'Create Pokedex', command = lambda: create_pokedex_database(dex_creation_data), height = 2, width = 22, pady = 5, padx = 7)
execute_button.grid(row = 6, column = 1, sticky="nsew")


#print("help")
root.mainloop()