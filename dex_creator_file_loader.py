from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from dex_creator_class import *

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
        elif(dex_creation_data.pokemon_name_loading_option == 'User Text List'):
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
    
def save_game_cfg(dex_creation_data):
 
    cfg_path = asksaveasfilename(title='Select location to save cfg file', defaultextension='.cfg',filetypes= [('config','.cfg')])

    
    try:
        with open(cfg_path, "w") as cfg:
            cfg.write(dex_creation_data.rom_folder_path + '\n')
            cfg.write(dex_creation_data.game + '\n')
            cfg.write(dex_creation_data.game_text_path + '\n')
            cfg.write(dex_creation_data.pokemon_name_loading_option + '\n')
            
            if(dex_creation_data.pokemon_name_loading_option == 'Forme Insertion CSV'):
                cfg.write(dex_creation_data.insertion_output_list + '\n')
            elif(dex_creation_data.pokemon_name_loading_option == 'User Text List'):
                cfg.write(dex_creation_data.text_file_name_list + '\n')
            else:
                cfg.write('\n')

            if(dex_creation_data.game in {'XY', 'ORAS'}):
                cfg.write(dex_creation_data.extracted_egg_moves_folder_path)

        print('Config file saved to ' + cfg_path)
    except:
        print("No file selected")