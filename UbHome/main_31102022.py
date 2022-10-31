import re
import datetime
import yaml
import datetime as datetime
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
global rasp
global list_date
global fio
global list_prep
global ur_norm
global ur_20
global list_group_spo
global list_group_npo
global date_sokr
global dir_aud


class ScreenOne(Screen):
    #global rasp
    #global list_date
    #global fio
    #global list_prep
    #global ur_norm
    #global ur_20


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
            if ' 0 ' in k:
                print(k)
                start = 0
                pos = k.find(' 0 ',start)
                while pos != -1:
                    start = pos + 3
                    k = k[:pos+1] + k[pos+3:]
                    pos = k.find(' 0 ', start)
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

        rasp_s = []
        try:
            rp = self.rasp_for_view[self.gr]
            rasp_gr = rp[d]
            list_ur = []
            rasp_s = rasp_gr
            #print(rasp_s)

            sokr_d = list(date_sokr.keys())
            #print(sokr_d)

            if d in sokr_d:
                note_sokr = "\nУРОКИ СОКРАЩЕННЫЕ!!!"
                #print('sokr')
                if date_sokr[d][0] == 20:
                    uu = ur_20[::]
                elif date_sokr[d][0] == 30:
                    uu = ur_30[::]
            else:
                note_sokr = ""
                #print('norm')
                uu = ur_norm[::]

            #print(uu)

            while len(rasp_s) > 0:
                num_ur = rasp_s[0][0]
                if len(rasp_s) > 1 and rasp_s[0][0] == rasp_s[1][0]:
                    str1 = F"{num_ur} ({uu[int(num_ur)-1]}) {rasp_s[0][3]} {rasp_s[0][2]} {rasp_s[0][4]}/{rasp_s[1][3]} {rasp_s[1][2]} {rasp_s[1][4]}"
                    rasp_s = rasp_s[2:]
                    list_ur.append(str1)
                else:
                    if rasp_s[0][2] == '0':
                        str1 = f"{num_ur} ({uu[int(num_ur)-1]}) {rasp_s[0][3]} {rasp_s[0][4]}"
                    else:
                        str1 = f"{num_ur} ({uu[int(num_ur)-1]}) {rasp_s[0][3]} {rasp_s[0][2]} {rasp_s[0][4]}"
                    rasp_s = rasp_s[1:]
                    list_ur.append(str1)

            k = "\n".join(list_ur)
            self.ids["itogRasp"].text = k
            self.ids["name_gr"].text = '\n' + self.gr + '\n' + d + note_sokr
        except:
            self.ids["itogRasp"].text = self.gr + '\n' + d


    def clear_gr(self):
        for i in range(0, 7):
            try:
                self.ids["gr" + str(i + 1)].text = ""
            except:
                continue

    def change_group(self, level, kurs):
        print(level)
        if level == "" or kurs == "":
            return 0
        if level == "Профессии":
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
    global list_aud

    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        self.data_list = list_date
        self.first_digit_aud = 1
        self.aud_list = list_aud[::]


    def result_aud(self, d):
        # pass
        try:
            rasp = dir_aud[self.aud][d]
            #print(rasp)

            temp = []
            for lst in rasp:
                ur = ' '.join(lst)
                temp.append(ur)

            k = '\n'.join(temp)

            self.ids["itog_aud"].text = k
            #print(k)
            self.ids["select_aud"].text = self.aud + '\n' + d


        except:
            self.ids["select_aud"].text = self.aud + '\n' + d

    def change_aud(self, first_digit_aud):
        res = [aud for aud in list_aud if aud[0] == str(first_digit_aud)]
        return res


    def select_aud(self, p):
        self.aud = p
        self.ids["select_aud"].text = self.aud
        self.ids["itog_aud"].text = ""

    def clear_aud(self):
        for i in range(0, 15):
            try:
                self.ids["aud" + str(i + 1)].text = ""
            except:
                continue

    def update_aud(self, t):
        if t == 'BACK' and self.first_digit_aud > 1:
            self.first_digit_aud -= 1

        elif t == 'NEXT' and self.first_digit_aud < 6:
            self.first_digit_aud += 1

        else:
            return 0

        self.aud_list = self.change_aud(self.first_digit_aud)

        self.clear_aud()

        for i in range(0, 15):
            try:
                self.ids["aud" + str(i + 1)].text = self.aud_list[i]
            except:
                continue

        #print(self.aud_list)
        # pass


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

def load_data(url):
    http = urllib3.PoolManager(ca_certs=certifi.where())
    resp = http.request('GET', url)
    r = str(resp.data.decode('utf-8'))
    return r

if __name__ == "__main__":

    url = 'https://raw.githubusercontent.com/five76/rasp/main/r1.txt'
    url_date_sokr = 'https://raw.githubusercontent.com/five76/rasp/main/sokr.yaml'
    url_ur_20 = 'https://raw.githubusercontent.com/five76/rasp/main/ur_20.txt'
    url_ur_30 = 'https://raw.githubusercontent.com/five76/rasp/main/ur_30.txt'

    r = load_data(url)
    df1 = r.split('\n')
    df = [x.split(',') for x in df1]
    df = df[:-1]
    ur_norm = ['8.30', '9.20', '10.15', '11.05', '12.00', '12.50', '13.45', '14.35', '15.30', '16.20', '17.10', '18.00', '18.50', '19.40']

    r_ur_20 = load_data(url_ur_20)
    ur_20 = r_ur_20.split('\n')[:-1]
    #ur_20 = yaml.safe_load(r_ur_20)
    r_ur_30 = load_data(url_ur_30)
    ur_30 = r_ur_20.split('\n')[:-1]
    #print(ur_20)
    #print(ur_30)
    #ur_20 = ['8.30', '8.55', '9.20', '9.45', '10.10', '10.35', '11.00', '11.25', '11.50', '12.15', '12.40', '13.05', '13.30', '13.55']
    #ur_30 = ['8.30', '8.55', '9.20', '9.45', '10.10', '10.35', '11.00', '11.25', '11.50', '12.15', '12.40', '13.05', '13.30', '13.55']


    r_sokr =  load_data(url_date_sokr)
    #date_sokr = r_sokr.split('\n')[:-1]
    http = urllib3.PoolManager(ca_certs=certifi.where())
    ds = http.request('GET', url_date_sokr)
    #r = str(resp.data.decode('utf-8'))
    #print(ds)
    date_sokr = yaml.safe_load(ds.data)
    #print(date_sokr['01.11.2022'])
    #print(date_sokr)
    #print(list(date_sokr.keys()))
    ss = lambda x: int(x[:2])
    lst1 = [datetime.datetime.strptime(x[0], '%d.%m.%Y') for x in df if '.' in x[0]]
    lst2 = list(set(lst1))
    list_date = [x.strftime("%d.%m.%Y") for x in sorted(lst2)]#for x in sorted(date_d): print(x.strftime("%d.%m.%Y"))
    #list_date = sorted(list(set([x[0] for x in df if '.' in x[0]])),key=ss)
    list_prep = sorted(list(set([x[5] for x in df if '.' in x[5] and 'Обед' not in x[5]])))
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

    list_aud =  sorted(list(set(x[6] for x in df)))
    dir_aud = {}
    ss1 = lambda x: int(x[0][:2])
    for aud in list_aud:
        lesson_in_dates = {}
        for d in list_date:

            lessons_in_aud = []
            for x in df:
                if x[0] == d and x[6] == aud:
                    lessons_in_aud.append([x[1], x[2], x[5]])
            lesson_in_dates[d] = sorted(lessons_in_aud,key=ss1)
        dir_aud[aud] = lesson_in_dates
    #print(dir_aud)

    rasp = create_rasp(df, list_prep, list_date, 5)              # расписание преподавателей
    rasp_gr_npo = create_rasp(df, list_group_npo, list_date, 2)  # расписание групп нпо
    rasp_gr_spo = create_rasp(df, list_group_spo, list_date, 2)  # расписание групп спо
    MainApp().run()
