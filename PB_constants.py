"""

Constants of the Database, Constants for the API requests and Constants for the menu

"""

import os

#------------ Some Categories from OpenFood Facts ------------#
CATEGORIES = [
    "Boissons",
    "Viandes",
    "Produits laitiers",
    "Plats préparés",
    "Biscuits et gâteaux",
    "Desserts",
    "Produits de la mer"
    ]

#------------ Some useful fields required for each product requested ------------#
CHOSEN_FIELDS = [
    "product_name_fr",
    "generic_name_fr",
    "code",
    "url",
    "brands",
    "nutrition_grades",
    "nova_groups",
    "pnns_groups_1",
    "pnns_groups_2",
    "stores"
    ]

#------------ Configuration Database ------------#
CONFIG = {
    "host" : "localhost",
    "user" : "root",
    "passwd" : os.getenv("DB_PWD")
}

#------------ Options interface menu ------------#
QUEST = " ***** Souhaitez-vous :\n"
OPT0 = "     0- Retourner au menu ?\n"
OPT1 = "     1- Remplacer un aliment ?\n"
OPT2 = "     2- Retrouver mes aliments substitués?\n"
OPT3 = "     3- Quitter PUR BEURRE ?\n"
INPUT_OPT = " ** Rentrez le numéro de l'option :\n"
NOT_OPT = " Oups ! Ce choix n'est pas dans les options\n"
NOT_INT = " Oups !  Ce n'est pas un nombre... Rentrez une option valide !\n"
