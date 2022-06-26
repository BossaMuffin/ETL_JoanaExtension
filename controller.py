'''
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
'''
import lib_display as ds
ds.printn()
from model import Model
from view import TkView
from datetime import datetime
from time import strftime

class Controller:
    '''
    Classdocs
    '''
    
    def __init__(self, p_model, p_view):
        self.model = p_model
        self.view = p_view

    def start(self):
        print(">> Joana's patch is begining")
        print(">> Start the model")
        self.model.main()
        print(">> Setup the view")
        self.view.setup(self)
        print(">> Start to loop")
        self.view.startMainLoop()
    
    def getDictRecettes(self):
        return self.model.getDictRecettes()
    
    def updateDictRecettes(self, p_new_recettes):
        self.model.g_temp_recettes = p_new_recettes
    
    def _getAskedDay(self):
        return self.g_asked_day

    def _updateAskedDay(self, p_int_day):
        self.model.g_asked_day = p_int_day
    
    def getAskedDayInPortionsApp(self):
        return self.model.g_asked_day_in_app

    def _updateAskedDayInPortionsApp(self, p_int_day):
        self.model.g_asked_day_in_app = p_int_day
    
    def showWeekMenu(self):
        self.view.showDaysButtons()
        e_text_result = self.model.showMealsByDay()
        self.view.var_message_to_show.set(e_text_result)
    
    # App to change portions of meals
    def showPortionsApp(self):
        self.view.hideDaysButtons()
        self.view.hideNavButtons()
        self.view.hideContentMessage()
        self.view.btn_hide_portionsApp.pack(fill='x', pady=2) 
        self.view.showDaysButtonsInApp()
        self.view.showPortionsScalesByDay(self.model.g_asked_day_in_app)
        self.view.frame_portionsApp.pack(side='left', fill='y', ipady=10, ipadx=50)
    
    def showIngredientsList(self):
        self.view.hideDaysButtons()
        e_text_result = self.model.showIngredients()
        self.view.var_message_to_show.set(e_text_result)
        
    def exportIngredientsInFile(self):
        e_horaire = str(datetime.now())
        self.model.exportIngredientsInFile(e_horaire)
        e_text_result = f'Fichier bien enregistré : {self.model.getFilesPath("ingredients")} \n à {e_horaire} '
        self.view.var_message_to_show.set(e_text_result)
        
    def getListWeekDays(self):
        return self.model.getListWeekDays()
            
    def chooseDayToShow(self, p_day_id, p_current_view='menu'):
        print(self.model.g_asked_day)
        self.model.g_asked_day = p_day_id
        print(self.model.g_asked_day)
        if p_current_view == 'menu':
            e_text_result = self.model.showMealsByDay()
            self.view.var_message_to_show.set(e_text_result)
            
    def chooseDayToShowInApp(self, p_day_id):
        self.view.hidePortionsScalesByDay()
        self.model.g_asked_day_in_app = p_day_id
        self.view.showPortionsScalesByDay(self.model.g_asked_day_in_app)
        
    def hidePortionsApp(self):
        self.view.frame_portionsApp.pack_forget()
        self.view.btn_hide_portionsApp.pack_forget()
        self.view.showNavButtons()
        self.view.hideDaysButtonsInApp()
        self.view.showContentMessage()
    
    def updatePortion(self, p_day_id, p_meal_id, p_meal_scale, p_var_btn_txt):    
        e_temp_recettes = self.getDictRecettes()
        p_meal_id += 1
        self.model.update1Portion(p_day_id, p_meal_id, p_meal_scale.get())
        e_new_text_btn = "Jude, c'est ok pour " + str(p_meal_scale.get())
        p_var_btn_txt.set(e_new_text_btn)
        print(e_temp_recettes[str(p_day_id)][str(p_meal_id)]['name'], ' to ', str(p_meal_scale.get()))

        
if __name__== "__main__":
    # # SCRAPPING JOANA&VOUS 
    joana_patch = Controller(Model(), TkView())
    joana_patch.start()