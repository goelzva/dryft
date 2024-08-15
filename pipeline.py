import pandas as pd

from connect_to_db import connect
from queries import insert_into_history_query, update_current_record_query, insert_current_record_query, check_if_entry_exists_query


def upsert_df_to_db(df: pd.DataFrame, conn, cur):
    for index, row in df.iterrows():

        reservation_number = row['reservation_number']
        position = row['pos']
        project_order_number = row['project_order_number']

        # check if the reservation exists
        cur.execute(check_if_entry_exists_query, (reservation_number, position))
        exists = cur.fetchall()[0][0]

        if not exists:
            cur.execute(insert_current_record_query, (*row.values,))
            conn.commit()
            return
        else:
            cur.execute(insert_into_history_query, (reservation_number, position, project_order_number))
            cur.execute(update_current_record_query, (*row.values,))
            conn.commit()
            return

