import json
import html
import re
from bs4 import BeautifulSoup

ALL_DATA = ""
color_mapping = {
    "Primary": {
        "Default": "#3761F7",
        "Lighten 1": "#739AFE",
        "Lighten 2": "#B2CDFF",
        "Lighten 3": "#F6FAFF",
    },
    "Dark": {
        "Default": "#252837",
        "Lighten 1": "#6A6D77",
        "Lighten 2": "#B0B2B7",
        "Lighten 3": "#F6F7F7",
    },
    "Success": {
        "Default": "#18D357",
        "Lighten 1": "#5EE583",
        "Lighten 2": "#A7F4B8",
        "Lighten 3": "#F5FEF6",
    },
    "Warning": {
        "Default": "#B2E93C",
        "Lighten 1": "#D4F477",
        "Lighten 2": "#EDFB85",
        "Lighten 3": "#FEFFF7",
    },
    "Error": {
        "Default": "#E93C3C",
        "Lighten 1": "#F47179",
        "Lighten 2": "#FB85BD",
        "Lighten 3": "#FF7F8F",
    },
    "Secondary": {
        "Default": "#EFF31F",
        "Lighten 1": "#FCF562",
        "Lighten 2": "#FFFFA9",
        "Lighten 3": "#FFFFF5",
    },
}


def replace_colors_in_xml(content, color_category):
    for color_name, color_code in color_mapping[color_category].items():
        print(
            f"Replacing {color_mapping['Primary'][color_name]} with {color_code} for {color_category}"
        )
        content = content.replace(color_mapping["Primary"][color_name], color_code)
        content = content.replace(
            color_mapping["Primary"][color_name].lower(), color_code
        )
        content = content.replace(
            color_mapping["Primary"][color_name].upper(), color_code
        )

    return content


def process_file(color_category):

    data = json.loads(ALL_DATA)
    for entry in data:
        if "xml" in entry:
            entry["xml"] = replace_colors_in_xml(entry["xml"], color_category)

    return data


def save_processed_file(content, output_file):
    if output_file == "Primary.drawio":
        return
    xml_content = json.dumps(content, indent=2)
    xml_content = f"<mxlibrary>{xml_content}</mxlibrary>"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(xml_content)

    print(f"Processed content saved to {output_file}")


def create_files_from_primary():
    all_entries = []
    all_entries += json.loads(ALL_DATA)
    for category in color_mapping.keys():
        if category == "Primary":
            continue
        print(f"Processing for category: {category}")

        updated_content = process_file(category)
        output_file = f"{category.lower()}.drawio"
        save_processed_file(updated_content, "./Library/Temp/" + output_file)

        all_entries += updated_content

    save_processed_file(all_entries, "all.drawio")


if __name__ == "__main__":
    primary_file = "primary.json"
    with open(primary_file, "r", encoding="utf-8") as file:
        ALL_DATA = file.read()
    create_files_from_primary()
