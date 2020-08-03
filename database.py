"""

Class Database:
- Has a method (call_api) to request data from the Open Food Facts API
- Regroups all methods to interact with the database using sql queries.

"""


import mysql.connector
import requests

from constants import CONFIG, CATEGORIES, CHOSEN_FIELDS

class Database:
    """ Class to manage the database """
    def __init__(self, db_name):
        """ Initialisation """
        self.cnx = mysql.connector.connect(**CONFIG)
        self.cursor = self.cnx.cursor(buffered=True)
        self.db_name = db_name
        self.category_list = []
        self.id_category_list = 0
        self.product_from_category = 0
        self.product_attributs = 0
        self.substitute_attributs = 0
        self.favorite = 0
        self.json_category_product = 0

    def call_api(self):
        """ Request and import data from the Open Food Facts API """
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        headers = {"User-Agent": "P5_PurBeurre - Version 1.0"}

        # Record products by category in the dictionnary json_cat_prod
        self.json_category_product = {}
        print("\n *******************************************************************\n"
              " ** Requêtes importation de données de l'API Open Food Facts :\n")

        for category in CATEGORIES:
            i = 1
            products_resu = []

            for i in range(1, 15):
                # Search criteria for API
                payload = {
                    "action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "tag_0": category,
                    "tagtype_1": "countries",
                    "tag_contains_1": "contains",
                    "tag_1": "france",
                    "tagtype_2": "categories_lc",
                    "tag_contains_2": "contains",
                    "tag_2": "fr",
                    # Sort by popularity
                    "sort_by": "unique_scans_n",
                    "page": i,
                    "page_size": 10,
                    "json": True
                    }

                req = requests.get(search_url, params=payload, headers=headers)

                results_json = req.json()
                products_json = results_json["products"]

                for product in products_json:
                    product_resu = {
                        k : v for k, v in product.items()
                        if k in CHOSEN_FIELDS and v != ""
                    }
                    if len(product_resu) == len(CHOSEN_FIELDS):
                        products_resu.append(product_resu)
            print(" Catégorie '{}': {} produits importés de l'API Open Food Facts \n" \
                .format(category, len(products_resu)))
            self.json_category_product[category] = products_resu

    def create_database(self):
        """ Method to create a database if it does not exist """
        try:
            # Execute cursor with execute method and pass SQL query
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.db_name + ";")
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()


    def create_table(self):
        """ Method to create tables in the database """
        try:
            self.cursor.execute("USE " + self.db_name + ";")
            # Read the sql queries to create the tables of the database
            with open("table_queries.sql", "r") as table_sql:
                sql_file = table_sql.read()
            table_sql.close()
            # Execute the sql queries from the file
            sql_commands = sql_file.split(';')
            for command in sql_commands:
                self.cursor.execute(command)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def insert_category(self):
        """ Method to insert or update category from JSON data (requested from API) """
        try:
            add_cat = ("INSERT INTO Category (cat_name) VALUES (%s) "
                       "ON DUPLICATE KEY UPDATE cat_name = %s")
            self.category_list = []
            for cat_al in self.json_category_product:
                data_cat = (cat_al, cat_al)
                self.category_list.append(cat_al)
                self.cursor.execute(add_cat, data_cat)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def insert_product(self):
        """ Method to insert or update product from each category
        in the JSON data requested from API """
        try:
            add_prod = (
                "INSERT INTO Product (product_name, generic_name, "
                "cat_id, code_prod, brand_name, url, nova_gps, "
                "nutri_grades, pnns_gps_1, pnns_gps_2, store_name) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE product_name = %s, generic_name = %s, "
                "cat_id = %s, code_prod = %s, brand_name = %s, url = %s, "
                "nova_gps = %s, nutri_grades = %s, pnns_gps_1 = %s, "
                "pnns_gps_2 = %s, store_name = %s"
                )
            print("\n *******************************************************************\n"
                  " Insertion ou Mise à jour des produits :\n ")

            for cat in self.category_list:
                self.cursor.execute("SELECT id FROM Category WHERE cat_name = %s", (cat,))
                id_req = self.cursor.fetchone()
                id_value = id_req[0]
                for food in self.json_category_product[cat]:
                    data_prod = (
                        food["product_name_fr"], food["generic_name_fr"], id_value, food["code"],
                        food["brands"], food["url"], food["nova_groups"], food["nutrition_grades"],
                        food["pnns_groups_1"], food["pnns_groups_2"], food["stores"],
                        food["product_name_fr"], food["generic_name_fr"], id_value, food["code"],
                        food["brands"], food["url"], food["nova_groups"], food["nutrition_grades"],
                        food["pnns_groups_1"], food["pnns_groups_2"], food["stores"]
                        )
                    self.cursor.execute(add_prod, data_prod)
                print(" Nombre de produits insérés ou mis à jour dans la table {}: {} \n" \
                    .format(cat, len(self.json_category_product[cat])))
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def get_category(self):
        """ Get the categories name and id from the database """
        try:
            self.cursor.execute("USE " + self.db_name + ";")
            self.cursor.execute("SELECT id, cat_name FROM Category")
            self.id_category_list = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def get_product_from_category(self, cat_id):
        """ Get products from a category which have bad nova group and nutrition grade """
        try:
            self.cursor.execute("SELECT id, product_name FROM Product WHERE cat_id = %s "
                                "AND nova_gps > 2  AND nutri_grades >= 'c' ", (cat_id,))
            self.product_from_category = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def get_chosen_product(self, id_product_to_compare):
        """ Get some attributes of the product selected by the user """
        try:
            self.cursor.execute("SELECT product_name, brand_name, code_prod, url, nova_gps, "
                                "nutri_grades, cat_id, pnns_gps_1, pnns_gps_2 "
                                "FROM Product WHERE id = %s", (id_product_to_compare,))
            self.product_attributs = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def find_substitute(self):
        """ Find different substitutes to the selected product """
        try:
            self.cursor.execute("SELECT id, product_name, brand_name, nova_gps, "
                                "nutri_grades, code_prod, url, store_name "
                                "FROM Product WHERE cat_id = %s AND "
                                "pnns_gps_1 = %s AND pnns_gps_2 = %s AND "
                                "((nova_gps < %s AND nutri_grades <= %s) OR "
                                "(nova_gps <= %s AND nutri_grades < %s)) "
                                "ORDER BY nova_gps ASC, nutri_grades ASC LIMIT 5",
                                (self.product_attributs[0][6], self.product_attributs[0][7], \
                                	self.product_attributs[0][8], self.product_attributs[0][4], \
                                	self.product_attributs[0][5], self.product_attributs[0][4], \
                                    self.product_attributs[0][5]))
            self.substitute_attributs = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def save_favorite(self, id_product_to_compare, id_product_to_save):
        """ Save in the favorite table the id of the selected product and selected substitute """
        try:
            add_favorite = ("INSERT INTO Favorite_product (prod_id, substitute_id) "
                            "VALUES (%s, %s) ON DUPLICATE KEY UPDATE prod_id = %s, "
                            "substitute_id = %s")
            value_favorite = (id_product_to_compare, id_product_to_save, \
            	id_product_to_compare, id_product_to_save)
            self.cursor.execute(add_favorite, value_favorite)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def get_favorite(self):
        """ Get some attributes from the product and substitute
        of the favorite table using their id """
        try:
            self.cursor.execute("USE " + self.db_name + ";")
            self.cursor.execute("SELECT p1.product_name, p1.brand_name, p1.nova_gps, "
                                "p1.nutri_grades, p2.product_name, p2.brand_name, "
                                "p2.nova_gps, p2.nutri_grades, "
                                "p2.code_prod, p2.url, p2.store_name "
                                "FROM favorite_product AS fp "
                                "INNER JOIN product as p1 ON fp.prod_id = p1.id "
                                "INNER JOIN product as p2 ON fp.substitute_id = p2.id ;")
            self.favorite = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()
