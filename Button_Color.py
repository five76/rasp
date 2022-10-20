from kivy.app import App
from kivy.lang import Builder


KV = """
GridLayout:
    cols: 3
    rows: 2
    Button:
        text: "Red"
        background_color: 1,0,0,1
    Button:
        text: "Green"
        background_color: 0,1,0,1
    Button:
        text: "Blue"
        background_color: 0,0,1,1
    Button:
        text: "Black"
        background_color: 0,0,0,1
    Button:
        text: "White"
        color: 0,0,0,1
        background_normal: ""
    Button:
        text: "aasd"
        background_color: 102/255,255,255,1         
"""


class MyApp(App):
    def build(self):
        return Builder.load_string(KV)

MyApp().run()