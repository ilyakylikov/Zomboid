import csv
import argparse


class Readear:
    """Class for reading CSV files and returning data as a list of dictionaries."""

    @staticmethod
    def read_csv(file_path):
        """Reads data from a CSV file and returns it as a list of dictionaries."""
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            return list(csv_reader)


class Inventory:
    """Class to manage items from a CSV file, allowing loading, searching, and viewing data."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.inventory = Readear.read_csv(file_path)

    def get_item_by_id(self, item_id):
        """Finds an item by ID."""
        return [item for item in self.inventory if item.get('ID') == str(item_id)]

    def search_items_by_name(self, search_term):
        """Finds items by a partial name match."""
        return [item for item in self.inventory if search_term.lower() in item.get('Name', '').lower()]

    def display_items(self, items_per_page=10, page=1, filter_field=None, filter_value=None):
        """Displays items with optional filtering and pagination."""
        if filter_field and filter_value:
            filtered_items = [
                item for item in self.inventory
                if str(item.get(filter_field, "")).lower() == str(filter_value).lower()
            ]
        else:
            start = (page - 1) * items_per_page
            end = start + items_per_page
            filtered_items = self.inventory[start:end]

        if filtered_items:
            column_sizes = {
                'ID': 5,
                'Name': 20,
                'Type': 15,
                'Condition': 10,
                'Amount': 7
            }

            header = (
                f"{'ID'.ljust(column_sizes['ID'])} | "
                f"{'Name'.ljust(column_sizes['Name'])} | "
                f"{'Type'.ljust(column_sizes['Type'])} | "
                f"{'Condition'.ljust(column_sizes['Condition'])} | "
                f"{'Amount'.ljust(column_sizes['Amount'])}"
            )
            print(header)
            print('-' * len(header))

            for item in filtered_items:
                row = (
                    f"{item['ID'].ljust(column_sizes['ID'])} | "
                    f"{item['Name'].ljust(column_sizes['Name'])} | "
                    f"{item['Type'].ljust(column_sizes['Type'])} | "
                    f"{item['Condition'].ljust(column_sizes['Condition'])} | "
                    f"{item['Amount'].ljust(column_sizes['Amount'])}"
                )
                print(row)

    def get_condition_percentages(self):
        """Calculates percentage of each condition in the inventory."""
        condition_count = {}
        total_items = len(self.inventory)

        for item in self.inventory:
            condition = item.get('Condition', 'Unknown')
            condition_count[condition] = condition_count.get(condition, 0) + 1

        return {condition: round((count / total_items) * 100, 2) for condition, count in condition_count.items()}

    def get_condition_percentage_by_name(self, name):
        """Calculates percentage of each condition for items with a specific name."""
        matching_items = [item for item in self.inventory if name.lower() in item.get('Name', '').lower()]
        total_matching_items = len(matching_items)
        if total_matching_items == 0:
            return {}

        condition_count = {}
        for item in matching_items:
            condition = item.get('Condition', 'Unknown')
            condition_count[condition] = condition_count.get(condition, 0) + 1

        return {condition: round((count / total_matching_items) * 100, 2) for condition, count in condition_count.items()}


def display_all_items_with_percentages(inventory):
    """Displays all items with their condition and percentage."""
    total_items = len(inventory.inventory)

    # Count the number of items in each condition
    condition_count = {}
    for item in inventory.inventory:
        condition = item.get('Condition', 'Unknown')
        condition_count[condition] = condition_count.get(condition, 0) + 1

    # Calculate the percentage of each condition
    condition_percentages = {
        condition: round((count / total_items) * 100, 2)
        for condition, count in condition_count.items()
    }

    # Print the table header
    print(f"{'ID':<5} | {'Name':<20} | {'Type':<15} | {'Condition':<10} | {'Amount':<7} | {'Percentage':<12}")
    print('-' * 80)

    # Print each item with its data and percentage
    for item in inventory.inventory:
        condition = item.get('Condition', 'Unknown')
        percentage = condition_percentages.get(condition, 0)
        print(
            f"{item['ID']:<5} | {item['Name']:<20} | {item['Type']:<15} | {condition:<10} | "
            f"{item['Amount']:<7} | {percentage:<12}%"
        )


def main():
    parser = argparse.ArgumentParser(description="Survival Inventory CLI")
    parser.add_argument("file", help="Path to the CSV file")
    parser.add_argument("--name", type=str, help="Get percentage of conditions for items by name")
    parser.add_argument("--display-all", action="store_true", help="Display all items with percentages")

    args = parser.parse_args()
    inventory = Inventory(args.file)

    if args.name:
        percentages = inventory.get_condition_percentage_by_name(args.name)
        if percentages:
            for condition, percent in percentages.items():
                print(f"{condition}: {percent}%")
        else:
            print(f"No items found with name containing '{args.name}'")
    elif args.display_all:
        display_all_items_with_percentages(inventory)


if __name__ == "__main__":
    main()
