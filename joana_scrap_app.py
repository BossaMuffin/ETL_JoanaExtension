#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# # SCRAPPING JOANA&VOUS 
import lib_display as ds
import joana_scrap_class
import sys
import lorem
# Import view func tkinter 
import tkinter as tkt

joana = joana_scrap_class.Scrap()

joana.initAppScrapping()

try:
    joana.initAppScrapping()
except:
    print(">> Scrap init error")
else:
    print('>> Loading recettes file and init portions...')
    joana.initRecettesDatas()
    print('Init ok')

#joana.scrapCurrentWeek()
#joana.showMeals()
#joana.showIngredients()
#joana.updatePortions()
#joana.printIngredientsInFile()

# APP VIEW
class UseDatasInView(tkt.Tk):
    
    def __init__(self):
        self.LOREM = lorem.get_word(count=100)
        
        tkt.Tk.__init__(self)    
        self.BG_CLR = 'white'
        self.BG_CLR_1 = "#41B77F"
        self.BG_CLR_2 = "#f2f2f2"
        self.TXT_CLR = 'white'
        self.GTRY = '1080x'+str(self.winfo_screenheight())
        self.MIN_WIDTH = 720
        self.MIN_HEIGHT = 720
        self.WIDTH_BTN = 20
        self.IPADY_CONTENT = 20
        self.WIDTH_CONTENT_AREA=self.MIN_WIDTH
        self.LOGO_ICO = 'logo.ico'
        self.BORDER = 1
        
        #Create the main window
        self.title("Titre fenêtre")
        self.geometry(self.GTRY)
        #self.iconbitmap("img/icon_checked.ico")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.config(background=self.BG_CLR)
        self.resizable(width=True, height=True)
        #self.attributes('-fullscreen', True) 
        
        self.frame_buttons = tkt.Frame(self, bg=self.BG_CLR_1)
        self.btn_opt_menu = tkt.Button(self.frame_buttons, 
                                  text="Bouton menu", 
                                  command=self.showWeekMenu, 
                                  width=self.WIDTH_BTN)
        self.btn_opt_portions = tkt.Button(self.frame_buttons, 
                                      text="Bouton portions", 
                                      command=self.showAppPortions, 
                                      width=self.WIDTH_BTN)
        self.btn_opt_ingredients = tkt.Button(self.frame_buttons, 
                                         text="Bouton ingrédients", 
                                         command=self.showIngredientsList, 
                                         width=self.WIDTH_BTN)
        
        self.btn_opt_menu = tkt.Button(self.frame_buttons, 
                                  text="Bouton menu", 
                                  command=self.showWeekMenu, 
                                  width=self.WIDTH_BTN)
        self.btn_opt_portions = tkt.Button(self.frame_buttons, 
                                      text="Bouton portions", 
                                      command=self.showAppPortions, 
                                      width=self.WIDTH_BTN)
        self.btn_opt_ingredients = tkt.Button(self.frame_buttons, 
                                         text="Bouton ingrédients", 
                                         command=self.showIngredientsList, 
                                         width=self.WIDTH_BTN)
        self.label_space = tkt.Label(self.frame_buttons, 
                                     bg=self.BG_CLR_1, 
                                     text='')
        self.asked_day = 0
        self.asked_day_in_app = 0
        self.btn_choosing_day = {}
        self.btn_choosing_day_in_app = {}
        for l0_i, l0_day in enumerate(joana.WEEK_DAYS):
            self.btn_choosing_day[l0_i] = tkt.Button(self.frame_buttons, 
                                                     text=l0_day, 
                                                     width=self.WIDTH_BTN,
                                                     command=lambda day_id=l0_i : self.chooseDayToShow(p_day_id=day_id, p_current_view='menu'))
            
            self.btn_choosing_day_in_app[l0_i] = tkt.Button(self.frame_buttons,
                                                            text=l0_day, 
                                                            width=self.WIDTH_BTN,
                                                            command=lambda day_id=l0_i : self.chooseDayToShowInApp(day_id))
        
        self.frame_content = tkt.Frame(self,
                                       width=self.WIDTH_CONTENT_AREA,
                                       bg=self.BG_CLR_2)
        
        self.message_to_show = tkt.StringVar()
        #e_bourrage = self.LOREM
        e_bourrage = ''
        self.message_to_show.set('Bienvenue \n Tu vas pouvoir personnaliser ton menu de la semaine à partir des propositions de Joana. \n'+e_bourrage)
        self.message_content = tkt.Message(self.frame_content, 
                                      text="Text par défaut", 
                                      textvariable=self.message_to_show, 
                                      width=self.WIDTH_CONTENT_AREA, 
                                      justify="left")
        
        #Define none displayed elements
        self.btn_quit_app_portions = tkt.Button(self.frame_buttons, 
                                           text="Bouton quitter", 
                                           command=self.quitAppPortions, 
                                           width=self.WIDTH_BTN)

        self.frame_app_portions = tkt.Frame(self.frame_content, 
                                            bg=self.BG_CLR_2,  
                                            width=self.WIDTH_CONTENT_AREA)
        self.frame_by_day = {}
        self.label_by_day = {}
        for l0_i, l0_day in enumerate(joana.WEEK_DAYS):
            self.frame_by_day[l0_i] = tkt.Frame(self.frame_app_portions, 
                                       width=self.WIDTH_CONTENT_AREA)
            self.label_by_day[l0_i] = tkt.Label(self.frame_by_day[l0_i], 
                                       text=joana.WEEK_DAYS[l0_i],
                                       width=self.WIDTH_CONTENT_AREA)
            self.label_by_day[l0_i].pack(pady=2)
            for l1_i, l1_day_meal in enumerate(joana.temp_recettes[str(l0_i)].values()):
                e_current_btn_txt = tkt.StringVar()
                ds.separator()
                e_frame_slider_by_meal = tkt.Frame(self.frame_by_day[l0_i], 
                                                   width=self.WIDTH_CONTENT_AREA)
                e_btn_by_meal = tkt.Button(e_frame_slider_by_meal, 
                                                       text="Valider",
                                                       textvariable=e_current_btn_txt)
                e_current_btn_txt.set("Valider")
                e_scale_by_meal = tkt.Scale(e_frame_slider_by_meal, 
                                        orient='horizontal', 
                                        from_=0, to=3,
                                        resolution=1, 
                                        tickinterval=1, 
                                        length=self.WIDTH_CONTENT_AREA/2, 
                                        label=l1_day_meal['name'])  
                e_scale_by_meal.set(joana.temp_recettes[str(l0_i)][str(l1_i+1)]["portions"])
                e_btn_by_meal['command'] = lambda day_id=l0_i, meal_id=l1_i, scale=e_scale_by_meal, btn_text=e_current_btn_txt: self.updatePortion(day_id, meal_id, scale, btn_text)
                e_frame_slider_by_meal.pack(pady=2)
                e_scale_by_meal.pack()
                e_btn_by_meal.pack()

        self.initView()
        self.frame_buttons.pack(side="left", fill='y', padx= 30, ipadx=10, ipady=20)
        self.showNavButtons()
        self.showContent()
        self.showContentMessage()

    
    def initView(self):
        # Create the app window
        self.frame_title = tkt.Frame(self, 
                                bg="blue", 
                                width=self.MIN_WIDTH, 
                                height=self.MIN_HEIGHT)
        self.label_title = tkt.Label(self.frame_title, 
                                text='Menu de la semaine', 
                                bg=self.BG_CLR_1, 
                                fg=self.TXT_CLR)
        self.label_subtitle = tkt.Label(self.frame_title, 
                                   text='Hello Judith', 
                                   bg=self.BG_CLR_1, 
                                   fg=self.TXT_CLR)
        self.frame_title.pack(fill='x')
        self.label_title.pack(fill='x')
        self.label_subtitle.pack(fill='x')
        self.showPortionsScalesByDay(p_asked_day=0)
        
        
    def chooseDayToShowInApp(self, p_day_id):
        self.hidePortionsScalesByDay()
        self.asked_day_in_app = p_day_id
        self.showPortionsScalesByDay(p_asked_day=self.asked_day_in_app)
    
    def chooseDayToShow(self, p_day_id, p_current_view='menu'):
        self.asked_day = p_day_id
        if p_current_view == 'menu':
            e_text = joana.showMealsByDay(p_asked_day=self.asked_day)
            self.message_to_show.set(e_text)
    
    def showEmptySpace(self):
        self.label_space.pack(fill='x', pady=2)
    
    def hideEmptySpace(self):
        self.label_space.pack_forget()
        
    def showNavButtons(self):
        self.btn_opt_menu.pack(fill='x', pady=2)
        self.btn_opt_portions.pack(fill='x', pady=2)
        self.btn_opt_ingredients.pack(fill='x', pady=2)
        
    def hideNavButtons(self):
        self.btn_opt_menu.pack_forget()
        self.btn_opt_portions.pack_forget()
        self.btn_opt_ingredients.pack_forget()
    
    def showDaysButtons(self):
        self.showEmptySpace()
        for l0_i in range(len(joana.WEEK_DAYS)):
            self.btn_choosing_day[l0_i].pack(fill='x', pady=2)
    
    def hideDaysButtons(self):
        self.hideEmptySpace()
        for l0_i in range(len(joana.WEEK_DAYS)):
            self.btn_choosing_day[l0_i].pack_forget()

    def showDaysButtonsInApp(self):
        self.showEmptySpace()
        for l0_i in range(len(joana.WEEK_DAYS)):
            self.btn_choosing_day_in_app[l0_i].pack(fill='x', pady=2)
    
    def hideDaysButtonsInApp(self):
        self.hideEmptySpace()
        for l0_i in range(len(joana.WEEK_DAYS)):
            self.btn_choosing_day_in_app[l0_i].pack_forget()

    def showContent(self):
        self.frame_content.pack(side='left', fill='both')

    def showContentMessage(self):
        self.message_content.pack(fill='both', ipady=10, ipadx=50)
        
    def hideContentMessage(self):
        self.message_content.pack_forget()
    
    def showWeekMenu(self):
        self.showDaysButtons()
        e_text = joana.showMealsByDay(self.asked_day_in_app)
        self.message_to_show.set(e_text)

    # App to change portions of meals
    def showAppPortions(self):
        self.hideDaysButtons()
        self.hideNavButtons()
        self.hideContentMessage()
        self.btn_quit_app_portions.pack(fill='x', pady=2) 
        self.showDaysButtonsInApp()
        self.frame_app_portions.pack(side='left', fill='y', ipady=10, ipadx=50)
        
    def showIngredientsList(self):
        self.hideDaysButtons()
        e_text = joana.showIngredients()
        self.message_to_show.set(e_text)
    
    def showPortionsScalesByDay(self, p_asked_day):
        self.frame_by_day[p_asked_day].pack(pady=2)
        
    def hidePortionsScalesByDay(self):
        self.frame_by_day[self.asked_day_in_app].pack_forget()
            
    def updatePortion(self, p_day_id, p_meal_id, p_meal_scale, p_btn_txt):    
        p_meal_id = p_meal_id+1
        joana.temp_recettes[str(p_day_id)][str(p_meal_id)]['portions'] = p_meal_scale.get() 
        e_new_text_btn = "Jude, c'est ok pour " + str(p_meal_scale.get())
        p_btn_txt.set(e_new_text_btn)
    
    def quitAppPortions(self):
        self.frame_app_portions.pack_forget()
        self.btn_quit_app_portions.pack_forget()
        self.showNavButtons()
        self.hideDaysButtonsInApp()
        self.showContentMessage()


# In[ ]:


if __name__== "__main__":
        #Create the application in a Tkinter window
        app = UseDatasInView()
        #Events manager
        app.mainloop()
        


# In[ ]:




