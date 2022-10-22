from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import requests

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

    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        url = "https://raw.githubusercontent.com/five76/rasp/main/r1.txt"
        requests.adapters.DEFAULT_RETRIES = 5
        r = requests.get(url,timeout=3).content.decode('utf-8')

        df1 = r.split('\n')
        df = [x.split(',') for x in df1]

        self.data_list = list(set([x[0] for x in df if '.' in x[0]]))

    def result(self, d):
        pass


class MainApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    MainApp().run()