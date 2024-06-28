from tkinter import CURRENT
from dex_creator_file_loader import *
from dex_creator_class import *
from utilities import *
import sys




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
    print(garc_info.path, which_garc)
    with open(garc_info.path, 'rb') as f:
        hexdata = f.read()
    garc_filesize = len(hexdata)
    
    #find start of data
    cur = 0    
    while True:
        if([hexdata[cur + 0], hexdata[cur + 1], hexdata[cur + 2], hexdata[cur + 3]] == garc_info.header):
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
            block_length = hexdata[cur + 2] + 256*hexdata[cur + 3]

            #this is the number of egg moves. Each egg move is 2 bytes, plus the 4-byte header
            block_length = 2*block_length + 4
            
            for offset in range(block_length):
                temp.append(hexdata[cur + offset])
            
            output_file.append(temp)
            
            cur += block_length
            
            try:
                #skip the FF FF blocks, they are inconsistently placed. If cur and cur+1 are FF FF, then move 2 ahead
                if(hexdata[cur + 0] == hexdata[cur + 1] == 0xFF):
                    cur += 2
            #end of file
            except:
                break

            if(cur >= garc_filesize - 1):
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

def evolution_array_builder(crnt_evolution, cur, dex_creation_data, current_forme):
    output_array = []
    
    #append method
    output_array.append(crnt_evolution[cur + 0])
    #append species
    output_array.append(crnt_evolution[cur + 4])
    output_array.append(crnt_evolution[cur + 5])
            
    #append forme
            
    #in gen VI, forme is not changed unless method is 0x22 (sets to forme 1)
    if(dex_creation_data.game in {'XY', 'ORAS'}):
        if(crnt_evolution[cur + 0] == 0x22):
            output_array.append(0x1)
        else:
            output_array.append(current_forme)
    else:
        output_array.append(crnt_evolution[cur + 6])
                
    #this holds the Item, Move, or Type for evolution methods that use that. In XYORAS, this is incompatible with level-up as that uses the same byte
    if(dex_creation_data.game in {'XY', 'ORAS'}):
        if(crnt_evolution[cur + 0] in {1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 28, 32, 33, 34}):
            #parameter does not exist
            output_array.append(0)
            output_array.append(0)
            #level
            output_array.append(crnt_evolution[cur + 2])
        else:
            #other parameter
            output_array.append(crnt_evolution[cur + 2])
            output_array.append(crnt_evolution[cur + 3])
            #level
            output_array.append(0)
            
    #SMUSUM
    else:
        #other parameter
        output_array.append(crnt_evolution[cur + 2])
        output_array.append(crnt_evolution[cur + 3])
        #Level
        output_array.append(crnt_evolution[cur + 7])
        
    return(output_array)

def source_evolution_array_builder(crnt_evolution, cur, dex_creation_data, source_nat_dex, source_personal_forme):
    output_array = []
    
    #append method
    output_array.append(crnt_evolution[cur + 0])
    #append species
    species_temp = little_endian_chunks(source_nat_dex)
    output_array.append(species_temp[0])
    output_array.append(species_temp[1])


    #append forme
    output_array.append(source_personal_forme)
        
    #this holds the Item, Move, or Type for evolution methods that use that. In XYORAS, this is incompatible with level-up as that uses the same byte
    if(dex_creation_data.game in {'XY', 'ORAS'}):
        if(crnt_evolution[cur + 0] in {1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 28, 32, 33, 34}):
            #parameter does not exist
            output_array.append(0)
            output_array.append(0)
            #level
            output_array.append(crnt_evolution[cur + 2])
        else:
            #other parameter
            output_array.append(crnt_evolution[cur + 2])
            output_array.append(crnt_evolution[cur + 3])
            #level
            output_array.append(0)
            
    #SMUSUM
    else:
        #other parameter
        output_array.append(crnt_evolution[cur + 2])
        output_array.append(crnt_evolution[cur + 3])
        #Level
        output_array.append(crnt_evolution[cur + 7])
        
    return(output_array)

def find_pre_evolutions(evolution_info, nat_dex, current_forme, dex_creation_data, evo_block_size, personal_info):
    list_pre_evolutions = []
    
    #in USUM, eight slots, each of eight bytes
    #0x0 - Evolution type
    #0x1 - unused
    #0x2 - other parameter low byte
    #0x3 - other parameter high byte
    #0x4 - target species low byte
    #0x5 - target species high byte
    #0x6 - Target forme (FF is preserve current)
    #0x7 - Level (0 is "NA")
    
    for pers_pointer, evotable in enumerate(evolution_info):
        if(pers_pointer == 0):
            continue
        #need to figure out what the current personal forme is (of the pokemon we are checking to see if it evolves from)
        pers_forme_pointer = personal_info[pers_pointer][0x1c] + 256*personal_info[pers_pointer][0x1d]
        #if the forme pointer is 0 or pers pointer is less than forme pointer, we are at forme 0. Also, in this case we are the nat dex number
        if(pers_forme_pointer == 0 or pers_pointer < pers_forme_pointer):
            pers_forme = 0
            source_nat_dex = pers_pointer
        #pers_pointer is bigger than or equal to the forme pointer. Then pers_pointer - forme_pointer is 0 if forme is 1, 1 if 2, etc. Also, we need to search for the nat dex    
        else:
            pers_forme = pers_pointer - pers_forme_pointer + 1
            for x in range(len(personal_info)):
                if(x == 0):
                    pass
                elif(personal_info[x][0x1c] + 256*personal_info[x][0x1d] == pers_forme_pointer):
                    source_nat_dex = x
            
        

        evolution_count = 0
        while True:
            cur = int(evo_block_size*evolution_count)
        
            if(cur >= len(evotable)):
                break
            #if this is 0, this evolution is disabled and the evolution list has ended
            elif(evotable[cur] == 0):
                break
        
            if(evotable[cur + 4] + 256*evotable[cur + 5] == nat_dex):
                #for forme to match, cases are:
                #XYORAS - either matching source personal file has same forme, or current_forme is 1 and evolution method is 0x22
                #SMUSUM - either matching source personal file has same forme and byte 0x6 is FF or byte 0x6 == current_forme

                if(dex_creation_data.game in {'XY', 'ORAS'}):
                    if(current_forme == pers_forme or (current_forme == 1 and evotable[0] == 0x22)):
                        list_pre_evolutions.append(source_evolution_array_builder(evotable, cur, dex_creation_data, source_nat_dex, pers_forme))
                else:
                    if((current_forme == pers_forme and evotable[cur + 6] == 0xFF) or (evotable[cur + 6] == current_forme)):
                        list_pre_evolutions.append(source_evolution_array_builder(evotable, cur, dex_creation_data, source_nat_dex, pers_forme))
            evolution_count += 1
    return(list_pre_evolutions)
                        
        
        
        


def power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, evo_block_size, max_nat_dex, nat_dex = 1, current_forme = 0, forme_count = 1, pers_pointer = 1, egg_pointer = 1, regional_list = []):
    
    if(current_forme == 0):
        match nat_dex:
            case 1:
                print('Compiling Kantonian data')
            case 152:
                print('Compiling Johtonian data')
            case 252:
                print('Compiling Hoennian data')
            case 387:
                print('Compiling Sinnohan data')
            case 494:
                print('Compiling Unovan data')
            case 650:
                print('Compiling Kalosian data')
            case 722:
                print('Compiling Alolan data')
    print('Compiling data on species', nat_dex, current_forme)
    
    #this will hold the data for this Pokemon
    output_array = [0]*80
            
    #personal, evolution, levelup, are by personal file index and exist for all
    crnt_personal = personal_info[pers_pointer]
    crnt_evolution = evolution_info[pers_pointer]
    crnt_levelup = levelup_info[pers_pointer]
                
    #megas only exist for forme 0
    if(current_forme == 0):
        crnt_mega = mega_info[pers_pointer]
    else:
        crnt_mega = mega_info[nat_dex]
        
        

    #egg move handling
    if(egg_pointer != 0):
        crnt_eggmov = eggmov_info[egg_pointer]
        
        #if the egg pointer doesn't equal the current egg pointer value, we're on an alt forme that doesn't have an egg move file. If length of crnt_eggmov is 0, no egg moves (no need to set 0, since default value is 0)
        if(len(crnt_eggmov) == 0):
            pass
        elif(crnt_eggmov[0] + crnt_eggmov[1]*256 != egg_pointer):
            egg_pointer = 0
        else:
    
            #egg moves
            #first byte is count of egg moves, second empty
            if(dex_creation_data.game in {'XY', 'ORAS'}):
                output_array[0] = crnt_eggmov[0]
                for x in range(2,len(crnt_eggmov)):
                    output_array.append(x)
            #first two bytes are the pointer to alt forme egg move (or self if no alt forme), next two same as XY/ORAS
            else:
                output_array[0] = crnt_eggmov[2]
                for x in range(4,len(crnt_eggmov)):
                    output_array.append(x)
        
            
    #evolves-into handling
              
    #in USUM, eight slots, each of eight bytes
    #0x0 - Evolution type
    #0x1 - unused
    #0x2 - other parameter low byte
    #0x3 - other parameter high byte
    #0x4 - target species low byte
    #0x5 - target species high byte
    #0x6 - Target forme (FF is preserve current)
    #0x7 - Level (0 is "NA")

    #in XYORAS
    #0x0 - Evolution type
    #0x1 - unused
    #0x2 - other parameter low byte
    #0x3 - other parameter high byte
    #0x4 - target species low byte
    #0x5 - target species high byted
    
    evolution_count = 0
    
    while True:
        cur = int(evo_block_size*evolution_count)
        
        if(cur >= len(crnt_evolution)):
            break
        #if this is 0, this evolution is disabled and the evolution list has ended
        elif(crnt_evolution[cur] == 0):
            break
        else:
            temp = evolution_array_builder(crnt_evolution, cur, dex_creation_data, current_forme)
            
            for x in temp:
                output_array.append(x)
                
        evolution_count += 1
    output_array[1] = evolution_count
    

    #now need to find all the places where a Pokemon evolves into this one
    temp_pre_evolutions = find_pre_evolutions(evolution_info, nat_dex, current_forme, dex_creation_data, evo_block_size, personal_info)
    output_array[2] = len(temp_pre_evolutions)/7
    for x in temp_pre_evolutions:
        output_array.append(x)

    #set nat dex, forme, and personal pointer
    output_array[5], output_array[6] = little_endian_chunks(nat_dex)
    output_array[7] = current_forme
    output_array[8], output_array[9] = little_endian_chunks(pers_pointer)

    #stats
    output_array[10] = crnt_personal[0]
    output_array[11] = crnt_personal[1]
    output_array[12] = crnt_personal[2]
    output_array[13] = crnt_personal[4]
    output_array[14] = crnt_personal[5]
    output_array[15] = crnt_personal[3]

    #Types and base catch rate
    output_array[16] = crnt_personal[6]
    output_array[17] = crnt_personal[7]
    output_array[18] = crnt_personal[8]
    


    # counting from rightmost bit (first is 1 = 2^0)
    #EV, byte 1
    #0	HP 1
    #1	HP 2
    #2	ATK 1
    #3	ATK 2
    #4	DEF 1
    #5	DEF 2
    #6	Spe 1
    #7	Spe 2

    #EV byte 2
    #8	SA 1
    #9	SA 2
    #10	SD 1
    #11	SD 2
    #12	
    #13	
    #14	
    #15	

    #HP
    output_array[19] = crnt_personal[0xa] & 3
    #Atk
    output_array[20] = (crnt_personal[0xa] >> 2) & 3
    #Def
    output_array[21] = (crnt_personal[0xa] >> 4) & 3
    #Spe
    output_array[24] = (crnt_personal[0xa] >> 6) & 3
    
    #SA
    output_array[22] = crnt_personal[0xb] & 3
    #SD
    output_array[23] = (crnt_personal[0xb] >> 2) & 3


    #wild hold items, gender, hatch cycles, friendship, exp curve, egg groups, 
    for offset in range(12):
        output_array[25 + offset] = crnt_personal[0xc + offset]
    #abilities, flee rate
    output_array[37] = crnt_personal[0xc + 11 + 1]
    output_array[39] = crnt_personal[0xc + 11 + 2]
    output_array[41] = crnt_personal[0xc + 11 + 3]
    output_array[44] = crnt_personal[0xc + 11 + 4]
    


    #TM/HM list is immediately followed by tutor list, starting from least bit being TM001
    for offset in range(13):
        output_array[46 + offset] = crnt_personal[0x28 + offset]

    #in XYORAS, the last few HMS are in 0x35
    if(dex_creation_data.game in {'XY', 'ORAS'}):    
        output_array[59] = crnt_personal[0x35]
        
    #the specual tutors (pledges, then elemental supermoves, then Draco Meteor and Dragon Ascent) are in 0x38 for everything
    output_array[60] = crnt_personal[0x38]
    

    #XY and SM don't have the nice tutors
    #ORAS skips a bunch of bytes, need to mess around to normalize it
    if(dex_creation_data.game == 'ORAS'):

        output_array[61] = crnt_personal[0x40]
        
        #0x41 doesn't do anything with the highest bit for some reason. grab the lowest bit of the next byte and shift it to the highest position, this way the list matches up with USUM
        output_array[62] = crnt_personal[0x41] + ((crnt_personal[0x44] & 0x01) << 7)
        
        #so bitshift the remainder down and add it to the highest bit of the next...
        output_array[63] = (crnt_personal[0x44] >> 1) + ((crnt_personal[0x45] & 0x01) << 7)

        #and again... fortunately, 0x46 only uses the very lowest byte so we're even now
        output_array[64] = (crnt_personal[0x45] >> 1) + ((crnt_personal[0x46] & 0x01) << 7)
        

        output_array[65] = crnt_personal[0x48]
        output_array[66] = crnt_personal[0x49]
        output_array[67] = crnt_personal[0x4c]
        output_array[68] = crnt_personal[0x4d]

    elif(dex_creation_data.game == 'USUM'):
        for offset in range(8):
            output_array[61 + offset] = crnt_personal[0x3c + offset]
        #only the low nibble of the last byte
        output_array[69] = crnt_personal[0x44] & 0x0F

    #base_exp
    output_array[44] = crnt_personal[0x22]
    output_array[45] = crnt_personal[0x23]
        
    
    #height in decimeters
    output_array[70] = crnt_personal[0x24]
    output_array[71] = crnt_personal[0x25]
    

    #mass in decigrams
    output_array[72] = crnt_personal[0x26]
    output_array[73] = crnt_personal[0x27]

    
    #z-crystal, base move, Z-move
    if(dex_creation_data.game in {'SM', 'USUM'}):
        for offset in range(6):
            output_array[74 + offset] = crnt_personal[0x4c + offset]


    forme_pointer = crnt_personal[0x1c] + 256*crnt_personal[0x1d]
    
    #get forme count, also make a table of regional formes in SMUSUM
    if(forme_pointer != 0 and current_forme == 0):
        if(dex_creation_data.game in {'SM', 'USUM'}):
            regional_list = [0]
        cur = 0
        while True:
            try:
                if(personal_info[forme_pointer + cur][0x1c] + 256*personal_info[forme_pointer + cur][0x1d] == forme_pointer):
                    forme_count += 1
                    if(dex_creation_data.game in {'SM', 'USUM'}):
                        regional_list.append(personal_info[forme_pointer + cur][0x52] & 0x01)
                    else:
                        regional_list.append(0)
                else:
                    break
            except:
                break
            cur += 1
                


    if(forme_pointer != 0):
        #don't list in order. First do Mega, then Ultra, then Ability/special (Meloetta, Aegislash, Greninja, Castform, Wishiwashi, Darmanitan), then all others


        # forme reference:
        # 0 = Mega (reference item)
        # 1 = Ultra  (reference z-crystal)
        # 2 = Transformed by Move (reference move)
        # 3 = Transformed by Ability (reference ability)
        # 4 = Transformed by held item (out of battle)
        # 5 = Variant Forme
        # 6 = Base Forme
    
        mega = 0
        ultra = 1
        transformed_move = 2
        transformed_ability = 3
        transformed_held_item = 4
        variant_forme = 5
        base_forme = 6
        fused_forme = 7
        regional_forme = 8
        
        # forme, method, needed thing
        done_forme_array = []
        for offset in range(int(len(crnt_mega)/8)):
            if(crnt_mega[offset*8 + 3] != 0x00):
                
                #base forme if current is a mega forme
                if(current_forme == crnt_mega[offset*8]):
                    output_array[3] += 1
                    output_array.append(0)
                    done_forme_array.append(0)
                    output_array.append(base_forme)
                    output_array.append(crnt_mega[offset*8 + 5])
                    output_array.append(crnt_mega[offset*8 + 6])  
                #alternate mega or all mega if base forme
                else:
                    output_array[3] += 1
                    output_array.append(crnt_mega[offset*8])
                    done_forme_array.append(crnt_mega[offset*8])
                    output_array.append(mega)
                    output_array.append(crnt_mega[offset*8 + 5])
                    output_array.append(crnt_mega[offset*8 + 6])

        #for Ultra, need to check forme 3 for having Ultranecrozium Z (923) in the z-crystal slot
        #will update when more generalized version is achieved
        #forme_pointer is the file for forme 1, so 2 after is our target
        if(forme_count > 3):
            if(923 == personal_info[forme_pointer + 2][0x4c] + 256*personal_info[forme_pointer + 2][0x4d]):
                if(current_forme != 3):
                    output_array[3] += 1
                    output_array.append(3)
                    done_forme_array.append(3)
                    output_array.append(ultra)
                    output_array.append(personal_info[forme_pointer + 2][0x4c])
                    output_array.append(personal_info[forme_pointer + 2][0x4d])
                #is the Ultra forme
                else:
                    for x in range(3):
                        output_array[3] += 1
                        output_array.append(x)
                        done_forme_array.append(x)
                        output_array.append(base_forme)
                        output_array.append(personal_info[forme_pointer + 2][0x4c])
                        output_array.append(personal_info[forme_pointer + 2][0x4d])
                    

        #just Meloetta
        if(nat_dex == 648):
                output_array[3] += 1
                output_array.append(1 - current_forme)
                done_forme_array.append(1 - current_forme)
                output_array.append(transformed_move)
                output_array.append(0x23)
                output_array.append(0x02)
        
        #Ability
        # Forecast, Flower Gift, Zen mode, Stance Change, Shields Down, Schooling, Disguise, Battle Bond, Power Construct        
        #59, 122, 161, 176, 197, 208, 209, 210, 211
        ability_list = {crnt_personal[0x18], crnt_personal[0x19], crnt_personal[0x1A]}
        
        base_ability_list = {personal_info[nat_dex][0x18], personal_info[nat_dex][0x19], personal_info[nat_dex][0x1A]}
        
        if(59 in ability_list or 59 in base_ability_list):
                for x in range(4):
                    if(x != current_forme):
                        output_array[3] += 1
                        output_array.append(x)
                        done_forme_array.append(x)
                        output_array.append(transformed_ability)
                        output_array.append(59)
                        output_array.append(0x00)
                
        elif(122 in ability_list or 122 in base_ability_list):
                for x in range(2):
                    if(x != current_forme):
                        output_array[3] += 1
                        output_array.append(x)
                        done_forme_array.append(x)
                        output_array.append(transformed_ability)
                        output_array.append(122)
                        output_array.append(0x00)
                
        elif(161 in ability_list or 161 in base_ability_list):
                for x in range(2):
                    if(x != current_forme):
                        output_array[3] += 1
                        output_array.append(x)
                        done_forme_array.append(x)
                        output_array.append(transformed_ability)
                        output_array.append(161)
                        output_array.append(0x00)
                
        elif(176 in ability_list or 176 in base_ability_list):
                for x in range(2):
                    if(x != current_forme):
                        output_array[3] += 1
                        output_array.append(x)
                        done_forme_array.append(x)
                        output_array.append(transformed_ability)
                        output_array.append(176)
                        output_array.append(0x00)
                
        elif(197 in ability_list):
                output_array[3] += 1
                #Shields up forme    
                if(current_forme <= 6):
                    output_array.append(current_forme + 7)
                    done_forme_array.append(current_forme + 7)
                else:
                    output_array.append(current_forme - 7)
                    done_forme_array.append(current_forme - 7)
                    
                output_array.append(transformed_ability)
                output_array.append(197)
                output_array.append(0x00)
                
        elif(208 in ability_list or 208 in base_ability_list):
                for x in range(2):
                    if(x != current_forme):
                        output_array[3] += 1
                        output_array.append(x)
                        done_forme_array.append(x)
                        output_array.append(transformed_ability)
                        output_array.append(208)
                        output_array.append(0x00)
                
        elif(209 in ability_list or 209 in base_ability_list):
                output_array[3] += 1
                if(current_forme in {0, 2}):
                    output_array.append(current_forme + 1)
                    done_forme_array.append(current_forme + 1)
                    output_array.append(transformed_ability)
                else:
                    output_array.append(current_forme - 1)
                    done_forme_array.append(current_forme - 1)
                    output_array.append(base_forme)
                output_array.append(209)
                output_array.append(0x00)
                
        elif(210 in ability_list or 210 in {personal_info[pers_pointer + 0][0x18], personal_info[pers_pointer + 0][0x19], personal_info[pers_pointer + 0][0x1A]}):
                output_array[3] += 1
                if(current_forme == 1):
                    output_array.append(2)
                    done_forme_array.append(2)
                elif(current_forme == 2):
                    output_array.append(1)
                    done_forme_array.append(1)
                output_array.append(transformed_ability)
                output_array.append(210)
                output_array.append(0x00)
        
        #zygarde and power construct. wrote it like this to avoid out of index
        elif(nat_dex == 718):
            if(211 in ability_list or 210 in {personal_info[pers_pointer + 2][0x18], personal_info[pers_pointer + 2][0x19], personal_info[pers_pointer + 2][0x1A], personal_info[pers_pointer + 3][0x18], personal_info[pers_pointer + 3][0x19], personal_info[pers_pointer + 3][0x1A]}):
                if(current_forme in {2, 3}):
                    output_array[3] += 1
                    output_array.append(4)
                    done_forme_array.append(4)
                    output_array.append(transformed_ability)
                    output_array.append(210)
                    output_array.append(0x00)
                elif(current_forme == 4):
                    output_array[3] += 1
                    output_array.append(2)
                    done_forme_array.append(2)
                    output_array.append(base_forme)
                    output_array.append(210)
                    output_array.append(0x00)
                    output_array[3] += 1
                    output_array.append(3)
                    done_forme_array.append(3)
                    output_array.append(base_forme)
                    output_array.append(210)
                    output_array.append(0x00)
            
        #just Giratina Origin
        if(nat_dex == 487):
            if(current_forme <= 1):
                output_array[3] += 1
                output_array.append(1 - current_forme)
                done_forme_array.append(1 - current_forme)
                output_array.append(transformed_held_item)
                output_array.append(112)
                output_array.append(0x00)

        #Kyurem and Necrozma
        if(nat_dex in {648, 800} and current_forme <= 2):
            #forme 1 or forme 2 looking at forme 0
            if(current_forme in {1, 2} and 0 not in done_forme_array):
                output_array[3] += 1
                output_array.append(0)
                done_forme_array.append(0)
                output_array.append(base_forme)
                
                #call the Pokemon to be fused or defused with (current forme is 1 or 2. Forme one matches the first nat dex fusion, so 1-1, second is one after so 2-1)
                if(nat_dex == 648):
                    output_array.append(0x83 + current_forme - 1)
                    output_array.append(0x02)
                else:
                    output_array.append(0x17 + current_forme - 1)
                    output_array.append(0x03)

            #base forme or forme 2 looking at forme 1
            if(current_forme in {0, 2} and 1 not in done_forme_array):
                output_array[3] += 1
                output_array.append(1)
                done_forme_array.append(1)
                output_array.append(fused_forme)
                
                #call the Pokemon to be fused or defused with
                if(nat_dex == 648):
                    output_array.append(0x83)
                    output_array.append(0x02)
                else:
                    output_array.append(0x17)
                    output_array.append(0x03)
                    
            #base forme or forme 1 looking at forme 2
            if(current_forme in {0,1} and 2 not in done_forme_array):
                output_array[3] += 1
                output_array.append(2)
                done_forme_array.append(2)
                output_array.append(fused_forme)
                
                #call the Pokemon to be fused or defused with
                if(nat_dex == 648):
                    output_array.append(0x84)
                    output_array.append(0x02)
                else:
                    output_array.append(0x18)
                    output_array.append(0x03)
                
                
        #handle all other variant formes
        
        for forme_number in range(forme_count):
            if(current_forme != forme_number and forme_number not in done_forme_array):
                output_array[3] += 1
                output_array.append(forme_number)
                if(dex_creation_data.game in {'SM', 'USUM'} and regional_list[forme_number] == 1):
                    output_array.append(regional_forme)
                else:
                    output_array.append(variant_forme)
                output_array.append(0x00)
                output_array.append(0x00)

    #levelup moves
    #first two bytes move, 3rd byte level
    for cur in range(int(len(crnt_levelup)/4)):
        #terminator flag
        if(crnt_levelup[cur + 0] == crnt_levelup[cur + 1] == crnt_levelup[cur + 2] == crnt_levelup[cur + 3] == 0xFF):
            break
        else:
            output_array[4] += 1
            output_array.append(crnt_levelup[cur + 0])
            output_array.append(crnt_levelup[cur + 1])
            output_array.append(crnt_levelup[cur + 2])
    print(output_array)
    return(output_array)
    if(forme_pointer != 0 and current_forme + 1 < forme_count):
        #forme starts from 0, e.g. if no alt formes forme count is 1 and current forme is 0
        if(egg_pointer != 0):
            #set up egg pointer for alternate forme:
            if(dex_creation_data.game in {'XY', 'ORAS'}):
                temp_egg_pointer = 0
            elif(current_forme == 0):
                temp_egg_pointer = crnt_eggmov[0] + crnt_eggmov[1]*256
            else:
                temp_egg_pointer = egg_pointer + 1
        else:
            temp_egg_pointer = 0
        return([*output_array, *power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, evo_block_size, max_nat_dex, nat_dex, current_forme + 1, forme_count, forme_pointer + current_forme, temp_egg_pointer, regional_list)])
    
    #personal info has length total personal files + 1.
    #move to next species        
    elif(pers_pointer < max_nat_dex):
        return([*output_array, *power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, evo_block_size, max_nat_dex, nat_dex + 1, 0, 1, nat_dex + 1, nat_dex + 1)])
    #reached final pokemon
    else:
        return(output_array)



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
    print(dex_creation_data.rom_folder_path)
    romfs_path = os.path.join(dex_creation_data.rom_folder_path, 'ExtractedRomFS')
    print(romfs_path)
    match dex_creation_data.game:
        case "XY":
            #not implemented for XY or ORAS
            eggmov.path = os.path.join(romfs_path, "a/2/1/3")
            #eggmov.header = 
            #eggmov.start = 
            #eggmov.blocksize = 0x30
            
            evolution.path = os.path.join(romfs_path, "a/2/1/5")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x3C
            evolution.blocksize = 0x30
            
            levelup.path = os.path.join(romfs_path, "a/2/1/4")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(romfs_path, "a/2/1/6")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x24
            mega.blocksize = 0x18
            
            personal.path = os.path.join(romfs_path, "a/2/1/8")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x50
            personal.blocksize = 0x50
            
        case "ORAS":
            #not implemented for XY or ORAS
            eggmov.path = os.path.join(romfs_path, "a/1/9/0")
            #eggmov.header = 
            #eggmov.start = 
            #eggmov.blocksize = 0x30
            
            evolution.path = os.path.join(romfs_path, "a/1/9/2")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x3C
            evolution.blocksize = 0x30
            
            levelup.path = os.path.join(romfs_path, "a/1/9/1")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(romfs_path, "a/1/9/3")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x24
            mega.blocksize = 0x18
            
            personal.path = os.path.join(romfs_path, "a/1/9/5")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x60
            personal.blocksize = 0x50
            
        case "SM":
         
            eggmov.path = os.path.join(romfs_path, "a/0/1/2")
            eggmov.header = [0x42, 0x4D, 0x49, 0x46]
            eggmov.start = 0x10
            
            evolution.path = os.path.join(romfs_path, "a/0/1/4")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x4C
            evolution.blocksize = 0x40
            
            levelup.path = os.path.join(romfs_path, "a/0/1/3")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(romfs_path, "a/0/1/5")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x1C
            mega.blocksize = 0x10
            
            personal.path = os.path.join(romfs_path, "a/0/1/7")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x60
            personal.blocksize = 0x54
            
        case "USUM":
            eggmov.path = os.path.join(romfs_path, "a/0/1/2")
            eggmov.header = [0x42, 0x4D, 0x49, 0x46]
            eggmov.start = 0x10
            
            evolution.path = os.path.join(romfs_path, "a/0/1/4")
            evolution.header = [0x42, 0x4D, 0x49, 0x46]
            evolution.start = 0x4C
            evolution.blocksize = 0x40
            
            levelup.path = os.path.join(romfs_path, "a/0/1/3")
            levelup.header = [0x42, 0x4D, 0x49, 0x46]
            levelup.start = 0x10
            
            mega.path = os.path.join(romfs_path, "a/0/1/5")
            mega.header = [0x42, 0x4D, 0x49, 0x46]
            mega.start = 0x1C
            mega.blocksize = 0x10
            
            personal.path = os.path.join(romfs_path, "a/0/1/7")
            personal.header = [0x42, 0x4D, 0x49, 0x46]
            personal.start = 0x60
            personal.blocksize = 0x54
    
    personal_info = garc_parser(personal, dex_creation_data, which_garc = 'personal')
    evolution_info = garc_parser(evolution, dex_creation_data, which_garc = 'evolution')
    levelup_info = garc_parser(levelup, dex_creation_data, which_garc = 'levelup')
    eggmov_info = garc_parser(eggmov, dex_creation_data, which_garc = 'eggmov')
    mega_info = garc_parser(mega, dex_creation_data, which_garc = 'mega')
    
    max_nat_dex = 0
    for personal_pointer, rows in enumerate(personal_info):
        try:
            #former case base species w/ alt formes, latter case no alt formes
            if(personal_pointer < rows[0x1c] + 256*rows[0x1c] or rows[0x1c] == rows[0x1c] == 0):
                max_nat_dex += 1
        except:
            pass


    print('Loaded World Data')
    
    default_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(int(2*len(personal_info)))
    output_array = power_construct(personal_info, evolution_info, levelup_info, eggmov_info, mega_info, dex_creation_data, int(evolution.blocksize/8), max_nat_dex)
    sys.setrecursionlimit(default_limit)
    

    with open(dex_database_output_path, "r+b") as file_dex:
        for x in output_array:
            file_dex.write(int(x).to_bytes(1, 'little'))
            
    return












