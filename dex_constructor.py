from dex_creator_file_loader import *
from dex_creator_class import *
from utilities import *





def gen_vi_egg_garc_handling(garc_info, dex_creation_data):
    pass




#returns list where the kth element is the kth data block of the GARC
#for personal, stops when it hits the 0 block that marks the start of the compilation file
#for XY/ORAS, calls a different function for Egg
def garc_parser(garc_info, dex_creation_data, which_garc = ''):
    
    if(which_garc == 'egg' and dex_creation_data.game in {'XY', 'ORAS'}):
        return(gen_vi_egg_garc_handling(garc_info, dex_creation_data))

    with open(garc_info.path, 'rb') as f:
        hexdata = f.read()
    garc_filesize = len(hexdata)
    
    #find start of data
    cur = 0    
    while True:
        if([hexdata[0], hexdata[1], hexdata[2], hexdata[3]] == garc_info.header):
            cur += garc_info.start
            break
        elif(cur == garc_filesize):
            print('Something is wrong with your Garc file ' + which_garc + ', could not locate the header.')
            return(False)
            
    
            personal.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/7")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x5C
            personal.blocksize = 0x50
    



def create_pokedex_database(dex_creation_data):
    

    
    #construct the objects that will hold the various GARC reference data
    personal = GARC_file_info()
    evolution = GARC_file_info()
    levelup = GARC_file_info()
    eggmov = GARC_file_info()
    mega = GARC_file_info()
    
    move = GARC_file_info()
    


    
    match dex_creation_data.game:
        case "XY":
            #not implemented for XY or ORAS
            eggmov.path = os.path.join(dex_creation_data.rom_folder_path, "/a/2/1/3")
            #eggmov.header = 
            #eggmov.start = 
            #eggmov.blocksize = 0x30
            
            evolution.path = os.path.join(dex_creation_data.rom_folder_path, "/a/2/1/5")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x3C
            evolution.blocksize = 0x30
            
            levelup.path = os.path.join(dex_creation_data.rom_folder_path, "/a/2/1/4")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(dex_creation_data.rom_folder_path, "/a/2/1/6")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x24
            mega.blocksize = 0x18
            
            personal.path = os.path.join(dex_creation_data.rom_folder_path, "/a/2/1/8")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x4C
            personal.blocksize = 0x50
            
        case "ORAS":
            #not implemented for XY or ORAS
            eggmov.path = os.path.join(dex_creation_data.rom_folder_path, "/a/1/9/0")
            #eggmov.header = 
            #eggmov.start = 
            #eggmov.blocksize = 0x30
            
            evolution.path = os.path.join(dex_creation_data.rom_folder_path, "/a/1/9/2")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x3C
            evolution.blocksize = 0x30
            
            levelup.path = os.path.join(dex_creation_data.rom_folder_path, "/a/1/9/1")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(dex_creation_data.rom_folder_path, "/a/1/9/3")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x24
            mega.blocksize = 0x18
            
            personal.path = os.path.join(dex_creation_data.rom_folder_path, "/a/1/9/5")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x5C
            personal.blocksize = 0x50
            
        case "SM":
         
            eggmov.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/2")
            eggmov.header = [0x42, 0x4D, 0x49, 0x46]
            eggmov.start = 0x10
            
            evolution.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/4")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x4C
            evolution.blocksize = 0x40
            
            levelup.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/3")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/5")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x1C
            mega.blocksize = 0x10
            
            personal.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/7")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x5C
            personal.blocksize = 0x50
            
        case "USUM":
            eggmov.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/2")
            eggmov.header = [0x42, 0x4D, 0x49, 0x46]
            eggmov.start = 0x10
            
            evolution.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/4")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x4C
            evolution.blocksize = 0x40
            
            levelup.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/3")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/5")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x1C
            mega.blocksize = 0x10
            
            personal.path = os.path.join(dex_creation_data.rom_folder_path, "/a/0/1/7")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x5C
            personal.blocksize = 0x50
            

    


    

    #select database for output
    dex_database_output_path = asksaveasfilename(title='Select location to save database for Pokedex', defaultextension='.db',filetypes= [('Database','.db')])

    try:
        open(dex_database_output_path, 'w').close()
        print('Cleared old data')
    except:
        print('')

    with open(dex_database_output_path, "r+b") as file_dex:
        with mmap.mmap(file_dex.fileno(), length = 0, access=mmap.ACCESS_WRITE) as dex:
            dex.flush()
            
            #will track Pokemon by [nat dex, forme number, personal index]
            pokemon_index_current = [0, 0, 0]