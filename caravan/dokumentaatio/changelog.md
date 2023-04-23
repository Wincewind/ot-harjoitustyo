# Changelog

## Viikko 3
- Lisätty luokkia pelin komponenteille.
  - Card, CardSet, Deck, Caravan, Player
- Alustettu main:iin ajettava demo, missä voidaan lisätä kortteja pelaajan Caravaneihin. 
  - Korttien arvojen tai sallittujen positioiden laskussa ei vielä oteta huomioon pelin sääntöjä

## Viikko 4
- Lisätty moduuli "rules.py", jolla voidaan varmistaa kaikkia pelin keskeisiä sääntöjä, niin lailliset siirrot kuten myös kuvakorttien efektit.
- Lisätty pelin tekstipohjaiselle käyttöliittymälle luokka GameInterface. 
  - Toteutettu tällä pelin ensimmäinen toimiva versio jota voi pelata kaksinpelinä ns. Hotseat-moninpelimuotona, eli samalta koneelta.
  - Päivitetty main starttaamaan tämä versio poetry start:illa.

## Viikko 5
- Toteutettu ensimmäinen versio pelin graaffisesta käyttöliittymästä pygamella.
  - Ainoat puuttuvat toiminnallisuudet itse pelistä on korttien ja karavaanien poisto.
  - Main starttaa nyt tämän version pelistä.
- Pelinkulkua ja näytön päivitystä suoritetaan uudella Gameloop luokalla ja kortti "sprite":jen sijoituksen, värin, yms. päivitystä tehdään GameSprites luokasta.
