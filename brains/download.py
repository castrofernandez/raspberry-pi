#!/usr/bin/python

from __future__ import print_function

import pymysql

conn = pymysql.connect(host='juancastro.es', port=3306, user='juancast_circo', passwd='neuronal_org_1', db='juancast_circo')

cur = conn.cursor()

cur.execute("SELECT * FROM users")

print(cur.description)

print()

for row in cur:
   print(row)

cur.close()
conn.close()
