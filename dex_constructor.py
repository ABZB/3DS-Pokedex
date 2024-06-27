from dex_creator_file_loader import *
from dex_creator_class import *
from utilities import *




    



def create_pokedex_database(dex_creation_data):
    
    #Need to open:
    #personal
    #evoltuon
    #egg move
    #levelup move
    

    #list out the various bits of information we need to handle the game data before we set the game-specific stuff
    personal_file_local_path = ''
    personal_table_length = 0
    personal_file_start = 
    

    evolution_table_length = 0






    
    match dex_creation_data.game:
        case "XY":







    

    #select SQL database for output
    dex_database_output_path = asksaveasfilename(title='Select location to save database for Pokedex', defaultextension='.db',filetypes= [('Database','.db')])

    with open(dex_database_output_path, "r+b") as file_dex:
        with mmap.mmap(file_dex.fileno(), length = 0, access=mmap.ACCESS_WRITE) as dex:
            dex.flush()
            
            #zero out file
            for x in dex:
                x = 0
            
            species_index = 