import MySQLdb
import re

class MySQLPipeline(object):
    """
    ItemをMySQLに保存するPipeline。
    """

    def open_spider(self, spider):
        """
        Spider開始時にMySQLサーバーに接続
        """

        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'scraping'),
            'user': settings.get('MYSQL_USER', ''),
            'passwd': settings.get('MYSQL_PASSWORD', ''),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor()

    def close_spider(self, spider):
        """
        Spider終了時にMySQLサーバーへの接続を切断
        """

        self.conn.close()

    def process_item(self, item, spider):
        """
        Itemをitemsテーブルに挿入する。
        """

        reserve_info = []
        reserve_info.extend(self.parse_data(item['horseshoe_lunch_name'], item['horseshoe_lunch_info']))
        reserve_info.extend(self.parse_data(item['horseshoe_dinner_name'], item['horseshoe_dinner_info']))
        reserve_info.extend(self.parse_data(item['polynesian_lunch_name'], item['polynesian_lunch_info']))
        reserve_info.extend(self.parse_data(item['polynesian_dinner_name'], item['polynesian_dinner_info']))

        for reserve in reserve_info:
            self.c.execute('INSERT INTO RESERVATIONS (name, rank, time, is_empty, regist_date, update_date) VALUES (%s, %s, %s, %s, NOW(), NOW())', (reserve.name, reserve.rank, reserve.time, reserve.status))
        self.conn.commit()  # 変更をコミット。
        return item

    def parse_data(self, name, item):
        """
        スクレイプしたjsonデータからレストランの情報を整形する関数
        @param name string レストラン名
        @param item list スクレイピングしたデータ(時間と座席情報)
        @return Restaurantクラスのlist
        """

        reserve_info = []
        for i,data in enumerate(item):
            rank, time, status = "", "", "1"
            if re.match(r'[0-9]{2}:[0-9]{2}', data):
                time = data
                if i != len(item)-1 and item[i+1] == "満席":
                    status = "0"
                restaurant = Restaurant(name, rank, time, status)
                reserve_info.append(restaurant)

        performance_repeat = len([x for x in item if re.match(r'[0-9]{2}:[0-9]{2}', x) ]) / 3
        for i,restaurant in enumerate(reserve_info):
            if i // performance_repeat == 0:
                reserve_info[i].setRank("S")
            elif i // performance_repeat == 1:
                reserve_info[i].setRank("A")
            elif i // performance_repeat == 2:
                reserve_info[i].setRank("B")
            else:
                pass
        return reserve_info

class Restaurant:
    def __init__(self, name, rank, time, status):
        self.name = name
        self.rank = rank
        self.time = time
        self.status = status

    def setRank(self, rank):
        self.rank = rank
