# Entities — Master Worksheet

Bu dosya projenin **tek kaynağı**. Buradan TEI header'a, CSV'ye, conceptual model'e ve RDF'e veri akar.
Her entity için: ID · tip (class) · metadata (özellikler) · authority ID · metinde geçiyor mu · ilişkiler.

> **TODO** yazan yerleri Wikidata'da arayıp doldur (https://www.wikidata.org). Uydurma — gerçek ID gir.
> "Metinde?" = entity TEI gövde metninde annotasyonlanacak mı (`evet` → TEI header) yoksa ekstra mı (`hayır` → `data/extra_entities.csv`).

---

## 0. Merkez / hub

### Atatürk (the bridging subject)
- **id:** `ataturk`
- **primary type:** `crm:E21_Person` · **+** `foaf:Person`, `schema:Person`
- **metadata:** name "Mustafa Kemal Atatürk" · doğum c.1881 · ölüm 1938-11-10 · meslek devlet adamı/asker nickname Father of Turks
- **authority:** Wikidata (https://www.wikidata.org/wiki/Q5152) · VIAF `TODO`
- **metinde?** evet (gövdede annotasyonlu)

---

## 1–10. The Ten Entities

| # | Entity | id | Primary type | + Additional types | Metadata (kendin yaz) | Wikidata | Metinde? |
|---|---|---|---|---|---|---|---|

| 1 | Republic of Türkiye | `turkey` | `schema:Country` | `crm:E74_Group`, `foaf:Organization` | 
has type: country
kuruluş: 1923-10-29 · 
başkent Ankara 
anthem İstiklal marşı
| `https://www.wikidata.org/wiki/Q43`

| 2 | CHP | `chp` | `schema:PoliticalParty` | `crm:E74_Group`, `foaf:Organization` | kuruluş 1923 · merkez Ankara | `https://www.wikidata.org/wiki/Q19079`

| 3 | Anıtkabir | `anitkabir` | `schema:Mausoleum` | `crm:E27_Site`, `schema:Place` | yapım 1944–1953 · mimar Emin Onat & Orhan Arda · Ankara | `https://www.wikidata.org/wiki/Q615404`

| 4 | Turkish Lira banknote | `tl_banknote` | `crm:E84_Information_Carrier` | `dcmi:PhysicalObject` | Atatürk portreli · ihraç Merkez Bankası | `https://www.wikidata.org/wiki/Q172872`

| 5 | Nutuk | `nutuk` | `schema:Book` | `crm:E33_Linguistic_Object`, `dcmi:Text` | yazar Atatürk · 1927 · dil Türkçe | `https://www.wikidata.org/wiki/Q2005693`

| 6 | The Incredible Turk (film) | `incredible_turk` | `schema:Movie` | `crm:E73_Information_Object`, `dcmi:MovingImage` | 1958 · belgesel · konu Atatürk | `https://www.wikidata.org/wiki/Q31190822`

| 7 | Republic Day | `republic_day` | `schema:Event` | `crm:E5_Event` | 29 Ekim · yıllık · 1923 ilanı | `https://www.wikidata.org/wiki/Q803181`

| 8 | Ankara | `ankara` | `schema:City` | `crm:E53_Place` | başkent (1923) · GeoNames TODO | `https://www.wikidata.org/wiki/Q3640`

| 9 | Kemalism | `kemalism` | `skos:Concept` | `crm:E89_Propositional_Object` | ideoloji · Atatürk'e dayanır | `https://www.wikidata.org/wiki/Q269443`

| 10 | Law No. 5816 | `law_5816` | `schema:Legislation` | `crm:E73_Information_Object`, `dcmi:Text` | 1951 · Atatürk anısını korur | `https://www.wikidata.org/wiki/Q1519065`

---

## Ara / ekstra entity'ler (conceptual model'e YENİ sınıf/property eklerler)

> Bunlar bireysel olarak conceptual model'de görünmez; sadece sınıflarıyla (Person, Group...) temsil edilir.

| Entity | id | type | metadata | Wikidata | nereye |
|---|---|---|---|---|---|
| Emin Onat (mimar) | `onat` | `crm:E21_Person` | Anıtkabir mimarı | `TODO` | CSV |
| Orhan Arda (mimar) | `arda` | `crm:E21_Person` | Anıtkabir mimarı | `TODO` | CSV |
| TBMM | `tbmm` | `crm:E74_Group` | yasama · 5816'yı çıkardı | `TODO` | CSV |
| TC Merkez Bankası | `tcmb` | `foaf:Organization` | banknotu ihraç eder | `TODO` | CSV |

---

## İlişkiler (theoretical-model.md'den — RDF triple'lar)

### Layer 1 — Atatürk'ü ölümsüzleştirme biçimleri
| Subject | Property (RDF) | Object |
|---|---|---|
| anitkabir | `crm:P67_refers_to` | ataturk |
| tl_banknote | `crm:P138_represents` / `schema:about` | ataturk |
| incredible_turk | `schema:about` | ataturk |
| nutuk | `schema:author` / `crm:P94i` | ataturk |
| kemalism | `crm:P67_refers_to` | ataturk |
| turkey | `schema:founder` / `crm:P14i` | ataturk |
| chp | `schema:founder` | ataturk |
| republic_day | `crm:P11_had_participant` | ataturk |
| ankara | `schema:homeLocation` / `crm:P74i` | ataturk |
| law_5816 | `schema:about` | ataturk |

### Layer 2 — Birbirini pekiştiren ilişkiler
| Subject | Property | Object |
|---|---|---|
| anitkabir | `crm:P53_has_former_or_current_location` / `schema:location` | ankara |
| republic_day | `schema:location` | ankara |
| nutuk | `schema:about` | kemalism |
| chp | `schema:about` | kemalism |
| turkey | `schema:capital` | ankara |
| turkey | `crm:P108_has_produced` | tl_banknote |
| turkey | `schema:about` | kemalism |
| anitkabir | `crm:P94i_was_created_by` | onat, arda |
| law_5816 | `crm:P14_carried_out_by` | tbmm |
| tl_banknote | `crm:P14_carried_out_by` | tcmb |
