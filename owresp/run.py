from argparser import get_debug_level, get_user_info
import sys
import logging
import coloredlogs
from owdata import OWData
from grapher import Grapher

if __name__ == "__main__":
    debug = True
    dlevel = get_debug_level(sys.argv)
    coloredlogs.install()
    logger = logging.getLogger(__name__)
    coloredlogs.install(level=dlevel)
    btag, system, region = get_user_info(sys.argv)
    owd = OWData("boludo00", "xbl", region=region, debug=debug, debug_level=dlevel)

    print owd.total_elims / owd.mins_played 
    print owd.elimspm

    # for hero in owd.heros:
    #     print owd.get_hero_summary(hero), "\n"
    
    # hs = owd.kstreaks['Genji']
    # y, x = zip(*owd.avg_elims.get_data())
    # Grapher().multiple_tiles([owd.top_epm,owd.top_deaths,owd.top_dmgs,owd.top_skills,owd.top_wpn,owd.top_played])
    # plt = Grapher().horizontal_bar(x, y)