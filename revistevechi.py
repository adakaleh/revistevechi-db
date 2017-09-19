# -*- coding: utf-8 -*-

import sqlite3
from string import Template
import re
import operator
import os
import collections

if not os.path.isdir("level"):
    os.mkdir("level")

conn = sqlite3.connect("arhiva_reviste.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

pagina_principala = """https://revistevechi.blogspot.ro/2011/07/level-1997-2004-colectia-de-reviste.html

https://mega.nz/#F!SxckBRQa!AZl0AUzjFQvg0AED2iWDBA

"""

template = Template("""====== LEVEL nr. $numar ($luna $an) ======
$contribuie
| {{ $img_coperta?direct&150 }} ||
^ Info ^^
| **Pagini** | $nr_pagini |$disc_demo$joc_complet
| **Preț** | $pret lei |$redactor_sef
$tabel_download
$lista_redactori
$cuprins""")

luna = {
    1: "ianuarie",
    2: "februarie",
    3: "martie",
    4: "aprilie",
    5: "mai",
    6: "iunie",
    7: "iulie",
    8: "august",
    9: "septembrie",
    10: "octombrie",
    11: "noiembrie",
    12: "decembrie",
}

# functie folosita pentru a genera textul unei ancore (#ancora)
# de exemplu, pentru numele redactorilor: K'shu -> kshu, Marius Ghinea -> marius_ghinea
def genereaza_ancora(string):
    return re.sub('[^A-z0-9 -]', '', string).lower().replace(" ", "_")

# face ca un string care contine caractere precum "|" si "^" sa poata fi inclus intr-un tabel
def in_tabel(string):
    return string.replace("|", "%%|%%").replace("^", "%%^%%")

# transofrma un cursor.fetchall() intr-o lista de dict-uri
def dictfetchall(cursor):
    return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

# functie care ia din DB link-urile de download si le sorteaza dupa prioritate
def get_downloads(editie_id, categorie):
    download_prioritati = ("archive.org", "libgen", "scribd.com", "mediafire.com", "mega.nz")

    c.execute("SELECT item, link FROM downloads WHERE editie_id = ? AND categorie = ?;", (str(editie_id), categorie))
    downloads = dictfetchall(c)

    for dwd in downloads:
        dwd["nume"] = dwd["link"].split("//", 1)[-1].split("/", 1)[0].replace("www.", "", 1)
        if dwd["nume"] in download_prioritati:
            dwd["prioritate"] = download_prioritati.index(dwd["nume"])
        else:
            dwd["prioritate"] = 99
    return sorted(downloads, key=operator.itemgetter("prioritate"))


# TODO: suplimente?
toate_revistele = conn.cursor().execute("SELECT * FROM editii WHERE tip = 'revista' AND revista_id = 7 ORDER BY an;")

for e in toate_revistele:

    # construieste pagina principala
    header_an = "\n\n===== %d =====\n\n" % e["an"]
    if header_an not in pagina_principala:
        pagina_principala += header_an

    # TODO: tabel
    pagina_principala += "[[level:%d:%d]], " % (e["an"], e["luna"])

    # sari peste revistele care nu au numar
    if e["numar"] == "":
        continue

    # creeaza directoare
    if not os.path.isdir("level/%d" % e["an"]):
        os.mkdir("level/%d" % e["an"])

    contribuie = ""
    if e["scan_info_observatii"]:
        contribuie = "\n<color red>--- //" + e["scan_info_observatii"] + ". Vă rugăm să [[:contribuie|contribuiți]].// ---</color>\n"


    ### tabel info ###

    img_coperta = ":level:%d:%d:level_%d.png" % (e["an"], e["luna"], e["numar"])

    disc_demo = ""
    if e["disc_demo"] not in (None, ""):
        img_disc = ":level:%d:%d:level_disc_%d.png" % (e["an"], e["luna"], e["numar"])
        disc_demo = "\n| **Disc demo** | " + e["disc_demo"] + " {{" + img_disc + "?direct&20}}|" # TODO: daca sunt mai multe discuri?

    joc_complet = ""
    if e["joc_complet"] not in (None, ""):
        joc_complet = "\n| **Joc complet** | " + e["joc_complet"] + " |"

    redactor_sef = ""
    if e["redactor_sef"] not in (None, ""):
        redactor_sef = "[[level:redactori#" + genereaza_ancora(e["redactor_sef"]) + "|" + e["redactor_sef"] + "]]"
        redactor_sef = "\n| **Redactor-șef** | " + redactor_sef + " |"


    ### download revista ###

    tabel_download = ""
    link_pagina_cuprins = ""

    downloads_revista = get_downloads(e["editie_id"], "revista")

    if len(downloads_revista):
        # extrage link-ul pentru cuprins
        link_cuprins = downloads_revista[0]["link"]
        if "archive.org" in link_cuprins:
            id_revista = link_cuprins.rsplit('/', 1)[-1]
            link_pagina_cuprins = "[[https://archive.org/stream/" + id_revista + "#page/n%d/mode/2up|%s]]"
        # construieste tabelul
        for dwd in downloads_revista:
            tabel_download += "| ::: |[[%s|%s]]|\n" % (dwd["link"], dwd["nume"])
        tabel_download = tabel_download.replace(":::", "**Revista**", 1)


    ### download CD/DVD ###

    link_cuprins_disc_demo = ""
    c.execute("SELECT pg_toc FROM articole WHERE editie_id = ? AND rubrica = 'Cuprins CD/DVD';", (e["editie_id"], ))
    pagina = c.fetchone()
    if pagina:
        pagina = pagina["pg_toc"]
        if link_pagina_cuprins != "":
            link_cuprins_disc_demo = link_pagina_cuprins % (pagina - 1, "cuprins") + ", "

    downloads_CD = get_downloads(e["editie_id"], "CD")

    if len(downloads_CD):
        tabel_download += "| **CD** |{{%s?linkonly|scan}}, %s[[catalog]]|\n" % (img_disc, link_cuprins_disc_demo)
        for dwd in downloads_CD:
            tabel_download += "| ::: |[[%s|imagine completă (%s)]]|\n" % (dwd["link"], dwd["nume"])

    downloads_DVD = get_downloads(e["editie_id"], "DVD")
    if len(downloads_DVD):
        tabel_download += "| **DVD** |{{%s?linkonly|scan}}, %s[[catalog]]|\n" % (img_disc, link_cuprins_disc_demo)
        for dwd in downloads_DVD:
            tabel_download += "| ::: |[[%s|imagine completă (%s)]]|\n" % (dwd["link"], dwd["nume"])

    if tabel_download != "":
        tabel_download = "^ Download ^^\n" + tabel_download


    ### lista redactori ###

    lista_redactori = ""
    redactori = {}
    for r in c.execute("SELECT autor, count() nr_articole FROM articole WHERE editie_id = ? GROUP BY autor;", (e["editie_id"], )):
        if not r["autor"]:
            continue
        # autorii pot fi mai multi, separati de virgule
        autori = r["autor"].split(",")
        for autor in autori:
            autor = autor.strip() # sterge spatiile de la inceput si sfarsit
            if autor not in redactori:
                redactori[autor] = 0
            redactori[autor] += r["nr_articole"]
    redactori = collections.OrderedDict(sorted(redactori.items())) # sorteaza redactorii alfabetic
    for autor, nr_articole in redactori.items():
        ancora = genereaza_ancora(autor)
        articol_e = "articole" if nr_articole > 1 else "articol"
        lista_redactori += "\n  * [[level:redactori#%s|%s]] (%s %s)" % (ancora, autor, nr_articole, articol_e)
    if lista_redactori != "":
        lista_redactori = "\n===== Redactori =====\n" + lista_redactori + "\n"


    ### cuprins ###

    cuprins = ""
    rubrica = ""
    for cup in c.execute("SELECT * FROM articole WHERE editie_id = ? ORDER BY pg_toc;", (e["editie_id"], )):

        if cup["rubrica"] == "Cuprins CD/DVD":
            continue

        if rubrica != cup["rubrica"]:
            rubrica = in_tabel(cup["rubrica"])
            cuprins += "^" + rubrica + "^^^^\n"

        titlu = cup["titlu"]
        if rubrica in ("Cuprins CD/DVD", "News", "Cheats") or (rubrica == "Chatroom" and titlu == ""):
            titlu = rubrica

        pagina = cup["pg_toc"]
        # daca link_pagina_cuprins a fost definit, completeaza-l si foloseste-l in loc de pagina
        if link_pagina_cuprins != "":
            pagina = link_pagina_cuprins % (pagina - 1, pagina)

        cuprins += Template("|$pagina|$titlu|$autor|$nota|\n").substitute(
            pagina = pagina,
            titlu = in_tabel(titlu),
            autor = cup["autor"],
            nota = in_tabel(cup["nota"]),
        )
    if cuprins != "":
        cuprins = "\n===== Cuprins =====\n" + cuprins + "\n"


    ### output pagina wiki ###

    fo = open("level/%d/%d.txt" % (e["an"], e["luna"]), "w")
    fo.write(template.substitute(
        numar = e["numar"],
        luna = luna[e["luna"]],
        an = e["an"],
        contribuie = contribuie,
        img_coperta = img_coperta,
        disc_demo = disc_demo,
        nr_pagini = e["nr_pagini"],
        joc_complet = joc_complet,
        pret = e["pret"],
        redactor_sef = redactor_sef,
        tabel_download = tabel_download,
        lista_redactori = lista_redactori,
        cuprins = cuprins,
    ))
    fo.close()


### output pagina principala ###

fo = open("level.txt", "w")
fo.write(pagina_principala)
fo.close()
