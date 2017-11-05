import unittest
import sys, os
import logging
# sys.path.append("..")
sys.path.insert(0, os.getcwd())
from owdata import OWData
import coloredlogs

coloredlogs.install()
logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG)

class TestDataXBL(unittest.TestCase):

    def setUp(self):
        self.owd = OWData("boludo00", "xbl", debug=True, debug_level=logging.CRITICAL)
        self.owd.data.pop("ALL HEROES", None)

    def test_heros_and_data(self):
        assert self.owd.heros == self.owd.data.keys()

    def test_hero_indexing(self):
        for i, hero in enumerate(self.owd.wpn_acc):
            print self.owd.wpn_acc[hero.name]
            assert self.owd.wpn_acc[hero.name].value == hero.value

    def test_div_epm(self):
        assert self.owd.elimspm.values == (self.owd.total_elims / self.owd.mins_played).values

    def test_div_dpm(self):
        assert self.owd.deathspm.values == (self.owd.total_deaths / self.owd.mins_played).values
    
    def test_div_dmgpm(self):
        assert self.owd.dmgpm.values == (self.owd.total_dmg / self.owd.mins_played).values

    def test_div_dpm(self):
        assert self.owd.solokills.values == (self.owd.total_solo_kills / self.owd.mins_played).values

