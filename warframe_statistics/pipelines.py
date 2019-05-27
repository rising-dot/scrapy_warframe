# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
import datetime

# this code is for local database
class WarframeStatisticsPipeline(object):
    collection = 'prime_statistics'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if self.db[self.collection].count_documents({"item_name": item.get("item_name")}) == 1:

            self.db[self.collection].update_one(
                {"item_name": item.get("item_name")},
                {
                    "$push": {
                        "buy.max_value": item.get("buy").get("max_value")[0],
                        "buy.min_value": item.get("buy").get("min_value")[0],
                        "buy.avg_value": item.get("buy").get("avg_value")[0],
                        "buy.accuracy_value": item.get("buy").get("accuracy_value")[0],
                        "sell.max_value": item.get("sell").get("max_value")[0],
                        "sell.min_value": item.get("sell").get("min_value")[0],
                        "sell.avg_value": item.get("sell").get("avg_value")[0],
                        "sell.accuracy_value": item.get("sell").get("accuracy_value")[0]
                    }
                }
            )

            #check for max 24
            scrap_x_time = 25
            from_zero_to = 24

            for check in self.db[self.collection].find({"item_name": item.get("item_name")}):


                if len(check.get("buy").get("max_value")) >= scrap_x_time and len(
                        check.get("buy").get("min_value")) >= scrap_x_time and len(
                        check.get("buy").get("avg_value")) >= scrap_x_time and len(
                        check.get("buy").get("accuracy_value")) >= scrap_x_time and len(
                        check.get("sell").get("max_value")) >= scrap_x_time and len(
                        check.get("sell").get("min_value")) >= scrap_x_time and len(
                        check.get("sell").get("avg_value")) >= scrap_x_time and len(
                        check.get("sell").get("accuracy_value")) >= scrap_x_time:


                    sell_buy = ["buy", "sell"]

                    statistics_data = {}
                    for text in sell_buy:
                        max_value = max(check.get(text).get("max_value")[0:from_zero_to])
                        min_value = min(check.get(text).get("min_value")[0:from_zero_to])
                        avg_value = round(sum(check.get(text).get("avg_value")[0:from_zero_to]) / len(check.get(text).get("avg_value")[0:from_zero_to]), 2)
                        accuracy_value = round((sum(check.get(text).get("accuracy_value")[0:from_zero_to]) / 240) * 100, 2)

                        #insert the last value back into it and delete the old data
                        self.db[self.collection].update_one(
                           {"item_name": check.get("item_name")},
                           { "$set":
                              {
                                text+".max_value": check.get(text).get("max_value")[from_zero_to:scrap_x_time],
                                text+".min_value": check.get(text).get("min_value")[from_zero_to:scrap_x_time],
                                text+".avg_value": check.get(text).get("avg_value")[from_zero_to:scrap_x_time],
                                text+".accuracy_value": check.get(text).get("accuracy_value")[from_zero_to:scrap_x_time]

                              }
                           }
                        )
                        #create the new vaule for the day
                        statistics_data[text] = {
                            "max_value": max_value,
                            "min_value": min_value,
                            "avg_value": avg_value,
                            "accuracy_value": accuracy_value
                        }

                    today_datetime = datetime.date.today()

                    #now insert it into the database if over 121

                    self.db[self.collection].update_one(
                            {"item_name": check.get("item_name")},
                            {
                                "$push": {
                                    "statistics_list": {
                                                "datetime" : str(today_datetime),
                                                "data": statistics_data

                                    }
                                }
                            }
                    )
            #how many days do we want ?
            self.db[self.collection].update_one(
                {"statistics_list.120": {"$exists": 1}},
                {"$pop": {"statistics_list": -1}}

            )








        else:
            self.db[self.collection].insert_one(dict(item))

        return item




