from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

from kivy.core.window import Window

width = 288.96 * 2
height = 618.24 * 2

Window.size = (width, height)
Window.left = 0
Window.top = 0

class MainWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MainApp(MDApp):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MainApp().run()
