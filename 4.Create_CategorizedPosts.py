import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456',
                       db='test_data', charset='utf8')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `CategorizedPosts` (
	`post_id` INT(11) NULL DEFAULT NULL,
	`user_id` INT(11) NULL DEFAULT NULL,
	`category` INT(11) NULL DEFAULT NULL,
	`total_score` FLOAT NULL DEFAULT NULL
)""")
cursor.execute("TRUNCATE TABLE CategorizedPosts")
conn.commit()

cursor.execute("SELECT * FROM AllPosts")
results = cursor.fetchall()
for i in results:
    post_id = i[0]
    user_id = i[1]

    try:
        q = """INSERT INTO CategorizedPosts
    SELECT post_id, user_id, category, sum(score) AS total_score
        FROM Preprocessed JOIN ClusteringModel
        WHERE Preprocessed.post_id = {0}
            AND Preprocessed.user_id = {1}
            AND Preprocessed.word = ClusteringModel.word
        GROUP BY category""".format(post_id, user_id)

        cursor.execute(q)
        conn.commit()
    except:
        continue

conn.close()
