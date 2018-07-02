**Örnefni API**
====

Einfalt API til að búa til ný íslensk örnefni og mannanöfn.
Hægt er búa til nöfn í nokkrum mismunandi flokkum:
- Sveit
- Landörnefni
- Vatnaörnefni
- Þéttbýli
- Sjávarörnefni
- Jökla- og snævarörnefni
- Karlkynsnöfn (ekki komið)
- Kvennmansnöfn (ekki komið)

**Aðgerðir**
----
**URL:**
  /:flokkur
  /:flokkur/:n
  /:flokkur/:n/:forskeyti

**Method:**
  `GET`

 **URL breytur:**

   `flokkur=[farm, land, water, town, see, ice, kk, kvk]`: Flokkur til að búa til nöfn úr
   `n=[heiltala]`: Fjöldi nafna til að búa til
   `forskeyti=[strengur]`: Búa til nöfn sem byrja á <forskeyti>

**Dæmi:**

  * **URL:** /ice/
    **Code:** 200
    **Content:** `{"names":["Sandfellsjökull",
"Kvíslajökull eystri-Brækur",
"Jökull eystri",
"Lónsjökull",
"Hrútárjökull",
"Lambárjökull",
"Austurárdalsjökull",
"Tungnakvíslajökull",
"Vatnsdalsjökull",
"Reka"]}
`
