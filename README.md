****************************************************************************************************************
# P5_PurBeurre
*Create a program which suggests healthier alternatives to junk food : requests API OpenFoofFacts, MySQL database*
*****************************************************************************************************************


### About The Project:

In the same spirit that the famous 'Ratatouille' restaurant on the Butte Montmartre, 'Pur Beurre' application 
promotes healthier eating.
By interacting with an interface, the user can choose a product from a category and access to different healthier 
substitutes. Using:

NOVA classification : from 1 (unprocessed or minimally processed foods) to 4 (ultra-processed food and drink products)

NUTRI-SCORE : from A (good) to E (bad) 

The database of this application based on the Open Food Facts API data, lists several products selected in different
category fields (e.g.: meat, drinks,...). The available informations of each product like its nova-group and nutrition-grade, allow to easily find a healthier 
substitute. The proposed substitutes will have a better nova-group and better nutrition grade than the selected product 
and will share the same category fields.


### Getting Started:

The program is composed of 5 files:
	* PB_appli.py: main script
	* PB_constants.py: module which regroups constants of the program
	* Class_database.py & Class_interface.py: one module for each class of the program
	* table_queries.sql: script with sql queries to create tables in the database
	
##### Prerequisites:
Python must be installed:
	- Virtualenv Module too, otherwise : pip install virtualenv
	
MySQL must be installed, otherwise:
	- Installation : http://dev.mysql.com/downloads/mysql/#downloads
	- Configuration : "host", "user", "passwd"

##### Installation:

	1- Clone this repository: git clone https://github.com/MarionGiusti/P5_PurBeurre.git
	
	2- Create a virtualenv: virtualenv -p python3 P5_PurBeurre
	
	3- Activate the virtualenv:
		Linux & MacOS user: source P5_PurBeurre\bin\activate
		Windows user: P5_PurBeurre\Scripts\activate
	
	4- Install the required libraries list in the requirements.txt file: pip install -r requirements.txt
		
	5- To allow the program to connect to your SQL Server:
		- Create a .env file and write in it your password in the constant DB_PWD: DB_PWD=yourchosenpasswd
		- if your SQL user is not root: 
			In the CONFIG dictionnary of the PB_constants.py file, change the value "root" of the variable "user" with your username.

	6- Run the program:
		For Windows user, you must initialise your password DB_PWD before to run the program:
			
			> echo %DB_PWD%
			
			> set DB_PWD=yourchosenpasswd
			
		After which, you can directly run the program like Linux & MacOS users:	
		First launch, you must create the Pur Beurre database and load the data OR just update the data of your database if any change occured in the OpenFoodFacts API:
			> PB_appli.py -uDB
			
		Do not update the Pur Beurre database:
			> PB_appli.py


### Features:

The program counts 2 classes: Database and InterfaceManager

##### Database Class:
**Methods to set up the Pur Beurre database (create / update):**

	* Create its own database (*create_database(), create_table() methods*)
	
	* Search requests in the OpenFoodFacts API and import data from the OpenFoodFacts API (*call_api() method*). 
	In the PB_constants.py file, the CATEGORIES and CHOSEN_FIELDS lists can be changed. CHOSEN_FIELDS list select some useful fields for each product requested.
	For more informations about the API requests: https://documenter.getpostman.com/view/8470508/SVtN3Wzy?version=latest#4a0c27c3-3abc-42c4-bf97-63f4e4108294
	
	* Save them in its database or update them (*insert_cat(), insert_product() methods*)


**Methods to interact with the Pur Beurre database using SQL queries.** 

SQL queries are executed in order to:
	
	* Get informations about categories, products, substitutes (*get_prod_from_cat(cat_id), get_chosen_prod(id_prod_to_comp), get_fav()*)
	
	* Compare them (*find_substitute()*)
	
	* Save them (*save_fav(id_prod_to_comp, id_prod_to_save)*)


Object of the Database class is an attribute of the InterfaceManager class. In this way, methods to interact with the database can be directly execute in methods from 
the InterfaceManager class.

##### InterfaceManager Class:
Regroups all methods which allow the user to interact with the PurBeurre interface. 
For wrong user inputs, the program repeats the questions.

Description of these main methods are in the followed section Usage.


### Usage:

The program interacts with the user by proposing different options (*display_menu(), display_all_options(), display_options() methods from InterfaceManager class*): 
	
	0- Main menu
	
	1- Replace a product
	
	2- Display saved substitutes
	
	3- Quit PUR BEURRE
	
	
**When the user selects the option 1:**

	* The program displays random categories from the Pur Beurre database (*using method random_cat() from InterfaceManager class*)
	
	* The user chooses one of those categories by entering the corresponding number (*variable enter_1*)
	
	* The program checks that the user input is correct (*using method verif_input1() from InterfaceManager class*)
	
	* The program displays random products from the selected category (*using method random_prod(enter_1) from InterfaceManager class*)
	
	* The user chooses one of those products by entering the corresponding number (*variable enter_2*)
	
	* The program checks that the user input is correct (*using method verif_input2() from InterfaceManager class*)
	
	* The program searchs substitutes to the selected product (*find_substitute() from Database class*)
	
	* If substitutes are found, the program displays them (*display_substitute() from InterfaceManager class*) with some descriptions (i.e. its brand, nova-group, nutrition-grade, store where you can buy it ...)
	
	* The user can choose to save one of the substitute by entering the corresponding number
	
	* Depending on the user input, the program save the selected product and its substitute in the table 'Favorite_product' of the Pur Beurre database (*save_substitute() from InterfaceManager class*)
	
	* Then, the program displays the 4 different options (*display_all_options() from InterfaceManager class*)
	
	
**When the user selects the option 2:**
	* The program displays the list of the product/substitute saved by the user (*display_fav() from InterfaceManager class*)
	* Then the program displays the different options (*display_options() from InterfaceManager class*)
