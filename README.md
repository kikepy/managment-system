# Management System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-Latest-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)


## Description
This is a management system developed in Python that allows managing inventory, staff, and events. Data is stored in a JSON file.


## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [License](#license)


## Features
- **Inventory Management**: Add, view, and save items.
- **Staff Management**: Add, view, and save staff information.
- **Event Scheduling**: (Feature under development).

## Requirements
- Python 3.8 or higher
- Required packages (installable via `pip`):
  - `tkinter`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/kikepy/managment-system.git
   
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
    python main.py
    ```

## Project Structure
```
managment-system/
├── gui/
│   ├── item_gui.py
│   ├── staff_gui.py
│   └── main_gui.py
├── resources/
│   ├── inventory/
│   ├── staff/
│   └── ...
├── main.py
├── data.json
├── .gitignore
└── README.md
```

## Data Storage

All the data is stored in a JSON file named `data.json`. The structure of the JSON file is as follows:

```json
{
  "items": [
    {
      "name": "Item Name",
      "type": "Item Type",
      "details": "Additional Details"
    }
  ],
  "staff": [
    {
      "name": "Staff Name",
      "experience": 5,
      "languages": ["English", "Spanish"]
    }
  ]
}
```

## License
This project is licensed under the MIT License.

---
Made with ❤️ by [kikepy](https://github.com/kikepy)