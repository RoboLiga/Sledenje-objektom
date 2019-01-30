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

V sistemu Windows si namestite okolje [Anaconda](https://www.anaconda.com/). Zaženite `Anaconda command prompt` in se v ukvazni vrstici premaknite v direktorij z datotekami sledilnika objektov. Zaženite ukaz `conda env create -f environment.py` in nato aktiviratje okolje preko ukaza `conda activate tracker`.

V okolju Linux si namestite najnovejšo verzijo Python 3. V ukazni vrstici se premaknite v direktorij z datotekami sledilnika objektov in zaženite ukaz `pip install -r ./requirements.txt`.

## Zagon
* Vse sistemske nastavitve so v datoteki `Resources.py`.
* Podatki o ekipah in nastavitve tekme so v datoteki `gameData.json`.
* Sledenje zaženete z ukazom `python ./Tracker.py`, pri čemer se morate nahajati v mapi z datotekami sledilnika objektov. Če uporabljate Windows, morate to storiti preko programa `Anaconda command prompt`, v katerem ste pred tem aktivirali ustrezno okolje z ukazom `conda activate tracker`. 
