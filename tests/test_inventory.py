from resources.inventory import Inventory, Ball, Net, SellerProduct, MaintenanceItem

def test_inventory_with_various_items():
    inventory = Inventory()

    # Create items
    volleyball = Ball("volleyball")
    futsal = Ball("futsal")
    basketball = Ball("basket")
    net = Net("volleyball net")
    product = SellerProduct("water bottle", 5.0)
    maintenance_item = MaintenanceItem("paint", "field marking")

    # Add items to the inventory
    inventory.add_item(volleyball, 3)
    inventory.add_item(futsal, 5)
    inventory.add_item(basketball, 2)
    inventory.add_item(net, 1)
    inventory.add_item(product, 10)
    inventory.add_item(maintenance_item, 4)

    # List all items in the inventory
    print("Items in inventory:")
    for item in inventory.list_items():
        print(item)

    # Count balls by sport
    ball_counts = inventory.count_balls_by_sport()
    print("\nBall counts by sport:")
    for sport, count in ball_counts.items():
        print(f"{sport.capitalize()}: {count}")

    # Find specific items by name
    print("\nFind items by name:")
    for name in ["volleyball", "water bottle", "paint"]:
        found_items = inventory.find_item_by_name(name)
        print(f"Items with name '{name}': {found_items}")

    # Remove some items
    inventory.remove_item(volleyball, 1)
    inventory.remove_item(product, 5)

    # Verify inventory after removal
    print("\nItems after removal:")
    for item in inventory.list_items():
        print(item)

if __name__ == "__main__":
    test_inventory_with_various_items()