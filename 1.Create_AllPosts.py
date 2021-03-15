import glob
import pymysql
import random

conn = pymysql.connect(host='localhost', user='root', password='123456',
                       db='test_data', charset='utf8')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `AllPosts` (
	`post_id` INT(11) NULL DEFAULT NULL,
	`user_id` INT(11) NULL DEFAULT NULL,
	`text` TEXT NULL DEFAULT NULL
)""")
cursor.execute("TRUNCATE TABLE AllPosts")
conn.commit()

idx = 0
for filename in glob.iglob('posts/*', recursive=True):

    idx += 1

    f = open(filename, "rt")
    text = f.read()
    f.close()

    q = "INSERT INTO AllPosts(post_id, user_id, text) VALUES ({0}, {1}, \"{2}\")".format(
        idx, random.randrange(1, 100), conn.escape_string(text))
    cursor.execute(q)
    conn.commit()

conn.close()
