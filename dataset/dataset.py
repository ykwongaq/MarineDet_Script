import os
import json

class Annotation:
    def __init__(self, json_data):
        self.json_data = json_data 
        self.process_category()

    def process_category(self):
        category = self.json_data["category"]
        new_category = category.strip().lower()
        self.json_data["category"] = new_category
    
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
    
    def is_small_bbox(self):
        return self.get_area() < 1024
    
    def get_category_id(self):
        return self.json_data["category_id"]
    
    def set_category_id(self, category_id):
        self.json_data["category_id"] = category_id

    def set_category(self, category):
        self.json_data["category"] = category

    def set_caption(self, caption):
        self.json_data["caption"] = caption

    def get_segmentation(self):
        return self.json_data["segmentation"]
    
    def set_segmentation(self, segmentation):
        self.json_data["segmentation"] = segmentation

    def set_label(self, label):
        self.json_data["label"] = label

    def set_negative_tags(self, negative_tags):
        self.json_data["negative_tags"] = negative_tags

    def get_label(self):
        return self.json_data["label"]
    
    def get_negative_tags(self):
        return self.json_data["negative_tags"]
    
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
                pass
                # Do not add the image with only small bbox
                # self.images.append(image)
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
            "images": [image.json_data for image in self.images],
            "annotations": [anno.json_data for image in self.images for anno in image.get_annotations()]
        }