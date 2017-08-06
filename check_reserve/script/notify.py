import requests
import configparser
import MySQLdb

def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    conn = MySQLdb.connect(
        host = config['MYSQL']['HOST'],
        db = config['MYSQL']['DATABASE'],
        user = config['MYSQL']['USER'],
        passwd = config['MYSQL']['PASSWORD'],
        charset = config['MYSQL']['CHARSET']
    )

    restaurant_name = config['TARGET']['NAME']
    restaurant_rank = config['TARGET']['RANK']
    restaurant_time = config['TARGET']['TIME']

    c = conn.cursor()
    c.execute('SELECT * FROM reservations WHERE name = %s AND rank = %s AND time = %s AND is_empty = 1 ORDER BY regist_date desc LIMIT 1'
            , (restaurant_name, restaurant_rank, restaurant_time))
    result = c.fetchall()

    if len(result) > 0:
        url = "https://notify-api.line.me/api/notify"
        token = "line token"
        headers = {"Authorization" : "Bearer "+ token}
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

        message =  "予約が可能になりました！\n" \
                 + "レストラン名：%s\n" % restaurant_name\
                 + "時間：%s\n" % restaurant_time\
                 + "席のランク：%s\n" % restaurant_rank\
                 + starturl
        print(message)
        payload = {"message" :  message}
        r = requests.post(url ,headers = headers ,params=payload)

if __name__ == '__main__':
    main()
