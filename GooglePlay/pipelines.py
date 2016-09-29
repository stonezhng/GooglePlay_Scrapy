
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log

SETTINGS = get_project_settings()

class GoogleplayPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        #Instantiate DB
        self.dbpool = adbapi.ConnectionPool ('MySQLdb',
            host=SETTINGS['MYSQL_HOST'],
            user=SETTINGS['MYSQL_USER'],
            passwd=SETTINGS['MYSQL_PASSWD'],
            port=SETTINGS['MYSQL_PORT'],
            db=SETTINGS['MYSQL_DBNAME'],
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        print item
        # print '########################insert'
        # print item['stockid']
        result = tx.execute(
            """
                insert into apps(`app_name`, `app_category`, `developer`, `reviewer_name`, `reviewer_link`, `title`,
                `date`, `content`, `rank`)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (item['app_name'], item['app_category'], item['developer'], item['name'], item['link'],
                  item['title'], item['date'], item['content'], item['rank'])
        )
        # result = tx.execute(
        #     'update `stock_2016` set `volume` = %s, `amount` = %s where `stockid` = %s',
        #     (item['volume'], item['amount'], item['stockid'])
        # )
        if result > 0:
            self.stats.inc_value('database/items_added')

    def _handle_error(self, e):
        log.err(e)