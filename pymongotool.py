# -*-coding:utf-8 -*-
import pymongo

from nec_scraper import settings
connection = pymongo.MongoClient(settings.MONGO_URI)
with open('./data.txt', 'w', encoding='utf8') as f:
    db = connection[settings.MONGO_DB]
    print(db.collection_names())
    users = db[settings.MONGO_COLLECTION_NAME]
    count = 0
    for item in users.find():
        try:
            print("Number:", count)
            print(item['_id'])
            print(item['rating_num'])
            # print(item['articleContent'])
            f.write("Number:%d\n" % count)
            f.write("articleId:%s\n" % (item['_id']))
            count = count + 1
        except Exception as e:
            print(e)
