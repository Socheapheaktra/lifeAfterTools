from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

from kivy.lang.builder import Builder

from libs.components.card import ItemCard, ProfitCard

import json

Builder.load_file("libs//uix//kv//profit_screen.kv")

class ProfitScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = list()

        self.fetch_data()
        self.load_data()

    def fetch_data(self):
        self.data = list()
        with open("database.json", "r") as file:
            json_object = json.load(file)

        for item in json_object['workable']['weapon']:
            self.data.append(item)

        for item in json_object['workable']['armor']:
            self.data.append(item)

    def on_search(self, search_input):
        self.ids.item_list.clear_widgets()
        search_result = list()

        if search_input == "":
            self.load_data()
        else:
            for item in self.data:
                if search_input.lower() in item['name'].lower():
                    search_result.append(item)

            if not search_result:
                self.ids.item_list.clear_widgets()
                self.ids.item_list.add_widget(
                    MDLabel(
                        text="No Result",
                        halign="center",
                        font_style="H2"
                    )
                )
            else:
                self.ids.item_list.clear_widgets()
                for item in search_result:
                    self.ids.item_list.add_widget(
                        ItemCard(
                            item_name=item['name'],
                            components=item['components'],
                            on_release=lambda x=item: self.goto_profit_detail(x)
                        )
                    )

    def load_data(self):
        self.ids.item_list.clear_widgets()

        for item in self.data:
            self.ids.item_list.add_widget(
                ItemCard(
                    item_name=item['name'],
                    components=item['components'],
                    on_release=lambda x=item: self.goto_profit_detail(x)
                )
            )

    def goto_profit_detail(self, item):

        def prev_screen():
            self.ids.scrn_mngr.transition.direction = 'right'
            self.ids.scrn_mngr.current = "home_scrn"

        self.ids.profit_card.clear_widgets()
        detail = ProfitCard(
            item_name=item.item_name,
            components=item.components
        )
        detail.add_widget(MDRaisedButton(
            text="Return",
            size_hint_x=1,
            on_release=lambda x: prev_screen()
        ))
        self.ids.profit_card.add_widget(detail)

        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "profit_scrn"
