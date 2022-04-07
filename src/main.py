import logging
import os
import json
import xml.etree.ElementTree as ET 
class ForensicsModule:     

    def __init__(self, cache_path) :
        self.cache_path = cache_path
        self.timeline = []

    def get_user_profile(self):
            
            logging.info("Getting user profile...")
            xml_file = open(os.path.join(self.cache_path, "shared_prefs", "aweme_user.xml"))
            user_profile ={}
            # values = xmltodict.parse(xml_file.read())
            nodes = ET.parse(xml_file).getroot() 
            for key in nodes:
                if key.attrib["name"].endswith("_aweme_user_info"):
                    #try:
                    dump=json.loads(key.text)
                    atributes =["account_region", "follower_count","following_count", "gender", "google_account", "is_blocked", "is_minor", "nickname", "register_time", "sec_uid", "short_id", "uid", "unique_id"]

                    for index in atributes:
                        if index in dump:
                            user_profile[index] = dump[index]
                    break
                
            user_profile["url"] = "https://www.tiktok.com/@{}".format(user_profile["unique_id"])
            
            timeline_event = {}
            timeline_event["uniqueid"] = user_profile["unique_id"] 
            timeline_event["url"]= user_profile["url"]

            self.timeline.append((user_profile["register_time"],"user", timeline_event))
            
            return user_profile
    

module = ForensicsModule('../data')
profile = module.get_user_profile()
print(profile)