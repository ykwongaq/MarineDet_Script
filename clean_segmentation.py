import os
import json

from dataset.dataset import Dataset, Image, Annotation

def clear_segmentation(dataset):
    for annotation in dataset.get_all_annotations():
        annotation.set_segmentation([])
    return dataset

def main(json_path:str):
    with open(json_path, 'r', encoding="utf-8") as f:
        print(f"Loading {json_path}")
        json_data = json.load(f)

    dataset = Dataset(json_data)

    clear_segmentation(dataset)
    output_path = json_path.replace(".json", "_cleaned.json")
    with open(output_path, 'w', encoding="utf-8") as f:
        print(f"Writing to {output_path}")
        json.dump(dataset.to_json(), f)


if __name__ == "__main__":
    json_path = "./data/combined_processed.json"
    main(json_path)