# sledenje-objektom

## Odvisnosti
* Windows
  * [Anaconda](https://www.anaconda.com/) s Python 3.7+
  * OpenCV,
  * Shapely,
  * Ujson.
  
* Linux
  * Python 3.7+,
  * OpenCV,
  * Shapely,
  * Ujson.
  
## Namestitev
Repozitorij klonirajte v poljubno mapo. 

### Windows
Namestite si okolje [Anaconda](https://www.anaconda.com/). Zaženite `Anaconda command prompt` in se v ukvazni vrstici premaknite v direktorij z datotekami sledilnika objektov. Zaženite ukaz `conda env create -f environment.yml` in nato aktiviratje okolje preko ukaza `conda activate tracker`.

### Linux
Namestite najnovejšo verzijo Python 3. V ukazni vrstici se premaknite v direktorij z datotekami sledilnika objektov in zaženite ukaz `pip3 install -r ./requirements.txt`.

### Spletni strežnik
Namestite in nastavite spletni strežnik [nginx](https://nginx.org/en/).

V datoteki `Resources.py` nastavite `gameLiveDataFileName = "..."` tako, da bo sledilnik podatke o tekmi zapisoval v mapo iz katere nginx streže spletno vsebino.

## Zagon
* Nastavitve sistema so v datoteki `Resources.py`.
* Podatki o ekipah in nastavitve tekme so v datoteki `gameData.json`.
* Sledenje zaženete z ukazom `python3 ./Tracker.py`, pri čemer se morate nahajati v mapi z datotekami sledilnika objektov. Če uporabljate Windows, morate to storiti preko programa `Anaconda command prompt`, v katerem ste pred tem aktivirali ustrezno okolje z ukazom `conda activate tracker`. 
