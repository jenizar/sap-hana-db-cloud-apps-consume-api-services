import requests
import json
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import platform
from hdbcli import dbapi
app=Flask(__name__)

response = json.loads(requests.get("https://services.odata.org/V3/northwind/northwind.svc/Products?$format=json").text)
#print(response)

#values = [item['first'] for item in response['data']]
@app.route("/")
#@app.route("/index")
def index():
    con = dbapi.connect(
    address="2a5b9eaa-3a38-42fd-b10f-fc34db808672.hana.trial-us10.hanacloud.ondemand.com",
    port=443,
    user="DBADMIN",
    password="MyHanadb911_")

    #con=sql.connect("db_web.db")
    #con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM ODATA.PRODUCTS ORDER BY PRODUCTID")

    data=cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM ODATA.PRODUCTS")
    data_count = cur.fetchone()[0]
    data_records = str(data_count)
    
    return render_template("index.html",datas=data,dbrecords=data_records)  

@app.route("/add_data",methods=['POST','GET'])
def add_data():
    for item in response["value"]:
        ProductID1=item["ProductID"]
        ProductName1=item["ProductName"]
        SupplierID1=item["SupplierID"]
        CategoryID1=item["CategoryID"]    
        QuantityPerUnit1=item["QuantityPerUnit"]
        UnitPrice1=item["UnitPrice"]
        UnitsInStock1=item["UnitsInStock"]
        UnitsOnOrder1=item["UnitsOnOrder"]
        ReorderLevel1=item["ReorderLevel"]
        Discontinued1=item["Discontinued"]
        Discontinued1 = str(Discontinued1)   
        con = dbapi.connect(
        address="2a5b9eaa-3a38-42fd-b10f-fc34db808672.hana.trial-us10.hanacloud.ondemand.com",
        port=443,
        user="DBADMIN",
        password="MyHanadb911_")
        cur=con.cursor()
        cur.execute("SELECT ProductID FROM ODATA.PRODUCTS WHERE PRODUCTID = ?", (ProductID1))
        data=cur.fetchall()
        #print(item)
        if len(data)==0:
           sql = "INSERT INTO ODATA.PRODUCTS(ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued) VALUES (?,?,?,?,?,?,?,?,?,?)"
           val = (ProductID1,ProductName1,SupplierID1,CategoryID1,QuantityPerUnit1,UnitPrice1,UnitsInStock1,UnitsOnOrder1,ReorderLevel1,Discontinued1)
           cur.execute(sql, val)
           con.commit()
           message3 = "Data Added " + str(ProductID1) + " " + ProductName1
           flash(message3, 'success')
        else:
           message5 = "Data already exist! " + str(ProductID1) + " " + ProductName1
           flash(message5, 'danger')     
    return redirect(url_for("index"))
    #return render_template("add_data.html")

@app.route("/delete_data/<string:productid>",methods=['GET'])
def delete_data(productid):
    con = dbapi.connect(
       address="2a5b9eaa-3a38-42fd-b10f-fc34db808672.hana.trial-us10.hanacloud.ondemand.com",
       port=443,
       user="DBADMIN",
       password="MyHanadb911_")
    cur=con.cursor()
    cur.execute("DELETE FROM ODATA.PRODUCTS WHERE productid=?",(productid))
    con.commit()
    flash('Data Deleted','warning')
    return redirect(url_for("index"))

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)     