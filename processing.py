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

    def set_caption(self, caption):
        self.json_data["caption"] = caption
    
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
    
def process_category(dataset):
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

        "albacore tuna": "albacore",
        "anemone": "sea anemone",
        "angel shark": "angelshark",
        "bare-tailed goatfish": "bare tailed goatfish",
        "butterfly fish": "butterflyfish",
        "chionoecetes opilio underwater": "chionoecetes opilio",
        "clown fish": "clownfish",
        "common octopus": "octopus",
        "common decorator crab": "decorator crab",
        "common whelk": "whelk",
        "crinoids": "crinoid",
        "jelly fish": "jellyfish",
        "longtail": "tuna",
        "manta": "manta ray",
        "octopuscoral": "coral",
        "porcupine fish": "porcupinefish",
        "scsllop": "scallop",
        "sea eel": "eel",
        "sea snell": "seashell",
        "sea ship": "sea whip",
        "sea urchine": "sea urchin",
        "sea weed": "seaweed",
        "sea shell": "seashell",
        "shell": "seashell",
        "unicorn fish": "unicornfish",
        "yellowfin": "yellowfin tuna",
        "pink anemone fis": "pink anemone fish",
        "red tailed butterfly fis": "red tailed butterfly fish"
    }

    for annotation in dataset.get_all_annotations():
        category = annotation.get_category()
        if category in refine_map:
            print(f"Refine {category} to {refine_map[category]}")
            annotation.set_category(refine_map[category])

        category = annotation.get_category()
        new_category = category.strip().lower()
        annotation.set_category(new_category)

    return dataset

def process_caption(dataset):
    print(f"Processing captions")
    for annotation in dataset.get_all_annotations():
        caption = annotation.get_caption()
        new_caption = caption.strip()
        new_caption = new_caption.replace("  ", " ")
        annotation.set_caption(new_caption)
    return dataset

def category_analysis(dataset, output_path):
    print(f"Category analysis")
    # Key is the category_id
    # Value is the (category_name, count)
    category_count = {}

    for annotation in dataset.get_all_annotations():
        category = annotation.get_category()
        category_id = annotation.get_category_id()
        if category_id not in category_count:
            category_count[category_id] = (category, 1)
        else:
            # Check is the category_name match or not
            assert category_count[category_id][0] == category, f"Category name mismatch {category_count[category_id][0]} vs {category}"
            category_count[category_id] = (category, category_count[category_id][1] + 1)

    # Sort the category by id
    category_count = {k: v for k, v in sorted(category_count.items(), key=lambda item: item[0])}
    
    print(f"Writing category analysis to {output_path}")
    with open(output_path, 'w', encoding="utf-8") as f:
        for category_id, (category, count) in category_count.items():
            f.write(f"{category_id};{category};{count}\n")


def main(json_path):

    with open(json_path, 'r', encoding="utf-8") as f:
        print(f"Loading {json_path}")
        main_json_data = json.load(f)

    dataset = Dataset(main_json_data)

    # process_category must be called before dataset.define_category_id()
    dataset = process_category(dataset)
    dataset = process_caption(dataset)

    # Rearrange the category id
    dataset.define_category_id()

    category_analysis(dataset, "category_analysis.txt")

    print(f"There are in total {len(dataset.get_images())} images and {len(dataset.get_all_annotations())} annotations in the combined dataset.")
    output_path = json_path.replace(".json", "_processed.json")
    with open(output_path, 'w', encoding="utf-8") as f:
        json.dump(dataset.to_json(), f)


if __name__ == "__main__":
    json_path = "../combine.json"
    main(json_path)