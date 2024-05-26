import os
import json
from dataset.dataset import Dataset, Image, Annotation
    

def remove_small_bbox_caption(dataset):
    for image in dataset.get_images():
        for annotation in image.get_annotations():
            if annotation.get_area() < 1024:
                annotation.set_caption("")
    return dataset

def rearrange_ids(dataset):
    # Rearrange annotation ids
    for i, anno in enumerate(dataset.get_all_annotations()):
        anno.json_data["id"] = i + 1
    
    # Rearrange image ids and the corresponding annotation ids
    for i, image in enumerate(dataset.get_images()):
        image.json_data["id"] = i + 1
        for anno in image.get_annotations():
            anno.json_data["image_id"] = i + 1

    return dataset

def check_small_dataset_have_caption(dataset):
    for annotation in dataset.get_all_annotations():
        if "caption" not in annotation.json_data:
            print(f"Annotation id {annotation.get_id()} does not have caption.")
            annotation.json_data["caption"] = "undefined"
        assert annotation.get_caption()  == "undefined", "Small bbox dataset should not have caption."

def main(main_json_path, small_bbox_folder):

    with open(main_json_path, 'r', encoding="utf-8") as f:
        print(f"Reading {main_json_path}...")
        main_json_data = json.load(f)

    main_dataset = Dataset(main_json_data)

    print(f"There are in total {len(main_dataset.get_images())} images and {len(main_dataset.get_all_annotations())} annotations in the main dataset.")
    additional_json_files = []
    for folder_name in os.listdir(small_bbox_folder):
        json_file = os.path.join(small_bbox_folder, folder_name, "annotations.json")
        additional_json_files.append(json_file)

    for json_file in additional_json_files:
        with open(json_file, 'r', encoding="utf-8") as f:
            print(f"Reading {json_file}...")
            json_data = json.load(f)
        dataset = Dataset(json_data)
        check_small_dataset_have_caption(dataset)
        print(f"Adding {len(dataset.get_images())} images and {len(dataset.get_all_annotations())} annotations from {json_file}.")
        main_dataset.append_dataset(dataset)
    
    main_dataset = rearrange_ids(main_dataset)
    main_dataset = remove_small_bbox_caption(main_dataset)

    print(f"There are in total {len(main_dataset.get_images())} images and {len(main_dataset.get_all_annotations())} annotations in the combined dataset.")
    with open("./data/combined.json", 'w', encoding="utf-8") as f:
        json.dump(main_dataset.to_json(), f, ensure_ascii=False)


if __name__ == "__main__":
    json_path = "../final_caption_annotations.json"
    small_bbox_folder = "../refine_small_bbox/refine_small_bbox"
    main(json_path, small_bbox_folder)