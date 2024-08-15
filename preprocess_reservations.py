import pandas as pd


def preprocess_reservations(df: pd.DataFrame) -> pd.DataFrame:

    # drop duplicate column 'BME.1'
    df = df.drop(columns=['BME.1'])

    # Rename columns
    df = df.rename(columns={
        'Pos': 'pos',
        'ReservNr': 'reservation_number',
        'Bedarfsmenge': 'required_quantity',
        'BME': 'order_quantity_unit',
        'Material': 'material',
        'BedTermin': 'required_date',
        'Gel': 'is_deleted',
        'KdA-Pos': 'project_order_position',
        'Auftrag': 'project_order_number',
        'Angel.am': 'registration_date',
        'Uhrzeit': '_time'}
    )

    # Format dates
    df['required_date'] = pd.to_datetime(df['required_date'], format='%d.%m.%y')
    df['registration_date'] = df['registration_date'].apply(convert_date_to_datetime)
    df['_time'] = pd.to_datetime(df['_time'], format='%H:%M:%S')

    # format required_quantity
    df['required_quantity'] = df['required_quantity'].apply(convert_required_quantity_to_float)

    # format deleted
    df['is_deleted'] = df['is_deleted'].apply(convert_deleted_string_to_boolean)

    # drop duplicates
    df = df.drop_duplicates()

    return df


def convert_required_quantity_to_float(value: str) -> float:
    if ',' in value and '.' in value:
        value = value.replace('.', '').replace(',', '.')
    elif ',' in value:
        value = value.replace(',', '.')

    # strip any whitespace
    value = value.strip()
    return float(value)


def convert_deleted_string_to_boolean(value) -> bool:
    if type(value) is str:
        value.strip()
        if value == 'X' or value == 'x':
            return True
        else:
            return False
    elif type(value) is float:
        if value == 1.0:
            return True
        else:
            return False


def convert_date_to_datetime(value: str) -> pd.Timestamp:
    # handle 21.06.24 as well as 2024-06-20
    if '-' in value:
        return pd.to_datetime(value, format='%Y-%m-%d')
    else:
        return pd.to_datetime(value, format='%d.%m.%y')
