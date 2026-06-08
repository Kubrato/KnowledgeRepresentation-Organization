# Proje Notları — Hocanın (Daquino) Anlattıkları

> Kaynak: *"Information Science and Cultural Heritage – Daquino"* ders kaydı dökümü (PDF, 14 sayfa).
> Bu dosya, hocanın derste **adım adım** anlattığı proje akışını ve uyarılarını, sayfa referanslarıyla birlikte not eder.
> Bizim somut karşılığımız için bkz. [README.md](../README.md) ve [ontology/entities.md](../ontology/entities.md).

---

## 0. Projenin özü (s.1)

- Proje **bireysel**. Herkes "aşağı yukarı aynı şeyleri" yapar, **ama farklı vaka çalışmaları üzerinde**.
- Kişiden kişiye değişen asıl şey: **modelleme çabası** — yani domain'e uyan bir **ontoloji kurmak**.
  > *"What will actually change from one person to another is indeed the modelling effort, like creating an ontology that fits your domain."* (s.1)
- Bu yıl **kılavuz değişti** → önceki yılların projeleri birebir örnek alınamaz. (s.1)

---

## 1. Bir metinden başla (s.1–2)

- İdeal başlangıç: bir **Wikipedia sayfası** (zorunlu değil ama önerilir, çünkü çok sayıda entity'ye referans verir).
  > *"So you need to start ideally from a Wikipedia page."* (s.1)
- Bizim metnimiz: **Mustafa Kemal Atatürk** Wikipedia sayfası.
- Sayfada ilginç bölümler seç (örn. "popüler kültürde", "anma", "etkisi"). Bu bölümler ana entity'yi başka artefakt/kişi/yerlere bağlar.
- **İlk iş kodlamadan önce:** metni oku, bağlamak istediğin **entity'leri ve yerlerini** belirle. (s.2)

---

## 2. En az 10 entity + farklı türler (s.2)

- Makul sayı: **10 entity** (daha fazla olabilir).
  > *"You need to include a reasonable amount. It's 10 entities. It can be more."* (s.2)
- **Farklı entity türleri** ve ideal olarak **farklı ilişki türleri** hedefle (kişi, kitap, TV şovu, kurum, yer...).
- Kodlamadan önce: entity'leri yaz, türlerini anla, ana özne ile ilişkilerini hayal et → **mind map** çiz.

---

## 3. Theoretical model = Mind map (s.2–3)

- Mind map = **teorik model**. İlk aşamada **eskiz / kaba** olabilir.
  > *"At this point, it can be really sketchy."* (s.3)
- Radyal bir graf: merkezde özne (Atatürk), düğümler entity'ler, oklar ilişkiler.
- **Okunur olmalı** — 10 kez zoom gerektirmemeli, devasa olmamalı. (s.7)
- ✅ İyi örnek: **Vivienne Westwood** mind map'i — "süper kolay okunan" (s.11).
- İyi mind map kuralı: ana kavram + doğrudan ilişkiler **+ grafın ötesine uzaması** (dolaylı ilişkiler de). (s.11)

---

## 4. TEI/XML kodlaması — çekirdek (s.3–4, 6)

- Seçilen metni **TEI XML**'e kodla. **Tüm sayfayı değil**, sadece bağlamak istediğin entity'leri içeren **snippet'ler**.
  > *"You don't need to encode the whole page. You can just take snippets."* (s.3)
- **Bu yılın farkı:** TEI belgesi artık **çekirdek** — diğer entity'leri ondan çıkarıyoruz (geçen yıl TEI sadece 10 öğeden biriydi). (s.7)
- TEI belgesi **mutlaka** şunları içermeli (s.3):
  1. Metnin **mantıksal yapısı**: bölümler (`div`), başlıklar, paragraflar.
  2. **Entity annotasyonları**: `persName`, `placeName`, kitap/artefakt vb.
  3. **Kayıtlar** (teiHeader içinde): kişiler için `person`, yerler için `place`... + dış otorite linkleri.
  4. **İlişkiler**: `listRelation` / `relation` ile entity'ler arası bağlar (XML ID'leri üzerinden).
     > *"You want to create in your TEI file a list relation element where you relate your object ... saying that there is a relation between these two entities."* (s.4)
- Annotasyonları dış otoritelere bağla: **Wikidata, VIAF, ULAN** vb. (s.3)
- İki özel durum (s.3):
  - **(a)** Bağlamak istediğin entity metinde geçmeyebilir → ekstra veri üretmen gerekir.
  - **(b)** Entity hiçbir veri setinde olmayabilir → TEI'de "hook" olur ama dış veri olmaz (niş konularda).

> 📌 Bizde: çekirdek metin [tei/ataturk_kemal.xml](../tei/ataturk_kemal.xml).

---

## 5. Ekstra veri (metinde olmayan entity'ler) (s.4, 6)

- Metinde olmayan ama grafikte istediğin entity'ler için **dışarıda veri üret**: en kolayı bir **tablo (CSV)**.
  > *"The easiest way is to make a table ... about these extra entities and ... the relations between these extra entities and the entities that are mentioned in the text."* (s.4)
- Bu CSV'leri de **RDF'e dönüştür ve ana grafikle birleştir** → sonuçta **tek graf**.
- Mevcut dış veri (örn. Orwell'i anlatan bir XML kaydı) varsa **yeniden kullanmak artı puan** — ama zorunlu değil. (s.6)

> 📌 Bizde: [data/](../data/) altındaki CSV'ler (anitkabir, ankara, nutuk, kemalism, ...) bu "ekstra veri" rolünde.

---

## 6. Conceptual model = Ontoloji (s.5)

- Mind map'ten (teorik model) **kavramsal modele** geç.
- Çizimde **sınıflar ve özellikler** olmalı; **bireyler (individuals) OLMAMALI**.
  > *"The graph ... need to include classes and properties. Do not need to include the individuals."* (s.5)
  - Örn: "Orwell 5 kitap yazdı" → modelde Orwell ve kitaplar görünmez; sadece `Person —yazdı→ Book` sınıf ilişkisi görünür.
- **Yeni ontoloji icat etme** — mümkün olduğunca **mevcut ontolojileri yeniden kullan**. Değerlendirilen şey bu.
  > *"Ideally you don't create a new ontology. You try to reuse as much as possible existing ontologies. And that's what is judged."* (s.5)
  - Müze nesneleri → **CIDOC-CRM**. Arşiv standartları → **RICO / RDA**. (s.5)
- **Kurallar** (s.12):
  - Bir sınıf grafikte **yalnızca bir kez** görünmeli (tekrar yok).
  - "Üçgen" yapma (birey → property → sınıf). Doğrudan **sınıftan sınıfa ok** çiz: `MusicRecording —item location→ Place`.
  - Aynı iki sınıf arası **birden fazla property** olabilir, sorun değil.
- Görsel **küçük, derli toplu, okunur** olmalı.

> 📌 Bizde ontoloji listesi/eşleştirmeler: [ontology/](../ontology/) (CIDOC-CRM, FRBRoo, SKOS, DCTerms).

---

## 7. Dönüşümler — Python + XSLT (s.4, 6–7)

- **Zorunlu:** TEI belgesinden **RDF** üret (Python).
  > *"The mandatory thing is to transform things from your TI document into RDF."* (s.14)
- Sadece TEI varsa → 1 Python dosyası (TEI→RDF). Ekstra veri de varsa → ayrıca CSV→RDF + **birleştirme**. (s.6)
- **XSLT:** TEI'den **HTML** üret. Web sitesinde hem TEI hem HTML çıktısı hem XSLT linki olmalı. (s.7)
- Python: **CSV** okumak için yerleşik `csv` kütüphanesi (liste-of-list ya da dict). (s.1)

> 📌 Bizde: [transformations/](../transformations/) (tei_to_html.xsl, tei_to_rdf.py, csv_to_rdf.py).

---

## 8. ⚠️ Ontoloji ↔ Veri TAM eşleşmesi (s.6–7)

- Hocanın **en çok vurguladığı** nokta. Geçen yılların büyük sorunu buydu.
  > *"The ontology needs to be complete and needs to match perfectly what you do in the data ... There needs to be a kind of a perfect match."* (s.6–7)
- Yani: ontolojide çizdiğin **her terim** veride kullanılmalı; veride kullandığın her terim ontolojide olmalı.

---

## 9. Konsept / anlatı önemli (s.8–9)

- İlişkilerin arkasında bir **kavram / anlatı** olmalı — sadece metadata dökmek değil.
  > *"There needs to be a concept behind the relations that you create."* (s.9)
- İyi proje ≠ öznenin metadata'sını listelemek (yazar, yayıncı, yer...). Bu "sığ" kalır. (s.9)
- **Soyut bir özne** genelde daha iyi çalışır (ilişkiler daha az bariz/rastgele). (s.10)
  - ✅ En beğenilen örnek: **Çay Töreni / Book of Tea** — Zen, Budizm, kimono, malzeme bilimi gibi soyut+somut köprüsü. (s.10)
  - ⚠️ Daha zayıf örnek: **Queen Elizabeth** — sadece "ona atıf yapan nesneler", ilişki sığ. (s.10)

> 📌 Bizim anlatımız: *"Bir ulus kurucusunun kültürel mirasta ölümsüzleştirilmesi"* — bkz. README §1. Atatürk'ü "köprü-özne" yaparak biyografi-metadata tuzağından kaçınıyoruz.

---

## 10. Web sitesi — teslim listesi (s.7)

Sitede **zorunlu** olarak bulunmalı:

- [ ] Konunun tanıtımı / anlatı (neden bu özne?)
- [ ] **Mind map** (theoretical model) — okunur görsel
- [ ] **Ontoloji** (conceptual model) — derli toplu görsel
- [ ] Entity'lerin **kısa açıklamaları**
- [ ] **TEI/XML** belgesi
- [ ] **HTML** çıktısı + **XSLT** linki
- [ ] **TEI→RDF** Python betiği
- [ ] (Varsa) ekstra veri → RDF Python betiği + birleştirme
- [ ] Nihai grafiğin önizlemesi ya da link (serialize edilmiş hali)

- Her şey büyük ihtimalle bir **GitHub deposunda** olmalı (erişilebilirlik için), ama rahatlık açısından **siteye de gömün**. (s.7)
- Graf görselleştiricileri "şart değil" — genelde dağınık/okunmaz olur. (s.7)

---

## 11. Genel notlar (s.13)

- CSV'leri nasıl organize ettiğin **serbest** — önceki projelerin CSV yapısını örnek alma, onlar dağınık. Tek şart: RDF'e dönüştürülebilir olması. (s.13)
- **Gen AI kullanımı serbest** — ama **sunumda soruları yanıtlayabilmen** gerekir. (s.13)
- Proje **bireysel** → her şeyi tek başına yapacaksın. (s.13)

---

## Özet akış (tek bakışta)

```
Wikipedia metni
   ↓ (oku, ≥10 entity seç, türleri+ilişkileri belirle)
Mind map (teorik model, okunur)
   ↓
TEI/XML  ← çekirdek: yapı + annotasyon + kayıtlar + listRelation
   │           ↘ (metinde olmayan entity'ler)
   │            CSV (ekstra veri)
   ↓ XSLT          ↓ Python
 HTML          RDF parçaları
   ↓ Python (TEI→RDF)  ↓
        RDF  ──birleştir──►  tek graf (Turtle)
   ↑
Conceptual model (ontoloji) ── veriyle BİREBİR eşleşmeli
   ↓
Web sitesi (hepsini sunan rapor + GitHub Pages)
```
