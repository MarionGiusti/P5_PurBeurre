"""

PurBeurre application: Eat better !
This application


Script Python
Files:
purbeurre_app.py (main script),
database.py, interface.py and constants (modules),
table_queries (sql queries to create tables in the database)

"""
import argparse
from database import Database
from interface import InterfaceManager
from constants import STARS_LINE2

def main():
    """ Run PurBeurre application """

    try:

        pb_db = Database('PurBeurre_db')

        # The user can choose to run only the PurBeurre application (> purbeurre_app.py) or
        # to update the PurBeurre Database before to run the application (> purbeurre_app.py -uDB)
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
            pb_db.insert_category()
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
                pb_menu.random_category()
                print()
                pb_menu.verif_input1()
                
                print("\n ***** Sélectionnez un aliment :\n ")
                pb_menu.random_product(pb_menu.enter_1)
                print()
                pb_menu.verif_input2()
                print(STARS_LINE2)

                pb_menu.display_chosen_product()
                print(STARS_LINE2)

                pb_menu.display_substitute()
                pb_menu.display_ask_save()
                pb_menu.display_all_options()
                print(STARS_LINE2)

            if pb_menu.option == 2:
                # Option 2: Access to the favorite table
                print(STARS_LINE2)

                pb_menu.display_favorite()
                pb_menu.display_options()
                print(STARS_LINE2)

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
