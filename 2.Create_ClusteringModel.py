import spacy
import pymysql
import random

nlp = spacy.load("en_core_web_sm")

conn = pymysql.connect(host='localhost', user='root', password='123456',
                       db='test_data', charset='utf8')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `ClusteringModel` (
	`word` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`category` INT(11) NULL DEFAULT NULL,
	`score` FLOAT NULL DEFAULT NULL,
	PRIMARY KEY (`word`, `row_end`) USING BTREE
)""")
cursor.execute("TRUNCATE TABLE ClusteringModel")
conn.commit()

cursor.execute("SELECT * FROM AllPosts")
results = cursor.fetchall()
for i in results:
    text = i[2]
    doc = nlp(text)

    for word in doc:
        if word.pos_ in ["NOUN"]:
            try:
                q = "INSERT INTO ClusteringModel(word, category, score) VALUES (\"{0}\", {1}, {2})".format(
                    word.text.lower(), random.randrange(1, 10), random.uniform(0, 1.0))
                cursor.execute(q)
                conn.commit()
            except:
                continue

conn.close()
