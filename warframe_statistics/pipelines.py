# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from datetime import datetime


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

            # get date from database
            datebase_date = ""
            for get_date in self.db[self.collection].find({"item_name": item.get("item_name")}):
                datebase_date = get_date.get("date")

            # today date
            date = datetime.now()
            present_to_int = int(date.strftime('%Y%m%d'))

            # if this is a new day then do this
            if 20200708 > datebase_date:     #    present_to_int
                # new day -- need to clear date to the new list

                # copy all the data to yesterday first
                for get_yes in self.db[self.collection].find({"item_name": item.get("item_name")}):

                    self.db[self.collection].update_one(
                        {"item_name": item.get("item_name")},
                        {"$set":
                            {

                                "buy_yesterday.max_value": get_yes.get("buy").get("max_value"),
                                "buy_yesterday.min_value": get_yes.get("buy").get("min_value"),
                                "buy_yesterday.avg_value": get_yes.get("buy").get("avg_value"),
                                "buy_yesterday.accuracy_value": get_yes.get("buy").get("accuracy_value"),
                                "sell_yesterday.max_value": get_yes.get("sell").get("max_value"),
                                "sell_yesterday.min_value": get_yes.get("sell").get("min_value"),
                                "sell_yesterday.avg_value": get_yes.get("sell").get("avg_value"),
                                "sell_yesterday.accuracy_value": get_yes.get("sell").get("accuracy_value")

                            }
                        }
                    )





######################################################################################################################################



                    # get the higest and lowest of yesterday

                    sell_buy = ["buy", "sell"]
                    statistics_data = {}
                    for text in sell_buy:

                        max_value = max(get_yes.get(text).get("max_value"))
                        min_value = min(get_yes.get(text).get("min_value"))
                        avg_value = sum(get_yes.get(text).get("avg_value")) / len(item.get(text).get("avg_value")) #calculate the average of average

                        accuracy_value = str(round(((sum(get_yes.get(text).get("accuracy_value")) / 480) * 100), 2)) + "%"



                    # create the new vaule for the day
                    statistics_data[text] = {
                        "max_value": max_value,
                        "min_value": min_value,
                        "avg_value": avg_value,
                        "accuracy_value": accuracy_value
                    }



                    # reset the array --- delete all in array
                    self.db[self.collection].update_one(
                        {"item_name": item.get("item_name")},
                        {"$set":
                            {
                                "date": present_to_int,
                                text + ".max_value": [],
                                text + ".min_value": [],
                                text + ".avg_value": [],
                                text + ".accuracy_value": []
                            }
                        }
                    )



                # now insert it into the statistics_list
                self.db[self.collection].update_one(
                    {"item_name": item.get("item_name")},
                    {
                        "$push": {
                            "statistics_list": {
                                "datetime": str(date.date()),
                                "data": statistics_data
                            }
                        }
                    }
                )

                # how many days do we want ?
                self.db[self.collection].update_one(
                    {"statistics_list.120": {"$exists": 1}},
                    {"$pop": {"statistics_list": -1}}
                )


                # same day -- just insert data
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


            else:
                # same day -- just insert data
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

        else:
            self.db[self.collection].insert_one(dict(item))

        return item
