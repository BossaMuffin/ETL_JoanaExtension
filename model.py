'''
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
'''
# constants available in the whole app
import global_constants as g_const
# dependency
from model_scrapping import ModelScrapping
# # #
import lib_display as ds
import pandas as pd
import copy, sys, os
import urllib.request

class Model:
    '''
    Classdocs
    '''
    
    def __init__(self):
        self.scrap = ModelScrapping()
        # Les choix proposés au menu du programme sont compris entre l'indice 1 et l'avant-dernier (réservés au titre et à la question) 
        self.g_asked_day = 0
        self.g_asked_day_in_app = 0

    def start(self):
        e_results_to_return = self.scrap.start()
        print(e_results_to_return['text'])
        return e_results_to_return
    
    def getDictRecettes(self):
        return self.scrap.g_temp_recettes
    
    def updateDictRecettes(self, p_new_recettes):
        self.scrap.g_temp_recettes = p_new_recettes
    
    def update1Portion(self, p_day_id, p_meal_id, p_new_quantity):
        self.scrap.g_temp_recettes[str(p_day_id)][str(p_meal_id)]['portions'] = p_new_quantity 
    
    def getListWeekDays(self):
        return self.scrap.WEEK_DAYS
    
    def getFilesPath(self, p_file_type):
        # p_file_type = 'ingredients'.txt OU 'week'.json
        file_path_to_return = self.scrap.constructFilesPath()[p_file_type]
        return file_path_to_return
    
    def downloadJoanaPngMenu(self):
        e_text_to_return = g_const.OPTIONS['download_menu']
        e_png_url = g_const.URL_API[:-1]+self.scrap.week_png
        e_file_path = self.getFilesPath('menu')
        print(">> Download is starting")
        try:
            urllib.request.urlretrieve(e_png_url, e_file_path)
            self._openFileInNewWindow(e_file_path)
        except:
            e_text_to_return = "Erreur de téléchargement"
            print(">> Download error")
        else:
            e_text_to_return = f'Cible : {g_const.URL_API[:-1]}\n Document : {self.scrap.week_png}\n Téléchargé dans : {e_file_path}'
            print(">> Download ok")
        finally :
            return e_text_to_return
    
    def forceScrapping(self):
        e_text_to_return = self.scrap.scrapCurrentWeek()
        return e_text_to_return
    
    def showMealsByDay(self):
        e_temp_recettes = self.getDictRecettes()
        e_text_to_return = ""
        e_text_to_return += g_const.OPTIONS['show_menu'] + " :\n"
        e_text_to_return += "\n"
        e_text_to_return += ">> "
        e_text_to_return += g_const.WEEK_DAYS[self.g_asked_day]
        for l0_day_meal in e_temp_recettes[str(self.g_asked_day)].values():
            e_text_to_return += "\n"
            e_text_to_return += "\n"
            e_text_to_return += ds.separator(5) + l0_day_meal['name']
            if int(l0_day_meal['portions']) and l0_day_meal['portions'] > 0:
                e_text_to_return += f"\n{'-':<5}{'pour':<10}{l0_day_meal['portions']:<5}{'pax'}"

            if int(l0_day_meal['preparation_time']) and l0_day_meal['preparation_time'] > 0:
                e_text_to_return += f"\n{'-':<5}{'compte':<10}{l0_day_meal['preparation_time']:<5}{'min de prépa'}"

            if int(l0_day_meal['cooking_time']) and l0_day_meal['cooking_time'] > 0:
                e_text_to_return += f"\n{'-':<5}{'et':<10}{l0_day_meal['cooking_time']:<5}{'min de cuisson'}"
            
        print(e_text_to_return)
        return e_text_to_return 
    
    def showIngredients(self):
        e_text_to_return = g_const.OPTIONS['list_ingredients'] + " :\n"
        for l0_i, l0_ingredient_group in self._orderIngredientsInDf().items():
            l1_line = f"{'>':<5}{l0_ingredient_group}"
            e_text_to_return = e_text_to_return + "\n" + l1_line
        print(e_text_to_return)
        return e_text_to_return

    def _orderIngredientsInDf(self):
        e_df_ingredients = pd.DataFrame(columns = ['Category', 'Name' , 'Quantity', 'Symbol'])
        e_nb_lines = 0
        e_temp_recettes = {}
        e_temp_recettes = copy.deepcopy(self.getDictRecettes())
        for l0_day_meals in e_temp_recettes.values():  
            for l1_day_meal in l0_day_meals.values():
                if l1_day_meal['portions'] != 0:
                    for l2_ingredient in l1_day_meal['ingredients'].values():
                        # change ingredients quantity by portions 
                        l2_ingredient['quantity'] = l2_ingredient['quantity'] * l1_day_meal['portions']
                        if l2_ingredient['unit_of_measure']['symbol'] != None:
                            l2_symbol = l2_ingredient['unit_of_measure']['symbol']
                        else:
                            l2_symbol = ""
                        # uniformisation des unités
                        if l2_symbol == 'cs':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*3
                            l2_symbol = 'cc'
                        elif l2_symbol == 'kg':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*1000
                            l2_symbol = 'g'
                        elif l2_symbol == 'cl':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*10
                            l2_symbol = 'ml'
                        elif l2_symbol == 'dl':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*100
                            l2_symbol = 'ml'
                        elif l2_symbol == 'l':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*1000
                            l2_symbol = 'ml'
                        e_df_ingredients.loc[e_nb_lines] = [ l2_ingredient['category']['name'], l2_ingredient['name'], l2_ingredient['quantity'], l2_symbol ]
                        l2_ingredient['unit_of_measure']['symbol'] = l2_symbol
                        e_nb_lines += 1
        e_df_ingredients_sorted = e_df_ingredients.groupby(['Category', 'Name', 'Symbol']).sum()
        return e_df_ingredients_sorted

    def exportIngredientsInFile(self, p_gdh):
        e_file_path = self.getFilesPath('ingredients')
        e_text_to_return = g_const.OPTIONS['export_ingredients'] + " :\n"                                    
        e_nb_lines = 0
        with open(e_file_path, "w") as l0_outfile:
            l0_outfile.write("LISTE DES INGREDIENTS DE LA SEMAINE \n\n-----------------\n")
            l0_outfile.write("Mis à jour le " + p_gdh + "\n-----------------\n\n")
            
            for l1_i, l1_ingredient_group in self._orderIngredientsInDf().items():
                l1_line = f"{'+':<5}{l1_ingredient_group}"
                e_text_to_return = e_text_to_return + "\n" + l1_line
                l0_outfile.write(l1_line + "\n")
                e_nb_lines += 1
        self._openFileInNewWindow(e_file_path)
        e_text_to_return += str(e_nb_lines)
        return e_text_to_return
    
    def _openFileInNewWindow(self, p_file_path):
        if "win" in sys.platform:
            os.startfile(p_file_path)
        else:
            os.system('xdg-open ' + p_file_path)
            