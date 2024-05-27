import os
import json
from dataset.dataset import Dataset, Image, Annotation

def check_image_id(dataset):
    print("Checking image id...")
    # Check if image ids are unique
    image_ids = [image.get_id() for image in dataset.get_images()]
    if len(image_ids) != len(set(image_ids)):
        return False
    return True

def check_annotation_id(dataset):
    print("Checking annotation id...")
    # Check if annotation ids are unique
    annotation_ids = [anno.get_id() for anno in dataset.get_all_annotations()]
    if len(annotation_ids) != len(set(annotation_ids)):
        return False
    return True

def check_image_annotation_id(dataset):
    print("Checking image and annotation id...")
    # Check if image containing the annotation has the same id as the annotation
    for image in dataset.get_images():
        for annotation in image.get_annotations():
            if annotation.get_image_id() != image.get_id():
                return False
    return True

def check_image_filename(dataset):
    print("Checking image filename...")
    # Check if image filenames are unique
    filenames = [image.get_filename() for image in dataset.get_images()]
    if len(filenames) != len(set(filenames)):
        return False
    return True 

def check_category(dataset):
    print("Checking category...")
    # Check if category in annotation are not empty string
    for annotation in dataset.get_all_annotations():
        if annotation.get_category() == "":
            print(f"At annotation id {annotation.get_id()}, category is empty.")

    return True

def count_small_bbox(dataset):
    count = 0
    for annotation in dataset.get_all_annotations():
        if annotation.get_area() < 1024:
            count += 1
    print(f"Number of small bounding box: {count}")

def check_small_bbox_caption(dataset):
    print("Checking small bounding box caption...")
    for annotation in dataset.get_all_annotations():
        if annotation.get_area() < 1024 and annotation.get_caption() != "":
            print(f"At annotation id {annotation.get_id()}, it is a small bbox, and the caption should be empty.")

def check_segmentation(dataset):
    print("Checking segmentation...")
    for annotation in dataset.get_all_annotations():
        if annotation.get_segmentation() != []:
            print(f"At annotation id {annotation.get_id()}, segmentation is not empty.")

def check_caption(dataset):
    print("Checking caption...")

    for image in dataset.get_images():
        have_caption = False
        for annotation in image.get_annotations():
            
            if annotation.get_area() < 1024:
                # Small bounding box does not require caption
                continue
            
            if annotation.get_caption() == "":
                print(f"At annotation id {annotation.get_id()}, caption is empty.")
                continue

            have_caption = True
            
            # Check if the caption contain "<image>"
            if "<image>" in annotation.get_caption():
                print(f"At annotation id {annotation.get_id()}, caption contains '<image>'.")
                continue
            
            # Check if the caption contain "description:"
            if "description:" in annotation.get_caption():
                print(f"At annotation id {annotation.get_id()}, caption contains 'description:'.")
                continue

        if not have_caption:
            print(f"At image id {image.get_id()}, there is no caption.")
        
    return True

def check_double_space(dataset):
    print("Checking double space...")
    for image in dataset.get_images():
        for annotation in image.get_annotations():
            caption = annotation.get_caption()
            if "  " in caption:
                print(f"At annotation id {annotation.get_id()}, caption contains double space.")
    return True

def check_small_bbox_label(dataset):
    print("Checking small bbox label...")
    for annotation in dataset.get_all_annotations():
        if annotation.is_small_bbox():
            if annotation.get_label() != -1:
                print(f"At annotation id {annotation.get_id()}, label should be -1.")
    return True

def check_small_bbox_negative_tags(dataset):
    print("Checking small bbox negative tags...")
    for annotation in dataset.get_all_annotations():
        if annotation.is_small_bbox():
            if annotation.get_negative_tags() != "":
                print(f"At annotation id {annotation.get_id()}, negative tags should be empty.")
    return True

def main(json_path):
    with open(json_path, 'r', encoding="utf-8") as f:
        print(f"Reading {json_path}...")
        json_data = json.load(f)

    dataset = Dataset(json_data)
    check_small_bbox_caption(dataset)
    # check_segmentation(dataset)

    check_image_id(dataset)

        
    
    if not check_annotation_id(dataset):
        print("Annotation ids are not unique.")
        
    
    if not check_image_annotation_id(dataset):
        print("Image ids and annotation ids do not match.")
        
    
    if not check_image_filename(dataset):
        print("Image filenames are not unique.")
        
    
    if not check_category(dataset):
        print("Category in annotation is empty.")
        
    
    if not check_caption(dataset):
        print("Caption in annotation is empty or contains '<image>' or 'description:'.")
    
    check_double_space(dataset)
    check_small_bbox_label(dataset)
    check_small_bbox_negative_tags(dataset)
    
    count_small_bbox(dataset)
    
if __name__ == "__main__":
    json_path = "./data/combined_processed.json"
    main(json_path)
    

    


    