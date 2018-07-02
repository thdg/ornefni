# **Örnefni API**

Einfalt API til að búa til ný íslensk örnefni og mannanöfn.
Hægt er búa til nöfn í nokkrum mismunandi flokkum:
- Sveit
- Landörnefni
- Vatnaörnefni
- Þéttbýli
- Sjávarörnefni
- Jökla- og snævarörnefni
- Drengjanöfn
- Stúlkunöfn
- Millinöfn

## **Aðgerðir**

### **URL:**
`GET  /:flokkur`

`GET /:flokkur/:n`

`GET /:flokkur/:n/:forskeyti`

### **URL breytur:**
`flokkur=[sveit, land, vatn, borg, sjor, jokull, kk, kvk, milli]`: Flokkur til að búa til nöfn úr

`n=[heiltala]`: Fjöldi nafna til að búa til, 0 < n <= 50

`forskeyti=[strengur]`: Búa til nöfn sem byrja á forskeyti

### **GET breytur**
`ekkitil=bool`: Sía út nöfn sem eru til


### **Dæmi:**
**URL:** `/jokull/`

**Code:** `200`

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
