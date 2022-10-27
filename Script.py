#from asyncio.windows_events import NULL
from code import interact
import psycopg2
import json 
import requests 

# Connect to an existing databset
conn = psycopg2.connect(
    database='exampledb',
    user='docker',
    password='docker',
    host="0.0.0.0"
)
###############################
# Get the data from IQ Data API

url = 'https://iqdata.social/v2.0/api/dict/interests?hide_deprecated=true'
'''
headers = {
    'X-Api-Key':'62e19481443ed5d02b23e2f4.be378ffa7332b14c',
    'user':'product@magiclinks.com:62e19481443ed5d02b23e2f4.be378ffa7332b14c.a42a13a26b31569e'
}
'''
data = requests.get(url).text 
dic_data = json.loads(data)
#print(type(dic_data))
#print(dic_data['data']['interests'])
################################
# Open cursor to perform database operations
cur = conn.cursor()
# Insert data into Interests table
insert_script_interest = 'INSERT INTO "Interests" ("id","name","count","deprecated") VALUES (%s,%s,%s,%s)'
for index in range(len(dic_data['data']['interests'])):
    value = dic_data['data']['interests'][index]
    insert_value = (value['id'],value['name'],value['count'],value['deprecated'])
    cur.execute(insert_script_interest,insert_value)
# Insert data into Brands table
insert_script_brand = 'INSERT INTO "Brands" ("id","name","interest_id","count","deprecated") VALUES (%s,%s,%s,%s,%s)'
for index in range(len(dic_data['data']['brands'])):
    value = dic_data['data']['brands'][index]
    if "interest" not in value.keys():
        insert_value = (value['id'],value['name'],None,value['count'],value['deprecated'])
    else:
        insert_value = (value['id'],value['name'],value['interest'][0]['id'],value['count'],value['deprecated'])

    cur.execute(insert_script_brand,insert_value)

# Insert data 
'''
# This part is just sample code
insert_script = 'INSERT INTO "Student" ("Name","age") VALUES (%s,%s)'
insert_value = ('ee',22)
cur.execute(insert_script,insert_value)
'''

# Query the database
'''
cur.execute('SELECT * FROM "Student" ')

rows = cur.fetchall()
if len(rows) == 0:
    print('Empty')
else:

    for row in rows:
        print(row)
conn.commit()
'''
conn.commit()
# Close communication
cur.close()
conn.close()
