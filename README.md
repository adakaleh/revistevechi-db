[![Build Status](https://travis-ci.org/adakaleh/revistevechi-db.svg?branch=master)](https://travis-ci.org/adakaleh/revistevechi-db)

# reviste vechi - baza de date

Folosită în proiectele:
- https://github.com/adakaleh/revistevechi-wiki-scripts
- https://github.com/cristan2/ArhivaRevisteVechi

Baza de date se generează cu:
```
sh genereaza.sh db
```

Dump-ul se generează cu:
```
sh genereaza.sh dump
```

---

Valori editii('tip', 'parinte')

* revista, NULL
* supliment, editie_id
* almanah, editie_id

Valori editii('disc_demo')

* CD
* DVD
* CD, DVD

Valori download('categorie')

* revista
* disc_CD
* disc_DVD
* disc_CD_scan
* disc_DVD_scan
* coperta_CD
* coperta_DVD

Valori editii('scan_info_observatii')

* mențiunile legate de calitatea scan-ului vor fi prefixate cu una dintre valorile LQ, MQ, GQ (low-quality, etc);
* dacă fișierul e de calitate foarte bună, se lasă gol (nu are sens să folosim HQ);
* alte aprecieri se trec după o liniuță (ex: "LQ - rescan, recrop" ar însemna "calitate scăzută, necesită rescan sau cel puțin un recrop").

Valori download('item')

* „item” e un index al fiecărui obiect dintr-un set de mai multe CD-uri (sau DVD-uri sau orice altceva) per editie_id
* coloana „item” ne permite să avem, de exemplu, mai multe CD-uri asociate unei reviste, cu mai multe link-uri de download pentru fiecare
* Exemplu:

```
id    editie_id   categorie    item    link
---   ---------   ---------    -----   -------------------------
1     170         'revista'    1       'https://archive.org/...'
2     170         'revista'    1       'https://scribd.com/...'
3     170         'CD'         1       'https://mediafire.com/cd1...'
4     170         'CD'         1       'https://mega.nz/cd1...'
5     170         'CD'         2       'https://mediafire.com/cd2...'
6     170         'CD'         2       'https://mega.nz/cd2...'
```

