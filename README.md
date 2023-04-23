# Caravan, ohjelmistotekniikka harjoitustyö

Caravan on kahden pelaajan pelattava korttipeli, jota pelataan tavallisilla 52 korttipakan korteilla. Tämä versio pelistä on kehitetty käyttäen Pygame:a. Pelin kontrolleihin löytyy ohjeet pelinäytöltä, mutta tarkat kuvaukset pelin tavoitteesta, säännöistä ja eri korttien tarkemmista efekteistä voi lukea [täältä.](https://www.pagat.com/invented/caravan.html) 

## Dokumentaatio

- [Vaatimusmaarittely.md](caravan/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuuri.md](caravan/dokumentaatio/arkkitehtuuri.md)
- [Työaikakirjanpito](caravan/dokumentaatio/tuntikirjanpito.md)
- [Changelog](caravan/dokumentaatio/changelog.md)

## Asennus

Kun repo on kloonattu haluamaasi hakemistoon, siirry [caravan](caravan/)-alihakemistoon ja asenna riippuvuudet komennolla:

```bash
poetry install
```

## Komentorivitoiminnot

### Pelin käynnistäminen

Pelin käynnistys tapahtuu suorittamalla komento:

```bash
poetry run invoke start
```
Komennon käynnistämä peli tulee kehittymään viikkottain.

### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu _caravan/htmlcov/_-hakemistoon.


### Pylint

Laatutarkistuksen pytyy suorittamaan [.pylintrc](caravan/.pylintrc) määritysten mukaisesti komennolla:

```bash
poetry run invoke lint
```
