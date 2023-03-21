import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_setUp_saldo_oikein(self):
        self.assertEqual(str(self.maksukortti),"Kortilla on rahaa 10.00 euroa")
    
    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(100)

        self.assertEqual(str(self.maksukortti),"Kortilla on rahaa 11.00 euroa")

    def test_rahan_ottaminen_vahentaa_riittavaa_saldoa(self):
        kortti = Maksukortti(1000)
        self.assertEqual(kortti.ota_rahaa(500),True)
        self.assertEqual(str(kortti),"Kortilla on rahaa 5.00 euroa")

    def test_rahan_ottaminen_ei_vahenna_liian_pienta_saldoa(self):
        kortti = Maksukortti(400)
        self.assertEqual(kortti.ota_rahaa(500),False)
        self.assertEqual(str(kortti),"Kortilla on rahaa 4.00 euroa")