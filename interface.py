"""

Class InterfaceManager:
Regroups all methods which allow the user to interact with the PurBeurre interface.

"""
import sys
import random
from database import Database
from constants import STARS_LINE, STARS_UP, STARS_DOWN, \
QUEST, INPUT_OPT, OPT0, OPT1, OPT2, OPT3, NOT_OPT, NOT_INT


class InterfaceManager:
    """ Class to manage the interface """
    def __init__(self, dbase):
        """ Initialisation """
        self.dbase = Database(dbase.db_name)
        self.option = 0
        self.enter_1 = 0
        self.enter_2 = 0
        self.rand_categories_opt = []
        self.rand_products_opt = []
        self.id_product_to_compare = 0
        self.id_product_to_save = 0
        self.substitute_opt = 0

    def welcome(self):
        """ Welcoming message when opening PurBeurre application """
        print(STARS_UP)
        print("       * BIENVENUE SUR PURBEURRE ! *")
        print(STARS_DOWN, STARS_LINE)

    def goodbye(self):
        """ Goodbye message when closing the PurBeurre application """
        print(STARS_LINE, STARS_UP)
        print("       * A BIENTOT SUR PURBEURRE ! *")
        print(STARS_DOWN)
        sys.exit()

    def display_menu(self):
        """ Main menu: Display different options for the user and wait for the user input """
        while True:
            try:
                # Need to reset the value of self.enter_2, otherwise it keeps the old value
                self.enter_2 = 0
                print(QUEST, OPT1, OPT2, OPT3)
                self.option = int(input(INPUT_OPT))
                if self.option not in [1, 2, 3]:
                    print(NOT_OPT)
                    self.display_menu()
                break
            except ValueError:
                print(NOT_INT)

    def display_all_options(self):
        """ Display 4 different options for the user and wait for the user input """
        while True:
            try:
                # Need to reset the value of self.enter_2, otherwise it keeps the old value
                self.enter_2 = 0
                print("\n", QUEST, OPT0, OPT1, OPT2, OPT3)
                self.option = int(input(INPUT_OPT))
                if self.option not in [0, 1, 2, 3]:
                    print(NOT_OPT)
                    self.display_all_options()
                break
            except ValueError:
                print(NOT_INT)

    def display_options(self):
        """ Display 3 different options for the user and wait for the user input """
        while True:
            try:
                print("\n", QUEST, OPT0, OPT1, OPT3)
                self.option = int(input(INPUT_OPT))
                if self.option not in [0, 1, 3]:
                    print(NOT_OPT)
                    self.display_options()
                break
            except ValueError:
                print(NOT_INT)

    def random_category(self):
        """ Display 3 random categories """
        # Call method get_categories() from the database class
        self.dbase.get_category()
        k = 3
        i = 1
        self.rand_categories_opt = []
        # Choose randomly 3 categories from all the categories of the database
        rand_categories = random.sample(self.dbase.id_category_list, k)
        while i <= k:
            for category_id, category in rand_categories:
                print(i, "-", category)
                category_option = [i, category_id]
                # Save the indice, id and cat_name of the category chosen by the user.
                # Useful for methods verif_input1() and random_prod()
                self.rand_categories_opt.append(category_option)
                i += 1

    def verif_input1(self):
        """ Verification of the user input, self.enter_1 must be in the proposed categories """
        while True:
            try:
                self.enter_1 = int(input(" ** Rentrez le numéro de la catégorie souhaitée : \n "))
                ind_opt = []
                for ind, category_id in self.rand_categories_opt:
                    ind_opt.append(ind)
                while self.enter_1 not in ind_opt:
                    print("\n", NOT_OPT)
                    self.verif_input1()
                break
            except ValueError:
                print(NOT_INT)

    def random_product(self, enter_1):
        """ Display 6 random products from the category selected by the users """
        k = 6
        i = 1
        for ind, category_id in self.rand_categories_opt:
            if ind == self.enter_1:
                # Call method get_prod_from_cat() from the database class
                self.dbase.get_product_from_category(category_id)
                # Select 6 random products and save them in the rand_prod variable
                rand_product = random.sample(self.dbase.product_from_category, k)
        self.rand_products_opt = []
        while i <= k:
            for id_product, product in rand_product:
                print(i, "-", product)
                product_option = [i, id_product]
                # Save the indice, id and product_name of the product chosen by the user.
                # Useful for methods verif_input2()
                self.rand_products_opt.append(product_option)
                i += 1

    def verif_input2(self):
        """ Verification of the user input, self.enter_2 must be in the proposed products """
        while True:
            try:
                self.enter_2 = int(input(" ** Rentrez le numéro du produit souhaité : \n "))
                ind_opt = []
                for ind, product_id in self.rand_products_opt:
                    ind_opt.append(ind)
                    if self.enter_2 == ind:
                        # Save the id of the product to substitute.
                        # Useful in the method display_chosen_prod() and save_substitute()
                        self.id_product_to_compare = product_id
                while self.enter_2 not in ind_opt:
                    print("\n", NOT_OPT)
                    self.verif_input2()
                break
            except ValueError:
                print(NOT_INT)

    def display_chosen_product(self):
        """ Display the selected product with some descriptions """
        # Call method get_chosen_prod() from the database class
        self.dbase.get_chosen_product(self.id_product_to_compare)
        print(
            " ***** Produit à substituer sélectionné :"
            )
        print(
            "\n Nom :", self.dbase.product_attributs[0][0],
            "\n Marque :", self.dbase.product_attributs[0][1],
            "\n Groupe NOVA :", self.dbase.product_attributs[0][4],
            "\n Nutri-score :", self.dbase.product_attributs[0][5],
            "\n Code produit :", self.dbase.product_attributs[0][2],
            "\n URL :", self.dbase.product_attributs[0][3]
            )

    def display_substitute(self):
        """ Display different substitutes on the interface with some descriptions """
        print(
            " ***** Voici des substituts à l'aliment sélectionné :\n"
            )
        # Call method find_substitute() from the database class
        self.dbase.find_substitute()
        i = 1
        self.substitute_opt = []
        for id_product, prod_name, brand_name, nova_gps, nutri_grades, code_prod, \
        url, store_name in self.dbase.substitute_attributs:
            print(
                i, "-",
                "\n Nom :", prod_name,
                "\n Marque :", brand_name,
                "\n Groupe NOVA :", nova_gps,
                "\n Nutri-score :", nutri_grades,
                "\n Magasins :", store_name,
                "\n Code produit :", code_prod,
                "\n URL :", url,
                "\n -----"
                )
            substitute_option = [i, id_product]
            # Save the id of the chosen substitute.
            # Useful in the methods display_ask_save() and save_substitute()
            self.substitute_opt.append(substitute_option)
            i += 1
        if len(self.substitute_opt) == 0:
            print(
                " Excusez-nous, nous n'avons pas trouvé de substituts"
                " pour ce produit !\n "
                )

    def display_ask_save(self):
        """ Option to save (or not save) in the favorite table of
        the database, a pair which includes : a product and a substitute """
        if len(self.substitute_opt) != 0:
            print(" Souhaitez-vous enregistrer un substitut ? ")
            enter_3 = input(" o : oui / n : Non \n")
            if enter_3 == "o":
                self.save_substitute()
            elif enter_3 == "n":
                pass
            else:
                print(" Veuillez rentrer la bonne option\n")
                self.display_ask_save()
            # Need to reset the value of self.enter_3,
            # otherwise it keeps the old value
            enter_3 = 0
        else:
            pass

    def save_substitute(self):
        """ Can save the couple product / substitute
        in the favorite table of the database """
        while True:
            try:
                enter_4 = int(input(
                    " ** Rentrez le numéro du substitut que vous souhaitez"
                    " enregistrer dans vos favoris : \n "
                    ))
                ind_opt = []
                for ind, product_id in self.substitute_opt:
                    ind_opt.append(ind)
                    if enter_4 == ind:
                        self.id_product_to_save = product_id
                if enter_4 in ind_opt:
                    # Call method save_fav() from the database class
                    # to save the pair (product / substitute)
                    self.dbase.save_favorite(self.id_product_to_compare, self.id_product_to_save)
                else:
                    print(NOT_OPT)
                    self.save_substitute()
                break

            except ValueError:
                print(NOT_INT)

    def display_favorite(self):
        """ Display on the interface some attributes of the product and its substitute """
        print(
            " Liste de vos favoris :\n"
            )
        # Call method get_fav() from the database class
        self.dbase.get_favorite()
        for prod_name, brand_prod, nova_prod, nutri_prod, sub_name, brand_sub, \
        nova_sub, nutri_sub, code_sub, url, store in self.dbase.favorite:
            print(
                "* Produit à substituer:", prod_name,
                "\n Marque :", brand_prod,
                "\n Groupe NOVA :", nova_prod,
                "\n Nutri-score ", nutri_prod, " \n",
                "* Substitut :", sub_name,
                "\n Marque :", brand_sub,
                "\n Groupe NOVA :", nova_sub,
                "\n Nutri-score :", nutri_sub,
                "\n Code produit :", code_sub,
                "\n URL :", url,
                "\n Magasins :", store,
                "\n -----\n"
                )
