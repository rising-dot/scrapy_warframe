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
        # if self.db[self.collection].count_documents({"item_name": item.get("item_name")}) == 1:

        if self.db[self.collection].count_documents({"item_name": item.get("item_name")}) == 1:

            # check for new_day
            date = datetime.datetime.now()
            time_now = date.strftime("%x")
            new_day = datetime.datetime.strptime(time_now, "%m/%d/%y")
            # check for new_day
            # check for new_day

            if new_day > item.get("date"):
                # new day -- need to clear date to the new list

                sell_buy = ["buy", "sell"]

                statistics_data = {}
                for text in sell_buy:
                    max_value = max(item.get(text).get("max_value"))
                    min_value = min(item.get(text).get("min_value"))
                    avg_value = sum(item.get(text).get("avg_value")) / len(item.get(text).get("avg_value"))
                    accuracy_value = round((sum(item.get(text).get("accuracy_value")) / 240) * 100, 2)

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
                                text + ".max_value": [],
                                text + ".min_value": [],
                                text + ".avg_value": [],
                                text + ".accuracy_value": []


                            }
                        }
                    )

                # reset the array --- delete all in array
                self.db[self.collection].update_one(
                    {"item_name": item.get("item_name")},
                    {"$set":
                        {
                            "date": new_day
                        }
                    }
                )

                # now insert it into the statistics_list
                today_datetime = datetime.date.today()
                self.db[self.collection].update_one(
                    {"item_name": item.get("item_name")},
                    {
                        "$push": {
                            "statistics_list": {
                                "datetime": str(today_datetime),
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
