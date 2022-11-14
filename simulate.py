import csv, sqlite3
import numpy as np
import matplotlib.pyplot as plt


# define sql database and cursor
con = sqlite3.connect(":memory:")
cur = con.cursor()

# create tmep tables
cur.execute("CREATE TABLE rankings (position int, team text, ranking real);")
cur.execute("CREATE TABLE groups (team text, grp text);")
# insert rankings data
with open('fifa_world_ranking_men_2022.csv','r') as fin:
    dr = csv.DictReader(fin, delimiter=';')
    to_db = [(i['position'], i['team'], i['ranking']) for i in dr]
cur.executemany("INSERT INTO rankings (position, team, ranking) VALUES (?, ?, ?);", to_db)
# insert group data
with open('fifa_world_cup_groups_2022.csv','r') as fin:
    dr = csv.DictReader(fin, delimiter=';')
    to_db = [(i['team'], i['group']) for i in dr]
cur.executemany("INSERT INTO groups (team, grp) VALUES (?, ?);", to_db)

# combine tables for world cup 22 teams
cur.execute('CREATE TABLE teams22 AS SELECT t1.team, t1.grp, t2.position, t2.ranking FROM groups t1 LEFT JOIN rankings t2 ON t1.team=t2.team')
con.commit()

# get counts of team ranks in world cup 2022
cur.execute('SELECT ranking, count(*) FROM rankings WHERE team IN (SELECT team FROM teams22) GROUP BY ROUND(ranking/100)') 
data = np.array(cur.fetchall()).astype('int')
ranks1 = data[:, 0]
counts1 = data[:, 1]

# get counts of team ranks not in world cup 2022
cur.execute('SELECT ranking, count(*) FROM rankings WHERE team NOT IN (SELECT team FROM teams22) GROUP BY ROUND(ranking/100)') 
data = np.array(cur.fetchall()).astype('int')
ranks2 = data[:, 0]
counts2 = data[:, 1]

#plt.bar(ranks1, counts1, width=50,label='In world cup')
plt.bar(ranks2, counts2, width=50, bottom=counts2, label='Not in world cup')
plt.show()

con.close()