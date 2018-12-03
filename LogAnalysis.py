import psycopg2
DBNAME = "news"

def getarticlesname(name) :
    strall = name.replace("-"," ").split()
    result = ""
    for s in strall :
        result += s.capitalize() + " "
    l = len(result) - 1    
    return result[0:l]    

def connect() :  
    # connect to db
    db = psycopg2.connect(database = DBNAME)
 
    # create a cursor
    cur = db.cursor()
        
    # execute a Q1
    cur.execute("select articles.slug as article_name ,count(log.path) as views from log left join articles on log.path like concat('%',articles.slug) where status like '%200%' and log.path like '/article/%' group by log.path,articles.slug order by views desc limit 3 ;")
 
    # display Q1
    rows = cur.fetchall()
    print("What are the most popular three articles of all time?")
    for row in rows :
        str_result = "\"{}\" -- {} views".format(getarticlesname(row[0]),row[1])
        print(str_result )

    # execute a Q2
    cur.execute("select count(log.path) as views ,articles.author,authors.name from log left join articles on log.path like concat('%',articles.slug) left join authors on articles.author = authors.id where status like '%200%' and log.path like '/article/%' group by articles.author,authors.name order by views desc ;")

    # display Q2
    rows = cur.fetchall()
    print("\nWho are the most popular article authors of all time?")
    for row in rows :
        str_result = "{} -- {} views".format(row[2],row[0])
        print(str_result)

    # execute a Q3
    cur.execute("select * from (select main.d,main.errortrans,main.alltrans ,(cast(errortrans as float) / cast(main.alltrans as float) * 100.0) as percents from (select cast(time as date) as d,count(status) as alltrans,e.errortrans from log left join (select cast(time as date) as edate,count(status) as errortrans from log where status like '4%' group by cast(time as date)) as e on cast(time as date) = e.edate group by cast(time as date),e.errortrans ) as main) as result where result.percents > 1.0;")

    # display Q3
    rows = cur.fetchall()
    print("\nOn which days did more than 1% of requests lead to errors?")
    for row in rows :
        str_result = "{} -- {:.2f}% errors".format(row[0].strftime("%b %d, %Y"),row[3])
        print(str_result)

    cur.close()


if __name__ == "__main__":
    connect()

 
        
