# ============================================================
# Merge the two RDF datasets into one graph
#
# tei_to_rdf.py  ->  ataturk_tei.ttl   (data from the Wikipedia text)
# csv_to_rdf.py  ->  ataturk_csv.ttl   (extra data from the CSV tables)
#
# This script loads both files into a single graph and saves the
# final, complete dataset as ataturk.ttl. Triples that appear in
# both files are automatically kept only once.
#
# Run it from the "Knowledge representation" folder (after the other
# two scripts):
#     python3 merge.py
# ============================================================

import os
from rdflib import Graph

HERE = os.path.dirname(os.path.abspath(__file__))   # folder of this script (to_rdf)
BASE = os.path.dirname(HERE)                         # one level up: "Knowledge representation"
turtle_dir = os.path.join(BASE, "turtle")           # where the .ttl files live

# Start with an empty graph and read both Turtle files into it.
g = Graph()
g.parse(os.path.join(turtle_dir, "ataturk_tei.ttl"), format="turtle")
g.parse(os.path.join(turtle_dir, "ataturk_csv.ttl"), format="turtle")

# Save the single, merged dataset.
out_file = os.path.join(turtle_dir, "ataturk_merged.ttl")
g.serialize(destination=out_file, format="turtle")
print("Done. Merged graph has", len(g), "triples ->", out_file)
