import re

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition, SlideTransition, CardTransition, SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
# https://stackoverflow.com/questions/45171309/how-to-get-id-and-text-value-of-a-kivy-button-as-string

import urllib3
import certifi


class ScreenOne(Screen):
    global rasp
    global list_date
    global fio
    global list_prep

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.data_list = list_date
        self.beg = 0
        self.end = 9
        self.fi = ''

        self.ll = len(list_prep)
        self.prep_list = self.change_prep(self.beg, self.end)

    def result(self, d):
        # pass
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
        print('extract_id')

    def select_prep(self, p):
        self.fi = p
        self.ids["fio"].text = self.fi
        self.ids["itog"].text = ""

    def update_prep(self, t):
        if t == 'BACK' and self.beg >= 0:
            self.beg = self.beg - 9
            self.end = self.end - 9
            # self.ids["hole"].text = str(self.beg) + '-' + str(self.end-1)
        elif t == 'NEXT' and self.end < self.ll:
            self.beg = self.end
            self.end = self.end + 9
            # self.ids["hole"].text = str(self.beg) + '-' + str(self.end-1)
        else:
            return 0
        self.prep_list = self.change_prep(self.beg, self.end)

        for i in range(0, 9):
            try:
                self.ids["pr" + str(i + 1)].text = self.prep_list[i]
            except:
                continue
        # pass

class ScreenTwo(Screen):
    global rasp
    global list_date
    global fio
    global list_group_spo
    global list_group_npo

    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        self.data_list = list_date
        self.beg = 0
        self.end = 7
        self.fi = ''
        self.level = ""
        self.kurs = ""
        self.gr = "Выберите группу"
        self.rasp_for_view = []
        # self.but_color = get_color_from_hex('#FF94DF')
        # self.date_color = get_color_from_hex('#FFE861')

        #self.ll = len(list_group)
       # self.group_list = self.change_group(self.beg, self.end)

    def resultgr(self, d):
        # pass
       # print(d)
        #print(self.gr)
       # print(self.rasp_for_view)
        rasp_s = []
        try:
            rp = self.rasp_for_view[self.gr]
            rasp_gr = rp[d]
            #print(rasp_gr)
            #ss = lambda x: int(x[0])
            list_ur = []
            rasp_s = rasp_gr
            #print(rasp_s)

            while len(rasp_s) > 0:
            #for i in range(0, len(rasp_s)):
                if len(rasp_s)>1 and rasp_s[0][0] == rasp_s[1][0]:
                    str1 = F"{rasp_s[0][0]} {rasp_s[0][3]} {rasp_s[0][2]} {rasp_s[0][4]}/{rasp_s[0+1][3]} {rasp_s[1][2]} {rasp_s[0+1][4]}"
                    #print(str1)
                    rasp_s = rasp_s[2:]
                    list_ur.append(str1)
                    #0 += 1
                else:
                    if rasp_s[0][2] == '0':
                        str1 = f"{rasp_s[0][0]} {rasp_s[0][3]} {rasp_s[0][4]}"
                    else:
                        str1 = f"{rasp_s[0][0]} {rasp_s[0][3]} {rasp_s[0][2]} {rasp_s[0][4]}"
                    #print(str1)
                    rasp_s = rasp_s[1:]
                    #print(len(rasp_s))
                    list_ur.append(str1)

            k = "\n".join(list_ur)
            self.ids["itogRasp"].text = k
            self.ids["name_gr"].text = self.gr + '\n' + d
        except:
            self.ids["itogRasp"].text = self.gr + '\n' + d
            #self.ids["itogRasp"].text = d


    def clear_gr(self):
        for i in range(0, 7):
            try:
                self.ids["gr" + str(i + 1)].text = ""
            except:
                continue

    def change_group(self, level, kurs):
        if level == "" or kurs == "":
            return 0
        if level == "НПО":
            l1 = list_group_npo
            self.rasp_for_view = rasp_gr_npo
        else:
            l1 = list_group_spo
            self.rasp_for_view = rasp_gr_spo
        ll = [x for x in l1 if x[-1] == kurs]
        #print(self.rasp_for_view)
        self.clear_gr()
        for i in range(0, 7):
            try:
                self.ids["gr" + str(i + 1)].text = ll[i]
            except:
                continue
        return ll

    def extract_id(self, instance):
        print(instance.text)
        # wid in self.walk():
        #    print(wid.ids)
        print('extract_id')

    def select_group(self, gr):
        self.gr = gr
        self.ids["name_gr"].text = self.gr
        self.ids["itogRasp"].text = ""

    def select_level(self, lev):
        self.level = lev
        self.ids["name_gr"].text = self.level
        self.ids["itogRasp"].text = ""

        self.change_group(self.level, self.kurs)

    def select_kurs(self, kurs):
        self.kurs = kurs
        self.ids["name_gr"].text = self.level + ' '+ self.kurs+' курс'
        self.ids["itogRasp"].text = ""
        self.change_group(self.level, self.kurs)

    def update_group(self, t):
        if t == 'BACK' and self.beg >= 0:
            self.beg = self.beg - 9
            self.end = self.end - 9
            # self.ids["hole"].text = str(self.beg) + '-' + str(self.end-1)
        elif t == 'NEXT' and self.end < self.ll:
            self.beg = self.end
            self.end = self.end + 9
            # self.ids["hole"].text = str(self.beg) + '-' + str(self.end-1)
        else:
            return 0
        self.prep_list = self.change_prep(self.beg, self.end)

        for i in range(0, 9):
            try:
                self.ids["pr" + str(i + 1)].text = self.prep_list[i]
            except:
                continue
        # pass


class ScreenThree(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return Builder.load_file('main.kv')



def create_rasp(bd,list1,list2, compare_col):
    rasp = {}
    for p in list1:
        rec = {}
        for d in list2:
            list_ur = []
            for r in df:
                if p == r[compare_col] and d == r[0]:
                    list_ur.append([r[1], r[2], r[3], r[4], r[6]])
            rec[d] = list_ur
        rasp[p] = rec
    return rasp

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
    regex = re.compile(r'\S+-\d{3}')
    list_group = sorted(list(set([x[2] for x in df if len(x[2]) > 3])))

    list_group_spo = []
    list_group_npo = []
    for x in list_group:

        try:
            match = regex.search(x)
            gr = str(match.group())
            list_group_npo.append(gr)
        except:
            list_group_spo.append(x)

    rasp = create_rasp(df, list_prep, list_date, 5)                # расписание преподавателей
    rasp_gr_npo = create_rasp(df, list_group_npo, list_date, 2)  # расписание групп нпо
    rasp_gr_spo = create_rasp(df, list_group_spo, list_date, 2)  # расписание групп спо
    MainApp().run()
