import logging
import os
import json
import xml.etree.ElementTree as ET 
import sqlite3
logging.basicConfig(level = logging.INFO)
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
    #incomplete 
    # def get_user_searches(self):
    #     logging.info("Getting User Search History...")
        
    #     xml_file = os.path.join(self.internal_cache_path, "shared_prefs", "search.xml")
    #     searches = []

    #     nodes = ET.parse(xml_file).getroot() 
    #     try:
    #         dump = json.loads(Utils.xml_attribute_finder(xml_file, "recent_history")["recent_history"])
    #         for i in dump: searches.append(i["keyword"])
    #     except:
    #         pass

    #     logging.info("{} search entrys found".format(len(searches)))
    #     return searches

    def get_videos_publish(self):
        logging.info("Getting published videos")
        videos = []
        base_path = os.path.join(self.cache_path, "cache", "aweme_publish")
        aweme_publish_files = os.listdir(base_path)

        for aweme_file in aweme_publish_files:
            dump = json.load(open(os.path.join(base_path, aweme_file)))
            aweme_list = dump.get("aweme_list")
            if aweme_list:
                for entry in aweme_list:
                    video ={}
                    video["created_time"] = entry.get("create_time")
                    video["video"] = str(entry.get("video"))#.get("animated_cover").get("url_list")[0]
                    
                    
                    timeline_event = {}
                    timeline_event["url"]= video["video"]
                    
                    self.timeline.append((video["created_time"],"publish", timeline_event))
                    videos.append(video)
    
        logging.info("{} video(s) found".format(len(videos)))
        return videos
    
    def get_last_session(self):
        logging.info("Getting last session...")
        session = []

        relevant_keys = ["page", "request_method", "is_first","duration","is_first","rip","duration","author_id","access2","video_duration","video_quality","access",
        "page_uid","previous_page","enter_method","enter_page","key_word","search_keyword","next_tab","search_type", "play_duration", "content"]

        db = os.path.join(self.cache_path, "databases", "ss_app_log.db")
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        results = cursor.execute("select tag, ext_json, datetime(timestamp/1000, 'unixepoch', 'localtime'), session_id from event order by timestamp")
        for entry in results:
            session_entry={}
            session_entry["action"] = entry[0]
            
            body_dump = json.loads(entry[1])
            session_entry["time"] =entry[2]
            session_entry["session_id"] = entry[3]
            
            timeline_event = {}
            timeline_event["action"]= session_entry["action"]
            
            self.timeline.append((session_entry["time"],"system", timeline_event))
            
            session.append(session_entry)

            #json body parser
            body = {}
            for key, value in body_dump.items():     
                if key in relevant_keys:
                    body[key] = value
            
            session_entry["body"] =body

        connection.close()
        return session

    def get_file_ext_from_directory(self,directory,ends_with):
        files = os.listdir(directory)
        f = None
        for file in files :
             if file.endswith(ends_with):
                f = os.path.join(directory,file)
        return f 

    def get_user_messages(self):
        logging.info("Getting User Messages...")
        base_path = os.path.join(self.cache_path, "databases")
        db = self.get_file_ext_from_directory(base_path,"_im.db")
        if not db:
            logging.info("User message database not found!")
            return [] 

        connection = sqlite3.connect(db)
        database = connection.cursor()
        
        conversations_list =[] 

        conversations_ids_list = database.execute("select conversation_id from conversation_core") 

        for conversation in conversations_ids_list:
            conversation_output={}

            id1 = conversation[0].split(':')[2]
            id2 = conversation[0].split(':')[3]

            conversation_output["participant_1"] = self.get_user_uniqueid_by_id(id1)
            conversation_output["participant_2"] = self.get_user_uniqueid_by_id(id2)
            conversation_output["messages"] = []
            
            messages_list = database.execute_query("select created_time/1000 as created_time, content as message, case when read_status = 0 then 'Not read' when read_status = 1 then 'Read' else read_status end read_not_read, local_info, type, case when deleted = 0 then 'Not deleted' when deleted = 1 then 'Deleted' else deleted end, sender from msg where conversation_id='{}' order by created_time;".format(conversation[0]))
            
            for entry in messages_list:
                message={}
                message["createdtime"] = entry[0]
                message["readstatus"] = str(entry[2])
                message["localinfo"] = entry[3]
                if entry[6] == int(id1):
                    message["sender"] = conversation_output["participant_1"]
                    message["receiver"] = conversation_output["participant_2"]
                else:
                    message["sender"] = conversation_output["participant_2"]
                    message["receiver"] = conversation_output["participant_1"]
                message_type = entry[4]

                message_dump = json.loads(entry[1])
                body=""

                if  message_type == 7: #text message type
                    message["type"] = "text"
                    body = message_dump.get("text")

                elif message_type == 8: #video message type
                    message["type"] = "video"
                    body= "https://www.tiktok.com/@tiktok/video/{}".format(message_dump.get("itemId"))
                
                elif message_type == 5:
                    message["type"] = "gif"
                    body=message_dump.get("url").get("url_list")[0]
                else:
                    message["type"] = "unknown"
                    body= str(message_dump)
                
                message["message"] = body
                message["deleted"] = str(entry[5])
                conversation_output["messages"].append(message)

                timeline_event = {}
                timeline_event["from"]= message["sender"]
                timeline_event["to"]= message["receiver"]
                timeline_event["message"]= message["message"]
                self.timeline.append((message["createdtime"],"message", timeline_event))
            
            connection.close()
            conversations_list.append(conversation_output)


        return conversations_list

module = ForensicsModule('../data')
profile = module.get_user_profile()
# print(profile)
videos = module.get_videos_publish()
# print(videos)
session = module.get_last_session()
print(session)
conversation = module.get_user_messages()
print(conversation)