# Immortalising a Nation's Founder

**Atatürk in cultural heritage: a Linked Open Data project**

🌐 **Website:** https://kubrato.github.io/KnowledgeRepresentation-Organization/

## What this project is

This project does not describe Mustafa Kemal Atatürk as a person. Instead, it
looks at *how a nation's founder is kept alive after death* — through the
buildings, books, films, money, laws and ideas that keep pointing back to him.

Atatürk is used as a **bridge subject**. The project gathers ten real entities
(a place, an event, an organisation, a concept, a cultural object, and so on),
and each one is connected to him in some way. Together they show one idea:
**how memory is built and protected inside cultural heritage.**

The work is done in two steps:

- **Knowledge Organization** — a mind map and a conceptual model that decide
  which entities to include, which ontology classes they belong to, and how
  they relate to Atatürk and to each other.
- **Knowledge Representation** — the same information turned into real data and
  linked into one RDF graph (see below).

## The entities

| Item | Entity type | Ontology class |
|---|---|---|
| Mustafa Kemal Atatürk | Person | `crm:E21_Person` |
| Republic of Türkiye | Country | `schema:Country` |
| Republican People's Party (CHP) | Political party | `schema:PoliticalParty` |
| Anıtkabir | Mausoleum | `schema:Mausoleum` |
| Turkish lira banknote | Object | `crm:E84_Information_Carrier` |
| Nutuk | Book | `schema:Book` |
| The Incredible Turk | Movie | `schema:Movie` |
| Republic Day | Event | `schema:Event` |
| Ankara | City | `schema:City` |
| Kemalism | Concept | `skos:Concept` |
| Law No. 5816 | Legislation | `schema:Legislation` |

Every entity is reconciled to a **Wikidata** identifier (plus VIAF and GeoNames
where available), so the local data links to shared, external authorities.

## Knowledge Representation

This is the heart of the project: it shows how plain text and tables become one
connected RDF graph. The pipeline has six steps.

1. **TEI/XML document** — short excerpts from the Wikipedia article on Atatürk
   are encoded in TEI. The *body* keeps the structure of the text and tags each
   of the ten entities where it appears (`<persName>`, `<placeName>`,
   `<orgName>`, `<title>`, `<rs>`); the *header* holds one record per entity
   (grouped by type) with its authority IDs, and a `<listRelation>` that records
   the relations the text states.
2. **TEI → HTML (XSLT)** — an XSLT stylesheet turns the same TEI source into a
   readable HTML page, showing the tagged entities in bold so the encoding can
   be checked. The presentation is generated; the text is never rewritten by hand.
3. **TEI → RDF (Python)** — a Python script reads the TEI file and writes the
   relations stated in the text as RDF triples. Each entity uses its Wikidata
   URI as its subject, so this data joins cleanly with the CSV data.
4. **CSV → RDF (Python)** — the CSV tables hold the *extra* facts that are not
   written in the text (architects, the parliament, the central bank, the
   language, the emblem, dates and dimensions). They are stored in
   *subject – predicate – object* form, one file per entity, and a script turns
   each row into RDF, typing dates and numbers with `xsd:`.
5. **Merge → one graph** — a final script loads both RDF files into a single
   graph. Because both parts share the same Wikidata URIs, triples about the
   same entity come together and identical triples are kept only once.
6. **The final graph** — the merged dataset is serialised in Turtle. It is one
   connected graph in which every entity points back to Atatürk
   (`wd:Q5152`) through the properties defined in the ontology. The graph is
   visualised with the [RDF Grapher](https://www.ldf.fi/service/rdf-grapher)
   online tool.

Throughout, only the classes and properties from the conceptual model are used,
drawn from **CIDOC CRM** (`crm:`), **schema.org** (`schema:`), **SKOS**
(`skos:`) and **Dublin Core Terms** (`dct:`).

## Repository structure

- `docs/` — the project website (GitHub Pages)
- `Knowledge organization/` — mind map, conceptual model (draw.io) and the entity worksheet
- `Knowledge representation/`
  - `tei/` — the TEI/XML encoding and the XSLT stylesheet
  - `csv/` — one CSV table per entity (subject–predicate–object)
  - `to_rdf/` — the Python scripts (`tei_to_rdf.py`, `csv_to_rdf.py`, `merge.py`)
  - `turtle/` — the generated RDF graphs (`ataturk_tei.ttl`, `ataturk_csv.ttl`, `ataturk_merged.ttl`)

## About

Created by Kübra Topçuoğlu for the course *Information Science and Cultural
Heritage*, A.Y. 2025/2026, Digital Humanities and Digital Knowledge master's
programme, University of Bologna (Alma Mater Studiorum).
