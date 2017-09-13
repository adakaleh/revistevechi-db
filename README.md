# reviste vechi

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
```
