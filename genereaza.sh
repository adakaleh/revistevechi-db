#!/bin/sh

if [ "$1" = "db" ]; then
    sqlite3 arhiva_reviste.db < schema.sql
    sqlite3 arhiva_reviste.db < data.sql
elif [ "$1" = "dump" ]; then
    if test ! -f arhiva_reviste.db; then
        echo "lipsește arhiva_reviste.db"
        exit
    fi
    sqlite3 arhiva_reviste.db .schema > schema.sql
    sqlite3 arhiva_reviste.db .dump > dump.sql
    grep -vx -f schema.sql dump.sql > data.sql
    rm dump.sql
    sed -i 's/^PRAGMA foreign_keys=OFF;$/PRAGMA foreign_keys=ON;/g' data.sql
    sed -i '/^CREATE TABLE sqlite_sequence(name,seq);$/d' schema.sql
else
    echo 'lipsește parametrul: "db" sau "dump"'
fi
