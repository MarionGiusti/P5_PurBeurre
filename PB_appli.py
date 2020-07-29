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
from class_interface import *


def main():
    """ Run PurBeurre application """

    try:

        pb_db = Database('PurBeurre_db')

        # The user can choose to run only the PurBeurre application (> PB_appli.py) or
        # to update the PurBeurre Database before to run the application (> PB_appli.py -uDB)
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-uDB", "--updateDB", help="Update database with Data from API", action="store_true"
            )
        args = parser.parse_args()

        if args.updateDB:
            # Create or Update the Database
            print("\n*** Création ou Mise à jour de la base de données ***\n ")

            pb_db.call_api()
            pb_db.create_database()
            pb_db.create_table()
            pb_db.insert_cat()
            pb_db.insert_product()

        else:
            pass

        pb_menu = InterfaceManager(pb_db)
        pb_menu.welcome()

        while pb_menu.option in [0, 1, 2, 3]:

            if pb_menu.option == 0:
                # Option 0 : Access to the main menu
                pb_menu.display_menu()

            if pb_menu.option == 1:
                # Option 1: Allow to research a substitute
                # by choosing a random product in a random category
                print("\n ***** Sélectionnez une catégorie :\n ")
                pb_menu.random_cat()
                print()
                pb_menu.verif_input1()
                print("\n ***** Sélectionnez un aliment :\n ")
                pb_menu.random_prod(pb_menu.enter_1)
                print()
                pb_menu.verif_input2()
                print(
                    "\n******************************************************"
                    "****************************************\n"
                    )
                pb_menu.display_chosen_prod()
                print(
                    "\n******************************************************"
                    "****************************************\n"
                    )
                pb_menu.display_substitute()
                pb_menu.display_ask_save()
                pb_menu.display_all_options()
                print(
                    "\n******************************************************"
                    "****************************************\n"
                    )
            if pb_menu.option == 2:
                # Option 2: Access to the favorite table
                print(
                    "\n******************************************************"
                    "****************************************\n"
                    )
                pb_menu.display_fav()
                pb_menu.display_options()
                print(
                    "\n******************************************************"
                    "****************************************\n"
                    )
            if pb_menu.option == 3:
                # Option3: Quit the PurBeurre application
                pb_menu.goodbye()

    except KeyboardInterrupt:
        pb_menu.goodbye()

    finally:
        # Close the database cursor and connection
        if pb_db.cursor:
            pb_db.cursor.close()
            pb_db.cnx.close()

if __name__ == "__main__":
    main()
