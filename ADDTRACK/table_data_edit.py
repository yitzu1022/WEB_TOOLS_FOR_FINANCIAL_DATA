import psycopg2
import pandas as pd

# # Database connection details (settings.py照搬)
# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', 
#         'NAME': 'newdb_0117',
#         'USER': 'postgres', 
#         'PASSWORD': 'aqaaqq125', 
#         'HOST': 'localhost',  
#         'PORT': '5432', 
#     }
# }


# # Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     dbname=DATABASES['default']['NAME'],
#     user=DATABASES['default']['USER'],
#     password=DATABASES['default']['PASSWORD'],
#     host=DATABASES['default']['HOST'],
#     port=DATABASES['default']['PORT']
# )
# # Create a cursor to interact with the database
# cursor = conn.cursor()



def create_table():
    # Database connection details (settings.py照搬)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'newdb_0117',
            'USER': 'postgres', 
            'PASSWORD': 'aqaaqq125', 
            'HOST': 'localhost',  
            'PORT': '5432', 
        }
    }


    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASES['default']['NAME'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        host=DATABASES['default']['HOST'],
        port=DATABASES['default']['PORT']
    )
    # Create a cursor to interact with the database
    cursor = conn.cursor()


# Create the new table 'Track_table'
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Track_table (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        stock_inductor VARCHAR(255),
        start_date_inductor VARCHAR(255),
        end_date_inductor VARCHAR(255),
        d INTEGER
    );
    """
    cursor.execute(create_table_query)
    # Close the cursor and connection
    cursor.close()
    conn.close()
# example
# create_table()



# 將一行data丟進database table中
def insert_row_data(user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var):
    # Database connection details (settings.py照搬)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'newdb_0117',
            'USER': 'postgres', 
            'PASSWORD': 'aqaaqq125', 
            'HOST': 'localhost',  
            'PORT': '5432', 
        }
    }


    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASES['default']['NAME'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        host=DATABASES['default']['HOST'],
        port=DATABASES['default']['PORT']
    )
    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Insert a row of example data into 'Track_table'
    insert_data_query = """
    INSERT INTO Track_table (username, stock_inductor, start_date_inductor, end_date_inductor, d)
    VALUES (%s, %s, %s, %s, %s);
    """
    # Example data to insert
    example_data = (user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var)

    # Execute the insertion
    cursor.execute(insert_data_query, example_data)

    # Commit the transaction to save changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
# example
# user_name_var = '天竺鼠車車'
# stock_inductor_var = 'AAPL'
# start_date_inductor_var = '2025-01-01'
# end_date_inductor_var = '2025-02-01'
# d_var = 10
# insert_row_data(user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var)

# table中尋找符合五個var的其中一個刪掉
def delete_row_data(user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var):
    # Database connection details (settings.py照搬)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'newdb_0117',
            'USER': 'postgres', 
            'PASSWORD': 'aqaaqq125', 
            'HOST': 'localhost',  
            'PORT': '5432', 
        }
    }


    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASES['default']['NAME'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        host=DATABASES['default']['HOST'],
        port=DATABASES['default']['PORT']
    )
    # Create a cursor to interact with the database
    cursor = conn.cursor()


    # 刪除資料的 SQL 語句
    delete_data_query = """
    DELETE FROM Track_table
    WHERE ctid = (
        SELECT ctid
        FROM Track_table
        WHERE username = %s AND stock_inductor = %s AND start_date_inductor = %s
              AND end_date_inductor = %s AND d = %s
        LIMIT 1
    );
    """
    # 執行刪除語句
    cursor.execute(delete_data_query, (user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var))

    # 提交變更
    conn.commit()
    # print(f"Row with specified conditions deleted: ({user_name_var}, {stock_inductor_var}, {start_date_inductor_var}, {end_date_inductor_var}, {d_var})")
    # Close the cursor and connection
    cursor.close()
    conn.close()

# example
# user_name_var = '天竺鼠車車'
# stock_inductor_var = 'AAPL'
# start_date_inductor_var = '2025-01-01'
# end_date_inductor_var = '2025-02-01'
# d_var = 10
# delete_row_data(user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var)





# 去Track_table將所有column的數據全拿存成DataFrame
def fetch():
    # Database connection details (settings.py照搬)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'newdb_0117',
            'USER': 'postgres', 
            'PASSWORD': 'aqaaqq125', 
            'HOST': 'localhost',  
            'PORT': '5432', 
        }
    }


    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASES['default']['NAME'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        host=DATABASES['default']['HOST'],
        port=DATABASES['default']['PORT']
    )
    # Create a cursor to interact with the database
    cursor = conn.cursor()


    # Fetch and display the data from the table to verify
    cursor.execute("SELECT * FROM Track_table;")
    rows = cursor.fetchall()

    # Convert the fetched data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=['id', 'username', 'stock_inductor', 'start_date_inductor', 'end_date_inductor', 'd'])
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return df
# example
print(fetch())



def delete_row_by_id(row_id):
    # Database connection details (from settings.py)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'newdb_0117',
            'USER': 'postgres',
            'PASSWORD': 'aqaaqq125',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASES['default']['NAME'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        host=DATABASES['default']['HOST'],
        port=DATABASES['default']['PORT']
    )
    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # SQL query to delete a row by id
    delete_data_query = """
    DELETE FROM Track_table
    WHERE id = %s;
    """

    # Execute the delete query
    cursor.execute(delete_data_query, (row_id,))

    # Commit the transaction
    conn.commit()

    print(f"Row with id={row_id} has been deleted.")

    # Close the cursor and connection
    cursor.close()
    conn.close()
# delete_row_by_id(4)



# Close the cursor and connection
# cursor.close()
# conn.close()