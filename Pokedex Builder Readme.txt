Purpose:

This application compiles a database of all Pokemon information from the targeted game files, as well as other commonly modified data. On doing so, it also produces the two primary files required for custom builds of Pokehex (the .pkl containing the levelup information, and the untyped file containing the personal information) in the same directory as the output database.

The created database file can then be used to easily produce spreadsheets documenting changes, or with a seperate application that will display the information (both yet to produced as of version 1.0 of this program).

Instructions:

1) Set the various filepaths. As you select them, the button names will update with the filepaths (you can resize the window to confirm if they are too long)

Game - select target game (XY, ORAS, SM, or USUM)

Source for Names - choose whether the names of Pokemon and Formes will be read from the gametext file or from the output CSV from my Forme Insertion Tool (the latter is required for this program to function if you have inserted new formes, and will work with the same once we figure out inserting new species).

Extracted ROM Folder - select the top-level folder containing the extracted data (the same one pk3ds targets)

Dumped Game Text - dump your gametext file to .txt using pk3ds, and select that file

Name Source - select the csv file you will be using to source names from (if you chose the default option, you do not need to select anything here)

Extracted Egg Move Folder - extract the Egg Move GARC using pk3ds and select that folder here. This is only required for XY and ORAS (I have not quite figured out the unextracted format there)


2) Load/Save CFG. This will save the above options, so when you make further changes, you can just load your config file and rebuild the database. Please be reminded that if you updated your game text or egg moves (in XY/ORAS) you will need to respectively redump and reextract those files.


3) Create Pokedex. You will be prompted to choose a location and name for the database. The files that are needed for custom builds of pokehex (PKHeX.Core\Resources\byte\personal\personal_XX and PKHeX.Core\Resources\byte\levelup\lvlmove_XX.pkl) will be created in the same directory as the database.