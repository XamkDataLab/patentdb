import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

st.title("PostgreSQL Data Viewer")

def connect_to_database():
    try:
        engine = create_engine(
            f"postgresql://{st.secrets['user']}:{st.secrets['password']}@{st.secrets['host']}:{st.secrets['port']}/{st.secrets['database']}"
        )
        return engine
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

def load_table_data(engine, table_name):
    try:
        query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table_name))
        df = pd.read_sql_query(query.as_string(engine.raw_connection()), con=engine)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

if st.button("Connect"):
    engine = connect_to_database()

    if engine:
        st.success("Connected to the database!")

        table_name = st.text_input("Enter the table name to load data:")

        if st.button("Load Table"):
            if table_name:
                df = load_table_data(engine, table_name)
                if df is not None:
                    st.write(f"Data from table `{table_name}`:")
                    st.dataframe(df)

                    # Allow user to download the table as a CSV
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{table_name}.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("Please enter a table name.")
