"""
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
"""
import copy
import os
import sys
import urllib.request
from datetime import date, timedelta

import pandas as pd

# constants available in the whole app
import global_constants as g_const
# # #
import lib_display as ds
# dependency
from model_scrapping import ModelScrapping


class Model:
    """
    Classdocs
    """

    def __init__(self):
        self.scrap = ModelScrapping()
        # Les choix proposés au menu du programme sont compris entre l'indice 1 et l'avant-dernier (réservés au titre
        # et à la question)
        self.g_asked_day = 0
        self.g_asked_day_in_app = 0

    def start(self):
        e_results_to_return = self.scrap.start()
        print(e_results_to_return['text'])
        return e_results_to_return

    def getDictRecettes(self):
        return self.scrap.g_temp_recettes

    def _getDateBeginingWeek(self):
        return self.scrap.g_date_begining_week

    def _formatDateBeginingWeek(self, p_date_to_format: _getDateBeginingWeek):
        e_date = p_date_to_format.split('T', 1)
        e_datetime_to_return = date.fromisoformat(e_date[0])
        e_datetime_to_return += timedelta(days=1)
        return e_datetime_to_return

    def _formatDateEndWeek(self, p_datetime_beginning_week: _formatDateBeginingWeek):
        e_datetime_end_week_to_return = p_datetime_beginning_week + timedelta(days=6)
        return e_datetime_end_week_to_return

    def formatDatesToShowInStr(self):
        e_begin_date = self._getDateBeginingWeek()
        e_begin_date = self._formatDateBeginingWeek(e_begin_date)
        e_begin_day = g_const.WEEK_DAYS[e_begin_date.weekday()]
        e_end_date = self._formatDateEndWeek(e_begin_date)
        e_end_day = g_const.WEEK_DAYS[e_end_date.weekday()]
        e_year_to_show = ""
        if e_begin_date.year != e_end_date.year:
            e_year_to_show = f"/{e_begin_date.year}"
        e_dates_str_to_show = f"Semaine du {e_begin_day} {e_begin_date.day}/{e_begin_date.month}{e_year_to_show} au {e_end_day} {e_end_date.day}/{e_end_date.month}/{e_end_date.year}"
        return e_dates_str_to_show

    def updateDictRecettes(self, p_new_recettes):
        self.scrap.g_temp_recettes = p_new_recettes

    def update1Portion(self, p_day_id, p_meal_id, p_new_quantity):
        self.scrap.g_temp_recettes[str(p_day_id)][str(p_meal_id)]['portions'] = p_new_quantity

    def getListWeekDays(self):
        return self.scrap.WEEK_DAYS

    def getFilesPath(self, p_file_type):
        # p_file_type = 'ingredients'.txt OU 'week'.json
        file_path_to_return = self.scrap.constructFilesPath(self.scrap.g_date_begining_week)[p_file_type]
        return file_path_to_return

    def downloadJoanaPngMenu(self):
        e_text_to_return = g_const.OPTIONS['download_menu']
        e_isPngDownloadYet = self.scrap.cd.isWeekPresentInFolder(self._getDateBeginingWeek(), g_const.SCRAPPED_FOLDER,
                                                                 "png")
        if e_isPngDownloadYet['bool']:
            try:
                print(">> Downloaded yet")
                e_file_path = self.getFilesPath('menu')
                self._openFileInNewWindow(e_file_path)
                e_text_to_return = "Fichier déjà téléchargé"
            except:
                e_text_to_return = "Erreur de lecture du fichier"
                print(">> File reading error")
            else:
                e_text_to_return = f'Cible : {g_const.URL_API[:-1]}\n Document présent dans : {e_file_path}'
                print(">> Download ok")

        else:
            e_png_url = g_const.URL_API[:-1] + self.scrap.week_png
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
            finally:
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
        e_df_ingredients = pd.DataFrame(columns=['Category', 'Name', 'Quantity', 'Symbol'])
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
                            l2_ingredient['quantity'] = l2_ingredient['quantity'] * 3
                            l2_symbol = 'cc'
                        elif l2_symbol == 'kg':
                            l2_ingredient['quantity'] = l2_ingredient['quantity'] * 1000
                            l2_symbol = 'g'
                        elif l2_symbol == 'cl':
                            l2_ingredient['quantity'] = l2_ingredient['quantity'] * 10
                            l2_symbol = 'ml'
                        elif l2_symbol == 'dl':
                            l2_ingredient['quantity'] = l2_ingredient['quantity'] * 100
                            l2_symbol = 'ml'
                        elif l2_symbol == 'l':
                            l2_ingredient['quantity'] = l2_ingredient['quantity'] * 1000
                            l2_symbol = 'ml'
                        e_df_ingredients.loc[e_nb_lines] = [l2_ingredient['category']['name'], l2_ingredient['name'],
                                                            l2_ingredient['quantity'], l2_symbol]
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
            l_safe_file_path = r'/'.join((os.getcwd(), p_file_path))
            print(l_safe_file_path)
            try:
                os.startfile(l_safe_file_path)
            except FileNotFoundError as err:
                print(f'{l_safe_file_path} est introuvable')
                print(f'Tu peux l\'ouvrir directement dans {os.getcwd()}/{g_const.SCRAPPED_FOLDER}')

        else:
            os.system('xdg-open ' + p_file_path)
