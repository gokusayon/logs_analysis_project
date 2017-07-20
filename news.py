#!/usr/bin/env python
import psycopg2

# Title for each query
firstQueryTitle = "What are the most popular three articles of all time ?"
secondQueryTitle = "Who are the most popular article authors of all time? "
thirdQueryTitle = "On which days did more than 1% of requests lead to errors? "

# @returns query for first title


def firstQuery():
    query = """SELECT title, total FROM  (select path, count(*) as total from log
    group by path) as log ,articles where slug =
    regexp_replace(log.path, '^.*/', '') order by
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
    # Original Query.

    # query = """SELECT day, finalQuery.perc FROM(SELECT day, round(
    # (sum(requests)/(SELECT count(*)
    # FROM log where date(time) = day) * 100),2)   as perc FROM
    # (SELECT date(time) as day,count(*)
    # as requests FROM log where status like '%404%' group by day)
    # as finalPercentage group by day )
    # as finalQuery where finalQuery.perc > '1';"""

    # Updated Query after review 1
    query = """SELECT day, round(perc,3) FROM(SELECT date(time) as day,
    100.0 * sum(case when status != '200 OK' then 1 else 0 end)
    / count(*) as perc FROM log group by date(time)) as daily_errors
    where perc > 1;"""

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


def printQueryResults(queryResult, title, isView):
    print("* " + title)
    for result in queryResult:
        if isView == 'true':
            print("\t -> " + str(result[0]) +
                  " --- " + str(result[1]) + " views")
        else:
            print("\t -> " + str(result[0]) + " --- " + str(result[1]) + "%")


if __name__ == '__main__':
    # get first query
    queryResult = getQueryResult("news", firstQuery())
    # print first query
    printQueryResults(queryResult, firstQueryTitle, 'true')
    # get second query
    queryResult = getQueryResult("news", secondQuery())
    # print second query
    printQueryResults(queryResult, secondQueryTitle, 'true')
    # get third query
    queryResult = getQueryResult("news", thirdQuery())
    # print third query
    printQueryResults(queryResult, thirdQueryTitle, 'false')
