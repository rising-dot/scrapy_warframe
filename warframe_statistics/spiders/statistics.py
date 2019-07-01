# -*- coding: utf-8 -*-
import scrapy
import json

from datetime import datetime



class StatisticsSpider(scrapy.Spider):
    name = 'statistics'

    def start_requests(self):
        url = 'https://warframe.market/tools/ducats'
        yield scrapy.Request(url=url, callback=self.parse)

    #    get the url name of all prime set item
    def parse(self, response):
        script = response.xpath('//script[@id="application-state"]/text()').extract_first()
        json_response = json.loads(script)
        get_url_names = json_response.get('items')




        # get all the url of items
        urls = []

# ##############################################################################################################
#         # for link in get_url_names:
#         for link in get_url_names:
#             if "Prime Chassis" in link.get("item_name") or \
#                     "Prime Blueprint" in link.get("item_name") or \
#                     "Prime Systems" in link.get("item_name") or \
#                     "Prime Neuroptics" in link.get("item_name") or \
#                     "Prime Grip" in link.get("item_name") or \
#                     "Prime Lower Limb" in link.get("item_name") or \
#                     "Prime String" in link.get("item_name") or \
#                     "Prime Upper Limb" in link.get("item_name") or \
#                     "Prime Barrel" in link.get("item_name") or \
#                     "Prime Receiver" in link.get("item_name") or \
#                     "Prime Stock" in link.get("item_name") or \
#                     "Prime Ornament" in link.get("item_name") or \
#                     "Prime Handle" in link.get("item_name") or \
#                     "Prime Blade" in link.get("item_name") or \
#                     "Prime Head" in link.get("item_name") or \
#                     "Prime Link" in link.get("item_name") or \
#                     "Prime Pouch" in link.get("item_name") or \
#                     "Prime Stars" in link.get("item_name") or \
#                     "Prime Hilt" in link.get("item_name") or \
#                     "Prime Wings" in link.get("item_name") or \
#                     "Prime Cerebrum" in link.get("item_name") or \
#                     "Prime Carapace" in link.get("item_name") or \
#                     "Prime Harness" in link.get("item_name") or \
#                     "Kubrow Imprint" in link.get("item_name") or \
#                     "Prime Set" in link.get("item_name"):
#                 urls.append('https://warframe.market/items/' + link.get('url_name'))
#
#
#         #special prime item to add
#         urls.append('https://warframe.market/items/wolf_sledge_handle')
#         urls.append('https://warframe.market/items/wolf_sledge_blueprint')
#         urls.append('https://warframe.market/items/wolf_sledge_head')
#         urls.append('https://warframe.market/items/wolf_sledge_motor')
#
# ##############################################################################################################


        urls.append('https://warframe.market/items/vitality')




        # loop flow all the url one by one
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_scrapy_set_item)

    def parse_scrapy_set_item(self, response):
        script = response.xpath('//script[@id="application-state"]/text()').extract_first()
        json_response = json.loads(script)

        get_the_id = json_response.get("include").get("item").get("id")
        match_the_ids = json_response.get("include").get("item").get("items_in_set")

        # ************************************************************************
        item_name = ""
        item_img = ""
        item_set_name = ""
        for match_the_id in match_the_ids:
            if "Set" in match_the_id.get("en").get("item_name"):
                item_set_name = match_the_id.get("en").get("item_name")

            if get_the_id == match_the_id.get("id"):
                item_name = match_the_id.get("en").get("item_name")  # getting the name of one of the 5 prime parts

                if match_the_id.get("sub_icon") is None:
                    item_img = "https://warframe.market/static/assets/" + match_the_id.get("thumb")
                else:
                    item_img = "https://warframe.market/static/assets/" + match_the_id.get("sub_icon")
        # ************************************************************************

        parts_data = json_response.get("payload").get("orders")
        sell = []
        for users_sell in parts_data:
            if "sell" in users_sell.get("order_type") and "ingame" in users_sell.get("user").get("status"):
                sell.append(users_sell.get("platinum"))

        if sell:
            # List is NOT empty

            # sorting the array and take only ten of it
            sell.sort()
            take_ten_of_sell = sell[0:10]

            max_sell_value = max(sell[0:10])
            min_sell_value = min(sell[0:10])
            avg_sell_value = round(sum(take_ten_of_sell) / len(take_ten_of_sell), 2)
            length_of_sell = len(take_ten_of_sell)
        else:
            # List is empty
            max_sell_value = 0
            min_sell_value = 0
            avg_sell_value = 0
            length_of_sell = 0


#######################################################################################################################


        # Buy
        buy = []
        for users_sell in parts_data:
            if "buy" in users_sell.get("order_type") and "ingame" in users_sell.get("user").get("status"):
                buy.append(users_sell.get("platinum"))



        if buy:
            # List is NOT empty

            # sorting the array and take only ten of it
            buy.sort()
            take_ten_of_buy = buy[0:10]

            max_buy_value = max(buy[0:10])
            min_buy_value = min(buy[0:10])
            avg_buy_value = round(sum(take_ten_of_buy) / len(take_ten_of_buy), 2)
            length_of_buy = len(take_ten_of_buy)

        else:
            # List is empty
            max_buy_value = 0
            min_buy_value = 0
            avg_buy_value = 0
            length_of_buy = 0



#######################################################################################################################
        #save the date as INT
        date = datetime.now()
        date_to_int = int(date.strftime('%Y%m%d'))

        yield {
            "item_name": item_name,
            "item_set_name": item_set_name,
            "item_img": item_img,
            "date": date_to_int,
            "buy": {
                "max_value": [max_buy_value],
                "min_value": [min_buy_value],
                "avg_value": [avg_buy_value],
                "accuracy_value": [length_of_buy]
            },
            "sell": {
                "max_value": [max_sell_value],
                "min_value": [min_sell_value],
                "avg_value": [avg_sell_value],
                "accuracy_value": [length_of_sell]
            },
            "statistics_list": []

        }
#######################################################################################################################
