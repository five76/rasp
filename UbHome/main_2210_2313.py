from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import requests
import base64
import time
#from urllib.request import urlopen
import urllib3
import certifi

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
        row_default_height: 60
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

        self.data_list = list_date

    def result(self, d):
        #pass
        rp = rasp['Новиков Д.Н.']
        rasp_prep = rp[d]
        ss = lambda x: int(x[0])
        list_ur = []
        for x in sorted(rasp_prep, key=ss):
            list_ur.append(' '.join(x))
        k = '\n'.join(list_ur)
        self.ids["itog"].text = k


class MainApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    '''
    username = 'five76'
    token = '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'
    requests.adapters.DEFAULT_RETRIES = 5
    file_response = requests.get('https://api.github.com/repos/five76/rasp/contents/r1.txt', timeout=3,
                                 auth=(username, token))
    time.sleep(5)
    file_bytes = base64.b64decode(file_response.json()['content'])
    rr = file_bytes.decode('utf-8')
    '''
    http = urllib3.PoolManager(ca_certs=certifi.where())
    url = 'https://raw.githubusercontent.com/five76/rasp/main/r1.txt'
    resp = http.request('GET', url, timeout=10)
    # print(resp.status)
    r = str(resp.data.decode('utf-8'))
    # self.data_list = [r,r,r]
    df1 = r.split('\n')
    df = [x.split(',') for x in df1]
    #print(df)
    df = df[:-1]
    #print(type(df))
    list_date = list(set([x[0] for x in df if '.' in x[0]]))
    #print(df)
    list_prep = list(set([x[5] for x in df if '.' in x[5]]))
    print(list_date)
    #print(list_prep)

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
    #print(rasp)
    MainApp().run()

   #rec1 = subprocess.run(['wget','https://raw.githubusercontent.com/five76/rasp/main/r1.txt'], stdout = subprocess.PIPE)
   #rec1 = ['curl',
   #        '-H', r"'Authorization: token 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'",
    #       '-H',r"'Accept:application/vnd.github.v3.raw'",
    #       '-O','-L', 'https://api.github.com/five76/rasp/blob/main?r1.txt']
