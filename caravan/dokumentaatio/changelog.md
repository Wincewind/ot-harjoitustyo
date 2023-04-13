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
