from kivymd.uix.boxlayout import MDBoxLayout

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty

from libs.uix.baseclass.crafting_screen import CraftingScreen
from libs.uix.baseclass.profit_screen import ProfitScreen

Builder.load_file("libs//uix//kv//main_screen.kv")

class MainScreen(MDBoxLayout):

    crafting_screen = ObjectProperty()
    food_screen = ObjectProperty()
    profit_screen = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def goto_crafting_screen(self):
        self.ids.crafting_scrn.clear_widgets()
        self.crafting_screen = CraftingScreen()

        self.ids.crafting_scrn.add_widget(self.crafting_screen)
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "crafting_scrn"

        self.ids.toolbar.left_action_items = [
            ['arrow-left-bold', lambda x: self.goto_main_screen()]
        ]

    def goto_profit_screen(self):
        self.ids.profit_scrn.clear_widgets()
        self.profit_screen = ProfitScreen()

        self.ids.profit_scrn.add_widget(self.profit_screen)
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "profit_scrn"

        self.ids.toolbar.left_action_items = [
            ['arrow-left-bold', lambda x: self.goto_main_screen()]
        ]

    def goto_main_screen(self):
        self.ids.scrn_mngr.transition.direction = "right"
        self.ids.scrn_mngr.current = "home_scrn"

        self.ids.toolbar.left_action_items = []
