import os
import json

class Annotation:
    def __init__(self, json_data):
        self.json_data = json_data 
    
    def get_caption(self):
        return self.json_data["caption"]
    
    def get_category(self):
        return self.json_data["category"]
    
    def get_id(self):
        return self.json_data["id"]
    
    def get_image_id(self):
        return self.json_data["image_id"]
    
    def get_area(self):
        return self.json_data["bbox"][3] * self.json_data["bbox"][2]
    
class Image:
    def __init__(self, image_data, anno_datas):
        self.json_data = image_data
        self.annotations = [Annotation(anno_data) for anno_data in anno_datas]

    def get_annotations(self):
        return self.annotations
    
    def set_annotations(self, annotations):
        self.annotations = annotations

    def add_annotation(self, annotation):
        self.annotations.append(annotation)
        
    def get_filename(self):
        return self.json_data["file_name"] 
    
    def get_id(self):
        return self.json_data["id"]
    

class Dataset:
    def __init__(self, json_data):
        self.images = []
        for image_data in json_data["images"]:
            image_id = image_data["id"]
            anno_datas = [anno_data for anno_data in json_data["annotations"] if anno_data["image_id"] == image_id]
            self.images.append(Image(image_data, anno_datas))


    def rearange_ids(self):
        # Rearrange annotation ids
        for i, anno in enumerate(self.get_all_annotations()):
            anno.json_data["id"] = i + 1
        
        # Rearrange image ids and the corresponding annotation ids
        for i, image in enumerate(self.images):
            image.json_data["id"] = i + 1
            for anno in image.get_annotations():
                anno.json_data["image_id"] = i + 1

    def get_images(self):
        return self.images
    
    def set_images(self, images):
        self.images = images

    def get_all_annotations(self):
        return [anno for image in self.images for anno in image.get_annotations()]
    
    def append_dataset(self, dataset):
        for image in dataset.get_images():
            my_image = self.get_image(image.get_filename())
            if my_image is None:
                self.images.append(image)
            else:
                for annotation in image.get_annotations():
                    my_image.add_annotation(annotation)
    
    def get_image(self, filename):
        for image in self.images:
            if image.get_filename() == filename:
                return image
        return None
    
    def to_json(self):
        return {
            "categories": self.categories,
            "images": [image.json_data for image in self.images],
            "annotations": [anno.json_data for image in self.images for anno in image.get_annotations()]
        }

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
            return False
    return True

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

def main(json_path):
    with open(json_path, 'r', encoding="utf-8") as f:
        print(f"Reading {json_path}...")
        json_data = json.load(f)

    dataset = Dataset(json_data)

    if not check_image_id(dataset):
        print("Image ids are not unique.")
        
    
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
        
    
if __name__ == "__main__":
    json_path = "C:/Users/WYK/Documents/HKUST/MPhil/Research/dataset/final_caption_annotation.json"
    main(json_path)
    

    


    