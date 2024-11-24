*Survival Inventory*
This project implements a class to read data from CSV files containing information about items and provides the ability to filter and display that data.

# Description
The programme consists of two main classes:

- *CSVReader*: Responsible for reading data from a CSV file and returning it as a list of dictionaries.
- *SurvivalInventory*: Manages items, provides functionality for searching items by ID, partial name match, and allows displaying items with pagination and filtering.

# Requirements

- Python 3.x
- Library `csv` (included in the standard Python library)


# The structure of the CSV file:
The CSV file must have the following columns:

| ID | Name    | Type       | Condition | Amount |
|----|---------|------------|-----------|--------|
| 1  | Bat     | Weapon     | Bad       | 1      |
| 2  | Apple   | Food       | Bad       | 3      |
| 2  | Apple   | Food       | Good      | 1      |
| 3  | Salami  | Food       | Good      | 10     |
| 4  | Katana  | Weapon     | Good      | 1      |

# Classes
*CSVLoader*
The CSVLoader class is responsible for reading CSV files and returning the data as a list of dictionaries.

*Methods*
```python
read_csv(file_path: str) -> List[Dict[str, str]]:
```
- Reads data from a specified CSV file.
- Returns a list of dictionaries representing the rows in the CSV file.

*Constructor*
```python
 __init__(file_path: str):
 ```
- Initializes the SurvivalInventory with the path to the CSV file.
- Loads the inventory data into memory.

*Methods*
```python
get_item_by_id(item_id: str) -> List[Dict[str, str]]:
```
- Searches for an item by its ID.
- Returns a list of matching items.
```python
search_items_by_name(search_term: str) -> List[Dict[str, str]]:
```

- Searches for items with a partial name match.
- Returns a list of matching items.
```python
display_items(items_per_page: int = 10, page: int = 1, filter_field: str = None, filter_value: str = None):
```
- Displays a paginated list of items.
- Supports optional filtering based on a specific field and value.
- Outputs a formatted table to the console.

# Examples
Here's how you can use the SurvivalInventory:
```python
# Initialize the SurvivalInventory with the path to the CSV file
file_path = 'inventory.csv'
manager = SurvivalInventory(file_path)

# Display items filtered by ID
manager.display_items(filter_field='ID', filter_value='2')

# Display items filtered by name
manager.display_items(filter_field='Name', filter_value='Apple')

# Display items with pagination (without filtering)
manager.display_items(items_per_page=10, page=1)

# Display all items with condition percentages
manager.display_items_with_condition_percentage()
```
# New Feature: Interactive CLI
This project includes an interactive CLI that provides the following functionalities:

-Get item by ID.
-Search items by name.
-Calculate percentages of conditions.
-Display paginated and filtered items.
-Display all items with their condition percentages.
-Exit the program.

- Kulikov Ilya Nikolaevich

```mermaid
classDiagram
    %% CSVReader is a utility class used by SurvivalInventory for reading CSV files

    class CSVReader {
        +read_csv(file_path: str) : list[dict]
    }

    %% SurvivalInventory uses CSVReader as a helper through aggregation
    class SurvivalInventory {
        +file_path: str
        +inventory: list[dict]
        +get_item_by_id(item_id: str) : list[dict]
        +search_items_by_name(search_term: str) : list[dict]
        +calculate_condition_percentage(name_filter: str = None) : dict
        +display_items(items_per_page: int, page: int, filter_field: str = None, filter_value: str = None)
        +display_items_with_condition_percentage()
    }

    %% Interactive CLI operates on SurvivalInventory to provide user functionality
    class InteractiveCLI {
        +interactive_cli()
    }

    SurvivalInventory o-- CSVReader : "uses"
    InteractiveCLI --> SurvivalInventory : "manages"

