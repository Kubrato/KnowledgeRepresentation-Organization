# ============================================================
# CSV -> RDF transformation
#
# This script reads every CSV file in the ../csv folder and turns
# the "subject, predicate, object" rows into RDF triples, using the
# same classes and properties as our conceptual model.
#
# The CSV files hold the EXTRA data (architects, parliament, central
# bank, language, emblem, dates, dimensions...) that is not written
# in the Wikipedia text, so it is not in the TEI file.
#
# Run it from the "Knowledge representation" folder:
#     python3 csv_to_rdf.py
# ============================================================

import os
import csv                                  # built-in library to read CSV
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD       # rdf:type and the xsd: datatypes

# ----- 1. Namespaces (same prefixes as the conceptual model) -----
CRM    = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SCHEMA = Namespace("https://schema.org/")
SKOS   = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT    = Namespace("http://purl.org/dc/terms/")
WDT    = Namespace("http://www.wikidata.org/prop/direct/")
WD     = Namespace("http://www.wikidata.org/entity/")

# ----- 2. Every entity id used in the CSV files -> its Wikidata URI -----
# The first 11 are the same entities as in the TEI file (so the two RDF
# datasets join on the same URIs). The last 6 are the extra entities.
WIKIDATA = {
    "ataturk": "Q5152",   "turkey": "Q43",        "chp": "Q19079",
    "anitkabir": "Q615404", "tl_banknote": "Q172872", "nutuk": "Q2005693",
    "incredible_turk": "Q31190822", "republic_day": "Q803181",
    "ankara": "Q3640", "kemalism": "Q269443", "law_5816": "Q1519065",
    # extra entities (only in the CSV files)
    "onat": "Q5372464", "arda": "Q6065347", "tbmm": "Q274918",
    "tcmb": "Q580829", "turkish_language": "Q256", "six_arrows": "Q6030041",
}

# ----- 3. The conceptual model mapping -----
# "has type" value (in the CSV) -> the class of that entity.
TYPE_CLASS = {
    "mausoleum": SCHEMA.Mausoleum, "city": SCHEMA.City,
    "political party": SCHEMA.PoliticalParty, "emblem": CRM.E36_Visual_Item,
    "language": CRM.E56_Language, "person": CRM.E21_Person,
    "assembly": CRM.E74_Group, "organization": CRM.E74_Group,
    "movie": SCHEMA.Movie, "concept": SKOS.Concept,
    "legislation": SCHEMA.Legislation, "book": SCHEMA.Book,
    "event": SCHEMA.Event, "object": CRM.E84_Information_Carrier,
    "country": SCHEMA.Country,
}

# Every CSV predicate -> the property it becomes in RDF.
PROP = {
    "has title": SCHEMA.name,
    "has construction date": SCHEMA.dateCreated,
    "has foundation date": SCHEMA.foundingDate,
    "has publication date": SCHEMA.datePublished,
    "has release date": SCHEMA.datePublished,
    "has date": DCT.date,
    "has area": CRM.P43_has_dimension,
    "has genre": SCHEMA.genre,
    "is dedicated to": CRM.P67_refers_to,
    "is located in": SCHEMA.location,
    "has architect": SCHEMA.architect,
    "hosts": CRM.P7i_witnessed,
    "is residence of": CRM.P74i_is_current_or_former_residence_of,
    "is founded by": SCHEMA.founder,
    "is based in": SCHEMA.location,
    "follows": SCHEMA.about,
    "has flag": CRM.P138i_has_representation,
    "is about": SCHEMA.about,
    "is enacted by": SCHEMA.creator,
    "protects": SCHEMA.about,
    "has author": SCHEMA.author,
    "has language": DCT.language,
    "is published in": SCHEMA.locationCreated,
    "is delivered to": SCHEMA.about,
    "depicts": CRM.P138_represents,
    "is issued by": CRM.P108i_was_produced_by,
    "commemorates": SCHEMA.about,
    "is celebrated in": SCHEMA.location,
    "had participant": CRM.P11_had_participant,
    "has capital": WDT.P36,
    "has currency": CRM.P108_has_produced,
    "relates to": SCHEMA.about,
    "has official language": DCT.language,
    "is agency of": SCHEMA.parentOrganization,
    "is defined by": CRM.P138i_has_representation,
    "is based on": CRM.P67_refers_to,
}

# Predicates whose object is a literal value (text or number), not an entity.
DATE_PREDS    = {"has construction date", "has foundation date",
                 "has publication date", "has release date", "has date"}
DECIMAL_PREDS = {"has area"}
STRING_PREDS  = {"has title", "has genre"}


# Helper: turn an entity id ("ankara") into its Wikidata URI.
def uri(entity_id):
    return URIRef(WD + WIKIDATA[entity_id])


# ----- 4. Prepare the graph -----
g = Graph()
g.bind("crm", CRM)
g.bind("schema", SCHEMA)
g.bind("skos", SKOS)
g.bind("dct", DCT)
g.bind("wdt", WDT)
g.bind("wd", WD)

# ----- 5. Read every CSV file in the ../csv folder -----
HERE = os.path.dirname(os.path.abspath(__file__))   # folder of this script (to_rdf)
BASE = os.path.dirname(HERE)                         # one level up: "Knowledge representation"
csv_dir = os.path.join(BASE, "csv")

for filename in sorted(os.listdir(csv_dir)):
    if not filename.endswith(".csv"):
        continue
    with open(os.path.join(csv_dir, filename), encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)                        # skip the header row
        for row in reader:
            # Skip empty lines and comment lines (they start with "#").
            if not row or row[0].strip().startswith("#"):
                continue
            subject, predicate, obj = (cell.strip() for cell in row)

            # Case A: "has type" -> rdf:type with the class of the entity.
            if predicate == "has type":
                g.add((uri(subject), RDF.type, TYPE_CLASS[obj]))

            # Case B: the object is a date literal.
            # A full date (YYYY-MM-DD) is xsd:date; a year on its own is xsd:gYear.
            elif predicate in DATE_PREDS:
                date_type = XSD.date if obj.count("-") == 2 else XSD.gYear
                g.add((uri(subject), PROP[predicate], Literal(obj, datatype=date_type)))

            # Case C: the object is a number (we keep only the number, not the unit).
            elif predicate in DECIMAL_PREDS:
                number = obj.split()[0]
                g.add((uri(subject), PROP[predicate], Literal(number, datatype=XSD.decimal)))

            # Case D: the object is a plain text literal.
            elif predicate in STRING_PREDS:
                g.add((uri(subject), PROP[predicate], Literal(obj)))

            # Case E: the object is another entity -> use its URI.
            else:
                g.add((uri(subject), PROP[predicate], uri(obj)))

# ----- 6. Write the RDF to a Turtle file -----
out_file = os.path.join(BASE, "turtle", "ataturk_csv.ttl")
g.serialize(destination=out_file, format="turtle")
print("Done. Wrote", len(g), "triples to", out_file)
