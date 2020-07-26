"""

Class InterfaceManager: 
Regroups all methods which allow the user to interact with the PurBeurre interface.

"""
from Class_database import *
from PB_constants import QUEST, INPUT_OPT, OPT0, OPT1, OPT2, OPT3, NOT_OPT, NOT_INT


class InterfaceManager:
	""" Class to manage the interface """
	def __init__(self, db):
		""" Initialisation """
		self.db = Database(db.db_name)
		self.option = 0
		self.enter_1 = 0
		self.enter_2 = 0
		self.rand_cat_opt = 0
		self.rand_prod_opt = 0
		self.id_prod_to_comp = 0
		self.substitut_opt = 0 

	def welcome(self):
		""" Welcoming message when opening PurBeurre application """
		print()
		print("       *****************************")
		print("       *                           *")
		print("       * BIENVENUE SUR PURBEURRE ! *")
		print("       *                           *")
		print("       *****************************\n")
		print()
		print("*****************************************************\n")

	def goodbye(self):
		""" Goodbye message when closing the PurBeurre application """
		print()
		print("*****************************************************\n")
		print()
		print("       *****************************")
		print("       *                           *")
		print("       * A BIENTOT SUR PURBEURRE ! *")
		print("       *                           *")
		print("       *****************************\n")
		print()
		quit()

	def display_menu(self):
		""" Main menu: Display different options for the user and wait for the user input """
		while True:
			try:
				# Need to reset the value of self.enter_2, otherwise it keeps the old value
				self.enter_2 = 0
				# Print options				
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
				# Print options				
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

	def random_cat(self):
		""" Display 3 random categories """
		# Call method get_categories() from the database class
		self.db.get_categories()
		k = 3
		i = 1
		rand_cat_id = []
		# choose randomly 3 categories from all the categories of the database
		rand_cat = random.sample(self.db.id_cat_list, k)
		while i <= k:
		 	for idd, cat in rand_cat:
		 		print(i,"-", cat)
		 		cat_option = [i, idd, cat]
		 		rand_cat_id.append(cat_option) 
		 		i += 1
		# save the indice, id and cat_name of the category chosen by the user. Useful for methods verif_input1() and random_prod()		
		self.rand_cat_opt = rand_cat_id

	def verif_input1(self):
		""" Verification of the user input, self.enter_1 must be in the proposed categories """
		while True:
			try:
				self.enter_1 = int(input(" ** Rentrez le numéro de la catégorie souhaitée : \n "))
				ind_opt = []
				for ind, cat_id, cat_name in self.rand_cat_opt:
					ind_opt.append(ind)
				while self.enter_1 not in ind_opt:
					print("\n", NOT_OPT)
					self.verif_input1()
				break
			except ValueError:
				print(NOT_INT)

	def random_prod(self, enter_1):
		""" Display 6 random products from the category selected by the users """
		k = 6
		i = 1
		for ind, cat_id, cat_name in self.rand_cat_opt:
			if ind == self.enter_1:
				# Call method get_prod_from_cat() from the database class
				self.db.get_prod_from_cat(cat_id)
				# Select 6 random products and save them in the rand_prod variable
				rand_prod = random.sample(self.db.prod_from_cat, k)
		rand_prod_id = []
		while i <= k:
		 	for idd, prod in rand_prod:
		 		print(i,"-", prod)
		 		prod_option = [i, idd, prod]
		 		rand_prod_id.append(prod_option) 
		 		i += 1
		# Save the indice, id and product_name of the product chosen by the user. Useful for methods verif_input2()
		self.rand_prod_opt = rand_prod_id

	def verif_input2(self):
		""" Verification of the user input, self.enter_2 must be in the proposed products """
		while True:
			try:
				self.enter_2 = int(input(" ** Rentrez le numéro du produit souhaité : \n "))
				ind_opt = []
				for ind, prod_id, prod_name in self.rand_prod_opt:
					ind_opt.append(ind)
					if self.enter_2 == ind:
						# Save the id of the product to substitute. Useful in the method display_chosen_prod() and save_substitute()
						self.id_prod_to_comp = prod_id
						pass					
				while self.enter_2 not in ind_opt:
					print("\n", NOT_OPT)
					self.verif_input2()
				break
			except ValueError:
				print(NOT_INT)

	def display_chosen_prod(self):
		""" Display the selected product with some descriptions """
		# Call method get_chosen_prod() from the database class
		self.db.get_chosen_prod(self.id_prod_to_comp)
		print(" ***** Produit à substituer sélectionné :\n "
			" Produit | Marque | Gpe Nova | Nutri-score | Code produit | URL \n")
		print(" ", self.db.prod_attr[0][0], "|", self.db.prod_attr[0][1], "|", self.db.prod_attr[0][4], "|", 
			self.db.prod_attr[0][5], "|", self.db.prod_attr[0][2], "|", self.db.prod_attr[0][3] )

	def display_substitute(self):
		""" Display different substitutes on the interface with some descriptions """
		print(" ***** Voici des substituts à l'aliment sélectionné (meilleur nutri-score et classification nova) :\n "
				" Produit | Marque | Gpe Nova | Nutri-score | Code produit OpenFoodFacts | URL | Magasin(s) \n\n")
		# Call method find_substitute() from the database class
		self.db.find_substitute()
		i = 1
		substitut_id = []
		for idd, prod_name, brand_name, nova_gps, nutri_grades, store_name, code_prod, url in self.db.subst_attr:
			print (i, "-", prod_name," | ", brand_name," | ", nova_gps," | ", nutri_grades," | ", store_name," | ", code_prod, "|", url, "\n")
			substitut_option = [i, idd]
			substitut_id.append(substitut_option)
			i += 1
		if len(substitut_id) == 0:
			print(" Excusez-nous, nous n'avons pas trouvé de substituts pour ce produit !\n ")
		# Save the id of the chosen substitute. Useful in the methods display_ask_save() and save_substitute()
		self.substitut_opt = substitut_id

	def display_ask_save(self):
		""" Option to save (or not save) in the favorite table of the database, a pair which includes : a product and a substitute """
		if len(self.substitut_opt) != 0:
			print(" Souhaitez-vous enregistrer un substitut ? ")
			enter_3 = input(" o : oui / n : Non \n")
			if enter_3 == "o":
					self.save_substitute()
			elif enter_3 == "n":
				pass
			else:
				print(" Veuillez rentrer la bonne option\n")
				self.display_ask_save()
			# Need to reset the value of self.enter_3, otherwise it keeps the old value
			enter_3 = 0
		else:
			pass
		
	def save_substitute(self):
		""" Can save the couple product / substitute in the favorite table of the database """
		while True:
			try:
				enter_4 = int(input(" ** Rentrez le numéro du substitut que vous souhaitez enregistrer dans vos favoris : \n "))
				ind_opt = []
				for ind, prod_id in self.substitut_opt:
					ind_opt.append(ind)
					if enter_4 == ind:
						self.id_prod_to_save = prod_id
				if enter_4 in ind_opt:
					# Call method save_fav() from the database class to save the pair (product / substitute)
					self.db.save_fav(self.id_prod_to_comp, self.id_prod_to_save)				
				else:
					print(NOT_OPT)
					self.save_substitute()
				break

			except ValueError:
				print(NOT_INT)

	def display_fav(self):
		""" Display on the interface some attributes of the product and its substitute """
		print(" Liste de vos favoris (chaque ligne = un aliment associé à un de ses substitut) :\n "
			" * Produit initiale | Marque | Gpe Nova | Nutri-score | \n"
			" Substitut | Marque | Gpe Nova | Nutri-score | Code produit OpenFoodFacts | URL | Magasin(s) \n\n")
		#  Call method get_fav() from the database class
		self.db.get_fav()
		for prod_name, brand_prod, nova_prod, nutri_prod, sub_name, brand_sub, nova_sub, nutri_sub, code_sub, url, store in self.db.fav:
			print ("* ", prod_name, " | ", brand_prod, " | ", nova_prod, " | ", nutri_prod, " \n ",
				sub_name, " | ", brand_sub, " | ", nova_sub, " | ", nutri_sub, " | ", code_sub, "|", url, " | ", store, "\n" )
