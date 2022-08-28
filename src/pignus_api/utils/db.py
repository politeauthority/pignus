import pymysql.cursors


from pignus_api.utils import log

PIGNUS_DB_HOST="192.168.50.6"
PIGNUS_DB_PORT=int("3307")
PIGNUS_DB_NAME="pignus_1"
PIGNUS_DB_USER="root"
PIGNUS_DB_PASS="b48QJofXstMQ6qztKfuR"


def connect():
    # Connect to the database
    connection = pymysql.connect(
        host=PIGNUS_DB_HOST,
        port=PIGNUS_DB_PORT,
        user=PIGNUS_DB_USER,
        password=PIGNUS_DB_PASS,
        database=PIGNUS_DB_NAME)

    # with connection:
    #     # with connection.cursor() as cursor:
    #     #     # Create a new record
    #     #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    #     # # connection is not autocommit by default. So you must commit to save
    #     # # your changes.
    #     # connection.commit()


    log.info("Generating database connection")
    return {
        "conn": connection,
        "cursor": connection.cursor()
    }
