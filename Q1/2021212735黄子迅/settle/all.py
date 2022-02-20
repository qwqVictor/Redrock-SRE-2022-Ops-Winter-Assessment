#!/usr/bin/python3
import pymysql
import os
import datetime
import signal
import sys
import getpass

#mysql -h localhost -u myname -ppassword mydb < xxx.sql(执行.sql文件内的sql语句)
#分文件编辑指令
##主表以id字段作user_id(便于观察)，主表指user-username
#auto increment为自增字段，在插入表时不填写该字段则默认让数据库(按插入顺序)赋给其值
def environment_settle():
    os.system('mysql -uroot -p1029384756lxt < /Documents/environment_settle.sql')
    (db,cursor)=database_connecter('super_root')
    try:
        if id_creator('super_root','translate')=='1':
            cursor.execute('insert into translate (user_name) values(\'root\')')#默认用户名
            cursor.execute('insert into info (password) values(\'1029384756lxt\')')#默认密码
            db.commit()
        default_server_adder('root','server_list')
        default_server_adder('guest','server_list')
        default_server_adder('super_root','server_list')
    except:
        print('出现了错误')
        db.rollback()
        database_disconnecter(db,cursor)


def default_server_adder(base,tablename):
    try:
        (db,cursor)=database_connecter(base)
        if id_creator(base,tablename)=='1':#默认列表
            cursor.execute('insert into server_list (server_name,server_location) values(\'server_1\',\'root@172.18.0.3\')')
            cursor.execute('insert into server_list (server_name,server_location) values(\'server_2\',\'root@172.18.0.2\')')
            cursor.execute('insert into server_list (server_name,server_location) values(\'server_3\',\'root@172.18.0.4\')')
            db.commit()
    except:
            db.rollback()
            print('发生了错误')
            database_disconnecter(base,cursor)

            
def user_selector():
    environment_settle()
    while True:
        print('\n欢迎，接下来请选择您的身份：\n')
        print('G——宾客\n\nR——管理员\n\nS——超管\n')
        selection=input()
        if selection=='G':
            LoginSystem('guest')
        elif selection=='R':
            LoginSystem('root')
        elif selection=='S':
            LoginSystem('super_root')
        else:
            print('\n请输入指定的选项\n')
            continue
    

def signal_handler(siganal,frame):
    print('',end='')


def limmit_changer(changer_base,base,changer_id,user_id):
    print('输入A以更改用户的服务器访问权限\n')
    print('输入B以更改用户的命令权限\n')
    print('输入Q以退出\n')
    while True:
        choice=input()
        print('\n',end='')
        if choice=='A':
            guest_server_changer(changer_base,base,changer_id,user_id)
            return 0
        elif choice=='B':
            guest_command_changer(changer_base,base,changer_id,user_id)
            return 0
        elif choice=='Q':
            return 0
        else:
            print("请输入A/B/Q中的其中一个\n")
            continue

  
def guest_command_changer(changer_base,base,changer_id,user_id):
    while True:
        print('输入Q以返回，或输入A以为该用户添加权限，输入D以删除该用户的目标权限\n')
        selection=input()
        if selection=='Q':
            history_writter(changer_base,str(changer_id),'放弃对id为'+str(user_id)+'的'+str(base)+'用户修改权限')
            return 0
        elif selection=='D':
            print('\n',end='')
            while True:
                print('该用户拥有的权限有：') 
                authority_info_tuple=command_search(base,str(user_id))
                print('请输入权限的名称以删除对应权限，或输入Q以返回\n')
                select=input()
                print('\n',end='')
                if select=='Q':
                    break
                else:
                    if select in authority_info_tuple[0]:
                        (db,cursor)=database_connecter(base)
                        try:
                            cursor.execute("delete from command where user_id=\'"+str(user_id)+"\' and command_start=\'"+select+"\'")
                            db.commit()
                            print('权限删除成功！\n')
                        except:
                            db.rollback()
                            print('权限删除失败！请联系管理员\n')
                        database_disconnecter(db,cursor)
                        history_writter(changer_base,changer_id,'为id为'+str(user_id)+'的'+str(base)+'用户删除权限'+str(select))
                    else:
                        print('该用户没有持有该命令的权限')
        elif selection=='A':
            print('\n',end='')
            print('该用户持有的权限有：') 
            authority_info_tuple=command_search(base,str(user_id))
            if changer_base=='super_root':
                print('您可以添加任意权限\n')
            else:
                print('您持有的权限有：')
                add_authority=command_search(changer_base,str(changer_id))
            while True:
                print('请输入目标权限的名称以添加对应权限，或输入Q以返回\n')
                select=input()
                id=id_creator(base,"command")
                print('\n',end='')
                if select=='Q':
                   break
                else:
                    if select not in authority_info_tuple[0] and changer_base=='super_root':
                        (db,cursor)=database_connecter(base)
                        try:
                            cursor.execute("insert into command (user_id,command_start,command_last) values("+user_id+",\'"+select+"\',\'0\')")
                            db.commit()
                            print('权限添加成功！\n')
                        except:
                            db.rollback()
                            print('权限添加失败！请检查配置！\n')
                        database_disconnecter(db,cursor)
                        history_writter(changer_base,changer_id,'为id为'+str(user_id)+'的'+str(base)+'用户添加'+str(select)+'的全部权限')
                        continue
                    elif select in add_authority[0] and select not in authority_info_tuple[0]:
                        if command_parameter_changer(base,select)=='0':                        
                            (db,cursor)=database_connecter('guest') 
                            try:
                                cursor.execute("insert into command (user_id,command_start,command_last) values("+(user_id)+",\'"+select+"\',\'0\')")
                                db.commit()
                                print('权限添加成功！\n')
                            except:
                                db.rollback()
                                print('权限添加失败！请联系管理员！\n')
                            database_disconnecter(db,cursor)
                            history_writter(base,changer_id,'为id为'+str(user_id)+'的用户添加'+str(select)+'的全部权限')
                            continue
                        else:
                            print('您不存在更改该权限的权限\n')
                    else:
                        print('该用户已持有命令的权限或是您不存在添加此命令的权利\n')
        else:
            print('\n',end='')
            print('请输入A/D/Q的其中一个！\n')
            continue


def command_parameter_changer(base,inner):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from command')
    all_list=cursor.fetchall()
    database_disconnecter(db,cursor)
    command_name_list=[tuples[2] for tuples in all_list]
    command_parameter_list=[tuples[3] for tuples in all_list]
    if inner in command_name_list:
        location=command_name_list.index(inner)
        return str(command_parameter_list[location])
    elif inner in command_parameter_list:
        name=command_parameter_list.index(inner)
        return str(command_name_list[name])


def server_locate_changer(base,inner):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from server_list')
    all_list=cursor.fetchall()
    database_disconnecter(db,cursor)
    server_name_list=[tuples[1] for tuples in all_list]
    server_locate_list=[tuples[2] for tuples in all_list]
    if inner in server_name_list:
        location=server_name_list.index(inner)
        return str(server_locate_list[location])
    elif inner in server_locate_list:
        name=server_locate_list.index(inner)
        return str(server_name_list[name])


def guest_server_changer(changer_base,base,changer_id,user_id):
    while True:
        print('输入Q以返回，或输入A以为该用户添加可访问的服务器，输入D以删除该用户对目标服务器的访问权限\n')
        selection=input()
        if selection=='Q':
            history_writter(changer_base,str(changer_id),'放弃对id为'+str(user_id)+'的'+str(base)+'用户修改服务器访问权限')
            return 0
        elif selection=='D':
            print('\n',end='')
            while True:
                print('该用户可访问的服务器有：') 
                server_info_tuple=server_search(base,str(user_id))
                print('请输入目标服务器的名称以删除对应权限，或输入Q以返回\n')
                select=input()
                print('\n',end='')
                if select=='Q':
                    break
                else:
                    if select in server_info_tuple[0]:
                        (db,cursor)=database_connecter('guest')
                        try:
                            cursor.execute("delete from ssh_server where user_id=\'"+str(user_id)+"\' and server_name=\'"+select+"\'")
                            db.commit()
                            print('删除成功！\n')
                        except:
                            db.rollback()
                            print('出现错误！\n')
                        database_disconnecter(db,cursor)
                        history_writter(changer_base,changer_id,'为id为'+str(user_id)+'的'+str(base)+'用户删除服务器名为'+str(select)+'的访问权限')
                    else:
                        print('该用户没有持有该服务器的权限或该服务器不存在\n')
        elif selection=='A':
            print('\n',end='')
            while True:
                print('该用户可访问的服务器有：') 
                server_info_tuple=server_search(base,str(user_id))
                print('您持有的访问权限有：')
                add_authority=server_search(changer_base,str(changer_id))[0]
                print('请输入目标服务器的名称以添加对应权限，或输入Q以返回\n')
                select=input()
                print('\n',end='')
                if select=='Q':
                    break
                else:
                    if select in add_authority and select not in server_info_tuple[0]:
                        (db,cursor)=database_connecter(base) 
                        locate=server_locate_changer(base,select)
                        try:
                            cursor.execute("insert into ssh_server (user_id,server_name,server_target) values("+(user_id)+",\'"+select+"\',\'"+locate+"\')")
                            db.commit()
                            print('添加成功！\n')
                        except:
                            db.rollback()
                            print('出现错误！\n')
                        database_disconnecter(db,cursor)
                        history_writter(changer_base,changer_id,'为id为'+str(user_id)+'的'+str(base)+'用户添加服务器名为'+str(select)+'的访问权限')
                    else:
                        print('该用户已持有该服务器的权限或该服务器不存在又或是您不存在添加此服务器的权利\n')
        else:
            print('\n',end='')
            print('请输入A/D/Q中的其中一个！\n')
            continue
                
                    
def id_creator(base,tablename):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from '+tablename)
    data=cursor.fetchall()
    length=len(data)
    database_disconnecter(db,cursor)
    return str(length+1)


def name_id_changer(base,inner):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from translate')
    all_list=cursor.fetchall()
    database_disconnecter(db,cursor)
    user_name_list=[tuples[1] for tuples in all_list]
    user_id_list=[tuples[0] for tuples in all_list]
    if inner in user_name_list:
        location=user_name_list.index(inner)
        return str(user_id_list[location])
    elif inner in user_id_list:
        name=user_id_list.index(inner)
        return str(user_name_list[name])


def database_connecter(base):
    db=pymysql.connect(host='localhost',database=base,user='root',password='1029384756lxt')
    cursor=db.cursor()
    db.autocommit = False#关闭自动提交功能
    return (db,cursor)
    

def database_disconnecter(database,cursor):
    cursor.close()
    database.close()
    return 0


def server_search(base,user_id):#base=root/guest
    if base=='super_root':
        (db,cursor)=database_connecter(base)
        cursor.execute('select * from server_list')
        data=cursor.fetchall()
        print('\n',end='')
        for tuples in data:
            print(str(tuples[0])+"."+tuples[1]+"："+tuples[2]+'\n')
        database_disconnecter(db,cursor)
        history_writter(base,user_id,'查询可ssh的服务器')
        return ([tuples[1] for tuples in data],[tuples[2] for tuples in data])
    else:
        (db,cursor)=database_connecter(base)
        cursor.execute('select * from ssh_server where user_id='+user_id)
        data=cursor.fetchall()
        if len(data)==0:
            print('不存在可以访问的服务器\n')
        else:
            num=0
            print('\n',end='')
            for tuples in data:
                num=num+1
                print(str(num)+"."+tuples[2]+'\n')
        database_disconnecter(db,cursor)
        history_writter(base,user_id,'查询可ssh的服务器')
        return ([target[2] for target in data],[target[3] for target in data])


def user_help_root():
    print('\n',end='')
    print('C——更改密码\n\nQC——查询自己可以使用的命令\n')
    print('QS——查询自己可以访问的服务器\n\nB——返回至登陆界面\n')
    print('S——SSH指定的服务器\n\nCL——更改guest用户的权限/ssh权限\n')
    print('命令可直接输入\n')


def user_help_super_root():
    print('\n',end='')
    print('C——更改密码\n\nE——退出程序进入命令行\n')
    print('QS——查询自己可以访问的服务器\n\nB——返回至登陆界面\n')
    print('CL——更改guest/root用户的权限/ssh权限\n')
    print('U——创建root用户\n')
    print('命令可直接输入\n')


def user_help_guest():
    print('\n',end='')
    print('C——更改密码\n\nQC——查询自己可以使用的命令\n')
    print('QS——查询自己可以访问的服务器\n\nB——返回至登陆界面\n')
    print('S——SSH指定的服务器\n')
    print('命令可直接输入\n')


def time_getter():#记得做,且转换为str
    time=datetime.datetime.now()
    time=str(time)
    return time


def history_writter(base,user_id,inner):
    time=time_getter()
    try:
        (db,cursor)=database_connecter(base)
        cursor.execute("insert into history (user_id,time,content) values("+user_id+",\'"+time+"\',\'"+inner+"\')")
        db.commit()
    except:
        db.rollback()
        print('出现了未知的错误，请联系管理员\n')
    database_disconnecter(db,cursor)
    

def command_search(base,user_id):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from command where user_id='+user_id)
    data=cursor.fetchall()
    print('\n',end='')
    if len(data)==0:
        print('仅能在指定界面使用提供的ssh\n')
    else:
        for tuples in data:
            output=tuples[3]
            if tuples[3]=='0':
                output='可使用该参数的全部功能'
            print(str(tuples[0])+"."+tuples[2]+'：'+output+'\n')
    database_disconnecter(db,cursor)
    history_writter(base,user_id,'查询可使用的命令') 
    return ([a[2] for a in data],[a[3] for a in data])


def password_change(base,user_id):
    history_writter(base,user_id,'进入密码更改界面')
    print('\n',end='')
    while True:
        print('请输入旧密码或输入Q以返回用户界面\n')
        first_input=getpass.getpass('输入：')
        print('\n',end='')
        if first_input=='Q':
            history_writter(base,user_id,'离开密码更改界面')
            return 0
        else:
            former_password=password_obtain(base,user_id)
            if former_password != first_input:
                print('密码错误，请重新输入\n')
                history_writter(base,user_id,'更改用户密码时旧密码输入错误')
                continue
            else:
                while True:
                    print("请输入新密码\n")
                    newest_password = getpass.getpass('输入：')
                    print('\n',end='')
                    if len(newest_password)<6 or len(newest_password)>19:
                        print("请输入6-19位密码\n")
                        continue
                    print("请再输入一次密码以确保正确\n")
                    verify = getpass.getpass('输入：')
                    print('\n',end='')
                    (db,cursor)=database_connecter(base)
                    if verify == newest_password:
                        try:
                            cursor.execute("update info set password = \'"+str(newest_password)+"\' where id ="+str(user_id))
                            db.commit()
                        except:
                            db.rollback()
                            print('出现了未知的错误，请联系管理员\n')
                            continue
                        database_disconnecter(db,cursor)
                        print('修改成功！\n')
                        return 0
                    else:
                        print('前后密码不同，请重新输入，或键入Q以返回用户界面\n')
                        select=input()
                        if select=='Q':
                            history_writter(base,user_id,'离开密码更改界面\n')
                            print('\n',end='')
                            return 0
                        else:
                            continue

   
def User_Add_System(base):
    print('\n',end='')
    while True:
        print("输入新用户名(6-12位)，或输入Q以退出\n")
        newest_username = input()
        if len(newest_username)>5 and len(newest_username)<13:            
            print('\n',end='')
            user_list=user_list_obtain(base)
            if newest_username in user_list:
                print('该用户已存在\n')
                continue
            else:       
                print("输入密码\n")
                newest_password = getpass.getpass('输入：')
                print('\n',end='')
                if len(newest_password)<6 or len(newest_password)>19:
                    print("请输入6-19位密码\n")
                    continue
                print("请再输入一次密码以确保正确\n")
                verify = getpass.getpass('输入：')
                print('\n',end='')
                if verify == newest_password:
                    try:
                        (db,cursor)=database_connecter(base)
                        cursor.execute("insert into info (password) values(\'"+str(newest_password)+"\')")
                        cursor.execute("insert into ssh_server (user_id,server_name,server_target) values("+str(len(user_list)+1)+",\'server_1\',\'root@172.18.0.3\')")
                        cursor.execute("insert into translate (user_name) values(\'"+str(newest_username)+"\')")
                        if base=='root':
                            cursor.execute("insert into command (user_id,command_start,command_last) values("+str(len(user_list)+1)+",\'ls\',\'0\')")
                        db.commit()
                    except:
                        db.rollback()
                        print('出现了未知的错误，请联系管理员\n')
                        continue
                    database_disconnecter(db,cursor)
                    print('User Created')
                    return 0
                else:
                    print('前后密码不一致，请再试一次！\n')
                    continue
        elif newest_username.upper()=='Q':
            return 0
        else:
            continue
 

def user_list_obtain(base):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from translate')
    data=cursor.fetchall()
    user_list=[user[1] for user in data]
    database_disconnecter(db,cursor)
    return user_list


def password_obtain(base,user_id):
    (db,cursor)=database_connecter(base)
    cursor.execute('select * from info where id='+user_id)
    data=cursor.fetchone()
    former_password=data[1]
    database_disconnecter(db,cursor)
    return former_password


def ssh_connect(base,user_id):
    print('\n',end='')
    print('您可以连接的服务器有：')
    ssh_list=server_search(base,user_id)
    print("输入Q以返回或输入提供的ssh目标名称以进行ssh连接\n")
    while True:       
        target=input()
        print('\n',end='')
        if target=='Q':
            return 0
        else:
            if target in ssh_list[0]:
                locate=server_locate_changer(base,target)
                os.system('ssh '+locate)
                print('\n',end='')
                return 0
            else:
                print('请输入正确的服务器地址\n')
                continue


def LoginSystem(base):
    while True:
        print('\n',end='')
        print("欢迎来到跳板机系统\n")
        if base=='guest':
            print("输入I以进入登陆系统，输入C以创建新用户，或输入Q以返回\n")
        elif base=='root' or base=='super_root':
            print("输入I以进入登陆系统，或输入Q以返回\n")
        else:
            print('程序出现意料之外的错误，请上报管理员\n')
            return 0
        select=input()
        if select.upper()=="I":
            while True:
                print('\n',end='')
                print("请输入您的用户名,或输入Q以退出\n")
                username = input()
                print('\n',end='')
                user_list=user_list_obtain(base)
                if username.upper()=='Q':
                    return 0
                elif username not in user_list and base=='guest':
                    print('请输入密码\n')
                    password = getpass.getpass('输入：')
                    print('密码错误，请重新输入')
                    continue
                elif username in user_list:
                    print('请输入密码\n')
                    password = getpass.getpass('输入：')
                    user_id=str(name_id_changer(base,username))
                    user_password=password_obtain(base,user_id)
                    if password != user_password:
                        print('\n',end='')
                        print('密码错误，请重新输入')
                        continue
                    else:
                        UserGate(base,user_id,username)
                        break
                else:
                    print('请输入密码\n')
                    password = getpass.getpass('输入：')
                    print('密码错误，请重新输入')
                    continue
            continue
        elif select.upper()=='C' and base=='guest':
            print('\n',end='')
            User_Add_System(base) 
            continue
        elif select.upper()=='Q':
            print('\n',end='')
            return 0
        else:
            print('\n',end='')
            if base=='guest':
                print('请输入\'I\'或\'C\'或\'Q\'的其中一个')
                continue
            else:
                print('请输入\'I\'或\'Q\'的其中一个')


def UserGate(base,user_id,userinput):
    print('\n',end='')
    print('欢迎您的登陆，' + userinput+'\n')
    history_writter(base,user_id,'用户登录')
    os.system('date')
    print('\n',end='')
    print('输入H以查看帮助\n')
    while True:
        print('$ ', end=' ')
        commandin = input()
        if commandin=='B':
            history_writter(base,user_id,'返回登陆界面')
            return 0
        elif commandin=='E' and base=='super_root':
            print('\n程序已终止！\n')
            sys.exit()
        elif commandin=='QC' and base!='super_root':
            command_search(base,user_id)
        elif commandin=='QS' :
            server_search(base,user_id)
        elif commandin=='C':
            password_change(base,user_id)
        elif commandin=='H':
            if base=='root':
                user_help_root()
            elif base=='guest':
                user_help_guest()
            elif base=='super_root':
                user_help_super_root()
            else:
                print('出现了意料之外的错误，请上报管理员\n')
        elif commandin=='U' and base=='super_root':
            User_Add_System('root')
        elif commandin=='S':
            ssh_connect(base,user_id)
        elif commandin=='CL' and base!='guest':
            while True:
                print('\n',end='')
                u_choice='guest'
                if base=='super_root':
                    print('请输入目标组:guest/root或输入Q以退出\n')
                    t_choice=input()
                    print('\n',end='')
                    if t_choice=='Q':
                        break
                    elif t_choice!='guest' and t_choice!='root' and t_choice!='Q':
                        print('请输入正确的选项！')
                        continue
                    else:
                        u_choice=t_choice
                try:
                    print('\n',end='')
                    print('请输入目标用户id或输入Q以退出或输入S以查看当前选择组用户表单\n')
                    sel=input()
                    print('\n',end='')
                    if sel=='Q':
                        break
                    elif sel=='S':
                        (db,cursor)=database_connecter(u_choice)
                        cursor.execute('select * from translate')
                        data=cursor.fetchall()
                        if len(data)==0:
                            print('该组下不存在用户')
                        else:
                            for user in data:
                                print('id：'+str(user[1])+'——'+str(user[0]))
                        database_disconnecter(db,cursor)
                        continue
                    elif int(sel) < int(id_creator(u_choice,'translate')):
                        limmit_changer(base,u_choice,user_id,sel)
                        continue
                    else:
                        print('请输入符合条件的词句')
                        continue
                except:
                    print('请输入符合条件的词句')
        else:
            print('\n',end='')
            history_writter(base,user_id,str(commandin))
            result = command_exec(commandin, user_id,base)
            if result=='exit!!!':
                print('该命令不支持，请手动退出ssh\n')
                history_writter(base,user_id,'执行失败')
            elif result=='该界面不支持ssh指令':
                print('请使用前面提供的方法连接服务器\n')
                history_writter(base,user_id,'执行失败')
            else:
                print('\n',end='')
                history_writter(base,user_id,'执行成功')


def command_exec(command, user_id,base):
    if base=='super_root':
        out=(os.popen(command).readlines())
        print(str(out))
        return str(out)
    else:
        command_list = command.split(' ')
        content_verify=0
        for content in command_list:#通过验证确保命令尾端验证可以正确进行
            if content=='':
                content_verify=content_verify+1
            else:
                continue
        if content_verify!=0:
            print('请不要输入多余的空格')
            return '请不要输入多余的空格'
        (db,cursor)=database_connecter(base)
        cursor.execute('select * from command where user_id = '+user_id)
        data=cursor.fetchall()
        comm_list=[com[2] for com in data]
        database_disconnecter(db,cursor)
        while True:
            if command_list[0] == 'exit':
                return 'exit!!!'
            elif command_list[0] == 'ssh':
                return '该界面不支持ssh指令'
            elif command_list[0] in comm_list:
                (db,cursor)=database_connecter(base)
                cursor.execute('select * from command where user_id= '+user_id+' and command_start= \''+command_list[0]+"\'")
                data=cursor.fetchone()
                com_property=data[3]#参数字典
                try:
                    if str(com_property)=='0':
                        out=(os.popen(command).read())
                        print(str(out))
                        return str(out)
                    else:
                        database_disconnecter(db,cursor)
                        right=0
                        for settles in eval(com_property).items():
                            if -(int(settles[1]))<len(command_list):
                                right=right+1
                                continue
                            elif command_list[int(settles[1])]==settles[0]:#格式为("root@172.18.0.3",'-1')
                                right=right+1
                                continue
                            else:
                                break
                        if right==len(eval(com_property)):
                            out=(os.popen(command).readlines())
                            print(str(out))
                            return str(out)
                        else:
                            print('您没有执行该命令的权限！')
                            return '超出权限'
                except:
                    print('参数设定出现问题，请联系管理员')
                    return '参数设定出现问题导致无法正常运行'
            else:
                print('您没有执行该命令的权限！')
                return '超出权限'
signal.signal(signal.SIGINT,signal_handler)
signal.signal(signal.SIGTERM,signal_handler)
signal.signal(signal.SIGTSTP,signal_handler)#防ctrl+z
user_selector()


