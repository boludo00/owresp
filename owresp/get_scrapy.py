import json 
import requests
import logging, coloredlogs

class GetScrapy(object):

    def __init__(self, btag, platform, region, debug_level):
        
        coloredlogs.install()
        logging.basicConfig(level=debug_level,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )

        self.base_url = "http://enhanced-ow-api.herokuapp.com/"
        self.btag = btag   # note -- btag will require format of btag-0000 for PC users only
        self.platform = platform # ps4, xbox, pc
        self.region = region # na, kr, eu, oc
        self.data = self.make_request()

    def make_request(self):
        
        if self.region is None:
            user_url = self.base_url + self.btag + "/competetive/" + self.platform
        else:
            user_url = self.base_url + self.btag + "/competetive/" + self.platform + "/" + self.region
        
        logging.info("requesting at: %s" % (user_url))
    
        resp = requests.get(user_url)
        if resp.status_code == 200:
            logging.info("Request successful. Number of heroes returned: %d" %(len(resp.json()) - 1))
        else:
            logging.critical("Error, bad response.")
            return 
        return resp.json()