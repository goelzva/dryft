create_schema_query = """
CREATE SCHEMA IF NOT EXISTS reservation_schema;
"""

delete_schema_query = """
DROP SCHEMA IF EXISTS reservation_schema CASCADE;
"""

delete_table_query = """
DROP TABLE IF EXISTS reservations_table;
"""

delete_historical_table_query = """
DROP TABLE IF EXISTS reservations_history_table;
"""

create_table_query = """
CREATE TABLE IF NOT EXISTS reservations_table (
pos INT NOT NULL,
reservation_number INT NOT NULL,
required_quantity FLOAT NOT NULL,
order_quantity_unit VARCHAR NOT NULL,
material VARCHAR NOT NULL,
required_date DATE NOT NULL,
is_deleted BOOLEAN NOT NULL,
project_order_position INT NOT NULL,
project_order_number INT NOT NULL,
registration_date DATE NOT NULL,
_time TIME NOT NULL,
PRIMARY KEY (pos, reservation_number)
);
"""

create_history_table_query = """
CREATE TABLE IF NOT EXISTS reservations_history_table (
pos INT NOT NULL,
reservation_number INT NOT NULL,
required_quantity FLOAT NOT NULL,
order_quantity_unit VARCHAR NOT NULL,
material VARCHAR NOT NULL,
required_date DATE NOT NULL,
is_deleted BOOLEAN NOT NULL,
project_order_position INT NOT NULL,
project_order_number INT NOT NULL,
registration_date DATE NOT NULL,
_time TIME NOT NULL,
change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (pos, reservation_number, change_timestamp)
);
"""

insert_into_history_query = """
INSERT INTO reservations_history_table (pos, reservation_number, required_quantity, order_quantity_unit, material, required_date, is_deleted, project_order_position, project_order_number, registration_date, _time, change_timestamp)
SELECT pos, reservation_number, required_quantity, order_quantity_unit, material, required_date, is_deleted, project_order_position, project_order_number, registration_date, _time, CURRENT_TIMESTAMP
FROM reservations_table
WHERE pos = %s AND reservation_number = %s;
"""

update_current_record_query = """
UPDATE reservations_table
SET required_quantity = %s, order_quantity_unit = %s, material = %s, required_date = %s, is_deleted = %s, project_order_position = %s, registration_date = %s, _time = %s
WHERE pos = %s AND reservation_number = %s;
"""

insert_current_record_query = """
INSERT INTO reservations_table (pos, reservation_number, required_quantity, order_quantity_unit, material, required_date, is_deleted, project_order_position, project_order_number, registration_date, _time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

check_if_entry_exists_query = """
SELECT EXISTS (
    SELECT 1
    FROM reservations_table
    WHERE pos = %s AND reservation_number = %s
);
"""

