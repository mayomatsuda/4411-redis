import redis, csv, psycopg2, time

GAME_ID = 22200477  # Identifier for a specific game

# Setting up Redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Setting up PostgreSQL connection
conn = psycopg2.connect(
    dbname="nba", 
    user="mylesmacdonald", 
    password="", 
    host="localhost"
)

f = 'games_details_202312161309.csv'  # CSV file containing game details

def clear_redis():
    """
    Clear Redis database for the specific game ID.
    Removes all Redis entries related to the game ID.
    """
    for key in r.scan_iter(f'{GAME_ID}:*'):
        r.delete(key)

def clear_pqsql():
    """
    Clear PostgreSQL database for the specific game ID.
    Deletes all PostgreSQL entries related to the game ID.
    """
    cur = conn.cursor()
    cur.execute(f'DELETE FROM games_details WHERE game_id = {GAME_ID}')
    conn.commit()

def put_redis():
    """
    Populate Redis with data from the CSV file.
    Each row in the CSV is stored as a hash in Redis with the key format 'game_id:player_id'.
    """
    with open(f, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
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
    """
    Populate PostgreSQL with data from the CSV file.
    Each row in the CSV is inserted as a new record in the PostgreSQL database.
    """
    with open(f, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            query = "INSERT INTO games_details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            with conn.cursor() as cur:
                cur.execute(query, row)
    conn.commit()

def get_redis():
    """
    Retrieve data from Redis for the specific game ID.
    Fetches all Redis entries related to the game ID.
    """
    for key in r.scan_iter(f'{GAME_ID}:*'):
        r.hgetall(key)

def get_psql():
    """
    Retrieve data from PostgreSQL for the specific game ID.
    Fetches selected columns from the PostgreSQL database related to the game ID.
    """
    cur = conn.cursor()
    cur.execute(f'SELECT min, fgm, fga, fg3m, fg3a, ftm, fta, reb, ast, pts FROM games_details WHERE game_id = {GAME_ID}')
    rows = cur.fetchall()

# PSQL TESTING
# Testing the performance of PostgreSQL database operations
for TIMES_TO_RUN in (10, 100, 1000):
    print(f'{TIMES_TO_RUN} queries:')

    # Testing PostgreSQL insert performance
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

    # Testing PostgreSQL retrieval performance
    psql_sum = 0
    for i in range(TIMES_TO_RUN):
        start_time_psql = time.time()
        get_psql()
        end_time_psql = time.time()
        duration_ms_psql = (end_time_psql - start_time_psql) * 1000
        psql_sum += duration_ms_psql
    psql_avg = psql_sum / TIMES_TO_RUN
    print(f"Average request duration for retrieving from PSQL: {psql_avg:.2f} ms")


# REDIS TESTING
# Testing the performance of Redis database operations
for TIMES_TO_RUN in (10, 100, 1000):
    print(f'{TIMES_TO_RUN} queries:')

    # Testing Redis insert performance
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

    # Testing Redis retrieval performance
    redis_sum = 0
    for i in range(TIMES_TO_RUN):
        start_time_redis = time.time()
        get_redis()
        end_time_redis = time.time()
        duration_ms_redis = (end_time_redis - start_time_redis) * 1000
        redis_sum += duration_ms_redis
    redis_avg = redis_sum / TIMES_TO_RUN
    print(f"Request duration for retrieving from Redis: {redis_avg:.2f} ms")
    