# Ohjelmistotekniikka, harjoitustyö
# Tehtävät
## Viikko 1
[gitlog.txt](laskarit/viikko1/gitlog.txt)

[komentorivi.txt](laskarit/viikko1/komentorivi.txt)
## Viikko 2
[kattavuusraportti.png](laskarit/viikko2/kattavuusraportti.png)


# Caravan

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

### Ohjelman suorittaminen

Ohjelman pystyy suorittamaan komennolla:

```bash
poetry run invoke start
```
Tämän komennon aloittama ohjelma tulee kehittymään viikottain.

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
