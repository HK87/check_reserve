import scrapy
import configparser
import datetime

from check_reserve.items import RestaurantReserveInfo

class RestaurantSpider(scrapy.Spider):
    name = 'restaurant'
    allowed_domains = ['reserve.tokyodisneyresort.jp']

    config = configparser.ConfigParser()
    config.read('./config.ini')
    USE_DATE = config['CONDITION']['USE_DATE']
    ADULT_NUM = config['CONDITION']['ADULT_NUM']
    CHILD_NUM = config['CONDITION']['CHILD_NUM']
    starturl = 'https://reserve.tokyodisneyresort.jp/showrestaurant/list/' \
               '?useDate=' + USE_DATE + \
               '&adultNum=' + ADULT_NUM + \
               '&childNum=' + CHILD_NUM + \
               '&wheelchairCount=0' \
               '&stretcherCount=0' \
               '&freeword=' \
               '&childAgeInform=' \
               '&reservationStatus=0'
    print(starturl)

    start_urls = (
        starturl,
    )

    def parse(self, response):
        item = RestaurantReserveInfo()
        restaurant_list = [x for x in response.css('h3').xpath('string()').re(r'\S*') if x != ""]

        item['horseshoe_lunch_name'] = restaurant_list[0]
        item['horseshoe_lunch_info'] = [x for x in response.css('.section01').css('.boxShowRestaurant01').css('table')[0].css('td').css('li').xpath('string()').re(r'\S*') if x != ""]

        item['horseshoe_dinner_name'] = restaurant_list[1]
        item['horseshoe_dinner_info'] = [x for x in response.css('.section01').css('.boxShowRestaurant01').css('table')[1].css('td').css('li').xpath('string()').re(r'\S*') if x != ""]

        item['polynesian_lunch_name'] = restaurant_list[2]
        item['polynesian_lunch_info'] = [x for x in response.css('.section01').css('.boxShowRestaurant01').css('table')[2].css('td').css('li').xpath('string()').re(r'\S*') if x != ""]

        item['polynesian_dinner_name'] = restaurant_list[3]
        item['polynesian_dinner_info'] = [x for x in response.css('.section01').css('.boxShowRestaurant01').css('table')[3].css('td').css('li').xpath('string()').re(r'\S*') if x != ""]
        yield item
