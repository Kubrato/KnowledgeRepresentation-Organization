# ============================================================
# TEI -> RDF transformation
#
# This script reads our TEI file (tei/encoding.xml) and produces
# an RDF dataset (ataturk_tei.ttl) in Turtle format.
#
# It only uses the classes and properties that appear in our
# conceptual model, so the data matches the ontology exactly.
#
# Run it from the "Knowledge representation" folder:
#     python3 tei_to_rdf.py
# ============================================================

import os
import xml.etree.ElementTree as ET          # built-in library to read XML
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF            # gives us rdf:type

# ----- 1. Namespaces (the same prefixes used in our conceptual model) -----
CRM    = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SCHEMA = Namespace("https://schema.org/")
SKOS   = Namespace("http://www.w3.org/2004/02/skos/core#")
WDT    = Namespace("http://www.wikidata.org/prop/direct/")
WD     = Namespace("http://www.wikidata.org/entity/")   # our entities ARE Wikidata entities

# This is the namespace TEI uses for all its tags. ElementTree needs the
# full namespace in curly braces in front of every tag name.
TEI = "{http://www.tei-c.org/ns/1.0}"
# "xml:id" expands to this full attribute name.
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

# ----- 2. The conceptual model mapping -----
# Each entity (by its TEI xml:id) is an instance of one class.
TYPES = {
    "ataturk":         CRM.E21_Person,
    "turkey":          SCHEMA.Country,
    "chp":             SCHEMA.PoliticalParty,
    "anitkabir":       SCHEMA.Mausoleum,
    "tl_banknote":     CRM.E84_Information_Carrier,
    "nutuk":           SCHEMA.Book,
    "incredible_turk": SCHEMA.Movie,
    "republic_day":    SCHEMA.Event,
    "ankara":          SCHEMA.City,
    "kemalism":        SKOS.Concept,
    "law_5816":        SCHEMA.Legislation,
}

# Each relation name used in the TEI <listRelation> maps to a property.
RELATIONS = {
    "founder":   SCHEMA.founder,
    "represents": CRM.P138_represents,
    "about":     SCHEMA.about,
    "author":    SCHEMA.author,
    "refers_to": CRM.P67_refers_to,
    "location":  SCHEMA.location,
    "capital":   WDT.P36,
}

# ----- 3. Open the TEI file -----
HERE = os.path.dirname(os.path.abspath(__file__))   # folder of this script (to_rdf)
BASE = os.path.dirname(HERE)                         # one level up: "Knowledge representation"
tei_file = os.path.join(BASE, "tei", "encoding.xml")
tree = ET.parse(tei_file)
root = tree.getroot()

# Create an empty RDF graph and tell it our prefixes (for nice Turtle output).
g = Graph()
g.bind("crm", CRM)
g.bind("schema", SCHEMA)
g.bind("skos", SKOS)
g.bind("wdt", WDT)
g.bind("wd", WD)


# Small helper: given an entity element, find its human-readable name.
# Different entity types keep their name in different child tags.
def get_name(el):
    for tag in ("persName", "placeName", "orgName", "title", "label"):
        child = el.find(TEI + tag)
        if child is not None and child.text:
            return child.text.strip()
    # An <object> keeps its name one level deeper.
    obj_name = el.find(TEI + "objectIdentifier/" + TEI + "objectName")
    if obj_name is not None and obj_name.text:
        return obj_name.text.strip()
    # A <category> (concept) keeps it in <catDesc>; take the part before the dash.
    cat_desc = el.find(TEI + "catDesc")
    if cat_desc is not None and cat_desc.text:
        return cat_desc.text.split("—")[0].strip()
    return el.get(XML_ID)   # fallback: just use the id


# ----- 4. Read the entities -----
# We walk through every element. An entity is any element that has both an
# xml:id and a direct <idno type="Wikidata"> child. There are exactly 11.
# We remember each entity's Wikidata URI so we can use it as its RDF subject.
id_to_uri = {}
for el in root.iter():
    xml_id = el.get(XML_ID)
    idno = el.find(TEI + "idno[@type='Wikidata']")
    if xml_id is None or idno is None or not idno.text:
        continue

    uri = URIRef(idno.text.strip())     # e.g. http://www.wikidata.org/entity/Q5152
    id_to_uri[xml_id] = uri

    # Statement 1: the entity is an instance of its class.
    g.add((uri, RDF.type, TYPES[xml_id]))
    # Statement 2: the entity has a name (a string literal).
    g.add((uri, SCHEMA.name, Literal(get_name(el))))

# ----- 5. Read the relations from <listRelation> -----
# Each <relation> connects two entities; we turn it into one RDF triple.
for rel in root.iter(TEI + "relation"):
    name = rel.get("name")
    active = rel.get("active").lstrip("#")    # "#turkey" -> "turkey"
    passive = rel.get("passive").lstrip("#")
    g.add((id_to_uri[active], RELATIONS[name], id_to_uri[passive]))

# ----- 6. Write the RDF to a Turtle file -----
out_file = os.path.join(BASE, "turtle", "ataturk_tei.ttl")
g.serialize(destination=out_file, format="turtle")
print("Done. Wrote", len(g), "triples to", out_file)
