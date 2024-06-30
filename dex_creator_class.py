class Dex_creator:
	def __init__(self):
        #path variables   

		self.rom_folder_path = ''
		self.game = ''
		self.game_text_path = ''
        
		self.pokemon_name_loading_option = ''
        
        #for loading custom Pokemon names (not present in USUM, not required in XYORAS)
        #this pulls in output from my forme insertion tool
		self.insertion_output_list = ''
        #allows use of just a custom text file if desired
		self.text_file_name_list = ''

        #need this only for XY/ORAS
		self.extracted_egg_moves_folder_path = ''
        
        
        #name array variables
		self.pokemon_names = [] #00 terminator
		self.forme_names = [] 
        
		self.type_names = []
        
		self.ability_names = []
		self.ability_descriptions = []
        
		self.dex_data = []
        
		self.item_names = []
		self.item_descriptions = []
        
		self.move_names = []
		self.move_descriptions = []
        
		self.trainer_classes = [] #first entry is NOT empty
		self.trainer_names = []
        

		#text file locations
	def gametext_file_number(self, target):
		match target:
			case 'ability_descriptions':			
				match self.game:		
					case 'XY':	
						return(33)
					case 'ORAS':	
						return(36)
					case 'SM':	
						return(97)
					case 'USUM':	
						return(102)
			case 'ability_names':			
				match self.game:		
					case 'XY':	
						return(34)
					case 'ORAS':	
						return(37)
					case 'SM':	
						return(96)
					case 'USUM':	
						return(101)
			case 'dex_data':			
				match self.game:		
					case 'XY':	
						return(6)
					case 'ORAS':	
						return(6)
					case 'SM':	
						return(119)
					case 'USUM':	
						return(124)
			case 'forme_names':			
				match self.game:		
					case 'XY':	
						return(5)
					case 'ORAS':	
						return(5)
					case 'SM':	
						return(0)
					case 'USUM':	
						return(0)
			case 'item_descriptions':			
				match self.game:		
					case 'XY':	
						return(99)
					case 'ORAS':	
						return(117)
					case 'SM':	
						return(35)
					case 'USUM':	
						return(39)
			case 'item_names':			
				match self.game:		
					case 'XY':	
						return(98)
					case 'ORAS':	
						return(116)
					case 'SM':	
						return(36)
					case 'USUM':	
						return(40)
			case 'move_descriptions':			
				match self.game:		
					case 'XY':	
						return(15)
					case 'ORAS':	
						return(16)
					case 'SM':	
						return(112)
					case 'USUM':	
						return(117)
			case 'move_names':			
				match self.game:		
					case 'XY':	
						return(14)
					case 'ORAS':	
						return(14)
					case 'SM':	
						return(113)
					case 'USUM':	
						return(118)
			case 'pokemon_names':			
				match self.game:		
					case 'XY':	
						return(80)
					case 'ORAS':	
						return(98)
					case 'SM':	
						return(55)
					case 'USUM':	
						return(60)
			case 'trainer_classes':			
				match self.game:		
					case 'XY':	
						return(19)
					case 'ORAS':	
						return(21)
					case 'SM':	
						return(106)
					case 'USUM':	
						return(111)
			case 'trainer_names':			
				match self.game:		
					case 'XY':	
						return(20)
					case 'ORAS':	
						return(22)
					case 'SM':	
						return(105)
					case 'USUM':	
						return(110)
			case 'type_names':			
				match self.game:		
					case 'XY':	
						return(17)
					case 'ORAS':	
						return(18)
					case 'SM':	
						return(107)
					case 'USUM':	
						return(112)



class GARC_file_info:
    def __init__(self):
        self.path = ''
        #start is relative to specified code
        self.header = []
        self.start = 0
        self.blocksize = 0



default_forme_name_list_gen_vii = [['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['A','A'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Plant','Plant'],['Plant','Plant'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Overcast','Overcast'],['West','West'],['West','West'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Altered','Altered'],['',''],['',''],['',''],['',''],['Land','Land'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Red','Red'],['',''],['',''],['',''],['',''],['Standard','Standard'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Spring','Spring'],['Spring','Spring'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Incarnate','Incarnate'],['Incarnate','Incarnate'],['',''],['',''],['Incarnate','Incarnate'],['',''],['Ordinary','Ordinary'],['Aria','Aria'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Icy Snow','Icy Snow'],['',''],['',''],['Red','Red'],['Red','Red'],['Red','Red'],['',''],['',''],['',''],['',''],['Natural','Natural'],['',''],['Male','Male'],['',''],['',''],['Shield','Shield'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Small','Small'],['Small','Small'],['',''],['',''],['',''],['',''],['',''],['',''],['0.5','0.5'],['',''],['Confined','Confined'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Fire','Fire'],['',''],['',''],['',''],['Dawn','Dawn'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['Shielded Red','Shielded Red'],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['','Attack'],['','Defense'],['','Speed'],['','Sandy'],['','Trash'],['Attack','Sky'],['Defense','Origin'],['Speed','Heat'],['Sandy','Wash'],['Trash','Frost'],['Sky','Fan'],['Origin','Mow'],['Heat','Sunny'],['Wash','Rainy'],['Frost','Snowy'],['Fan','Sunshine'],['Mow','East'],['Sunny','East'],['Rainy','Blue'],['Snowy','Zen'],['Sunshine','Pirouette'],['East','White'],['East','Black'],['Blue','Resolute'],['Zen','Therian'],['Pirouette','Therian'],['White','Therian'],['Black','Mega'],['Resolute','Female'],['Therian','Heart Trim'],['Therian','Star Trim'],['Therian','Diamond Trim'],['Mega','Debutante Trim'],['Female','Matron Trim'],['Heart Trim','Dandy Trim'],['Star Trim','La Reine Trim'],['Diamond Trim','Kabuki Trim'],['Debutante Trim','Pharaoh Trim'],['Matron Trim','Mega'],['Dandy Trim','Mega'],['La Reine Trim','Mega'],['Kabuki Trim','X'],['Pharaoh Trim','Y'],['Mega','X'],['Mega','Y'],['Mega','Mega'],['X','Mega'],['Y','Mega'],['X','Mega'],['Y','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Blade'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Blade','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Medium'],['Mega','Large'],['Mega','Giant'],['Mega','Medium'],['Mega','Large'],['Medium','Giant'],['Large','Yellow'],['Giant','Orange'],['Medium','Blue'],['Large','White'],['Giant','Eternal'],['Yellow','Mega'],['Orange','Mega'],['Blue','Mega'],['White','Mega'],['Eternal','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Mega'],['Mega','Primal'],['Mega','Primal'],['Mega','Mega'],['Mega','Unbound'],['Mega','Mega'],['Primal','Mega'],['Primal','Mega'],['Mega','Mega'],['Unbound','School'],['Mega','Electric'],['Mega','Psychic'],['Mega','Ghost'],['Mega','Midnight'],['School','Alolan'],['Electric','Alolan'],['Psychic','Totem'],['Ghost','Alolan'],['Midnight','Alolan'],['Dusk','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Totem','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Alolan'],['Alolan','Ash'],['Alolan','Ash Battle Bond'],['Alolan','10 Percent'],['Alolan','10% Power Construct'],['Alolan','50% Power Construct'],['Alolan','One Hundred Percent'],['Totem','Shielded Orange'],['Ash','Shielded Yellow'],['Ash Battle Bond','Shielded Green'],['10 Percent','Shielded Blue'],['10% Power Construct','Shielded Indigo'],['50% Power Construct','Shielded Violet'],['One Hundred Percent','Core Red'],['Shielded Orange','Core Orange'],['Shielded Yellow','Core Yellow'],['Shielded Green','Core Green'],['Shielded Blue','Core Blue'],['Shielded Indigo','Core Indigo'],['Shielded Violet','Core Violet'],['Core Red','Alolan'],['Core Orange','Alolan'],['Core Yellow','Busted'],['Core Green','Totem'],['Core Blue','Totem Busted'],['Core Indigo','Original Color'],['Core Violet','Kantonian'],['Alolan','Johtonian'],['Alolan','Sinnohan'],['Busted','Unovan'],['Totem','Kalosian'],['Totem Busted','Alolan'],['Original Color','Totem'],['Kantonian','Totem'],['Johtonian','Totem'],['Sinnohan','Totem'],['Unovan','Totem'],['Kalosian',''],['Alolan',''],['I Choose You!',''],['Totem',''],['Totem',''],['Totem',''],['Totem',''],['Totem',''],['Dusk Mane',''],['Dawn Wings',''],['Ultra',''],['Totem',''],['Totem',''],['Totem',''],['Dusk','']]

        




