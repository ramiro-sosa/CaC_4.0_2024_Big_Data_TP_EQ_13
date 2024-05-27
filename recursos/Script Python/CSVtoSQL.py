import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from decimal import Decimal

def convert_currency(value):
    """ Convert string currency to decimal """
    try:
        if isinstance(value, str) and value.startswith('$'):
            return Decimal(value.replace("$", "").replace(".", "").replace(",", "."))
        return value
    except:
        return value

def create_insert_statements(csv_file, table_name):
    df = pd.read_csv(csv_file)

    # Convert specific columns
    for column in df.columns:
        if df[column].dtype == object and df[column].str.startswith('$').any():
            df[column] = df[column].apply(convert_currency)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')

    columns = ", ".join(df.columns)
    values_list = []
    omitted_count = 0
    omitted_records = []

    for idx, row in df.iterrows():
        if row.isnull().any():
            omitted_count += 1
            omitted_records.append(idx + 1)  # +1 to convert 0-based index to 1-based line number
            continue
        values = "', '".join([str(value).replace("'", "''") for value in row.values])
        values_list.append(f"('{values}')")

    values_str = ",\n".join(values_list)
    insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES\n{values_str};"
    return insert_statement, omitted_count, omitted_records

def main():
    # Database connection configuration
    config = {
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost',
        'database': 'codoacodo2024'
    }

    # CSV file and table names
    csv_files = [
        ('transactions.csv', 'transactions')
    ]

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        for csv_file, table_name in csv_files:
            print(f"Processing {csv_file}...")
            insert_statement, omitted_count, omitted_records = create_insert_statements(csv_file, table_name)
            print(f"Inserting data into {table_name}...")
            cursor.execute(insert_statement)
            cnx.commit()
            print(f"Data from {csv_file} inserted successfully into {table_name}.")
            print(f"Records omitted: {omitted_count}")
            print(f"List of omitted record lines: {omitted_records}")

        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

if __name__ == "__main__":
    main()
