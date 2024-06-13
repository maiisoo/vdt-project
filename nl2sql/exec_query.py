from pyhive import hive


def execute_query(query):
    try:
        hive_conn = hive.Connection(host='localhost', port=10000, username='root')
        cursor = hive_conn.cursor()

        cursor.execute("USE vdt")
        print(query.rstrip(';'))
        cursor.execute(query.rstrip(';'))


        # Fetch column names
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

        # Convert result to list of dictionaries
        result_dicts = []
        for row in result:
            result_dicts.append(dict(zip(columns, row)))

        hive_conn.close()
        return result_dicts
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

