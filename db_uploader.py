import csv
import os
import django
import sys

# os.chdir(".")
# print("Current dir=", end=""), print(os.getcwd())

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("BASE_DIR=", end=""), print(BASE_DIR)

# sys.path.append(BASE_DIR)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from kb_platform.models import Account,Trans, LSTM

# CSV_PATH = './goldbaby_accounts.csv' 

# with open(CSV_PATH, newline='',encoding='cp949') as csvfile: 
#     data_reader = csv.DictReader(csvfile) 
#     for row in data_reader: 
#         print(row) 
#         Account.objects.create( user_id = row['user_id'],
#                                 acc_num = row['acc_num'],  
#                                 acc_pwd = row['acc_pwd'], 
#                                 acc_type = row['acc_type'], 
#                                 acc_name = row['acc_name'], 
#                                 total = row['total'], 
#                                 created_at = row['created_at'],
#                                 updated_at = row['updated_at'],
#                                 acc_detail = row['acc_detail'],
#                              )


# CSV_PATH2 = './goldbaby_KB마이핏통장_trans.csv' 

# with open(CSV_PATH2, newline='',encoding='cp949') as csvfile: 
#     data_reader = csv.DictReader(csvfile) 
#     for row in data_reader: 
#         print(row) 
#         Trans.objects.create( account_id = row['account_id'],
#                                 trans_date = row['trans_date'],  
#                                 trans_price = row['trans_price'], 
#                                 trans_content = row['trans_content'], 
#                                 trans_type = row['trans_type'], 
#                              )
CSV_PATH3 = './kb.csv'

with open(CSV_PATH3, newline='') as csvfile: 
    data_reader = csv.DictReader(csvfile) 
    for row in data_reader: 
        print(row) 
        LSTM.objects.create( date = row['date'],
                            pred = row['pred'],  
                            act = row['act'], 
                            )