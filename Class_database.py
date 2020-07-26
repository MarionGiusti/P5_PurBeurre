"""

Class Database: 
- Has a method (call_api) to request data from the Open Food Facts API
- Regroups all methods to interact with the database using sql queries.

"""


import mysql.connector
import random
import requests
import json

from PB_constants import CONFIG, CATEGORIES, CHOSEN_FIELDS


class Database:
	def __init__(self, db_name):
		""" Initialisation """
		self.cursor = None
		self.cnx = None
		self.db_name = db_name
		self.cat_list = 0
		self.id_cat_list = 0
		self.prod_from_cat = 0
		self.prod_attr = 0
		self.subst_attr = 0
		self.fav = 0
		self.JSON_CAT_PROD = 0
		
		self.cnx = mysql.connector.connect (**CONFIG)
		self.cursor = self.cnx.cursor(buffered=True)

	def call_api(self):
		""" Request and import data from the Open Food Facts API """
		SEARCH_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
		HEADERS = {"User-Agent": "P5_PurBeurre - Version 1.0"}

		# Record products by category in the dictionnary JSON_CAT_PROD
		self.JSON_CAT_PROD = {}
		print("\n ********************************************************************************************** \n"
			" ** Requêtes importation de données de l'API Open Food Facts :\n")

		for category in CATEGORIES:
		  i = 1
		  products_resu = []

		  for i in range(1, 15):
		        #Search criteria for API
		        PAYLOAD = {"action": "process",
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

		        r = requests.get(SEARCH_URL, params=PAYLOAD, headers=HEADERS)

		        results_json = r.json()
		        products_json = results_json["products"]

		        for product in products_json:
		            product_resu = {
		            k : v for k, v in product.items()
		            if k in CHOSEN_FIELDS and v != ""
		            }  
		            if len(product_resu) == len(CHOSEN_FIELDS):
		              products_resu.append(product_resu)
		  print(" Catégorie '{}': {} produits importés de l'API Open Food Facts \n".format(category, len(products_resu)))
		  self.JSON_CAT_PROD[category] = products_resu
		# Can save the data in a json file
		# with open('JSON_CAT_PROD.json','w') as f:
		#   f.write(json.dumps(self.JSON_CAT_PROD, indent=4))

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
			with open('table_queries.sql', 'r') as fd:
				sqlFile = fd.read()
			fd.close()
			i = 0
			table_name = ["Category", "Product", "Favorite_product"]
			# Execute the sql queries from the file
			self.cursor.execute(sqlFile, multi=True)
			self.cnx.commit()
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()

	def insert_cat(self):
		""" Method to insert or update category from JSON data (requested from API) """
		add_cat = ( " INSERT INTO Category (cat_name) VALUES (%s) ON DUPLICATE KEY UPDATE cat_name = %s " )
		category_list = []
		for cat_al in self.JSON_CAT_PROD:
			data_cat = (cat_al, cat_al)
			category_list.append(cat_al) 
			self.cursor.execute(add_cat, data_cat)
		self.cnx.commit()
		# Save the list of categories
		self.cat_list = category_list

	def insert_product(self):
		""" Method to insert or update product from each category in the JSON data requested from API """
		try:
			add_prod = ( " INSERT INTO Product "
		 " (product_name, generic_name, cat_id, code_prod, brand_name, url, nova_gps, nutri_grades, pnns_gps_1, pnns_gps_2, store_name)"
		 " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
		 " ON DUPLICATE KEY UPDATE product_name = %s, generic_name = %s, cat_id = %s, code_prod = %s, brand_name = %s, "
		 " url = %s, nova_gps = %s, nutri_grades = %s, pnns_gps_1 = %s, pnns_gps_2 = %s, store_name = %s" )
			print("\n **********************************************************************************************\n"
				" Insertion ou Mise à jour des produits :\n ")

			for cat in self.cat_list:
				self.cursor.execute( " SELECT id FROM Category WHERE cat_name = %s ", (cat,))
				id_req = self.cursor.fetchone()
				id_value = id_req[0]
				for al in self.JSON_CAT_PROD[cat]:
					data_prod = (al["product_name_fr"], al["generic_name_fr"], id_value, al["code"], al["brands"], 
						al["url"], al["nova_groups"], al["nutrition_grades"], al["pnns_groups_1"], al["pnns_groups_2"], al["stores"],
						al["product_name_fr"], al["generic_name_fr"], id_value, al["code"], al["brands"], 
						al["url"], al["nova_groups"], al["nutrition_grades"], al["pnns_groups_1"], al["pnns_groups_2"], al["stores"])
					self.cursor.execute(add_prod, data_prod)
				print(" Nombre de produits insérés ou mis à jour dans la table {}: {} \n".format(cat, len(self.JSON_CAT_PROD[cat])))
			self.cnx.commit()
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()

	def get_categories(self):
		""" Get the categories name and id from the database """
		try:
			self.cursor.execute("USE " + self.db_name + ";")
			self.cursor.execute("SELECT id, cat_name FROM Category")
			cat_req = self.cursor.fetchall()
			self.id_cat_list = cat_req
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()

	def get_prod_from_cat(self, cat_id):
		""" Get products from a category which have bad nova group and nutrition grade """
		try:
			self.cursor.execute("SELECT id, product_name FROM Product WHERE cat_id = %s AND nova_gps > 2  AND nutri_grades >= 'c' ", (cat_id,))
			prod_req = self.cursor.fetchall()
			self.prod_from_cat = prod_req
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()

	def get_chosen_prod(self, id_prod_to_comp):
		""" Get some attributes of the product selected by the user """
		try:
			self.cursor.execute("SELECT product_name AS Produit, brand_name AS Marque, code_prod AS CODE_PROD, url AS URL, nova_gps AS CL_NOVA, "
				" nutri_grades AS NUTRI_SC, cat_id, pnns_gps_1, pnns_gps_2 FROM Product WHERE id = %s", (id_prod_to_comp,))
			self.prod_attr = self.cursor.fetchall()
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()

	def find_substitute(self):
		""" Find different substitutes to the selected product """
		try:
			self.cursor.execute("SELECT id AS ID, product_name AS Produit, brand_name AS Marque, nova_gps AS CL_NOVA, "
				" nutri_grades AS NUTRI_SC, code_prod AS CODE_PROD, url AS URL, store_name AS SHOP FROM Product WHERE cat_id = %s AND pnns_gps_1 = %s AND pnns_gps_2 = %s AND "
				" ((nova_gps < %s AND nutri_grades <= %s) OR (nova_gps <= %s AND nutri_grades < %s))"
				" ORDER BY nova_gps ASC, nutri_grades ASC LIMIT 5", 
				(self.prod_attr[0][6], self.prod_attr[0][7], self.prod_attr[0][8], self.prod_attr[0][4],self.prod_attr[0][5], self.prod_attr[0][4],self.prod_attr[0][5]))
			self.subst_attr = self.cursor.fetchall()
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()

	def save_fav(self, id_prod_to_comp, id_prod_to_save):
		""" Save in the favorite table the id of the selected product and selected substitute """
		try:
			add_fav = ("INSERT INTO Favorite_product (prod_id, substitute_id) "
					"VALUES (%s, %s) ON DUPLICATE KEY UPDATE prod_id = %s, substitute_id = %s " )
			value_fav = (id_prod_to_comp, id_prod_to_save, id_prod_to_comp, id_prod_to_save)
			self.cursor.execute(add_fav, value_fav)
			self.cnx.commit()
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()
		#except mysql.connector.errors.IntegrityError as err:
		#	print(err)
		# 	print()
		# 	print(" Ce couple produit / substitut est déjà enregistré dans vos favoris")
		#	self.cnx.rollback()

	def get_fav(self):
		""" Get some attributes from the product and substitute of the favorite table using their id """
		try:
			self.cursor.execute("USE " + self.db_name + ";")
			self.cursor.execute("SELECT p1.product_name AS Nom_Prod, p1.brand_name AS Marque, p1.nova_gps, p1.nutri_grades, " 
				" p2.product_name AS Nom_substitut, p2.brand_name AS Marque, p2.nova_gps, p2.nutri_grades, p2.code_prod AS Code, p2.url AS URL, p2.store_name AS Magasins"
				" FROM favorite_product AS fp"
				" INNER JOIN product as p1 ON fp.prod_id = p1.id"
				" INNER JOIN product as p2 ON fp.substitute_id = p2.id ;")
			self.fav = self.cursor.fetchall()
		except mysql.connector.Error as err:
			print(err)
			self.cnx.rollback()
