from tkinter.filedialog import askopenfilename
from utilities import *
from dex_exporter_class import *



def load_database(exporter):
    with open(askopenfilename(title='Select Dumped Game Text File', defaultextension='.pkwd', filetypes= [('Pokemon World Database','.pkwd')]), 'rb') as hexdata:
        exporter.datasource = hexdata.read()
        return(exporter)



def convert_text_from_binary(binary_text_array):
    #first create an array of the individual strings
    string_array = []
    cur = 0
    temp_string_array = []
    file_length = len(binary_text_array)
    
    while True:
        #reached end of text
        if(cur + 3 >= len(file_length)):
            break
        #locate terminator
        elif(binary_text_array[cur + 0] == binary_text_array[cur + 1] == binary_text_array[cur + 2] == binary_text_array[cur + 3] == 0):
            #write the integers converted to bytes converted back to text to the list of text
            string_array.append(bytes(temp_string_array).decode(encoding = 'utf-16'))
            
            #reset the temp string
            temp_string_array = []
        else:
            temp_string_array.append(binary_text_array[cur])
            
    return(string_array)

def extract_fixed_width_binary(binary_array, blocksize):
    #first create an array of the individual strings
    outarray = []
    block_count = int(len(binary_array)/blocksize)
    
    for block_number in range(block_count):
        start = block_number*blocksize
        outarray.append(binary_array[start : start + blocksize])
            
    return(outarray)


def load_pokemon_information(exporter):
    
    #check versions
    if(exporter.version_major != exporter.datasource[0] or exporter.version_minor != exporter.datasource[1]):
        print('Warning, version mismatch. Database was created with version ' + str(exporter[0]) + '.' + str(exporter[1]) + ', and this program is version ' + str(exporter.version_major) + '.' + str(exporter.version_minor))
    
    #grab max personal index
    exporter.max_personal_index = int((int_frm_bytes(exporter.datasource, int_frm_bytes(exporter.datasource, 2), 3) - int_frm_bytes(exporter.datasource, 2))/3 - 1)
    

    pokemon_data_table_pointer = exporter.datasource, int_frm_bytes(exporter.datasource, 2)
    next_pointer_address = pokemon_data_table_pointer + 3
    last_pointer = pokemon_data_table_pointer + 3*(exporter.max_personal_index - 1)
    
    text_pointer = int_frm_bytes(exporter.datasource, 6)

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
            next_pointer_address = text_pointer
        else:
            break


    segment_start_pointer_address = 6
    segment_end_pointer_address = segment_start_pointer_address + 4
    
    exporter.type_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.ability_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.ability_descriptions = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.dex_data = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.item_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.item_descriptions = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.move_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.move_descriptions = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.trainer_classes = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.trainer_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    

    exporter.move_data = extract_fixed_width_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)], 0x27)


    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.pokemon_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):int_frm_bytes(exporter.datasource, segment_end_pointer_address)])
    
    segment_start_pointer_address += 4
    segment_end_pointer_address += 4
    
    exporter.forme_names = convert_text_from_binary(exporter.datasource[int_frm_bytes(exporter.datasource, segment_start_pointer_address):])


    return(exporter)


def create_data_structures(exporter):
    