import numpy as np
import config
import psycopg2
import normalize_data

def connect_to_postgre(host, port, user, pwd, db_name):
    try:
        print('PostgreSQL connection is establishing...')
        connection = psycopg2.connect(user=user,
                                      password=pwd,
                                      host=host,
                                      port=port,
                                      database=db_name)
        cursor = connection.cursor()

        return connection, cursor
    except Exception as e:
        print("Error while connecting to PostgreSQL: ", e)
        return None, None

def close_postgre_connection(connection, cursor):
    try:
        cursor.close()
        connection.close()
        print("PostgreSQL connection closed")
    except Exception as e:
        print(e)


def load_raw_data_from_db(query=config.POSTGRES_QUERY_TRAIN):
    if query is None:
        raise Exception('Query is not define')
    connection, cursor = connect_to_postgre(config.POSTGRE_HOST,
                                                  config.POSTGRE_PORT,
                                                  config.POSTGRE_USER,
                                                  config.POSTGRE_PWD,
                                                  config.POSTGRE_DB_CREDIT_SCORE)

    cursor.execute(query)
    data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    # data_processed = normalize_data(data)
    close_postgre_connection(connection, cursor)

def load_raw_data_from_file(file_path):
    df = pd.read_csv(file_path)
    data = df.to_dict(orient="records")
    data_processed = normalize_data(data)
    return data_processed

def load_train_test_raw(file_path=None, query=None):
    if file_path is None:
        data = load_raw_data_from_db(query)
    else:
        data = load_raw_data_from_file(file_path)
    return data


if __name__ == '__main__':
    data_train = load_train_test_raw(query=config.POSTGRES_QUERY_TRAIN)

    print(data_train)

