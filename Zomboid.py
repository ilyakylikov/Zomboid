import csv

class CSVReader:
    """Class for reading CSV files and returning data as a list of dictionaries."""
    
    @staticmethod
    def read_csv(file_path):
        """Reads data from a CSV file and returns it as a list of dictionaries."""
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            return list(csv_reader)


class SurvivalInventory:
    """Class to manage items from a CSV file, allowing loading, searching, and viewing data."""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.inventory = CSVReader.read_csv(file_path)

    def get_item_by_id(self, item_id):
        """Finds an item by ID."""
        return [item for item in self.inventory if item.get('ID') == str(item_id)]

    def search_items_by_name(self, search_term):
        """Finds items by a partial name match."""
        return [item for item in self.inventory if search_term.lower() in item.get('Name', '').lower()]

    def calculate_condition_percentage(self, name_filter=None):
        """Calculates percentage of items by condition.
        
        If a name_filter is provided, calculates only for items matching that name.
        """
        filtered_inventory = (
            [item for item in self.inventory if name_filter.lower() in item.get('Name', '').lower()]
            if name_filter
            else self.inventory
        )

        total_items = len(filtered_inventory)
        if total_items == 0:
            return {}

        condition_counts = {}
        for item in filtered_inventory:
            condition = item.get('Condition', 'Unknown')
            condition_counts[condition] = condition_counts.get(condition, 0) + 1

        return {condition: (count / total_items) * 100 for condition, count in condition_counts.items()}

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
            column_sizes = {'ID': 5, 'Name': 20, 'Type': 15, 'Condition': 10, 'Amount': 7}

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
        else:
            print("No items to display for the given criteria.")


def interactive_cli():
    file_path = input("Enter the path to your inventory CSV file: ").strip()
    manager = SurvivalInventory(file_path)

    while True:
        print("\nAvailable commands:")
        print("1. Get item by ID")
        print("2. Search items by name")
        print("3. Calculate condition percentage")
        print("4. Display items")
        print("5. Display all items with condition percentages")
        print("6. Exit")
        
        command = input("\nEnter the number of the command: ").strip()
        
        if command == "1":
            item_id = input("Enter the item ID: ").strip()
            result = manager.get_item_by_id(item_id)
            print(result if result else "No item found with that ID.")
        
        elif command == "2":
            name = input("Enter the name or part of the name: ").strip()
            result = manager.search_items_by_name(name)
            print(result if result else "No items found matching that name.")
        
        elif command == "3":
            name_filter = input("Enter the name filter (leave blank for all items): ").strip()
            percentages = manager.calculate_condition_percentage(name_filter if name_filter else None)
            if percentages:
                for condition, percent in percentages.items():
                    print(f"{condition}: {percent:.2f}%")
            else:
                print("No items found matching the filter.")
        
        elif command == "4":
            try:
                items_per_page = int(input("Enter number of items per page: ").strip())
                page = int(input("Enter the page number: ").strip())
                filter_field = input("Enter filter field (leave blank for no filter): ").strip()
                filter_value = input("Enter filter value (leave blank for no filter): ").strip()
                manager.display_items(
                    items_per_page=items_per_page,
                    page=page,
                    filter_field=filter_field if filter_field else None,
                    filter_value=filter_value if filter_value else None
                )
            except ValueError:
                print("Invalid input. Please enter numbers for items per page and page number.")
        
        elif command == "5":
            print("\nAll items with their condition percentages:")
            all_items = manager.inventory

            for item in all_items:
                item_name = item.get('Name', 'Unknown')
                item_condition = item.get('Condition', 'Unknown')
                item_amount = item.get('Amount', 'Unknown')
                percentages = manager.calculate_condition_percentage()

                # Display each item with its condition and percentage
                percentage_text = f"{item_condition}: {percentages.get(item_condition, 0):.2f}%"
                print(f"{item_name} (Condition: {item_condition}, Amount: {item_amount}): {percentage_text}")
        
        elif command == "6":
            print("Exiting CLI. Goodbye!")
            break
        
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    interactive_cli()
