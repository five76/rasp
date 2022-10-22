from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import csv
import requests
import io
from os import getcwd

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
    #global rasp
    #global list_date

    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        url = "https://raw.githubusercontent.com/five76/rasp/main/r1.txt"
        #directory = getcwd()
        #print(directory)
        #filename = directory + '/somefile.txt'
        r = requests.get(url).content.decode('utf-8')
        df1 = r.split('\n')
        df = [x.split(',') for x in df1]

        self.data_list = list(set([x[0] for x in df if '.' in x[0]]))

    def result(self, d):
        '''
        rp = rasp['Новиков Д.Н.']
        rasp_prep = rp[d]
        ss = lambda x: int(x[0])
        list_ur = []
        for x in sorted(rasp_prep, key=ss):
            list_ur.append(' '.join(x))
        k = '\n'.join(list_ur)
        self.ids["itog"].text = k
        '''
        pass


class MainApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    #url = "https://raw.githubusercontent.com/five76/rasp/main/r1.txt"
    #directory = getcwd()
    #print(directory)
    #filename = directory + '/somefile.txt'
    #r = requests.get(url).content.decode('utf-8')
    #print(r1)
    #r = r1
    #with open(filename, 'w') as f:
        #f.write(r)
    #download = requests.get(url).content

    #df = csv.reader(io.StringIO(download.decode('utf-8')))
    #df = list(df)
    #list_date = list(set([x[0] for x in df if '.' in x[0]]))
    #df1 = r.split('\n')
    #print(df)
    #for r in  df1:
    #df = [x.split(',') for x in df1]
    #print(df)
    '''
    list_prep = list(set([x[5] for x in df if '.' in x[5]]))
    rasp = {}
    for p in list_prep:
        rec = {}
        for d in list_date:
            list_ur = []
            for r in df:
                if p == r[5] and d == r[0]:
                    list_ur.append([r[1],r[2],r[3],r[4],r[6]])
            rec[d] = list_ur
        rasp[p] = rec
    '''
    MainApp().run()