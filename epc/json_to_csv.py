import csv
import json
from pathlib import Path

src_path = Path(__file__).parent


def copy_pcs():
    f = open(src_path / "processed" / "pcs_formatted.py", "a")
    src = open(src_path / "processed" / "pcs.json", "r")
    data = json.load(src)
    f.write("{\n")
    for d in data:
        del d["file_name"]
        del d["taxonomies"]
        f.write(json.dumps(d, indent=4, ensure_ascii=False))
        f.write(",\n")
        f.flush()
    f.write("}\n")


def json_to_csv():
    data = json.load(open(src_path / "processed" / "pcs.json"))
    out = csv.writer(open(src_path / "processed" / "pcs.csv", "w+"))

    head = list(data[0].keys())[1:]
    head.remove("taxonomies")
    out.writerow(head)

    for d in data:
        out.writerow([
            d["prog_name"],
            d["hours_total"],
            d["hours_prac"],
            d["online"],
            d["difficulty"],
            d["min_listeners"],
            d["max_listeners"],
            d["taxonomy"],
            d["expected_taxonomy_match"],
            d["positive_reviews"],
            d["neutral_reviews"],
            d["negative_reviews"]
        ])


json_to_csv()
