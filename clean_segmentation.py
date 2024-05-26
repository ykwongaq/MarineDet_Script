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
    
    def get_category_id(self):
        return self.json_data["category_id"]
    
    def set_category_id(self, category_id):
        self.json_data["category_id"] = category_id

    def set_category(self, category):
        self.json_data["category"] = category

    def set_segmentation(self, segmentation):
        self.json_data["segmentation"] = segmentation
    
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

    def get_all_categories(self):
        categories = set()
        for annotation in self.get_all_annotations():
            category = annotation.get_category()
            categories.add(category)
        return categories
    
    def define_category_id(self):
        categories = self.get_all_categories()
        categories = sorted(list(categories))
        category_map = {category: i for i, category in enumerate(categories)}

        with open("./refined_category_id.txt", 'w', encoding="utf-8") as f:
            for category, category_id in category_map.items():
                f.write(f"{category_id}: {category}\n")

        for annotation in self.get_all_annotations():
            category = annotation.get_category()
            category_id = category_map[category]
            annotation.set_category_id(category_id)

        

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
        json.dump(dataset.to_json(), f)


if __name__ == "__main__":
    json_path = "combined.json"
    main(json_path)