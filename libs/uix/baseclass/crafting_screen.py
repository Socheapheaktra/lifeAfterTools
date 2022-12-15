from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

from kivy.lang.builder import Builder

from libs.components.card import ItemCard, DetailCard

import json

Builder.load_file("libs//uix//kv//crafting_screen.kv")

class CraftingScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_category = None
        self.data = None

        self.fetch_data()

    def fetch_data(self):
        with open("database.json", "r") as file:
            self.data = json.load(file)

    def on_search(self, search_input):
        self.ids.item_list.clear_widgets()
        search_result = list()
        if self.selected_category == "armor":
            if search_input == "":
                self.load_armor_recipe_list()
            else:
                for item in self.data['workable']['armor']:
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
                                on_release=lambda x=item: self.goto_crafting_detail(x)
                            )
                        )
        else:
            if search_input == "":
                self.load_weapon_recipe_list()
            else:
                for item in self.data['workable']['weapon']:
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
                                on_release=lambda x=item: self.goto_crafting_detail(x)
                            )
                        )

    def load_weapon_recipe_list(self):
        self.ids.item_list.clear_widgets()

        items = self.data['workable']['weapon']
        for item in items:
            self.ids.item_list.add_widget(
                ItemCard(
                    item_name=item['name'],
                    components=item['components'],
                    on_release=lambda x=item: self.goto_crafting_detail(x)
                )
            )

    def load_armor_recipe_list(self):
        self.ids.item_list.clear_widgets()

        items = self.data['workable']['armor']
        for item in items:
            self.ids.item_list.add_widget(
                ItemCard(
                    item_name=item['name'],
                    components=item['components'],
                    on_release=lambda x=item: self.goto_crafting_detail(x)
                )
            )

    def goto_weapon_list(self):
        self.ids.search_fld.text = ""
        self.load_weapon_recipe_list()
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "result_scrn"
        self.selected_category = "weapon"

    def goto_armor_list(self):
        self.ids.search_fld.text = ""
        self.load_armor_recipe_list()
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "result_scrn"
        self.selected_category = "armor"

    def goto_home_scrn(self):
        self.ids.scrn_mngr.transition.direction = "right"
        self.ids.scrn_mngr.current = "home_scrn"
        self.selected_category = None

    def goto_crafting_detail(self, item):

        def prev_screen():
            self.ids.scrn_mngr.transition.direction = 'right'
            self.ids.scrn_mngr.current = "result_scrn"

        self.ids.detail_card.clear_widgets()
        detail = DetailCard(
            item_name=item.item_name,
            components=item.components
        )
        detail.add_widget(MDRaisedButton(
            text="Return",
            size_hint_x=1,
            on_release=lambda x: prev_screen()
        ))
        self.ids.detail_card.add_widget(detail)

        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "detail_scrn"
