from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import urllib3
import certifi

KV = '''
box:

    id: root_widget
    orientation: 'vertical'
    canvas:
        Color: 
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self. pos
            size: self.size
    GridLayout:
        cols: 3
        rows: 4
        row_default_height: 20
        row_force_default: False
        Button:
            id: pr1
            text: root.prep_list[0]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr1.text)
        Button:
            id: pr2
            text: root.prep_list[1]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr2.text)
        Button:
            id: pr3
            text: root.prep_list[2]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr3.text)  
        Button:
            id: pr4
            text: root.prep_list[3]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr4.text)
        Button:
            id: pr5
            text: root.prep_list[4]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr5.text)
        Button:
            id: pr6
            text: root.prep_list[5]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr6.text)
        Button:
            id: pr7
            text: root.prep_list[6]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr7.text)
        Button:
            id: pr8
            text: root.prep_list[7]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr8.text)
        Button:
            id: pr9
            text: root.prep_list[8]
            background_color: 1,1,1,1
            on_press: root_widget.select_prep(pr9.text) 
        Button:
            id: back
            text: "BACK"
            background_color: 1,1,1,1
            on_press: root_widget.update_prep(back.text)
        Button:
            id: hole
            text: ""
            background_color: 0,0,0,0
            
        Button:
            id: next
            text: "NEXT"
            background_color: 1,1,1,1
            on_press: root_widget.update_prep(next.text) 
    GridLayout:
        cols: 3
        rows: 1
        row_default_height: 50
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
        row_default_height: 20
        row_force_default: True
        Label:
            id: fio
            text: ""
            color: 1, 1, 1, 1
            background_color: 0,0,1,1
            
    GridLayout:
        cols: 1
        rows: 1
        row_default_height: 50
        row_force_default: True
        Label:
            id: itog
            text: "Расписание"
            color: 1, 1, 1, 1
'''


class box(BoxLayout):
    global rasp
    global list_date
    global fio
    global list_prep

    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        self.data_list = list_date
        self.beg = 0
        self.end = 9
        self.fi = ''
        self.ll = len(list_prep)
        self.prep_list = self.change_prep(self.beg, self.end)

    def result(self, d):
        #pass
        try:
            rp = rasp[self.fi]
            rasp_prep = rp[d]
            ss = lambda x: int(x[0])
            list_ur = []
            for x in sorted(rasp_prep, key=ss):
                list_ur.append(' '.join(x))
            k = '\n'.join(list_ur)
            self.ids["itog"].text = k
            self.ids["fio"].text = self.fi + '\n' + d

        except:
            self.ids["fio"].text = self.fi + '\n' + d

    def change_prep(self, beg, end):
        return list_prep[beg:end]

    def select_prep(self,p):
        self.fi = p

    def update_prep(self, t):
        if t == 'BACK' and self.beg >= 0:
            self.beg = self.beg - 9
            self.end = self.end - 9
            #self.ids["hole"].text = str(self.beg) + '-' + str(self.end-1)
        elif t == 'NEXT' and self.end < self.ll:
            self.beg = self.end
            self.end = self.end + 9
            #self.ids["hole"].text = str(self.beg) + '-' + str(self.end-1)
        else:
            return 0
        self.prep_list = self.change_prep(self.beg, self.end)

        for i in range(0,9):
            try:
                self.ids["pr"+str(i+1)].text = self.prep_list[i]
            except:
                continue
        #pass

class MainApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    http = urllib3.PoolManager(ca_certs=certifi.where())
    url = 'https://raw.githubusercontent.com/five76/rasp/main/r1.txt'
    resp = http.request('GET', url, timeout=10)
    r = str(resp.data.decode('utf-8'))
    df1 = r.split('\n')
    df = [x.split(',') for x in df1]
    df = df[:-1]
    ss = lambda x: int(x[:2])
    list_date = sorted(list(set([x[0] for x in df if '.' in x[0]])),key=ss)
    list_prep = sorted(list(set([x[5] for x in df if '.' in x[5]])))
    print(list_date)
    rasp = {}
    for p in list_prep:
        rec = {}
        for d in list_date:
            list_ur = []
            for r in df:
                if p == r[5] and d == r[0]:
                    list_ur.append([r[1], r[2], r[3], r[4], r[6]])
            rec[d] = list_ur
        rasp[p] = rec
    #fio = 'Новиков Д.Н.'
    #fio = 'Новикова О.А'
    #fio = 'Исламшина Н.С.'
    fio = 'Хусейнов Р.В.'
    MainApp().run()
