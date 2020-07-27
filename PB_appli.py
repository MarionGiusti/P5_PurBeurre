#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""

PurBeurre application: Eat better !
This application 


Script Python
Files:
PB_appli.py (main script),
Class_database.py, Class_interface.py and PB_constants (modules),
table_queries (sql queries to create tables in the database)

"""
import argparse
from Class_interface import *


def main():
	""" Run PurBeurre application """

	try:

		PB_db = Database('PurBeurre_db')

		# The user can choose to run only the PurBeurre application (> PB_appli.py) or 
		# to update the PurBeurre Database before to run the application (> PB_appli.py -uDB)
		parser = argparse.ArgumentParser()
		parser.add_argument("-uDB", "--updateDB", help="Update database with Data from API", action="store_true")
		args = parser.parse_args()

		if args.updateDB:
			# Create or Update the Database
			print("\n*** Création ou Mise à jour de la base de données ***\n ")

			PB_db.call_api()
			PB_db.create_database()
			PB_db.create_table()
			PB_db.insert_cat()
			PB_db.insert_product()

		else:
			pass	
		
		PB_menu = InterfaceManager(PB_db)
		PB_menu.welcome()
		
		while PB_menu.option in [0, 1, 2, 3]:

			if PB_menu.option == 0:
				# Option 0 : Access to the main menu
				PB_menu.display_menu()
				
			if PB_menu.option == 1:
				# Option 1: Allow to research a substitute by choosing a random product in a random category
				print("\n ***** Sélectionnez une catégorie :\n ")
				PB_menu.random_cat()
				print()
				PB_menu.verif_input1()
				print("\n ***** Sélectionnez un aliment :\n ")
				PB_menu.random_prod(PB_menu.enter_1)
				print()
				PB_menu.verif_input2()
				print("\n**********************************************************************************************\n")
				PB_menu.display_chosen_prod()
				print("\n**********************************************************************************************\n")
				PB_menu.display_substitute()
				PB_menu.display_ask_save()
				PB_menu.display_all_options()
				print("\n**********************************************************************************************\n")

			if PB_menu.option == 2:
				# Option 2: Access to the favorite table
				print("\n**********************************************************************************************\n")
				PB_menu.display_fav()
				PB_menu.display_options()
				print("\n**********************************************************************************************\n")

			if PB_menu.option == 3:
				# Option3: Quit the PurBeurre application
				PB_menu.goodbye()

	except KeyboardInterrupt:
		PB_menu.goodbye()

	finally:
		# Close the database cursor and connection
		if PB_db.cursor:
			PB_db.cursor.close()
			PB_db.cnx.close()


if __name__ == "__main__":
    main()
