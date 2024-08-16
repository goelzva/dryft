import pandas as pd
from queries import (
    insert_into_history_query,
    update_current_record_query,
    insert_current_record_query,
    check_if_entry_exists_query
)


def upsert_df_to_db(df: pd.DataFrame, conn) -> None:
    with conn.cursor() as cur:
        current_idx = 0
        history_idx = 0
        for index, row in df.iterrows():

            reservation_number = row['reservation_number']
            position = row['pos']

            # check if the reservation exists
            cur.execute(check_if_entry_exists_query, (position, reservation_number))
            exists = cur.fetchall()[0][0]

            if not exists:
                cur.execute(insert_current_record_query, (*row.values,))
                current_idx += 1
            else:
                cur.execute(insert_into_history_query, (position, reservation_number))
                cur.execute(update_current_record_query, (
                    row['required_quantity'],
                    row['order_quantity_unit'],
                    row['material'],
                    row['required_date'],
                    row['is_deleted'],
                    row['project_order_position'],
                    row['registration_date'],
                    row['_time'],
                    row['pos'],
                    row['reservation_number']
                ))
                history_idx += 1
    conn.commit()

    print(f'Successfully added {current_idx} records to the current database.')
    print(f'Successfully added {history_idx} records to the history database.')

