import scrapy

class RestaurantReserveInfo(scrapy.Item):
    """
    レストランの予約情報を表すItem
    """

    horseshoe_lunch_name = scrapy.Field()
    horseshoe_lunch_info = scrapy.Field()

    horseshoe_dinner_name = scrapy.Field()
    horseshoe_dinner_info = scrapy.Field()

    polynesian_lunch_name = scrapy.Field()
    polynesian_lunch_info = scrapy.Field()

    polynesian_dinner_name = scrapy.Field()
    polynesian_dinner_info = scrapy.Field()
