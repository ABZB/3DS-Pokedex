from dex_creator_class import *


        #name array variables
#        self.pokemon_names = [] #00 terminator
 #       self.forme_names = [] 
  #      
   #     self.type_names = []
    #    
     #   self.ability_names = []
      #  self.ability_descriptions = []
       # 
        #self.dex_data = []
#        
 #       self.item_names = []
  #      self.item_descriptions = []
   #     
    #    self.move_names = []
     #   self.move_descriptions = []
      #  
       # self.trainer_classes = [] #first entry is NOT empty
        #self.trainer_names = []
        
#y.decode(encoding = 'UTF-16')
#y.encode(encoding = 'UTF-16')


def find_file_in_game_text(file_content, file_number):
    for line_number, text_line in enumerate(file_content):
        #dump uses header of this form
        if(text_line == 'Text File : ' + str(file_number)):
           #whatever the line number is, next row is a bunch of tildes, and the following is the first text line
           return(line_number + 2)
       
       

def load_names_from_csv(dex_creation_data):
    

