from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import pandas as pd

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
    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        self.data_list = list(rasp['data'].unique())

    def result(self, d):
        #global rasp
        #d
        #options = ['17.10.2022','18.10.2022','19.10.2022']
       # rasp_prep = rasp[(rasp['prepod'] == 'Новиков Д.Н.') & rasp['data'].isin(options[0])]
        rp = rasp[rasp['prepod'] == 'Новиков Д.Н.']
        rasp_prep = rp[rp['data'] == d]
        aa = rasp_prep.sort_values(by=['data', 'ur'])
        aq = aa[['ur', 'gr', 'podgr', 'lesson', 'aud']]
        a1 = aq.values.tolist()
        ss = lambda x: str(x)
        for x in a1:
            x[0] = ss(x[0])
        list_ur = []
        for x in a1:
            list_ur.append(' '.join(x))
        k = '\n'.join(list_ur)
        self.ids["itog"].text = k
        #self.ids["count"].text = str(d+1)
        #self.ids["itog"].text = str(rasp['data'].value_counts())

    #def Button_Day(self):


class MainApp(App):
    def build(self):
        return Builder.load_string(KV)

    def press_button(self, instance):

        print('Вы нажали на кнопку')
        print(instance)

if __name__ == "__main__":
    rasp = pd.read_csv('https://raw.githubusercontent.com/five76/rasp/main/r1.csv')



    MainApp().run()