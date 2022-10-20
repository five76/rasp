from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
#import pandas as pd
import csv
import requests
import io
from pprint import pprint


KV = '''
box:

    id: root_widget
    orientation: 'vertical'
    canvas:
        Color: 
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self. pos
            size: self.size
    GridLayout:
        cols: 3
        rows: 1
        row_default_height: 30
        row_force_default: True
        Button:
            id: day1
            text: root.data_list[0]
            background_color: 1,0,0,1
            on_press: root_widget.result(day1.text)
        Button:
            id: day2
            text: root.data_list[1]
            background_color: 0,1,0,1
            on_press: root_widget.result(day2.text)

        Button:
            id: day3
            text: root.data_list[2]
            background_color: 0,0,1,1
            on_press: root_widget.result(day3.text)        
    GridLayout:
        cols: 1
        rows: 1
        row_default_height: 50
        row_force_default: True
        Label:
            id: itog
            text: "Расписание"
            color: 0, 0, 0, 1

'''


class box(BoxLayout):
    global rasp
    global list_date

    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        self.data_list = list_date[::]

    def result(self, d):
        # global rasp
        # d
        # options = ['17.10.2022','18.10.2022','19.10.2022']
        # rasp_prep = rasp[(rasp['prepod'] == 'Новиков Д.Н.') & rasp['data'].isin(options[0])]
        rp = rasp['Новиков Д.Н.']
        rasp_prep = rp[d]
        ss = lambda x: int(x[0])
        #for x in a1:
        #    x[0] = ss(x[0])
        list_ur = []
        for x in sorted(rasp_prep, key=ss):
            list_ur.append(' '.join(x))
        k = '\n'.join(list_ur)
        self.ids["itog"].text = k



class MainApp(App):
    def build(self):
        return Builder.load_string(KV)

    def press_button(self, instance):
        print('Вы нажали на кнопку')
        print(instance)


if __name__ == "__main__":
    __version__ = '1.0.0'
    url = "https://raw.githubusercontent.com/five76/rasp/main/r1.csv"  # Make sure the url is the raw version of the file on GitHub
    download = requests.get(url).content
    df = csv.reader(io.StringIO(download.decode('utf-8')))
    list_date = set()
    df = list(df)
    df1 = df[::]
    df2 = df[::]
    list_date = list(set([x[0] for x in df if '.' in x[0]]))
    list_prep = list(set([x[5] for x in df1 if '.' in x[5]]))
   # print(list_date)
    #print(list_prep)
    rasp = {}
    for p in list_prep:
        rec = {}
        for d in list_date:
            #print(d)
            list_ur = []
            for r in df2:
                if p == r[5] and d == r[0]:
                    list_ur.append([r[1],r[2],r[3],r[4],r[6]])
            rec[d] = list_ur
        rasp[p] = rec
    #pprint(rasp)

    #rasp = read_csv('https://raw.githubusercontent.com/five76/rasp/main/r1.csv')
    MainApp().run()