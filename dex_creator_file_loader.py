from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from dex_creator_class import *


def select_top_folder(dex_creation_data):
    
    dex_creation_data.rom_folder_path = askdirectory(title='Select Extracted ROM Folder')
    return(dex_creation_data)

def select_name_source_file(dex_creation_data, name_text_options_temp):
    
    dex_creation_data.pokemon_name_loading_option = name_text_options_temp
    if(name_text_options_temp == 'Forme Insertion CSV'):
        dex_creation_data.insertion_output_list = askopenfilename(title='Select CSV output from Forme Insertion Tool', defaultextension='.csv')
    elif(name_text_options_temp == 'User Text File'):
        dex_creation_data.text_file_name_list = askopenfilename(title='Select Text File where each line has that Personal File index Forme name', defaultextension='.csv')
    else:
        print('Default option is selected, no file to load')
        #set to default to avoid edge cases
        dex_creation_data.pokemon_name_loading_option = 'Default'
    return(dex_creation_data)


def select_game_text_file(dex_creation_data):
    
    dex_creation_data.game_text_path = askopenfilename(title='Select Dumped Game Text File', defaultextension='.txt')
    return(dex_creation_data)

def select_egg_source_folder(dex_creation_data, game_temp = ''):
 
    if(not(game_temp in{'', 'Game'})):
        dex_creation_data.game = game_temp
    else:
        print('Please select Game')
        return
    
    if(dex_creation_data.game in {'SM', 'USUM'}):
        print('This is not used for Generation VII games')
        return
    elif(dex_creation_data.game == 'XY'):
        garc_path_name = 'a/2/1/3'
    elif(dex_creation_data.game == 'ORAS'):
        garc_path_name = 'a/1/9/0'
    else:
        print('Error, improper game selected: ' + str(dex_creation_data.game))
        return

    try:
        dex_creation_data.extracted_egg_moves_folder_path = askdirectory(title='Select extracted Egg Move Folder (from GARC ' + garc_path_name + ')')
        return(dex_creation_data)
    except:
        print('Was unable to load your selection, returning to main menu')
        return(dex_creation_data)



def load_dex_creator_cfg(dex_creation_data):
    
    cfg_path = askopenfilename(title='Select cfg file', defaultextension='.cfg',filetypes= [('config','.cfg')])
    
    cfg_desc = ["ROM Folder Path", "Game", "Dumped Game Text Path", "Pokemon Forme Name Loaded From", 'At', "Extracted Egg Move Folder Path"]

    with open(cfg_path, "r") as cfg:
        cfg_array = [line.rstrip() for line in cfg]
    try:
        dex_creation_data.rom_folder_path = cfg_array[0]
        dex_creation_data.game = cfg_array[1]
        dex_creation_data.game_text_path = cfg_array[2]
        dex_creation_data.pokemon_name_loading_option = cfg_array[3]
        
        if(dex_creation_data.pokemon_name_loading_option == 'Forme Insertion CSV'):
            dex_creation_data.insertion_output_list = cfg_array[4]
        elif(dex_creation_data.pokemon_name_loading_option == 'User Text File'):
            dex_creation_data.text_file_name_list = cfg_array[4]
            
        if(dex_creation_data.game in {'XY', 'ORAS'}):
            dex_creation_data.extracted_egg_moves_folder_path = cfg_array[5]
        
    except:
        print('Config file missing lines, loaded what was there')
    

    try:
        print('Data loaded as follows:')
        for x in range(len(cfg_desc)):
            if(cfg_desc[x] != '' and (dex_creation_data.game in {'XY', 'ORAS'} or x != 5)):
                print(cfg_desc[x] + ': ' + str(cfg_array[x]))
    except:
        print('Missing lines from config')
    print('\n')

    return(dex_creation_data)
    
def save_cfg(dex_creation_data, game_temp = ''):
 
    cfg_path = asksaveasfilename(title='Select location to save cfg file', defaultextension='.cfg',filetypes= [('config','.cfg')])

    if(game_temp != ''):
        dex_creation_data.game = game_temp

    
    try:
        with open(cfg_path, "w") as cfg:
            cfg.write(dex_creation_data.rom_folder_path + '\n')
            cfg.write(dex_creation_data.game + '\n')
            cfg.write(dex_creation_data.game_text_path + '\n')
            cfg.write(dex_creation_data.pokemon_name_loading_option + '\n')
            
            if(dex_creation_data.pokemon_name_loading_option == 'Forme Insertion CSV'):
                cfg.write(dex_creation_data.insertion_output_list + '\n')
            elif(dex_creation_data.pokemon_name_loading_option == 'User Text File'):
                cfg.write(dex_creation_data.text_file_name_list + '\n')
            else:
                cfg.write('\n')

            if(dex_creation_data.game in {'XY', 'ORAS'}):
                cfg.write(dex_creation_data.extracted_egg_moves_folder_path)

        print('Config file saved to ' + cfg_path)
    except:
        print("No file selected")