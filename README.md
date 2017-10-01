[![Build Status](https://travis-ci.org/adakaleh/revistevechi-db.svg?branch=master)](https://travis-ci.org/adakaleh/revistevechi-db)

# reviste vechi - baza de date

Folosită în proiectele:
- https://github.com/adakaleh/revistevechi-wiki-scripts
- https://github.com/cristan2/ArhivaRevisteVechi

Baza de date se generează cu următoarele comenzi:
```
sqlite3 arhiva_reviste.db < schema.sql
sqlite3 arhiva_reviste.db < data.sql
```

Dump-ul se generează cu următoarele comenzi:
```
sqlite3 arhiva_reviste.db .schema > schema.sql
sqlite3 arhiva_reviste.db .dump > dump.sql
grep -vx -f schema.sql dump.sql > data.sql
rm dump.sql
sed -i 's/^PRAGMA foreign_keys=OFF;$/PRAGMA foreign_keys=ON;/g' data.sql
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
