from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
# https://stackoverflow.com/questions/45171309/how-to-get-id-and-text-value-of-a-kivy-button-as-string
import urllib3
import certifi

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
        #self.but_color = get_color_from_hex('#FF94DF')
        #self.date_color = get_color_from_hex('#FFE861')

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

    def extract_id(self, instance):
        print(instance.text)
        # wid in self.walk():
        #    print(wid.ids)
        print('extract_id')

    def select_prep(self,p):
        self.fi = p
        self.ids["fio"].text = self.fi
        self.ids["itog"].text = ""

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
        #return Builder.load_string(KV)
        return Builder.load_file('main_21102126.kv')

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

    MainApp().run()
