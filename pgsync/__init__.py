# -*- coding: utf-8 -*-
import select
import subprocess

import psycopg2


__allow__ = [b'CREATE', b'ALTER']


pgql = dict(
    host='localhost',
    port=51314,
    user='postgres',
    password='',
    dbname='test'
)


def get_log(filepath, consumer):
    f = subprocess.Popen(['tail', '-n', '0', '-F', filepath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)
    while 1:
        if p.poll(1):
            consumer.send(f.stdout.readline())
            yield


def execute_sql(sql):
    try:
        print(sql)
        conn = psycopg2.connect(**pgql)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def execute_log():
    sql = []
    while 1:
        log = yield
        if b'STATEMENT:' in log[:15]:
            continue
        if b'ERROR:' in log[:15]:
            continue

        if b'LOG:' == log[:4]:
            sql = b' '.join(sql)
            u_sql = sql.upper()

            if b'TABLE' in u_sql:
                if_allow = False
                for allow in __allow__:
                    if allow in u_sql:
                        if_allow = True
                if if_allow:
                    print("="*30)
                    execute_sql(sql.decode())

            # clear
            sql = []
            log = log.replace(b'LOG:', b'')
            log = log.replace(b'statement:', b'')
        sql.append(log.strip())


if __name__ == "__main__":
    consumer = execute_log()
    consumer.send(None)

    produce = get_log('/tmp/pg.log', consumer)
    while 1:
        next(produce)
