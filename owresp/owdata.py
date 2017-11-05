import json
import re
from get_scrapy import GetScrapy
import coloredlogs, logging
from herostat import HeroStat, HerosStats
from argparser import get_debug_level
from grapher import Grapher
import sys, os
import numpy as np
import pandas as pd


class OWData(GetScrapy):

    """
        An instance of an OWData object will have made a single GET
        request in its instantiation and thereafter store useful
        and relevant data in a precise and clean structure. This
        will ease the burden of finding bugs in the overall RESTful
        service by writing more modular code as testing will be
        straight forward. 
    """

    def __init__(self, btag, platform, region=None, debug=False, debug_level=logging.CRITICAL):
        """
        Initializes a OWData instance, which delegates some 'setup' work to 
        the GetScrapy class which handles populating the data by making the
        request.

        :param btag: battletag of user. -- note: if PC player, btag should be in format of btag-####
        :param platform: one of xbl, pc, ps4
        :param region: FOR PC ONLY: one of na, eu, kr, oc 

        :type btag: str
        :type platform: str
        :type region: str

        """
        assert platform in ["xbl", "pc", "ps4"], platform + " must be in " + str(["xbl", "pc", "ps4"])
        logging.info("btag = %s, platform = %s, region = %s, debug = %s, debug_level = %s" % (btag, platform, region, debug, debug_level))
        if not debug:
            super(OWData, self).__init__(btag, platform, region, debug_level)
        else:
            if __file__ == "owdata.py":   
                with open("test_data/sample.json") as f:
                    self.data = json.loads(f.read())
            else:
                with open(os.path.dirname(__file__) + "/test_data/sample.json") as f:
                    self.data = json.loads(f.read())
        
        self.set_heros()
        self.set_avg_elims()
        self.set_best_kstreak()
        self.set_total_elims()
        self.set_minutes_played()
        self.set_total_deaths()
        self.set_total_dmg()
        self.set_total_solo_kills()
        self.set_weapon_accuracy()
        self.set_games_played()
        self.set_kdrs()
        self.summary = self.make_summary_table()


    def set_heros(self):
        """
        Called upon init. Sets the OWData instance's heros property.

        :returns: list of str

        """
        heros = [i for i in self.data if i != "ALL HEROES"]
        logging.info("Heros: %s" % heros)
        self.heros = heros

    def get_heros(self):
        return self.heros

    def set_avg_elims(self):
        avg_elims = self.hero_crawler("Average", "Eliminations - Average")
        logging.debug("%s: %s" % (avg_elims.stat_name, avg_elims))
        self.avg_elims = avg_elims
    
    def get_avg_elims(self):
        return self.avg_elims

    def set_best_kstreak(self):
        kstreaks = self.hero_crawler("Best", "Kill Streak - Best")
        logging.debug("%s: %s" % (kstreaks.stat_name, kstreaks))
        self.kstreaks = kstreaks
    
    def get_best_kstreak(self):
        return self.kstreaks

    def set_total_elims(self):
        total_elims = self.hero_crawler("Combat", "Eliminations")
        logging.debug("%s: %s" % (total_elims.stat_name, total_elims))
        self.total_elims = total_elims
    
    def get_total_elims(self):
        return self.total_elims

    def set_total_deaths(self):
        total_deaths = self.hero_crawler("Deaths", "Deaths")
        logging.debug("%s: %s" % (total_deaths.stat_name, total_deaths))
        self.total_deaths = total_deaths

    def get_total_deaths(self):
        return self.total_deaths

    def set_total_dmg(self):
        
        def remove_commas(seq):
            if isinstance(seq, int):
                return seq
            return eval("".join(seq.split(",")))

        heroes = self.hero_crawler("Combat", "All Damage Done", evl=False)
        total_dmg = HerosStats("Combat: Damage Done", map(lambda hero: (hero.name, remove_commas(str(hero.value))), heroes))
        logging.debug("%s: %s" % (total_dmg.stat_name, total_dmg))
        self.total_dmg = total_dmg
    
    def get_total_dmg(self):
        return self.total_dmg

    def set_total_solo_kills(self):
        total_solo_kills = self.hero_crawler("Combat", "Solo Kills")
        logging.debug("%s: %s" % (total_solo_kills.stat_name, total_solo_kills))
        self.total_solo_kills = total_solo_kills
    
    def get_total_solo_kills(self):
        return self.total_solo_kills

    def set_weapon_accuracy(self):

        def parse_pct(pct):
            if isinstance(pct, int):
                return pct
            return eval(pct.split("%")[0]) / 100.

        heroes = self.hero_crawler("Combat", "Weapon Accuracy", evl=False)
        wpn_acc = HerosStats("Combat: Weapon Accuracy", map(lambda hero: (hero.name, parse_pct(str(hero.value))), heroes))
        logging.debug("%s: %s" % (wpn_acc.stat_name, wpn_acc))
        self.wpn_acc = wpn_acc
    
    def get_weapon_accuracy(self):
        return self.wpn_acc

    def set_games_played(self):
        games_played = self.hero_crawler("Game", "Games Played")
        logging.debug("%s: %s" % (games_played.stat_name, games_played))
        self.games_played = games_played

    def get_games_played(self):
        return self.games_played

    def set_minutes_played(self):

        def strtime_eval(time_str):
            
            if "second" in time_str:
                return 1 
            if time_str == "--":
                return 1
            assert "hour" in time_str or "minute" in time_str, "malformed input: '" + time_str + "'"
            split = time_str.split(" ")
            rawnum = eval(split[0])

            if "hour" in split[1]:
                time = rawnum * 60
            elif "minute" in split[1]:
                time = rawnum
            return float(time)

        mins_played = HerosStats("Game: Time Played", map(lambda hero: (hero.name, strtime_eval(hero.value)), self.hero_crawler("Game", "Time Played", evl=False)))
        logging.debug("%s: %s" % (mins_played.stat_name, mins_played))
        self.mins_played = mins_played
    
    def get_minutes_played(self):
        return self.mins_played

    def set_kdrs(self):
        kdrs = (self.total_elims / self.total_deaths)
        logging.info(kdrs.__dict__.keys())
        kdrs.stat_name = "K/D ratio"
        logging.debug("%s: %s" % (kdrs.stat_name, kdrs))
        self.kdrs = kdrs

    def get_kdrs(self):
        return self.kdrs


    def make_summary_table(self):
        """
        Summary will correspond to top 3 played heros in variety of stats.

        elims/min?
        deaths/min?
        dmg/min?
        solokills/min?
        weapon acc?
        winrate? 
        most dmg ingame?
        avg time on fire?
         
        """

        def data_packer(total_stat, mins_played):
            """
            This helper function serves to calculate a stat per minute, given by `total_stat`.

            :param total_stat: The HerosStats instance to calculate per minute on
            :param mis_played: The HeroStats instance of minutes played
            :type total_stat: HerosStats
            :type total_stat: HerosStats
            :returns: HerosStats 
            """
            logging.debug("...Data Packing stat: %s" % (total_stat.stat_name))
            stat_min = np.array(total_stat.values) / np.array(mins_played.values)
            stat_min_hs = HerosStats(total_stat.stat_name+"/Minute", zip(total_stat.values, stat_min))
            return stat_min_hs

        def get_top_three(col):
            """
            Finds the top 3 heros in the stat specified by `col`. 
            Only looks for heros that have more than 5 games played. 

            :param col: The stat to reference
            :type col: str
            """
            top_stat = df[df['Games Played'] > 5][col].nlargest(3)
            logging.info("\n%s" % top_stat)
            top_stat_hs = HerosStats(col, zip(top_stat.index, top_stat))
            logging.debug("%s (Top 3): %s" % (top_stat_hs.stat_name, top_stat_hs))
            return top_stat_hs

        elims_min_hs = data_packer(self.total_elims, self.mins_played)        
        deaths_min_hs = data_packer(self.total_deaths, self.mins_played)
        dmg_min_hs = data_packer(self.total_dmg, self.mins_played)
        solo_kills_hs = data_packer(self.total_solo_kills, self.mins_played)

        wpn_acc = self.wpn_acc
        games_played = self.games_played

        data = {
            "Elims/Min": elims_min_hs.values,
            "Deaths/Min": deaths_min_hs.values,
            "Dmg/Min": dmg_min_hs.values,
            "SoloKills/Min": solo_kills_hs.values,
            "Weapon Accuracy": wpn_acc.values,
            "Games Played": games_played.values
        }

        df = pd.DataFrame(data=data, index = self.heros)
        
        logging.info("\n%s" % df)

        self.elimspm = HerosStats("Elims/Min", zip(df.index, df['Elims/Min']))
        self.deathspm = HerosStats("Deaths/Min", zip(df.index, df['Deaths/Min']))
        self.dmgpm = HerosStats("Dmg/Min", zip(df.index, df['Dmg/Min']))
        self.solokills = HerosStats("SoloKills/Min", zip(df.index, df['SoloKills/Min']))
        logging.debug("\n%s" % self.elimspm)
        logging.debug("\n%s" % self.deathspm)
        logging.debug("\n%s" % self.dmgpm)
        logging.debug("\n%s" % self.solokills)

        self.top_elimspm = get_top_three('Elims/Min')
        self.top_deathspm = get_top_three('Deaths/Min')
        self.top_dmgs = get_top_three('Dmg/Min')
        self.top_solokills = get_top_three('SoloKills/Min')
        self.top_wpnacc = get_top_three('Weapon Accuracy')
        self.top_played = get_top_three('Games Played')


    def get_hero_summary(self, hero):
        """
        Display several stats for a given hero. 

        :param hero: The hero name
        :type hero: str or instance of one HeroStat object

        :returns: str

        """
        logging.debug(self.elimspm[hero])
        s1 = "%s\nEliminations/Minute: %f" % (hero, self.elimspm[hero].get_value())
        s2 = "Accuracy: %f" % self.wpn_acc[hero].get_value()
        s3 =  "Damage/Minute: %f" % self.dmgpm[hero].get_value()
        s4 = "K/D ratio: %s" % self.kdrs[hero].get_value()
        return "\n".join([s1, s2, s3, s4])


    def hero_crawler(self, cat, subcat, evl=True):
        """
        This method is intended to be used whenever data is requested in such 
        a way where a mapping is directly accomplished by response indexing.
        Populates a list of heros mapping heros to data, in this specified
        by the parameters. 

        Example return:

        >>> self.set_avg_elims()
        >>> [(u'Pharah', 23.13), (u'McCree', 22.38), (u'Widowmaker', 22.31)]

        .. note:: Need to subclass a sort of hero data class to better repr this data type. 

        Something like... when printed of course.
        HeroDataBin(stat=Average Eliminations Per Game, data=[(u'Pharah', 23.13), (u'McCree', 22.38), (u'Widowmaker', 22.31)])

        :param cat: The 'parent' category of the data, e.g. "Average" or "Game"
        :param subcat: The subcategory corresponging to param cat.
                       e.g. if cat is "Best", subcat can be "All Damage Done - Most in Game".

        :returns: HerosStats object 

        """
        values = []
        for hero in self.heros:

            try:
                val = self.data[hero][cat][subcat]
                
                if evl:
                    values.append(eval(val)) # need to use eval() for strings
                else:
                    values.append(val)
            except:
                logging.warning("NO DATA FOR %s ON KEYS %s AND/OR %s" % (hero, cat, subcat))
                values.append(1)
                
        stat_name = cat + ": " + subcat
        hs = HerosStats(stat_name, zip(self.heros, values))
        return hs