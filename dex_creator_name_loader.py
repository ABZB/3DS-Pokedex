from dex_creator_class import *
from utilities import *




def find_file_in_game_text(file_content, file_number):
    for line_number, text_line in enumerate(file_content):
        #dump uses header of this form
        if(text_line == 'Text File : ' + str(file_number) + '\n'):
           #whatever the line number is, next row is a bunch of tildes, and the following is the first text line
           return(line_number + 2)
        
    print('Could not find file number ', file_number) 
    return(0) 


def load_text_from_gametext(game_text_data, cur):
    
     text_array = []
     
     while True:
        try:
            if(game_text_data[cur] == '~~~~~~~~~~~~~~~\n'):
                return(text_array)
            else:
                text_array.append((game_text_data[cur].strip()).encode(encoding = 'UTF-16'))
        except:
            print('Reached end of file, something might be wrong. Will print current output just in case')
            for x in text_array:
                print(x)
            return(text_array)



def load_names_from_csv(dex_creation_data):
    
    with open(dex_creation_data.insertion_output_list, 'r') as name_source:
        csv_data = name_source.readlines()
    
    #makes a list with number of entries equal to the maximum personal index plus one (zeroth entry is blank/egg)
    dex_creation_data.pokemon_names = ['']*(max_of_column(csv_data, 1)+1)
    dex_creation_data.forme_names = ['']*(max_of_column(csv_data, 1)+1)

    for line in csv_data:
        if(line[1] != ''):
            dex_creation_data.pokemon_names[line[1]] = line[3].encode(encoding = 'UTF-16')
            if(line[4] != ''):
                dex_creation_data.forme_names[line[1]] = line[4].encode(encoding = 'UTF-16')

    return(dex_creation_data)


def load_names_from_files(dex_creation_data):
    
    with open(dex_creation_data.game_text_path, 'r') as name_source:
        game_text_data = name_source.readlines()
    
    #pokemon and forme names

    #load from CSV instead of gametext depending on option
    if(dex_creation_data.pokemon_name_loading_option == 'Forme Insertion CSV'):
        load_names_from_csv(dex_creation_data)
    else:
        #load species names from gametext
        dex_creation_data.pokemon_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('pokemon_names')))
        #if gen VII, have to use the hardcoded list
        if(game_text_data.game in {'XY', 'ORAS'}):
            dex_creation_data.forme_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('forme_names')))
        elif(game_text_data.game == 'SM'):
            dex_creation_data.forme_names = default_formes_SM
        else:
            dex_creation_data.forme_names = default_formes_USUM
            
    
    dex_creation_data.type_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('type_names')))

    dex_creation_data.ability_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('ability_names')))
    dex_creation_data.ability_descriptions = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('ability_descriptions')))

    dex_creation_data.dex_data = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('dex_data')))

    dex_creation_data.item_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('item_names')))
    dex_creation_data.item_descriptions = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('item_descriptions')))

    dex_creation_data.move_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('move_names')))
    dex_creation_data.move_descriptions = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('move_descriptions')))

    dex_creation_data.trainer_classes = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('trainer_classes')))
    dex_creation_data.trainer_names = load_text_from_gametext(game_text_data, find_file_in_game_text(game_text_data, dex_creation_data.gametext_file_number('trainer_names')))


        
#y.decode(encoding = 'UTF-16')
#

    return(dex_creation_data)    