# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:48 2020

@author: Lenovo
"""

import MySQLdb
import random
import json
from MySQLdb._exceptions import OperationalError
from flask import Flask, render_template
from flask import request, make_response
from flask import url_for, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
server_addr = '127.0.0.1'
dbname = 'bank'

#bootstrap = Bootstrap(app)

@app.route('/', methods=("GET", "POST"))
@app.route('/index', methods=("GET", "POST"))
def index():
    return render_template('index.html')


@app.route('/login/', methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            global db
            db = MySQLdb.connect(server_addr, username, password, dbname, charset='utf8')
            cursor = db.cursor()
            cursor.execute("show tables")
            alldata = cursor.fetchall()
            print(alldata)
            return redirect(url_for('system'))
        except OperationalError:
            db = None
            errormsg = '数据库连接故障，请检查数据库服务是否开启、账号密码是否正确！'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:
        return render_template('login.html')
    

@app.route('/system/', methods=("GET", "POST"))
def system():
    return render_template('system.html')
    

@app.route('/newcustomer/', methods=("GET", "POST"))
def newcustomer():
    if request.method == "POST":
        userID = request.form['UserID']
        name = request.form['姓名']
        phone = request.form['联系电话']
        liveplace = request.form['家庭住址']
        contactphone = request.form['联系人手机号']
        relation = request.form['联系人关系']
        try:
            global db
            cursor = db.cursor()
            cursor.execute('insert into 客户(UserID, 姓名, 联系电话, 家庭住址, 联系人手机号, 联系人客户关系) values(%s, %s, %s, %s, %s, %s)',
                                (userID, name, phone, liveplace, contactphone, relation))
            db.commit()
            return redirect(url_for('system'))
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入或客户ID已被注册所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('newcustomer.html')
    
    
@app.route('/newaccount/', methods=("GET", "POST"))
def newaccount():
    if request.method == "POST":
        accountID = request.form['accountID']
        userID = request.form['UserID']
        bankname = request.form['bankname']
        staffID = request.form['staffID']
        balance = request.form['balance']
        balance = float(balance)
        opendate = request.form['opendate']
        openbank = request.form['openbank']
        accounttype = request.form['accounttype']
        interestrate = request.form['interestrate']
        currencytype = request.form['currencytype']
        overdraft = request.form['overdraft']
        if openbank == '':
            openbank = bankname
        try:
            global db
            cursor = db.cursor()
            # 先判断是否存在储蓄账户
            cursor.execute('select 储蓄账户ID, 支票账户ID from 账户约束 where UserID = "%s" and 支行Name = "%s"' % (userID, bankname))
            data = cursor.fetchone()
            storage_enable = 0
            check_enable = 0
            if data == None:
                storage_enable = 1
                check_enable = 1
                cursor.execute('insert into 账户约束(支行Name, UserID) values(%s, %s)',
                                    (bankname, userID))
                db.commit()
            elif data[0] == None:
                storage_enable = 1
            elif data[1] == None:
                check_enable = 1

            if accounttype == '0':  # 储蓄账户
                if storage_enable == 1:
                    interestrate = float(interestrate)
                    cursor.execute('insert into 账户(账户ID, 支行Name, StaffID, 账户类型, 余额, 开户日期, 开户支行) values(%s, %s, %s, %s, %s, %s, %s)',
                                    (accountID, bankname, staffID, '储蓄账户', balance, opendate, openbank))
                    cursor.execute('insert into 储蓄账户(账户ID, 支行Name, StaffID, 账户类型, 余额, 开户日期, 开户支行, 利率) values(%s, %s, %s, %s, %s, %s, %s, %s)',
                                    (accountID, bankname, staffID, '储蓄账户', balance, opendate, openbank, interestrate))
                    cursor.execute('update 账户约束 set 储蓄账户ID = "%s" where UserID = "%s" and 支行Name = "%s"' % (accountID, userID, bankname))
                    cursor.execute('insert into 使用账户(UserID, 账户ID, 使用时间) values(%s, %s, %s)',
                                    (userID, accountID, opendate))
                    db.commit()
                    return redirect(url_for('system'))
                else:  
                    errormsg = 'The user has registered an account for storage in this bank!'
                    print(errormsg)
                    return render_template('system_fail.html', errormsg=errormsg)
            else:                   # 支票账户
                if check_enable == 1:
                    overdraft = float(overdraft)
                    cursor.execute('insert into 账户(账户ID, 支行Name, StaffID, 账户类型, 余额, 开户日期, 开户支行) values(%s, %s, %s, %s, %s, %s, %s)',
                                    (accountID, bankname, staffID, '支票账户', balance, opendate, openbank))
                    cursor.execute('insert into 支票账户(账户ID, 支行Name, StaffID, 账户类型, 余额, 开户日期, 开户支行, 货币类型, 透支额) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    (accountID, bankname, staffID, '支票账户', balance, opendate, openbank, currencytype, overdraft))
                    cursor.execute('update 账户约束 set 支票账户ID = "%s" where UserID = "%s" and 支行Name = "%s"' % (accountID, userID, bankname))
                    cursor.execute('insert into 使用账户(UserID, 账户ID, 使用时间) values(%s, %s, %s)',
                                    (userID, accountID, opendate))
                    db.commit()
                    return redirect(url_for('system'))
                else:
                    errormsg = 'The user has registered an account for check in this bank!'
                    print(errormsg)
                    return render_template('system_fail.html', errormsg=errormsg)
            errormsg = 'Invalid account type!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入或账户ID已被注册所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('newaccount.html')
    

@app.route('/newloan/', methods=("GET", "POST"))
def newloan():
    if request.method == "POST":
        loanID = request.form['loanID']
        userID = request.form['userID']
        bankname = request.form['bankname']
        staffID = request.form['staffID']
        amount = request.form['amount']
        amount = float(amount)
        paytype = request.form['paytype']
        paytype = '分五年期' if paytype == '0' else '分十年期'
        try:
            global db
            cursor = db.cursor()
            cursor.execute('select 支票账户ID from 账户约束 where UserID = "%s" and 支行Name = "%s"' % (userID, bankname))
            data = cursor.fetchone()
            if data == None:
                errormsg = "The user doesn't have an account for check in this bank!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
            else:       # 可以贷款
                cursor.execute('insert into 贷款(贷款ID, StaffID, 支行Name, 金额, 支付方式) values(%s, %s, %s, %s, %s)',
                                    (loanID, staffID, bankname, amount, paytype))
                cursor.execute('insert into 借贷(贷款ID, UserID) values(%s, %s)',
                                    (loanID, userID))
                db.commit()
                return redirect(url_for('system'))
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入或贷款ID已被注册所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('newloan.html')


@app.route('/deletecustomer/', methods=("GET", "POST"))
def deletecustomer():
    if request.method == "POST":
        deleteID = request.form['deleteID']
        try:
            global db
            cursor = db.cursor()
            cursor.execute('select * from 账户约束 where UserID = "%s"' % deleteID)
            data = cursor.fetchone()
            if data == None:        # 可以删除
                cursor.execute('delete from 使用账户 where UserID = "%s"' % deleteID)
                cursor.execute('delete from 客户 where UserID = "%s"' % deleteID)
                db.commit()
                return redirect(url_for('system'))
            else:
                errormsg = "The user has registered accounts. Can't be deleted!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('deletecustomer.html')


@app.route('/deleteaccount/', methods=("GET", "POST"))
def deleteaccount():
    if request.method == "POST":
        deleteID = request.form['deleteID']
        try:
            global db
            cursor = db.cursor()
            cursor.execute('select 账户.账户类型, 账户.余额, 账户约束.UserID from 账户, 账户约束 where 账户ID = 储蓄账户ID and 账户ID = "%s"' % deleteID)
            data = cursor.fetchone()
            if data == None:
                cursor.execute('select 支票账户.账户类型, 支票账户.余额, 支票账户.透支额, 账户约束.UserID from 支票账户, 账户约束 where 账户ID = 支票账户ID and 账户ID = "%s"' % deleteID)
                data = cursor.fetchone()
            # print(data)
            if data == None:        # 账户不存在
                errormsg = "The account doesn't exist. Can't be deleted!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
            elif data[0] == '储蓄账户' and data[1] == 0: # 储蓄账户 且可删除
                cursor.execute('update 账户约束 set 储蓄账户ID = null where userID = "%s"' % data[2])
                cursor.execute('delete from 使用账户 where 账户ID = "%s"' % deleteID)
                cursor.execute('delete from 储蓄账户 where 账户ID = "%s"' % deleteID)
                cursor.execute('delete from 账户 where 账户ID = "%s"' % deleteID)
                db.commit()
                return redirect(url_for('system'))
            elif data[0] == '支票账户' and data[1] == 0 and data[2] == 0:   # 支票账户 且可能可以删除
                # 判断一下是否还有相关借贷
                cursor.execute('select 借贷.贷款ID from 借贷, 账户约束 where 借贷.UserID = 账户约束.UserID and 支票账户ID = "%s"' % deleteID)
                temploanID = cursor.fetchone()
                if temploanID == None:  # 可删除
                    cursor.execute('update 账户约束 set 支票账户ID = null where userID = "%s"' % data[3])
                    cursor.execute('delete from 使用账户 where 账户ID = "%s"' % deleteID)
                    cursor.execute('delete from 支票账户 where 账户ID = "%s"' % deleteID)
                    cursor.execute('delete from 账户 where 账户ID = "%s"' % deleteID)
                    db.commit()
                    return redirect(url_for('system'))
                else:
                    errormsg = "The account has unfinished loan. Can't be deleted!"
                    print(errormsg)
                    return render_template('system_fail.html', errormsg=errormsg)
            else:
                errormsg = "The account has balance in it. Can't be deleted!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('deleteaccount.html')
    
    
@app.route('/deleteloan/', methods=("GET", "POST"))
def deleteloan():
    if request.method == "POST":
        deleteID = request.form['deleteID']
        try:
            global db
            cursor = db.cursor()
            cursor.execute('delete from 借贷 where 贷款ID = "%s"' % deleteID)
            cursor.execute('delete from 付款 where 贷款ID = "%s"' % deleteID)
            cursor.execute('delete from 贷款 where 贷款ID = "%s"' % deleteID)
            db.commit()
            return redirect(url_for('system'))
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('deleteloan.html')


@app.route('/modifycustomer/', methods=("GET", "POST"))
def modifycustomer():
    if request.method == "POST":
        modifyID = request.form['modifyID']
        name = request.form['姓名']
        phone = request.form['联系电话']
        liveplace = request.form['家庭住址']
        relation = request.form['联系人关系']
        try:
            global db
            cursor = db.cursor()
            if name != '':         # 需要修改
                cursor.execute('update 客户 set 姓名 = "%s" where UserID = "%s"' % (name, modifyID))
            if phone != '':         # 需要修改
                cursor.execute('update 客户 set 联系电话 = "%s" where UserID = "%s"' % (phone, modifyID))
            if liveplace != '':     # 需要修改
                cursor.execute('update 客户 set 家庭住址 = "%s" where UserID = "%s"' % (liveplace, modifyID))
            if relation != '':     # 需要修改
                cursor.execute('update 客户 set 联系人客户关系 = "%s" where UserID = "%s"' % (relation, modifyID))
            db.commit()
            return redirect(url_for('system'))
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('modifycustomer.html')
    
    
@app.route('/modifyaccount/', methods=("GET", "POST"))
def modifyaccount():
    if request.method == "POST":
        modifyID = request.form['modifyID']
        staffID = request.form['staffID']
        try:
            global db
            cursor = db.cursor()
            if staffID != '':         # 需要修改
                cursor.execute('select * from 员工 where StaffID = "%s"' % staffID)
                tempstaff = cursor.fetchone()
                if tempstaff == None:
                    errormsg = "Staff doesn't exist. Can't Change!"
                    print(errormsg)
                    return render_template('system_fail.html', errormsg=errormsg)
                else:   # 可以修改
                    cursor.execute('update 账户 set StaffID = "%s" where 账户ID = "%s"' % (staffID, modifyID))
                    cursor.execute('update 储蓄账户 set StaffID = "%s" where 账户ID = "%s"' % (staffID, modifyID))
                    cursor.execute('update 支票账户 set StaffID = "%s" where 账户ID = "%s"' % (staffID, modifyID))
                    db.commit()
                    return redirect(url_for('system'))
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('modifyaccount.html')
    
    
@app.route('/issueloan/', methods=("GET", "POST"))
def issueloan():
    if request.method == "POST":
        loanID = request.form['loanID']
        time = request.form['time']
        try:
            global db
            cursor = db.cursor()
            cursor.execute('select 支行Name, 金额, 支付方式 from 贷款 where 贷款ID = "%s"' % loanID)
            temp = cursor.fetchone()
            if temp == None:
                errormsg = "loanID doesn't exist. Can't issue!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
            bankname = temp[0]
            totalamount = float(temp[1])
            paytype = temp[2]
            totalcount = 5 if paytype == '分五年期' else 10
            singleamount = totalamount / totalcount
            donecount = 0
            cursor.execute('select * from 付款 where 贷款ID = "%s"' % loanID)
            temp = cursor.fetchall()
            for item in temp:
                donecount += 1
            if donecount == totalcount:
                errormsg = "The loan has finished its payment. Can't issue!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
            # 银行资产是否足够
            cursor.execute('select 资产 from 支行 where 支行Name = "%s"' % bankname)
            fortune = float(cursor.fetchone()[0])
            if fortune < singleamount:
                errormsg = "The bank doesn't have enough money. Can't issue!"
                print(errormsg)
                return render_template('system_fail.html', errormsg=errormsg)
            # 满足放款条件
            # 对应支行资产减少
            newfortune = fortune - singleamount
            cursor.execute('update 支行 set 资产 = "%s" where 支行Name = "%s"' % (newfortune, bankname))
            # 对应账户透支额增加
            cursor.execute('select 透支额, 支票账户.账户ID, 账户约束.UserID from 借贷, 账户约束, 支票账户 where 借贷.UserID = 账户约束.UserID and 账户约束.支票账户ID = 支票账户.账户ID and 借贷.贷款ID = "%s" and 账户约束.支行Name = "%s"' % (loanID, bankname))
            temp = cursor.fetchone()
            overdraft = float(temp[0])
            accountID = temp[1]
            userID = temp[2]
            newoverdraft = overdraft + singleamount
            cursor.execute('update 支票账户 set 透支额 = "%s" where 账户ID = "%s"' % (newoverdraft, accountID))
            # 添加新的付款记录
            issueID = random.randint(10000, 99999)
            issueID = str(issueID)
            cursor.execute('insert into 付款(贷款号, 时间, 贷款ID, 金额) values(%s, %s, %s, %s)', 
                                (issueID, time, loanID, singleamount))
            # 添加新的账户使用记录
            cursor.execute('insert into 使用账户(UserID, 账户ID, 使用时间) values(%s, %s, %s)', 
                                (userID, accountID, time))
            db.commit()
            # 显示返回数据
            donecount += 1
            leftcount = totalcount - donecount
            leftamount = leftcount * singleamount
            item = []
            item.append(loanID)
            item.append(str(totalamount))
            item.append(paytype)
            item.append(str(singleamount))
            item.append(str(leftcount))
            item.append(str(leftamount))
            item.append(issueID)
            item.append(time)
            result = []
            result.append(item)
            return render_template('issueloan.html', result=result)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('issueloan.html')
    
    
@app.route('/searchcustomer/', methods=("GET", "POST"))
def searchcustomer():
    if request.method == "POST":
        searchkey = request.form['searchkey']
        searchmethod = request.form['searchmethod']
        try:
            global db
            cursor = db.cursor()
            if searchmethod == '0':
                cursor.execute('select 客户.UserID, 客户.姓名, 客户.联系电话, 客户.家庭住址, 联系人.姓名, 联系人.手机号, 客户.联系人客户关系 from 客户, 联系人 where 客户.联系人手机号 = 联系人.手机号 and 客户.UserID = "%s"' % searchkey)
                result = cursor.fetchall()
                print(result)
                return render_template('searchcustomer.html', result=result)
            else:
                cursor.execute('select 客户.UserID, 客户.姓名, 客户.联系电话, 客户.家庭住址, 联系人.姓名, 联系人.手机号, 客户.联系人客户关系 from 客户, 联系人 where 客户.联系人手机号 = 联系人.手机号 and 客户.姓名 = "%s"' % searchkey)
                result = cursor.fetchall()
                print(result)
                return render_template('searchcustomer.html', result=result)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('searchcustomer.html')
    
    
@app.route('/searchaccount/', methods=("GET", "POST"))
def searchaccount():
    if request.method == "POST":
        searchkey = request.form['searchkey']
        searchmethod = request.form['searchmethod']
        try:
            global db
            cursor = db.cursor()
            if searchmethod == '0':
                cursor.execute('select 账户ID, 支行Name, StaffID, 余额, 开户日期, 开户支行, 账户类型 from 账户 where 账户ID = "%s"' % searchkey)
                result = cursor.fetchall()
                print(result)
                return render_template('searchaccount.html', result=result)
            else:
                cursor.execute('select 账户ID, 支行Name, StaffID, 余额, 开户日期, 开户支行, 账户类型 from 账户 where 支行Name = "%s"' % searchkey)
                result = cursor.fetchall()
                print(result)
                return render_template('searchaccount.html', result=result)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('searchaccount.html')
    

@app.route('/searchloan/', methods=("GET", "POST"))
def searchloan():
    if request.method == "POST":
        searchkey = request.form['searchkey']
        searchmethod = request.form['searchmethod']
        try:
            global db
            cursor = db.cursor()
            if searchmethod == '0':
                cursor.execute('select 贷款.贷款ID, 支行Name, UserID, StaffID, 金额, 支付方式 from 贷款, 借贷 where 贷款.贷款ID = 借贷.贷款ID and 贷款.贷款ID = "%s"' % searchkey)
                result = cursor.fetchall()
                print(result)
                return render_template('searchloan.html', result=result)
            else:
                cursor.execute('select 贷款.贷款ID, 支行Name, UserID, StaffID, 金额, 支付方式 from 贷款, 借贷 where 贷款.贷款ID = 借贷.贷款ID and 支行Name = "%s"' % searchkey)
                result = cursor.fetchall()
                print(result)
                return render_template('searchloan.html', result=result)
        except OperationalError:
            errormsg = '数据库故障，可能是非法的输入所致!'
            print(errormsg)
            return render_template('system_fail.html', errormsg=errormsg)
    else:   
        return render_template('searchloan.html')


@app.route('/statistics-business/', methods=("GET", "POST"))
def statistics_business():
    try:
        global db
        cursor = db.cursor()
        banks = []
        total_store_amount = []
        total_loan_amount = []
        total_store_customer = []
        total_loan_customer = []
        leftforture = []
        result = []
        # 获取各支行信息
        cursor.execute('select 支行Name, 资产 from 支行')
        temp = cursor.fetchall()
        for item in temp:
            banks.append(item[0])
            leftforture.append(item[1])
        # 业务金额、用户数信息
        for bank in banks:
            # 用户数
            store_customer_cnt = 0
            loan_customer_cnt = 0
            cursor.execute('select * from 账户约束 where 支行Name = "%s"' % bank)
            temp = cursor.fetchall()
            for item in temp:
                if item[2] != None:
                    store_customer_cnt += 1
                if item[3] != None:
                    loan_customer_cnt += 1
            total_store_customer.append(store_customer_cnt)
            total_loan_customer.append(loan_customer_cnt)
            # 业务金额
            store_amount_cnt = 0
            loan_amount_cnt = 0
            cursor.execute('select 余额 from 储蓄账户 where 支行Name = "%s"' % bank)
            temp = cursor.fetchall()
            for item in temp:
                store_amount_cnt += float(item[0])
            total_store_amount.append(store_amount_cnt)
            cursor.execute('select 透支额 from 支票账户 where 支行Name = "%s"' % bank)
            temp = cursor.fetchall()
            for item in temp:
                loan_amount_cnt += float(item[0])
            total_loan_amount.append(loan_amount_cnt)
            # 统计表
            resultitem = []
            resultitem.append(bank)
            resultitem.append(store_amount_cnt)
            resultitem.append(loan_amount_cnt)
            resultitem.append(store_customer_cnt)
            resultitem.append(loan_customer_cnt)
            result.append(resultitem)

        return render_template('statistics-business.html', 
                plotXaxis=json.dumps(banks), 
                total_store_amount=json.dumps(total_store_amount),
                total_loan_amount=json.dumps(total_loan_amount),
                total_store_customer=json.dumps(total_store_customer),
                total_loan_customer=json.dumps(total_loan_customer),
                leftforture=json.dumps(leftforture),
                result=result)
    except OperationalError:
        errormsg = '数据库访问故障！'
        print(errormsg)
        return render_template('system_fail.html', errormsg=errormsg)


@app.route('/statistics-time/', methods=("GET", "POST"))
def statistics_time():
    try:
        global db
        cursor = db.cursor()
        banks = []
        total_amount = []
        total_customer = []
        leftforture = []
        amountresult = []
        customerresult = []
        # 获取各支行信息
        cursor.execute('select 支行Name, 资产 from 支行')
        temp = cursor.fetchall()
        banknum = 0
        for item in temp:
            banknum += 1
            banks.append(item[0])
            leftforture.append(item[1])
        # 业务金额、用户数信息
        for bank in banks:
            amountresult_item = []
            amountresult_item.append(bank)
            customerresult_item = []
            customerresult_item.append(bank)
            # 用户数
            customer_cnt = []
            for month in range(1, 13):
                monthstr = str(month) if month > 9 else '0'+str(month)
                monthtime = '2020-' + monthstr + '-01'
                cursor.execute("select * from 使用账户, 账户约束 where 使用账户.UserID = 账户约束.UserID and 账户约束.支行Name = '%s'\
                                     and DATE_FORMAT(使用时间, '%%Y-%%m') = DATE_FORMAT('%s', '%%Y-%%m')" % (bank, monthtime))
                temp = cursor.fetchall()
                curmonth_cnt = len(temp)
                customer_cnt.append(curmonth_cnt)
                customerresult_item.append(curmonth_cnt)
            total_customer.append(customer_cnt)
            customerresult.append(customerresult_item)
            # 业务金额
            amount_cnt = []
            for month in range(1, 13):
                curmonth_amount = 0
                monthstr = str(month) if month > 9 else '0'+str(month)
                monthtime = '2020-' + monthstr + '-01'
                # 储蓄金额
                cursor.execute("select 余额 from 使用账户, 账户 where 使用账户.账户ID = 账户.账户ID and 账户.支行Name = '%s' and 账户类型 = '储蓄账户'\
                                     and DATE_FORMAT(开户日期, '%%Y-%%m') = DATE_FORMAT('%s', '%%Y-%%m')" % (bank, monthtime))
                temp = cursor.fetchall()
                for item in temp:
                    curmonth_amount += float(item[0])
                # 贷款金额
                cursor.execute("select 付款.金额 from 付款, 贷款 where 付款.贷款ID = 贷款.贷款ID and 贷款.支行Name = '%s'\
                                     and DATE_FORMAT(时间, '%%Y-%%m') = DATE_FORMAT('%s', '%%Y-%%m')" % (bank, monthtime))
                temp = cursor.fetchall()
                for item in temp:
                    curmonth_amount += float(item[0])
                amount_cnt.append(curmonth_amount)
                amountresult_item.append(curmonth_amount)
            total_amount.append(amount_cnt)
            amountresult.append(amountresult_item)
            
        return render_template('statistics-time.html', 
                plotXaxis=json.dumps(banks), 
                banknum=banknum,
                total_amount=json.dumps(total_amount),
                total_customer=json.dumps(total_customer),
                leftforture=json.dumps(leftforture),
                amountresult=amountresult,
                customerresult=customerresult)
    except OperationalError:
        errormsg = '数据库访问故障！'
        print(errormsg)
        return render_template('system_fail.html', errormsg=errormsg)

    
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def not_found(e):
    errormsg = '请求的页面未找到'
    print(errormsg)
    return render_template('system_fail.html', errormsg=errormsg)

app.run()