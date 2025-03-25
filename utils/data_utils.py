import csv

from models.fabrics import FabricLinks


def is_duplicate_fabric(fabric_name: str, seen_names: set) -> bool:
    return fabric_name in seen_names


def is_complete_fabric(venue: dict, required_keys: list) -> bool:
    return all(key in venue for key in required_keys)


def save_fabrics_to_csv(fabrics: list, filename: str):
    if not fabrics:
        print("No fabrics to save.")
        return

    # Use field names from the Venue model
    fieldnames = FabricLinks.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(fabrics)
    print(f"Saved {len(fabrics)} venues to '{filename}'.")

