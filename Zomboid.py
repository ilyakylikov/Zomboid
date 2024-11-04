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


# Example usage
file_path = 'inventory.csv'
manager = SurvivalInventory(file_path)

# Display items filtered by ID
manager.display_items(filter_field='ID', filter_value='2')

# Display items filtered by name
manager.display_items(filter_field='Name', filter_value='Apple')

# Display items paginated (without filtering)
manager.display_items(items_per_page=10, page=1)
