import csv
from pathlib import Path

import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error


class MySQLHelper:
    def __init__(self, host='localhost', user='root', password='', database='mars'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        return self.connection

    def execute(self, query, params=None, many=False):
        cursor = self.connection.cursor()
        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()


def create_table(db):
    query = (
        'CREATE TABLE IF NOT EXISTS mars_weather ('
        'weather_id INT AUTO_INCREMENT PRIMARY KEY,'
        'mars_date DATETIME UNIQUE,'
        'temp INT,'
        'storm INT'
        ')'
    )
    db.execute(query)


def load_csv_rows(csv_path):
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mars_date = row.get('mars_date')
            temp = row.get('temp')
            storm = row.get('storm')
            if not mars_date:
                continue
            rows.append((mars_date, int(temp), int(storm)))
    return rows


def insert_weather_rows(db, rows):
    query = (
        'INSERT INTO mars_weather (mars_date, temp, storm) '
        'VALUES (%s, %s, %s) '
        'ON DUPLICATE KEY UPDATE temp = VALUES(temp), storm = VALUES(storm)'
    )
    db.execute(query, params=rows, many=True)


def save_summary_png(db, output_path):
    query = (
        'SELECT mars_date, temp, storm '
        'FROM mars_weather '
        'ORDER BY mars_date ASC'
    )
    records = db.fetch_all(query)
    if not records:
        print('시각화할 데이터가 없습니다.')
        return

    dates = [row[0] for row in records]
    temps = [row[1] for row in records]
    storms = [row[2] for row in records]

    fig, axis_temp = plt.subplots(figsize=(12, 6))
    axis_temp.plot(dates, temps, marker='o', color='tab:blue', label='temp')
    axis_temp.set_xlabel('mars_date')
    axis_temp.set_ylabel('temp', color='tab:blue')
    axis_temp.tick_params(axis='y', labelcolor='tab:blue')

    axis_storm = axis_temp.twinx()
    axis_storm.bar(dates, storms, alpha=0.25, color='tab:red', label='storm')
    axis_storm.set_ylabel('storm', color='tab:red')
    axis_storm.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Mars Weather Summary')
    fig.autofmt_xdate(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f'요약 이미지 저장 완료: {output_path}')


def main():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / 'mars_weathers_data.csv'
    png_path = base_dir / 'mars_weather_summary.png'

    if not csv_path.exists():
        print(f'CSV 파일이 없습니다: {csv_path}')
        return

    db = MySQLHelper(
        host='localhost',
        user='root',
        password='',
        database='mars',
    )

    try:
        db.connect()
        create_table(db)
        rows = load_csv_rows(csv_path)
        if not rows:
            print('삽입할 CSV 데이터가 없습니다.')
            return
        insert_weather_rows(db, rows)
        print(f'입력 완료: {len(rows)}건')
        save_summary_png(db, png_path)
    except Error as error:
        print(f'MySQL 처리 중 오류: {error}')
    except ValueError as error:
        print(f'CSV 형식 오류: {error}')
    finally:
        db.close()


if __name__ == '__main__':
    main()
