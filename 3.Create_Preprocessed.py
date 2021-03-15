import spacy
import pymysql

nlp = spacy.load("en_core_web_sm")

conn = pymysql.connect(host='localhost', user='root', password='123456',
                       db='test_data', charset='utf8')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `Preprocessed` (
	`post_id` INT(11) NULL DEFAULT NULL,
	`user_id` INT(11) NULL DEFAULT NULL,
	`word` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`frequency` INT(11) NULL DEFAULT NULL
)""")
cursor.execute("TRUNCATE TABLE Preprocessed")
conn.commit()

cursor.execute("SELECT * FROM AllPosts")
results = cursor.fetchall()
for i in results:
    post_id = i[0]
    user_id = i[1]
    text = i[2]
    doc = nlp(text)

    word_count_dict = dict()

    for word in doc:
        if word.pos_ in ["NOUN"]:
            w = word.text.lower()
            if w in word_count_dict:
                word_count_dict[w] += 1
            else:
                word_count_dict[w] = 1

    for i, j in word_count_dict.items():
        try:
            q = "INSERT INTO Preprocessed(post_id, user_id, word, frequency) VALUES ({0}, {1}, \"{2}\", {3})".format(
                post_id, user_id, i, j)
            cursor.execute(q)
            conn.commit()
        except:
            continue

conn.close()
