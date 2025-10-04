# File: tests/test_inventory.py
import unittest
from resources.inventory.inventory import Inventory
from resources.inventory.item import Item
from resources.inventory.balls import Ball

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.item1 = Item("microphone", 10)
        self.item2 = Item("Snacks", 50)
        self.ball1 = Ball("football", "soccer", 5)
        self.ball2 = Ball("basketball", "basketball", 3)

    def test_add_item(self):
        self.inventory.add_item(self.item1, 5)
        self.assertEqual(self.item1.total_quantity, 15)
        self.assertIn(self.item1, self.inventory.items)

    def test_remove_item(self):
        self.inventory.add_item(self.item1, 5)
        self.inventory.remove_item(self.item1, 5)
        self.assertEqual(self.item1.total_quantity, 10)
        self.inventory.remove_item(self.item1, 10)
        self.assertNotIn(self.item1, self.inventory.items)

    def test_remove_item_insufficient_quantity(self):
        self.inventory.add_item(self.item1, 5)
        with self.assertRaises(ValueError):
            self.inventory.remove_item(self.item1, 20)

    def test_list_items(self):
        self.inventory.add_item(self.item1, 5)
        self.inventory.add_item(self.item2, 10)
        items_list = self.inventory.list_items()
        self.assertIn("microphone: 15", items_list)
        self.assertIn("Snacks: 60", items_list)

    def test_count_balls_by_sport(self):
        self.inventory.add_item(self.ball1, 5)
        self.inventory.add_item(self.ball2, 3)
        ball_counts = self.inventory.count_balls_by_sport()
        self.assertEqual(ball_counts["soccer"], 10)
        self.assertEqual(ball_counts["basketball"], 6)

    def test_find_item_by_name(self):
        self.inventory.add_item(self.item1, 5)
        found_items = self.inventory.find_item_by_name("microphone")
        self.assertIn(self.item1, found_items)

if __name__ == "__main__":
    unittest.main()