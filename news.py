import psycopg2

# Title for each query
firstQueryTitle = "What are the most popular three articles of all time ?"
secondQueryTitle = "Who are the most popular article authors of all time? "
thirdQueryTitle = "On which days did more than 1% of requests lead to errors? "

# @returns query for first title


def firstQuery():
    query = """SELECT title, count(*) as total FROM log ,articles where
    slug = regexp_replace(log.path, '^.*/', '') group by title  order by
    total desc limit 3;"""
    return query

# @returns query for second title


def secondQuery():
    query = """SELECT name, count(*) as total FROM log ,articles, authors
    where authors.id=articles.author and slug =
    regexp_replace(log.path, '^.*/', '')
    group by name  order by total desc;"""
    return query

# @returns query for third title


def thirdQuery():
    query = """SELECT day, finalQuery.perc FROM(SELECT day, round(
    (sum(requests)/(SELECT count(*)
    FROM log where date(time) = day) * 100),2)   as perc FROM
    (SELECT date(time) as day,count(*)
    as requests FROM log where status like '%404%' group by day)
    as finalPercentage group by day )
    as finalQuery where finalQuery.perc > '1';"""
    return query

# Executes the query
# @returns the query result


def getQueryResult(dbName, query):
    dbconn = psycopg2.connect('dbname=' + dbName)
    cursor = dbconn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    dbconn.close()
    return result

# Prints the query result


def printQueryResults(queryResult, title):
    print("* " + title)
    for result in queryResult:
        print("\t -> " + str(result[0]) + " --- " + str(result[1]))


if __name__ == '__main__':
    # get first query
    queryResult = getQueryResult("news", firstQuery())
    # print first query
    printQueryResults(queryResult, firstQueryTitle)
    # get second query
    queryResult = getQueryResult("news", secondQuery())
    # print second query
    printQueryResults(queryResult, secondQueryTitle)
    # get third query
    queryResult = getQueryResult("news", thirdQuery())
    # print third query
    printQueryResults(queryResult, thirdQueryTitle)
