import os
import json
from dataset.dataset import Dataset, Image, Annotation

def get_all_categories(dataset):
    categories = set()
    for annotation in dataset.get_all_annotations():
        category = annotation.get_category()
        categories.add(category)
    return categories

def define_category_id(dataset):
    categories = get_all_categories(dataset)
    categories = sorted(list(categories))
    category_map = {category: i for i, category in enumerate(categories)}

    for annotation in dataset.get_all_annotations():
        category = annotation.get_category()
        category_id = category_map[category]
        annotation.set_category_id(category_id)

    return dataset

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
        "red tailed butterfly fis": "red tailed butterfly fish",
        "goby fish": "goby",
        "sea fans": "sea fan",
        "sea grape": "seagrape",

        "atlantic blue marlin": "marlin",
        "sailfish": "marilin",
        "benthic cnidarian": "coral",
        "pacific bluefin": "tuna",
        "atlantic bluefin": "tuna",
        "southern bluefin": "tuna",
        "chimera monstrosa": "chimaera",
        "finback": "whale",
        "giant frogfish": "frogfish",
        "goby fish": "goby",
        "humpback": "whale",
        "right whale": "whale",
        "minke whale": "whale",
        "narwhal": "whale",
        "megalodon": "whale",
        "large shark": "fish",
        "sea worm": "feather duster worm",
        "kind crab": "red king crab",
        # "lontra canadensis": "otter",
    }
    #by html
    #refine imageid 7350 -> marlin
    #refine imageid 7761 -> bigeye tuna
    #refine imageid 11569 -> fish -> starry flounder

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

        if annotation.is_small_bbox():
            annotation.set_caption("")

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
    dataset = define_category_id(dataset)

    category_analysis(dataset, "./data/category_analysis.txt")

    print(f"There are in total {len(dataset.get_images())} images and {len(dataset.get_all_annotations())} annotations in the combined dataset.")
    output_path = json_path.replace(".json", "_processed.json")
    with open(output_path, 'w', encoding="utf-8") as f:
        print(f"Writing to {output_path}")
        json.dump(dataset.to_json(), f)


if __name__ == "__main__":
    json_path = "./data/combined.json"
    main(json_path)