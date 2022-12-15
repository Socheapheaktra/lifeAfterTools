from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty

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