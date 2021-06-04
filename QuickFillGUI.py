# -*- coding: utf-8 -*-
from traceback import print_tb
import version1
from kivy.core.window import Window #
from kivy.lang import Builder
import os
import json
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import pandas as pd
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
#from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
import sys



root_kv ='welcome.kv' 
df = {}  # dataframe
PartitionResult = [] #liste de partition
Examples = [] # ens des exemples d'entree sortie
BoolClassifierResult  = {}

class MainApp(MDApp):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file(root_kv)
        self.title = "Strings Manipulation"
        Window.maximize() 
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        

        menu_items = []

        self.menu = MDDropdownMenu(
            caller=self.screen.ids.dropdown_item,
            items=menu_items,
            width_mult=3,
        )
        self.menu.bind()

       
        self.menu2 = MDDropdownMenu(
            caller=self.screen.ids.dropdown_item2,
            items=menu_items,
            width_mult=3,
        )        
        self.menu2.bind() # declencher les evenements

        self.menu3 = MDDropdownMenu(
            caller=self.screen.ids.dropdown_item3,
            items=menu_items,
            width_mult=3,
        )
        self.menu3.bind() 

        self.menu4 = MDDropdownMenu(
            caller=self.screen.ids.dropdown_item4,
            items=menu_items,
            width_mult=3,
        )
        self.menu4.bind() 
        


    def build(self):
         return self.screen 

###### gestionnaire de fichier

    def file_manager_open(self):
        self.file_manager.show(os.path.dirname(os.path.abspath(__file__)))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()
        file_name = path.split('/')[-1]
        file_extend = file_name.split('.')
        if((file_extend[-1]).lower()) != 'csv':
            self.show_confirmation_dialog("Veuillez charger un .csv")
        else:
            global df
            df = pd.read_csv(path)
            
            NumRows = df.shape[0]
            
            self.screen.ids.box.clear_widgets()
            self.screen.ids.montexte.text = ""
            self.screen.ids.numPartition.text = ""
            self.screen.ids.MyImageGenerateStr.source = "" 
            self.screen.ids.MyImageGenerateStr.reload()
            self.screen.ids.montextesortie.text = "" 
            self.screen.ids.longueur.text = "" 
            
            print(df)
            print("******* \n")
            print("nombre d'exemples: ",len(df))


    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True



#### gestion de la page d'accueil du botton SubSrting
    def PrintDataItem(self):
        if len(df) == 0:
            self.show_confirmation_dialog("Veuillez charger votre fichier")

        else:
            try:
                NumRows = df.shape[0] 
                
                menu_items = [
                {
                    "text": f"Example {i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"Example {i}": self.set_item(x),
                } for i in range( NumRows)
                ]
            

                self.menu = MDDropdownMenu(
                    caller=self.screen.ids.dropdown_item,
                    items=menu_items,
                    width_mult=3,
                )
                self.menu.bind() 

            except Exception as e:
                self.show_confirmation_dialog("Veuillez charger votre fichier")

    def PrintDataItem2(self):

        if len(df) == 0:
            self.show_confirmation_dialog("Veuillez charger votre fichier")

        else:
            try:
                NumRows = df.shape[0] 
                
                menu_items = [
                {
                    "text": f"Example {i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"Example {i}": self.set_item2(x),
                } for i in range( NumRows)
                ]

                self.menu2 = MDDropdownMenu(
                    caller=self.screen.ids.dropdown_item2,
                    items=menu_items,
                    width_mult=3,
                )
                self.menu2.bind() 

            except Exception as e:
                self.show_confirmation_dialog("Veuillez charger votre fichier")


    """ def PrintDataItem3(self):
        if len(df) == 0:
            self.show_confirmation_dialog("Veuillez charger votre fichier")

        else:
            try:
                NumRows = len(PartitionResult)
                
                menu_items = [
                {
                    "text": f"Sub set {i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"Sub set{i}": self.set_item3(x),
                } for i in range( NumRows)
                ]

                self.menu3 = MDDropdownMenu(
                    caller=self.screen.ids.dropdown_item3,
                    items=menu_items,
                    width_mult=3,
                )
                self.menu3.bind() 

            except Exception as e:
                self.show_confirmation_dialog("Veuillez charger votre fichier") """
        


    """ def PrintDataItem4(self):
        if len(PartitionResult) == 0:
            self.show_confirmation_dialog("Veuillez creer les partitions avant de classifier")
        else:
            try:
                NumRows = len(PartitionResult) 
                
                menu_items = [
                {
                    "text": f"Classifier {i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"Classifier {i}": self.set_item4(x),
                } for i in range( NumRows)
                ]

                self.menu4 = MDDropdownMenu(
                    caller=self.screen.ids.dropdown_item4,
                    items=menu_items,
                    width_mult=3,
                )
                self.menu4.bind() 

            except Exception as e:
                self.show_confirmation_dialog("Veuillez creer les partitions avant de classifier") """



    ##### gestion de la liste deroulante pour le cas de Substring
    def set_item(self, text_item):
        self.screen.ids.dropdown_item.set_item(text_item)
        self.menu.dismiss()  # masquer le menu

    def set_item2(self, text_item):
        self.screen.ids.dropdown_item2.set_item(text_item)
        self.menu2.dismiss()  
    
    def set_item3(self, text_item):
        self.screen.ids.dropdown_item3.set_item(text_item)
        self.menu3.dismiss() 

    def set_item4(self, text_item):
        self.screen.ids.dropdown_item4.set_item(text_item)
        self.menu4.dismiss() 

    def show_confirmation_dialog(self,text_to_print):
        if not self.dialog:
            self.dialog = MDDialog(
                 title=text_to_print,
                 md_bg_color=self.theme_cls.error_color,
                
                 type="custom",
            )#text_color = selft

        self.dialog.open()


    def GenerateSubstring2(self, item):
        #entree,s = BuildExample(item)
        if len(df) == 0:
            self.show_confirmation_dialog("Veuillez charger votre fichier")
        else:
            entree ={} 
            indice = item.split(" ")
            exemple = dict(df.iloc[int(indice[-1])])
            # construction de l'entree(dictionnaire sigma)
            listheads = list(df.columns)
            s = str(exemple[listheads[-1]])
            i = 0
            for elt in range(len(listheads)-1):
                elt1 = "v"+str(i)
                entree[elt1] = str(exemple[listheads[i]])              

            result =  version1.GenerateSubstring(entree,s)
            result = list(result)

            
            if result != []:
                for elt in result:
                    self.screen.ids.box.add_widget(              
                        OneLineListItem(text= elt)
                    )
                
                elt = "entree = " + str(entree)
                
                self.screen.ids.montexte.text = elt
                
                elt = "s = " + s
                
                self.screen.ids.montextesortie.text = elt

                elt = str(len(result))+"  manieres d'extraire s dans entree"
                self.screen.ids.longueur.text = elt

            else:
                self.screen.ids.box.clear_widgets()
                
                elt = "entree = " + str(entree)
                
                self.screen.ids.montexte.text = elt
                
                elt = "s = " + s
                
                self.screen.ids.montextesortie.text = elt
                elt = " 0 "+"  maniere d'extraire s dans entree"
                self.screen.ids.longueur.text = elt


    def PrintDag2(self, item):
        if len(df) ==0:
            self.show_confirmation_dialog("Veuillez charger votre fichier")
        else:
            entree ={} 
            indice = item.split(" ")
            exemple = dict(df.iloc[int(indice[-1])])
            # construction de l'entree(dictionnaire sigma)
            listheads = list(df.columns)
            s = str(exemple[listheads[-1]])
            i = 0
            for elt in range(len(listheads)-1):
                elt1 = "v"+str(i)
                entree[elt1] = str(exemple[listheads[i]])
            
            w,EtaTilda = version1.GenerateStr(entree,s)

            
            try:
                os.remove("GenerateStr.gv.png")
                os.remove("GenerateStr.gv")
                version1.PrintDag(EtaTilda, w,entree,s)
                self.screen.ids.MyImageGenerateStr.source = "GenerateStr.gv.png" 
                self.screen.ids.MyImageGenerateStr.reload()
            except OSError:
                version1.PrintDag(EtaTilda, w,entree,s)
                self.screen.ids.MyImageGenerateStr.source = "GenerateStr.gv.png" 
                self.screen.ids.MyImageGenerateStr.reload()
        


    def PrintPartition(self, item):
        if len(PartitionResult) == 0:
            self.show_confirmation_dialog("Veuillez au prealable effectuer le partitionnement")
        else:
            indice = item.split(" ") 
 
            if type(PartitionResult[int(indice[-1])][0]) == list:
                
                self.screen.ids.partition.text = str(set(list(version1.flatten(PartitionResult[int(indice[-1])][0]))))
            else:
                self.screen.ids.partition.text = str(PartitionResult[int(indice[-1])][0])
                


    def PrintClassifier(self, item):
        
            if len(PartitionResult) == 0:
                self.show_confirmation_dialog("Veuillez au prealable effectuer le partitionnement")
            else:
                indice = item.split(" ")
                
                
                
                if type(PartitionResult[int(indice[-1])][0]) == list:
                    
                    self.screen.ids.classifier.text = str(BoolClassifierResult[str(set(list(version1.flatten(PartitionResult[int(indice[-1])][0]))))])
                else:
                    self.screen.ids.classifier.text = str(BoolClassifierResult[str(set([PartitionResult[int(indice[-1])][0]]))])
                    



              
    def GeneratePartition2(self):
        if len(df) == 0:
            self.show_confirmation_dialog("Veuillez charger votre fichier")
        else:
            global Examples
            # pour structurer les exemples
            T = [] # pour le resultat de GenerateStr
            entree = {}
            listheads = list(df.columns)
            
           

            for i in range(len(df)):
                s = str(df.iloc[i][listheads[-1]])
                entree = {}
                for elt in range(len(listheads)-1):
                    elt1 = "v"+str(elt)
                    entree[elt1] = str(df.iloc[i][listheads[elt]])
                
                Examples.append((entree,s))

            for elt in Examples:
                dag = version1.GenerateStr(elt[0],elt[1])
                T.append((json.dumps(elt[0]),dag))
            

            global PartitionResult
            PartitionResult = [] 
            PartitionResult = version1.GeneratePartition(T) 
            

            
            
                


            if (len(PartitionResult)) == 0:
                print("tous les exemples forment une unique partition")
            else:
                    
                NumRows = len(PartitionResult)
                
                menu_items = [
                {
                    "text": f"Sub set {i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"Sub set {i}": self.set_item3(x),
                } for i in range( NumRows)
                ]

                self.menu3 = MDDropdownMenu(
                    caller=self.screen.ids.dropdown_item3,
                    items=menu_items,
                    width_mult=3,
                )
                self.menu3.bind() 

            elt = str(len(PartitionResult))+" Partitions"
            self.screen.ids.numPartition.text = elt




    def PrintStringProgramme(self):
        if len(BoolClassifierResult) == 0:
            self.show_confirmation_dialog("Veuillez faire BoolClassifier D'abord")
        else:
            StringProgram = "" 
            StringProgram = StringProgram + "Switch("
    
            for elt in BoolClassifierResult: 
            
                    
                for elt2 in PartitionResult:
                    newSetForme2 = set() 
                    if type(elt2[0]) == list:
                        newSetForme2 = newSetForme2.union(set(list(version1.flatten(elt2[0])))) 
                    else:
                        newSetForme2 = newSetForme2.union(set([elt2[0]]))
                    
                    if str(newSetForme2) == elt:
                        break
                
                if BoolClassifierResult[elt] != 'FAIL':
                    StringProgram = StringProgram + "("+ version1.MathStringexpression(BoolClassifierResult[elt]) +","+ version1.ListOfCancatenateExpression(elt2[1])+"),"
                
                else:
                    StringProgram = StringProgram + "("+ version1.MathStringexpressionCaseFail(list(newSetForme2)[0])+","+ version1.ListOfCancatenateExpression(elt2[1])+"),"



            StringProgram  = StringProgram[0:len(StringProgram)-1]+ ")"
            
            self.screen.ids.PrincipalProgram.text  = StringProgram
        
        

    def BoolClassifier(self):
        
        if len(PartitionResult) == 0:
            self.show_confirmation_dialog("Veuillez au prealable effectuer le partitionnement")
        else:

            global Examples
            global BoolClassifierResult
            
            SigmaSet = set()
            entree = {}
            listheads = list(df.columns)
            
            for i in range(len(df)):
                s = str(df.iloc[i][listheads[-1]])
                entree = {}
                for elt in range(len(listheads)-1):
                    elt1 = "v"+str(elt)
                    entree[elt1] = str(df.iloc[i][listheads[elt]])
                
                Examples.append((entree,s))
                
            for  elt in Examples:
                SigmaSet =  SigmaSet.union(set([json.dumps(elt[0])]))

            for elt in PartitionResult:
                newSetForme = set() 

                if type(elt[0]) == list:
                    newSetForme = newSetForme.union(set(list(version1.flatten(elt[0])))) 
                else:
                    newSetForme = newSetForme.union(set([elt[0]]))

                SigmaMoins = SigmaSet - newSetForme
                
                valeureDeRetour = version1.GenerateBoolClassifier(newSetForme,SigmaMoins)
                
                if valeureDeRetour == 'FAIL':
                    BoolClassifierResult[str(newSetForme)] = 'FAIL'
                else:
                    BoolClassifierResult[str(newSetForme)] = list(version1.flatten(valeureDeRetour))
                
                entrees = [] # ensembles des entrees dans l'ensemble du fichier

                elt = str(len(PartitionResult))+ " Clasifiers"
                self.screen.ids.numClassifier.text = elt

                NumRows = len(PartitionResult) 
                
                menu_items = [
                {
                    "text": f"Classifier {i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"Classifier {i}": self.set_item4(x),
                } for i in range( NumRows)
                ]

                self.menu4 = MDDropdownMenu(
                    caller=self.screen.ids.dropdown_item4,
                    items=menu_items,
                    width_mult=3,
                )
                self.menu4.bind() 


            

    

            
MainApp().run()
