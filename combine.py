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
        self.categories = json_data["categories"]
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

        with open("./category_id.txt", 'w', encoding="utf-8") as f:
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
    
def refine_category(dataset):
    refine_map = {
        "moray eels": "moray eel",
        "nurse sharks": "nurse shark",
        "orca (killer whale)": "orca",
        "sea star (starfish)": "sea star",
        "sharks as wild animals": "shark",
        "spong": "sponge",
        "whale sharks": "whale shark",
        "whitetip reef sharks": "whitetip reef shark",
        "wrasses": "wrasse",
        "crinoids (feather stars)": "crinoid",
        "belly countershading (on whale sharks)": "whale shark",
        "black rock sharks (unspecified species)": "black rock shark",
        "zebra shark juveniles (rarely seen with stripes)": "zebra shark",
        "banded sea kraits": "banded sea krait",
        "banggai cardinal fis": "banggai cardinalfish",
        "bare tailed goatfis": "bare-tailed goatfish",
        "beaked coral fis": "beaked coral fish",
        "beluga": "beluga whale",
        "blackfin": "blackfin tuna",
        "blue-spotted stingrays": "Bluespotted ribbontail ray",
        "bluespotted stingrays": "Bluespotted ribbontail ray",
        "clark's anemone fis": "clark's anemonefish",
        "crown of thorns starfish": "crown-of-thorns starfish",
        "dendronephthya soft corals": "dendronephthya",
        "fihs": "fish",
        "fimbriated morays": "fimbriated moray",
        "fsh": "fish",
        "giant manta rays": "giant manta ray",
        "grey reef sharks": "grey reef shark",
        "harlequin shrimps": "harlequin shrimp",
        "horned banner fis": "horned bannerfish",
        "juvenile emperor angelfis": "emperor angelfish",
        "leopard sharks (also known as zebra sharks)": "leopard shark",
        "moorish idols": "moorish idol",
        "yellow mask angel fis": "yellow mask angelfish",
        "yellow mask surgeron fis": "yellow mask surgeonfish",
        "yellow-edged morays": "yellow-edged moray",
        "croal": "coral",
    }

    for annotation in dataset.get_all_annotations():
        category = annotation.get_category()
        if category in refine_map:
            print(f"Refine {category} to {refine_map[category]}")
            annotation.set_category(refine_map[category])

    return dataset

def main(main_json_path, small_bbox_folder):

    with open(main_json_path, 'r', encoding="utf-8") as f:
        main_json_data = json.load(f)

    main_dataset = Dataset(main_json_data)

    print(f"There are in total {len(main_dataset.get_images())} images and {len(main_dataset.get_all_annotations())} annotations in the main dataset.")
    additional_json_files = []
    for folder_name in os.listdir(small_bbox_folder):
        json_file = os.path.join(small_bbox_folder, folder_name, "annotations.json")
        additional_json_files.append(json_file)

    for json_file in additional_json_files:
        with open(json_file, 'r', encoding="utf-8") as f:
            json_data = json.load(f)
        dataset = Dataset(json_data)
        print(f"Adding {len(dataset.get_images())} images and {len(dataset.get_all_annotations())} annotations from {json_file}.")
        main_dataset.append_dataset(dataset)
    dataset = refine_category(main_dataset)
    main_dataset.rearange_ids()
    main_dataset.define_category_id()
    print(f"There are in total {len(main_dataset.get_images())} images and {len(main_dataset.get_all_annotations())} annotations in the combined dataset.")
    with open("./combined.json", 'w', encoding="utf-8") as f:
        json.dump(main_dataset.to_json(), f, ensure_ascii=False)


if __name__ == "__main__":
    json_path = "./final_caption_annotation.json"
    small_bbox_folder = "./refine_small_bbox/refine_small_bbox"
    main(json_path, small_bbox_folder)