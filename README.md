# Ohjelmistotekniikka, harjoitustyö
# Tehtävät
## Viikko 1
[gitlog.txt](laskarit/viikko1/gitlog.txt)

[komentorivi.txt](laskarit/viikko1/komentorivi.txt)
## Viikko 2
[kattavuusraportti.png](laskarit/viikko2/kattavuusraportti.png)


# Caravan

Caravan on kahden pelaajan pelattava korttipeli, jota pelataan tavallisilla 52 korttipakan korteilla. Tämä versio pelistä on kehitetty käyttäen Pygame:a.

## Dokumentaatio

- [Vaatimusmaarittely.md](caravan/dokumentaatio/vaatimusmaarittely.md)
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
