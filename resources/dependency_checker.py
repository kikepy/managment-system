def check_dependencies(staff_list, inventory):
    for staff in staff_list:
        for item, quantity in staff.required_items.items():
            if not inventory.check_item(item, quantity):
                print(f"Missing {quantity} {item}(s) for {staff.role}: {staff.name}")
                return False
    return True