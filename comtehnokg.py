
import webbrowser
import json

from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import OneLineAvatarIconListItem
from kivymd.uix.list import OneLineIconListItem,IconLeftWidget 
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable

from db import DataBase
from myparser import Parser

import asyncio


class MyLabel(MDLabel):
    pass

class TimetableTable(MDDataTable):
    pass
class TimetableLayout(MDBoxLayout):
    pass

class Content(MDBoxLayout):
    pass

class ItemWithLink(OneLineAvatarIconListItem):
    url = None
    def web_open(self):
        webbrowser.open(self.url)
    

class ContentNavigationDrawer(MDBoxLayout):
    pass    




class Comtehnokg(MDApp,):
    def build(self):
        self.icon = "data/logo.png"
        return Builder.load_string("")

    def build_timetable(self,instance,value):
        with open("data/lessons.json", "r", encoding="utf-8") as f:
            if value:
                return 
            try: 
                group = self.root.ids.timetable_group.text.upper()
                day = self.root.ids.timetable_day.text.strip()
                print(group,self.day_codes[day])
                tt = json.load(f)[f"{group}||{self.day_codes[day]}"]
            except:
                
                return 
            ttv2 = list()
            ttv1 = list()
            for rowv1 in tt:
                if rowv1[1] == '1':
                    ttv1.append((rowv1[4], rowv1[6], rowv1[5], rowv1[7]))
                else:
                    ttv2.append((rowv1[4], rowv1[6], rowv1[5], rowv1[7]))
        if self.data_tables1 != None:
            self.root.ids.table1.remove_widget(self.data_tables1)
            self.root.ids.table2.remove_widget(self.data_tables2)
        self.data_tables1 = TimetableTable(
            row_data=ttv1
        )
        self.data_tables2 = TimetableTable(
            row_data=ttv2
        )  

        self.root.ids.table1.add_widget(self.data_tables1)
        self.root.ids.table2.add_widget(self.data_tables2)
    def switch_mode(self):
        if self.theme_cls.theme_style != "Dark":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    day_codes = {
        "1": "ПОНЕДЕЛЬНИК",
        "2": "ВТОРНИК",
        "3": "СРЕДА",
        "4": "ЧЕТВЕРГ",
        "5": "ПЯТНИЦА",
        "6": "СУББОТА",
    }

    data_tables1 = None
    data_tables2 = None

    async def documents(self):    
        with open("data/documents.txt", "r", encoding="utf-8") as f:
            docs = f.read()
        self.root.ids.documents_text.text = docs 

    
    async def speciality(self):

        with open("data/speciality.txt", "r", encoding="utf-8") as f:
            docs = f.read().split('\n')
        for x in range(len(docs)//2):
            self.root.ids.speciality_box.add_widget(
                MyLabel(
                    font_style="H6",
                    text=docs[2*x]
                )
            )
            self.root.ids.speciality_box.add_widget(
                MyLabel(
                    text=docs[2*x + 1]+"\n\n"
                )
            )
    
    async def networks(self):
        with open("data/networks.txt", "r", encoding="utf-8") as f:
            info = [ x.split(",")  for x in f.read().split("\n")]       
        for row in info:
            item = ItemWithLink(text=row[0])
            left = IconLeftWidget(icon=row[1])
            item.url = row[2]
            item.on_press=item.web_open
            item.add_widget(left)
            self.root.ids.networks_box.add_widget(item)


    async def mission(self):
        with open("data/mission.txt", "r", encoding="utf-8") as f:
            docs = f.read()
        self.root.ids.mission_text.text = docs
    
    async def about(self):
        with open("data/about.txt", "r", encoding="utf-8") as f:
            docs = f.read()
        self.root.ids.about_text.text = docs


    async def append(self): 
        with open("data/append.txt", "r", encoding="utf-8") as f:
            info = [ x.split(",")  for x in f.read().split("\n")]       
        for row in info:
            item = ItemWithLink(text=row[0])
            left = IconLeftWidget(icon=row[1])
            item.url = row[2]
            item.on_press=item.web_open
            item.add_widget(left)
            self.root.ids.append_box.add_widget(item)

        
    async def teach(self):
        with open("data/journal.txt", "r", encoding="utf-8") as f:
            info = [ x.split(",")  for x in f.read().split("\n")]
        for row in info:
            item = ItemWithLink(text=row[0])
            left = IconLeftWidget(icon="notebook")
            item.url = row[1]
            item.on_press=item.web_open
            item.add_widget(left)
            self.root.ids.teach_box.add_widget(item)
         


    async def contact(self):
        with open("data/contact.txt", "r", encoding="utf-8") as f:
            docs = f.read().split('\n')
        for doc in docs:
            doc = doc.split("_")
            for doc1 in doc[1].split(";"):
                item = OneLineIconListItem(text=doc1)
                item.add_widget(IconLeftWidget(icon=doc[0]))
                self.root.ids.contact_box.add_widget(
                    item
                ) 


    async def timetable(self):
        self.root.ids.timetable_day.bind(focus=self.build_timetable)
        self.root.ids.timetable_group.bind(focus=self.build_timetable)    
    
    async def connection_interface(self):
        await asyncio.gather(
            self.networks(),
            self.mission(),
            self.about(),
            self.append(),
            self.speciality(),
            self.documents(),
            self.contact(),
            self.timetable(),
            self.teach()  
        )
    
    async def connection_data(self):
        db= DataBase()
        pr = Parser()
        await asyncio.gather(
            db.get_lessons(),
            pr.parse_journal()
        )
       
    def on_start(self):
        # asyncio.run(self.connection_data())
        asyncio.run(self.connection_interface())
        return super().on_start()



