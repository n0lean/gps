import sqlite3
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import random
from datetime import time, datetime


# Try direct use nvidia-smi without gputil
# nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv


global idx

class Logger(object):
    def __init__(self, dataset_path='./test.db'):
        self.database_pth = dataset_path
        self._db_init()

        self.interval = 1  # 60s

        self.scheduler = BlockingScheduler()

    def connect(self, **kwargs):
        try:
            print("Connected to test.db.")

            conn = sqlite3.connect(self.database_pth, **kwargs)
            self.connection = True
            return conn
        except:
            raise sqlite3.Error

    def disconnect(self):
        try:
            self.db.close()
        except:
            raise sqlite3.Error

    def _db_init(self):
        self.db = self.connect(detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

        cursor = self.db.cursor()
        sql_del = "DROP TABLE IF EXISTS TEST;"
        cursor.execute(sql_del)
        self.db.commit()

        sql_create_tbl = (
            '''
            CREATE TABLE TEST
            (
            GPU_ID INT PRIMARY KEY NOT NULL,
            time timestamp,
            MEM INT NOT NULL
            );
            '''
        )
        print("Test table created.")
        cursor.execute(sql_create_tbl)
        self.db.commit()

        self.disconnect()

    def write(self):
        global idx
        self.db = self.connect()
        rand = random.randint(1, 100)

        cursor = self.db.cursor()
        cursor.execute(
            '''
            INSERT INTO TEST(GPU_ID, time, MEM) 
            VALUES (?, ?, ?)
            ''', (idx, datetime.now(), rand,)
        )

        self.db.commit()
        print(rand, datetime.now(), idx)

        idx += 1
        self.disconnect()

    def task(self, func):
        job = self.scheduler.add_job(func, 'interval', seconds=self.interval)
        return job

    def start(self):
        self.scheduler.start()

if __name__ == '__main__':
    db = Logger()
    idx = 0
    job = db.task(db.write)
    db.start()


