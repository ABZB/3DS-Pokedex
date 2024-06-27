from dex_creator_file_loader import *
from dex_creator_class import *
from utilities import *





def gen_vi_egg_garc_handling(garc_info, dex_creation_data):
    file_list = os.listdir(dex_creation_data.extracted_egg_moves_folder_path)
    output_file = [[0]]
    for x in file_list:
        with open(x, 'rb') as f:
            hexdata = f.read()
            output_file.append(hexdata)
    return(output_file)


#returns list where the kth element is the kth data block of the GARC
#for personal, stops when it hits the 0 block that marks the start of the compilation file
#for XY/ORAS, calls a different function for Egg
def garc_parser(garc_info, dex_creation_data, which_garc = ''):
    
    if(which_garc == 'eggmov' and dex_creation_data.game in {'XY', 'ORAS'}):
        return(gen_vi_egg_garc_handling(garc_info, dex_creation_data))
    
    #since the 0th entry is never used, just make it a single 0 entry to keep everything in line
    output_file = [[0]]

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
        cur += 1
    
    #handling for GARCs with fixed blocksizes is straightforward
    if(garc_info.blocksize >0):
        #cur is now pointing to the first byte of the first data block
        while True:
            temp = []
            for offset in range(garc_info.blocksize):
                temp.append(hexdata[cur + offset])
            #temp now contains the data from the current block
            
            #increment cur by the blocksize for next round
            cur += garc_info.blocksize
        
            #logic to avoid doubling up on the personal file
            #if all stats are 0, and the next byte is the same as the very first one we read, we are at compilation, so break
            if(which_garc == 'personal' and (temp[0] == temp[1] == temp[2] == temp[3] == temp[4] == temp[5] == temp[6] == 0) and hexdata[cur] == output_file[1][0]):
                print('Reached end of Personal file at address ', cur - garc_info.blocksize - 1)
                break
            else:
                #otherwise append temp to the ongoing list
                output_file.append(temp)

            #if this pushes it past the end of the file, break
            if(cur >= garc_filesize):
                break
    elif(which_garc == 'eggmov'):
        
        while True:
            temp = []
            #first read bytes at offsets 2 and 3, because that tells the size of the block
            block_length = hexdata[cur + 2] + hexdata[cur + 3]*256

            #this is the number of egg moves. Each egg move is 2 bytes, plus the 4-byte header
            block_length = 2*block_length + 4
            
            for offset in range(block_length):
                temp.append(hexdata[cur + offset])
            
            output_file.append(temp)
            
            cur += block_length
            if(cur >= garc_filesize):
                break
    elif(which_garc == 'levelup'):
        #Levelup uses terminator block FF FF FF FF
        while True:
            temp = []
            block_size = 0
            
            while True:
                temp.append(hexdata[cur])
                cur += 1
                #next four bytes being FF means we are at the end
                if(0xFF == hexdata[cur + 1] == hexdata[cur + 2] == hexdata[cur + 3] == hexdata[cur + 4]):
                    break

            output_file.append(temp)
            
            cur += 5
            if(cur >= garc_filesize):
                break
    return(output_file)



def create_pokedex_database(dex_creation_data):
    
    #construct the objects that will hold the various GARC reference data
    personal = GARC_file_info()
    evolution = GARC_file_info()
    levelup = GARC_file_info()
    eggmov = GARC_file_info()
    mega = GARC_file_info()
    
    move = GARC_file_info()
    
    #select database for output
    #don't need this until later, but let's do this first so if it screws up user hasn't waited for everything else
    dex_database_output_path = asksaveasfilename(title='Select location to save database for Pokedex', defaultextension='.db',filetypes= [('Database','.db')])

    try:
        open(dex_database_output_path, 'w').close()
        print('Cleared old data')
    except:
        print('')

    
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
            personal.blocksize = 0x54
            
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
            personal.blocksize = 0x54
            

    
    personal = GARC_file_info()
    evolution = GARC_file_info()
    levelup = GARC_file_info()
    eggmov = GARC_file_info()
    mega = GARC_file_info()
    
    personal_info = garc_parser(personal, dex_creation_data, which_garc = 'personal')
    evolution_info = garc_parser(evolution, dex_creation_data, which_garc = 'evolution')
    levelup_info = garc_parser(levelup, dex_creation_data, which_garc = 'levelup')
    eggmov_info = garc_parser(eggmov, dex_creation_data, which_garc = 'eggmov')
    mega_info = garc_parser(mega, dex_creation_data, which_garc = 'mega')
 
    output_array = power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, [])

    with open(dex_database_output_path, "r+b") as file_dex:
        with mmap.mmap(file_dex.fileno(), length = 0, access=mmap.ACCESS_WRITE) as dex:
            dex.flush()


def power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, output_array, nat_dex = 1, current_forme = 0, forme_count = 0, pers_pointer = 1, egg_pointer = 1):
    
            
    #personal, evolution, levelup, are by personal file index and exist for all
    crnt_personal = personal_info[pers_pointer]
    crnt_evolution = evolution_info[pers_pointer]
    crnt_levelup = levelup_info[pers_pointer]
                
    #megas only exist for forme 0
    if(current_forme == 0):
        crnt_mega = mega_info[pers_pointer]
                
    if(egg_pointer != 0):
        crnt_eggmov = eggmov_info[egg_pointer]
    







    if(forme_pointer != 0):
        if(current_forme < forme_count):
            #set up egg pointer for alternate forme:
            if(current_forme == 0):
                if(dex_creation_data.game in {'SM', 'USUM'}):
                    temp_egg_pointer = crnt_eggmov[0] + crnt_eggmov[1]*256
                else:
                    temp_egg_pointer = 0
    
            output_array = power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, output_array, nat_dex, current_forme + 1, forme_count, forme_pointer + current_forme, temp_egg_pointer)
    #personal info has length total personal files + 1.
    #move to next species        
    elif(pers_pointer + 1 < len(personal_info)):
        output_array = power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, output_array, nat_dex + 1, 0, 0, nat_dex + 1, nat_dex + 1)
        

    return(output_array)