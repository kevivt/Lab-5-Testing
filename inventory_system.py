# ...existing code...
"""Inventory management system."""

import json
import logging
from datetime import datetime
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# Global variable
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0) -> None:
    """Add qty of item to the stock_data inventory."""
    if not item:
        logging.warning("add_item called with empty item name; ignoring.")
        return
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        logging.error(
            "Quantity must be an integer; got %r. Ignoring add.", qty
        )
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logging.info("%s: Added %d of %s", datetime.now(), qty, item)


def remove_item(item: str, qty: int) -> None:
    """Remove qty of item from the stock_data inventory."""
    if not item:
        logging.warning("remove_item called with empty item name; ignoring.")
        return
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        logging.error(
            "Quantity must be an integer; got %r. Ignoring remove.", qty
        )
        return
    current = stock_data.get(item, 0)
    if current == 0:
        logging.warning("Attempted to remove %s which is not in stock.", item)
        return
    if qty >= current:
        logging.info(
            "Removing all of %s (requested %d, available %d).",
            item,
            qty,
            current,
        )
        del stock_data[item]
    else:
        stock_data[item] = current - qty
        logging.info(
            "Removed %d of %s; remaining %d.", qty, item, stock_data[item]
        )


def get_qty(item: str) -> int:
    """Return quantity of item in stock_data (0 if missing)."""
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory from JSON file into the module-level dict."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            logging.error("Loaded data is not a dict; ignoring load.")
            return
        # Ensure values are ints and update existing dict
        cleaned: Dict[str, int] = {}
        for k, v in data.items():
            try:
                cleaned[k] = int(v)
            except (TypeError, ValueError):
                logging.warning(
                    "Invalid qty for %s in file: %r. Skipping.", k, v
                )
        stock_data.clear()
        stock_data.update(cleaned)
        logging.info("Loaded inventory from %s", file)
    except FileNotFoundError:
        logging.warning("File %s not found; starting with empty inventory.", file)
    except json.JSONDecodeError as e:
        logging.error("JSON decode error when loading %s: %s", file, e)


def save_data(file: str = "inventory.json") -> None:
    """Save the current inventory to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        logging.info("Saved inventory to %s", file)
    except OSError as e:
        logging.error("Failed to save inventory to %s: %s", file, e)


def print_data() -> None:
    """Print a simple report of inventory items and quantities."""
    print("Items Report")
    for i in sorted(stock_data):
        print(i, "->", stock_data[i])


def check_low_items(threshold: int = 5) -> List[str]:
    """Return list of items with quantity less than threshold."""
    result: List[str] = []
    for i, qty in stock_data.items():
        try:
            if int(qty) < threshold:
                result.append(i)
        except (TypeError, ValueError):
            logging.warning("Non-integer qty for %s: %r", i, qty)
    return result


def main() -> None:
    """Example main routine demonstrating inventory operations."""
    add_item("apple", 10)
    add_item("banana", 2)
    add_item("apple", 10)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
# ...existing code...
if __name__ == "__main__":
    main()
# ...existing code...
