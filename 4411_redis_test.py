import redis, csv, psycopg2, time

GAME_ID = 22200477

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
conn = psycopg2.connect(
    dbname="nba", 
    user="mylesmacdonald", 
    password="", 
    host="localhost"
)

f = 'games_details_202312161309.csv'

def clear_redis():
    for key in r.scan_iter(f'{GAME_ID}:*'):
        r.delete(key)

def clear_pqsql():
    cur = conn.cursor()
    cur.execute(f'DELETE FROM games_details WHERE game_id = {GAME_ID}')
    conn.commit()

def put_redis():
    with open(f, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            r.hset(f'{row[0]}:{row[4]}', mapping={
                "min": row[9],
                "fgm": row[10],
                "fga": row[11],
                "fg3m": row[13],
                "fg3a": row[14],
                "ftm": row[16],
                "fta": row[17],
                "reb": row[21],
                "ast": row[22],
                "pts": row[27]
            })

def put_psql():
    with open(f, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            query = "INSERT INTO games_details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            with conn.cursor() as cur:
                cur.execute(query, row)
    conn.commit()

def get_redis():
    for key in r.scan_iter(f'{GAME_ID}:*'):
        r.hgetall(key)

def get_psql():
    cur = conn.cursor()
    cur.execute(f'SELECT min, fgm, fga, fg3m, fg3a, ftm, fta, reb, ast, pts FROM games_details WHERE game_id = {GAME_ID}')
    rows = cur.fetchall()

# # # # # # # # # #
# PSQL TESTING
# # # # # # # # # #

for TIMES_TO_RUN in (10, 100, 1000):
    print(f'{TIMES_TO_RUN} queries:')

    psql_sum = 0
    for i in range(TIMES_TO_RUN):
        clear_pqsql()
        start_time_psql = time.time()
        put_psql()
        end_time_psql = time.time()
        duration_ms_psql = (end_time_psql - start_time_psql) * 1000
        psql_sum += duration_ms_psql

    psql_avg = psql_sum / TIMES_TO_RUN
    print(f"Average request duration for inserting into PSQL: {psql_avg:.2f} ms")

    psql_sum = 0
    for i in range(TIMES_TO_RUN):
        start_time_psql = time.time()
        get_psql()
        end_time_psql = time.time()
        duration_ms_psql = (end_time_psql - start_time_psql) * 1000
        psql_sum += duration_ms_psql

    psql_avg = psql_sum / TIMES_TO_RUN
    print(f"Average request duration for retrieving from PSQL: {psql_avg:.2f} ms")


# # # # # # # # # #
# REDIS TESTING
# # # # # # # # # #

for TIMES_TO_RUN in (10, 100, 1000):
    print(f'{TIMES_TO_RUN} queries:')

    redis_sum = 0
    for i in range(TIMES_TO_RUN):
        clear_redis()
        start_time_redis = time.time()
        put_redis()
        end_time_redis = time.time()
        duration_ms_redis = (end_time_redis - start_time_redis) * 1000
        redis_sum += duration_ms_redis

    redis_avg = redis_sum / TIMES_TO_RUN
    print(f"Request duration for inserting into Redis: {redis_avg:.2f} ms")

    redis_sum = 0
    for i in range(TIMES_TO_RUN):
        start_time_redis = time.time()
        get_redis()
        end_time_redis = time.time()
        duration_ms_redis = (end_time_redis - start_time_redis) * 1000
        redis_sum += duration_ms_redis

    redis_avg = redis_sum / TIMES_TO_RUN
    print(f"Request duration for retrieving from Redis: {redis_avg:.2f} ms")