import psycopg2
from telega_bot.config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            # conn.close()
            # print('Database connection closed.')
            return conn


class PostgreSQLHandler:
    def __init__(self):
        self.conn = PostgreSQLHandler.connect()
        self.cur = self.conn.cursor()

    def execute(self):
        pass

    def commit(self):
        self.conn.commit()

    def cur_close(self):
        self.cur.close()

    def conn_close(self):
        self.conn.close()

    @staticmethod
    def connect():
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                # conn.close()
                # print('Database connection closed.')
                return conn


def save_user(update):
    db = PostgreSQLHandler()
    db.cur.execute("SELECT user_id FROM users WHERE user_id = %s", (update.effective_user['id'],))
    if db.cur.fetchone() is None:  # register new user
        sql = """ INSERT INTO users (
        user_id,
        user_name,
        first_name,
        last_name,
        language_code,
        is_bot,
        is_saved
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s);
        """
        db.cur.execute(sql, (update.effective_user['id'],
                             update.effective_user['username'],
                             update.effective_user['first_name'],
                             update.effective_user['last_name'],
                             update.effective_user['language_code'],
                             update.effective_user['is_bot'],
                             True,))
    else:  # old user start to save data
        db.cur.execute("UPDATE users SET is_saved = %s WHERE user_id = %s",
                       (True, update.effective_user['id'],))

        db.commit()
        db.cur_close()

        db.conn_close()


def reset_user_is_set(user_id):
    db = PostgreSQLHandler()
    db.cur.execute("UPDATE users SET is_saved = %s WHERE user_id = %s",
                   (False, user_id,))

    db.cur.close()
    db.conn.commit()


def get_saved_user_id(user_id):
    db = PostgreSQLHandler()
    db.cur.execute("SELECT user_id FROM users WHERE user_id = %s AND is_saved = %s", (user_id, True,))
    ret = db.cur.fetchone()
    db.cur_close()
    db.conn_close()
    return ret


def get_last_region(user_id):
    db = PostgreSQLHandler()
    db.cur.execute(
        "SELECT last_region, last_region_code FROM users WHERE user_id = %s AND is_saved = %s",
        (user_id, True,))
    ret = db.cur.fetchall()
    db.cur_close()
    db.conn_close()
    return ret


def get_last_city(user_id):
    db = PostgreSQLHandler()
    db.cur.execute("SELECT last_city, last_city_code FROM users WHERE user_id = %s", (user_id,))
    ret = db.cur.fetchall()[0]
    db.cur_close()
    db.conn_close()
    return ret


def update_last_region(last_region, last_region_code, user_id):
    db = PostgreSQLHandler()
    db.cur.execute("UPDATE users SET last_region = %s, last_region_code = %s WHERE user_id = %s",
                   (last_region, last_region_code, user_id,))

    db.cur.close()
    db.conn.commit()


def update_last_country(last_country, last_country_code, user_id):
    db = PostgreSQLHandler()
    db.cur.execute("UPDATE users SET last_country = %s, last_country_code = %s WHERE user_id = %s",
                   (last_country, last_country_code, user_id,))

    db.cur.close()
    db.conn.commit()


def update_last_city(last_city, last_city_code, user_id):
    db = PostgreSQLHandler()
    db.cur.execute("UPDATE users SET last_city = %s, last_city_code = %s WHERE user_id = %s",
                   (last_city, last_city_code, user_id,))

    db.cur.close()
    db.conn.commit()


if __name__ == '__main__':
    pass