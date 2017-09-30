CREATE TABLE "reviste" (
	`revista_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`revista_nume`	TEXT,
	`revista_alias`	TEXT,
	`status`	TEXT,
	`tip`	TEXT,
	`perioada`	TEXT,
	`aparitii`	TEXT,
	`descriere`	TEXT,
	`link_oficial`	TEXT,
	`observatii`	TEXT
);
CREATE TABLE "editii" (
	`editie_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`revista_id`	INTEGER NOT NULL,
	`tip`	TEXT DEFAULT 'revista',
	`parinte_editie_id`	TEXT,
	`numar`	INTEGER NOT NULL,
	`an`	INTEGER NOT NULL,
	`luna`	INTEGER NOT NULL,
	`luna_sfarsit`	TEXT,
	`pret`	NUMERIC,
	`nr_pagini`	INTEGER,
	`disc_demo`	TEXT,
	`joc_complet`	TEXT,
	`redactor_sef`	TEXT,
	`editie_link_oficial`	TEXT,
	`editie_observatii`	TEXT,
	`scan_info_nr_pg`	INTEGER,
	`scan_info_pg_lipsa`	TEXT,
	`scan_info_observatii`	TEXT,
	`scan_info_credits`	TEXT,
	FOREIGN KEY(`revista_id`) REFERENCES `reviste`(`revista_id`)
);
CREATE TABLE "downloads" (
	`editie_id`	INTEGER NOT NULL,
	`categorie`	TEXT NOT NULL DEFAULT 'revista',
	`item`	INTEGER DEFAULT 1,
	`link`	TEXT UNIQUE,
	FOREIGN KEY(`editie_id`) REFERENCES `editii`(`editie_id`)
);
CREATE TABLE "articole" (
	`articol_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`revista_id`	INTEGER NOT NULL,
	`revista_nume`	TEXT NOT NULL,
	`editie_id`	INTEGER NOT NULL,
	`editie_an`	INTEGER NOT NULL,
	`editie_luna`	INTEGER NOT NULL,
	`editie_luna_sfarsit`	TEXT,
	`editie_numar`	INTEGER NOT NULL,
	`pg_toc`	INTEGER,
	`pg_count`	INTEGER,
	`rubrica`	TEXT,
	`titlu`	TEXT,
	`joc_platforma`	TEXT,
	`autor`	TEXT,
	`nota`	TEXT,
	FOREIGN KEY(`editie_id`) REFERENCES `editii`(`editie_id`)
);
