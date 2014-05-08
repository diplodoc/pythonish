# coding: utf-8
import logging
import sqlite3

from grab.spider import Spider, Task

class ExampleSpider(Spider):
    initial_urls = ['http://habrahabr.ru/']

    def prepare(self):
        self.result_counter = 0
        self.new_posts = []


    def task_initial(self, grab, task):
        print 'Habrahabr home page'

        for elem in grab.doc.select('//h1[@class="title"]/a[@class="post_title"]'):
            yield Task('habrapost', url=elem.attr('href'))

        next_pages = grab.doc.select('//ul[@id="nav-pages"]/li/a')
        for page in next_pages:
            yield Task('page', url=self.initial_urls[0] + page.attr('href'))

    def task_page(self, grab, task):
        print task.url
        for elem in grab.doc.select('//h1[@class="title"]/a[@class="post_title"]'):
            yield Task('habrapost', url=elem.attr('href'))

    def task_habrapost(self, grab, task):
        post = (grab.doc.select('//h1/span[@class="post_title"]').text(), task.url)
        self.new_posts.append(post)
        self.result_counter += 1


def db_insert(post_list):
    db = sqlite3.connect('habraposts.db')
    cursor = db.cursor()
    for post in post_list:
        exists = cursor.execute('SELECT * FROM habraposts WHERE url=?', (post[1],)).fetchall()
        if len(exists) <=0 :
            cursor.execute('INSERT INTO habraposts(name, url) VALUES(?,?)', post)
    db.commit()


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    bot = ExampleSpider(thread_number=2)
    bot.run()
    # db_insert(bot.new_posts)
    for post in bot.new_posts :
        print post[0], post[1]