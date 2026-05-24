import uiautomator2 as u2
import os
import csv
from tqdm import tqdm
import time
import mysql.connector

device_id = ""

kode_akses = ""
pin = ""

host = 'localhost'
user = 'root'
password = ''
database = 'tes_scrap_bca'
port = 3306

d = u2.connect(device_id)

print("Login")
d(resourceId="com.bca:id/main_btn_bca").click()
time.sleep(5)
d(resourceId="com.bca:id/login_edit_text").set_text(kode_akses)
d(resourceId="com.bca:id/login_ok_button").click()

time.sleep(5)
print("m-Info")
d(description="Icon m-Info").click()

time.sleep(10)
print("Mutasi Rekening")
d(text="Mutasi Rekening").click()

time.sleep(5)
print("Set Date")
d(resourceId="com.bca:id/mutasi_rekening_et_startdate").click()
d(description="14 April 2026").click()
d(text="OK").click()
time.sleep(5)
d(resourceId="com.bca:id/mutasi_rekening_et_enddate").click()
d(description="20 April 2026").click()
d(text="OK").click()

time.sleep(5)
print("PIN")
d(resourceId="com.bca:id/button_title_right").click()
time.sleep(5)
d(resourceId="com.bca:id/input_text").set_text(pin)
d(resourceId="com.bca:id/button_2").click()

time.sleep(5)
parent = d(resourceId="com.bca:id/content_mutasi")
data_transaksi = []
detail = {}
print(parent.child())
print(len(parent.child()))
index = 0
for child_1 in parent.child():
    print(index)
    print(child_1.info)
    print(child_1.get_text())
    if index == 2:
        detail['date'] = child_1.get_text()
    if index == 3:
        detail['amount'] = child_1.get_text()
    if index == 5:
        detail['description'] = child_1.get_text()
    if index == 6:
        detail['debitcredit'] = child_1.get_text()
    if index == 8:
        detail['recipient'] = child_1.get_text()
    index = index + 1
    if index == 11:
        data_transaksi.append(detail)
        detail = {}
        index = 0
        print("Next Transaksi")

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = conn.cursor()

insert_stmt_transaksi = (
    "INSERT INTO bca_mutasi(date, amount, description, debitcredit, recipient)"
    "VALUES (%s, %s, %s, %s, %s)"
)
for row_transaksi in data_transaksi:
    data_insert_transaksi = (row_transaksi['date'], row_transaksi['amount'], row_transaksi['description'], row_transaksi['debitcredit'],row_transaksi['recipient'])
    try:
        cursor.execute(insert_stmt_transaksi, data_insert_transaksi)
        conn.commit()
        id_transaksi = cursor.lastrowid

    except Exception as e:
        conn.rollback()
        print(e)
    print("Insert Transaksi")
    print(data_insert_transaksi)
print("done!!!!")