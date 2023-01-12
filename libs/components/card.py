from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.behaviors import FakeRectangularElevationBehavior

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty

Builder.load_string("""
<ElevatedCard>:
    elevation: 25
    radius: [25, 25, 25, 25]
""")

class ElevatedCard(MDCard, FakeRectangularElevationBehavior):
    pass

Builder.load_string("""
<ItemCard>:
    elevation: 25
    radius: [25, 25, 25, 25]
    orientation: "horizontal"
    padding: 50, 20
    size_hint_y: None
    height: dp(56)
    
    MDLabel:
        text: root.item_name
""")
class ItemCard(ElevatedCard):

    item_name = StringProperty()

    def __init__(self, item_name: str, components: list, **kwargs):
        super().__init__(**kwargs)
        self.item_name = item_name
        self.components = components

Builder.load_string("""
<DetailCard>:
    orientation: "vertical"
    spacing: 20
    padding: 100, 50
    size_hint_y: None
    height: self.minimum_height
    
    MDBoxLayout:
        id: content
        orientation: "vertical"
        adaptive_height: True
    
        MDLabel:
            text: root.item_name
            font_style: "H4"
            bold: True
            adaptive_height: True
        
        MDGridLayout:
            id: detail_content
            cols: 1
            adaptive_height: True
""")

class DetailCard(ElevatedCard):

    item_name = StringProperty()
    components = ListProperty()

    def __init__(self, item_name: str, components: list, **kwargs):
        super().__init__(**kwargs)
        self.item_name = item_name
        self.components = components

        for component in self.components:
            item = MDBoxLayout(orientation="horizontal", adaptive_height=True, spacing=50)
            item.add_widget(MDLabel(text=f"{component['name']}", halign="left", size_hint_x=.5))
            item.add_widget(MDLabel(text=f"x{component['amount']}", halign="left", size_hint_x=.5))

            self.ids.detail_content.add_widget(item)

Builder.load_string("""
<ProfitCard>:
    orientation: "vertical"
    spacing: 20
    padding: 100, 50
    size_hint_y: None
    height: self.minimum_height
    
    MDBoxLayout:
        id: content
        orientation: "vertical"
        adaptive_height: True

        MDLabel:
            text: root.item_name
            font_style: "H4"
            bold: True
            adaptive_height: True

        MDGridLayout:
            id: detail_content
            cols: 1
            spacing: 20
            adaptive_height: True
            
        MDLabel:
            text: "Summary"
            font_style: "H4"
            bold: True
            adaptive_height: True
            
        MDBoxLayout:
            orientation: "horizontal"
            adaptive_height: True
            
            MDLabel:
                text: "Total Cost:"
                size_hint_x: .3
            MDLabel:
                id: total_cost
                text: "0"
                
        MDBoxLayout:
            orientation: "horizontal"
            adaptive_height: True
            spacing: 50
            
            MDLabel:
                text: "Sell Price:"
                size_hint_x: .3
            MDTextField:
                id: sell_inp
                text: "0"
                mode: "rectangle"
                input_filter: "int"
                size_hint_x: .4
                on_text:
                    root.update_sell_price(self.text)
                    root.update_info()
            MDLabel:
                text: ""
                
        MDBoxLayout:
            orientation: "horizontal"
            adaptive_height: True
            
            MDLabel:
                text: "Profit"
                size_hint_x: .3
            MDLabel:
                id: profit
                text: "0"
""")

class ProfitCard(ElevatedCard):

    item_name = StringProperty()
    components = ListProperty()
    profit = NumericProperty()
    cost_price = NumericProperty()
    sell_price = NumericProperty()

    def __init__(self, item_name: str, components: list, **kwargs):
        super().__init__(**kwargs)
        self.item_name = item_name
        self.components = components
        self.profit = 0
        self.cost_price = 0
        self.sell_price = 0

        for component in self.components:
            item = Item(item_name=component['name'], item_amount=component['amount'])

            self.ids.detail_content.add_widget(item)

    def update_sell_price(self, price):
        if price == "":
            self.sell_price = 0
        else:
            self.sell_price = int(price)

    def update_info(self):
        # print(self.ids.detail_content.children)
        total = 0
        for item in self.ids.detail_content.children:
            total += item.total_price

        self.cost_price = total
        self.ids.total_cost.text = str(self.cost_price)

        self.profit = self.sell_price - self.cost_price
        self.ids.profit.text = str(self.profit)

Builder.load_string("""
<Item>:
    orientation: "horizontal"
    adaptive_height: True
    spacing: 50
    
    MDLabel:
        text: root.item_name
        halign: "left"
        size_hint_x: .25
    MDLabel:
        text: str(root.item_amount)
        halign: "left"
        size_hint_x: .25
    MDTextField:
        id: unit_price
        mode: "rectangle"
        input_filter: "int"
        size_hint_x: .25
        on_text: root.update_price(self.text)
    MDLabel:
        id: total_price
        haling: "left"
        size_hint_x: .25
""")
class Item(MDBoxLayout):

    item_name = StringProperty()
    item_amount = NumericProperty()
    total_price = NumericProperty()

    def __init__(self, item_name: str, item_amount: int, **kwargs):
        super().__init__(**kwargs)

        self.item_name = item_name
        self.item_amount = item_amount
        self.total_price = 0

    def update_price(self, unit_price):
        if unit_price == "":
            self.ids.total_price.text = ""
            self.total_price = 0
        else:
            self.ids.total_price.text = str(int(unit_price) * self.item_amount)
            self.total_price = int(self.ids.total_price.text)

        self.parent.parent.parent.update_info()
