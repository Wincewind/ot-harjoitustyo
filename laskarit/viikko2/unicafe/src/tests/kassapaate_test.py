import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_konstruktori_toimii(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)

    def test_edullinen_kateisosto_toimii(self):
        vaihtorahat = self.kassapaate.syo_edullisesti_kateisella(500)
        vaihtorahat = self.kassapaate.syo_edullisesti_kateisella(vaihtorahat)
        self.assertEqual(self.kassapaate.edulliset,2)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100480)
        self.assertEqual(vaihtorahat,20)

    def test_ei_maksua_edullisesta_jos_kateisraha_riittamaton(self):
        vaihtorahat = self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(vaihtorahat,100)

    def test_maukas_kateisosto_toimii(self):
        vaihtorahat = self.kassapaate.syo_maukkaasti_kateisella(1000)
        vaihtorahat = self.kassapaate.syo_maukkaasti_kateisella(vaihtorahat)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,2)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100800)
        self.assertEqual(vaihtorahat,200)

    def test_ei_maksua_maukkaasta_jos_kateisraha_riittamaton(self):
        vaihtorahat = self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(vaihtorahat,100)

    def test_edullinen_veloitus_toimii_kortilla(self):
        kortti = Maksukortti(500)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti),True)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti),True)
        self.assertEqual(self.kassapaate.edulliset,2)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(kortti.saldo,20)

    def test_maukas_veloitus_toimii_kortilla(self):
            kortti = Maksukortti(1000)
            self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti),True)
            self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti),True)
            self.assertEqual(self.kassapaate.edulliset,0)
            self.assertEqual(self.kassapaate.maukkaat,2)
            self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
            self.assertEqual(kortti.saldo,200)

    def test_raha_ei_riita_kortilla_edulliseen_lounaaseen(self):
        kortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti),False)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(kortti.saldo,200)

    def test_raha_ei_riita_kortilla_maukkaaseen_lounaaseen(self):
        kortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti),False)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(kortti.saldo,200)
    
    def test_saldon_lataus_toimii(self):
        kortti = Maksukortti(200)
        self.kassapaate.lataa_rahaa_kortille(kortti,500)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100500)
        self.assertEqual(kortti.saldo,700)

    def test_negatiivisen_summan_lataus_ei_muuta_saldoja(self):
        kortti = Maksukortti(200)
        self.kassapaate.lataa_rahaa_kortille(kortti,-500)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(kortti.saldo,200)

    # seuraavissa testeissä tarvitaan myös Maksukorttia jonka oletetaan toimivan oikein
    # Korttiosto toimii sekä edullisten että maukkaiden lounaiden osalta
    #     Jos kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
    #     Jos kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
    #     Jos kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu, myytyjen lounaiden määrä muuttumaton ja palautetaan False
    #     Kassassa oleva rahamäärä ei muutu kortilla ostettaessa
    # Kortille rahaa ladattaessa kortin saldo muuttuu ja kassassa oleva rahamäärä kasvaa ladatulla summalla
