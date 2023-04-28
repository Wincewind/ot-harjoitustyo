# Vaatimusmäärittely

## Caravan-pelin tarkoitus

Caravan on kahden pelaajan pelattava korttipeli, jota pelataan tavallisilla 52 korttipakan korteilla. Peli kehitettiin alunperin minipeliksi peliin nimeltä Fallout New Vegas ja sen englanninkieliset säännöt löytyvät [täältä.](https://fallout.fandom.com/wiki/Caravan_(game)#Background)


## Pelin käyttöliittymä

- [x] Mahdollisimman aikaisen pelin pelaamisen mahdollistamiseksi, aloitetaan kehittämällä tekstipohjainen käyttöliittymä kaksinpelinä.

- [x] Peliin voi luoda käyttäjätiedot, joiden valinta ja luonti näkymä aukeaisi ensin. Tämän jälkeen valitaan/kootaan pakka ja valitaan pelin aloitus.

- [x] Alla kuvankaappaus Fallout New Vegas:in pelikentästä sekä omasta toteutetusta versiosta:

New Vegas             |  Oma pygame versio
:-------------------------:|:-------------------------:
![](./kuvat/pelikentta_hahmotelma.png)  |  ![](./kuvat/caravan_gameboard.png)

## Perusversion toiminnallisuuksia

### Käyttäjätiedot ja pelipakan kokoaminen

- [x] Käyttäjätietojen valinta ikkunasta valitaan joko olemassa oleva nimi tai kirjoitetaan tekstikenttään uusi nimi ja valitaan "Create". 
- [ ] Oleellinen osa peliä, on pakan kasaaminen.
  - [ ] Tähän liittyy myös korttien kerääminen, mutta tämä on parempi jättää alustavasti jatkokehitysideaksi.
- [x] Oletus-pakka vaihtoehto.
- [ ] Mahdollisuus koota pakka satunnaisista saatavilla olevista korteista. 

### Pelaajat

Vastuksen tekoälyn kehittämisen haasteellisuuden vuoksi, perusversion kehitys aloitetaan tavoitteena, että peliä pelataan samalta koneelta. Aloittava pelaaja saa nähdä kädessään olevat kortit ensin ja toinen pelaaja sulkee silmänsä kunnes hänen vuoronsa tulee. Pelaajan pelattua jonkun kortin, vuoro vaihtuu hetken viiveellä, jolloin toinen pelaaja saa avata silmänsä ja vuoronsa päättänyt sulkee omansa.
- [x] Hotseat versio pelistä

## Jatkokehitysideoita

Perusversion jälkeen peliä täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Interaktiivisempi korttien käsittely kanssa, esim. "drag and drop" toiminnallisuus. 
- "Tekoäly" vastustaja.
- Korttien keräily mekaniikka, esim. voittamalla vastustajia.
- Sääntöjen muokkaaminen ["Meta"-taktikoinnin](https://fallout.fandom.com/wiki/Caravan_(game)#cite_note-1) tehokkuuden vähentämiseksi.
