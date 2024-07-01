from tkinter.filedialog import askopenfilename
from utilities import *
from dex_exporter_class import *



def load_database(exporter):
    with open(askopenfilename(title='Select Dumped Game Text File', defaultextension='.pkwd', filetypes= [('Pokemon World Database','.pkwd')]), 'rb') as hexdata:
        exporter.datasource = hexdata.read()
        return(exporter)

def export_pokemon_information(exporter):
    
    #check versions
    if(exporter.version_major != exporter.datasource[0] or exporter.version_minor != exporter.datasource[1]):
        print('Warning, version mismatch. Database was created with version ' + str(exporter[0]) + '.' + str(exporter[1]) + ', and this program is version ' + str(exporter.version_major) + '.' + str(exporter.version_minor))
    
    #grab max personal index
    exporter.max_personal_index = int((int_frm_bytes(exporter.datasource, int_frm_bytes(exporter.datasource, 2), 3) - int_frm_bytes(exporter.datasource, 2))/3 - 1)
    

    pokemon_data_table_pointer = exporter.datasource, int_frm_bytes(exporter.datasource, 2)
    next_pointer_address = pokemon_data_table_pointer + 3
    last_pointer = pokemon_data_table_pointer + 3*(exporter.max_personal_index - 1)
    
    type_name_pointer = int_frm_bytes(exporter.datasource, 6)

    #start from the pointer to Bulbasaur, go up by 3 bytes to next pointereach time we finish. read the data in the range from current pointer to before next pointer
    while True:
        temp = []
        for x in range(int_frm_bytes(exporter.datasource, pokemon_data_table_pointer, 3), int_frm_bytes(exporter.datasource, next_pointer_address, 3)):
            temp.append(x)
            
        exporter.max_nat_dex = max(exporter.max_nat_dex, int_frm_bytes(x[:2]))
        exporter.pokemon_data.append(temp)
        
        #next pointer becomes current pointer
        pokemon_data_table_pointer += next_pointer_address

        #increment to next pointer
        next_pointer_address += 3
        if(pokemon_data_table_pointer < last_pointer):
            next_pointer_address += 3
        elif(pokemon_data_table_pointer == last_pointer):
            next_pointer_address = type_name_pointer
        else:
            break


    
        
    
	    
    
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
