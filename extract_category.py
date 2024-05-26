import os
import json

from dataset.dataset import Dataset, Image, Annotation

def main(json_path):
    with open(json_path, 'r', encoding="utf-8") as f:
        print(f"Loading {json_path}")
        json_data = json.load(f)


    dataset = Dataset(json_data)

    # key is the category id
    # value is the category name
    categories = {}
    for annotation in dataset.get_all_annotations():
        category = annotation.get_category()
        category_id = annotation.get_category_id()
        if category_id not in categories:
            categories[category_id] = category

    category_list = []
    for category_id, category_name in categories.items():
        category_list.append({"id": category_id, "name": category_name})

    for category in category_list:
        print(category)


if __name__ == "__main__":
    json_path = "./data/combined_processed.json"
    main(json_path)