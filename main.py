from tkinter import *
from tkinter import messagebox as ms
import pymysql as sql
from PIL import Image , ImageTk
def login():
    l_u = user_name_login.get()
    l_p = password_login.get()
    x  =(l_u , l_p)
    main_cursor.execute("SELECT * FROM malt.users where username =  %s and password = %s;",x)
    info = main_cursor.fetchone()
    temp = is_empty(info)
    if temp == False:
        ms.showinfo('Welcome' , f'Welcome {info[3]}')
        user_name_login.delete(0,END)
        password_login.delete(0,END)
    else:
        ms.showerror('Error' , 'User does not exists')

def move_to_register_window():
    root.withdraw()
    register_window.deiconify()
    user_name_login.delete(0,END)
    password_login.delete(0,END)

def is_empty(myinput):
    if myinput:
        return False
        # is not empty
    else:
        return True
        # empty

def register():
    name = name_register.get()
    lastname = lastname_register.get()
    password = password_register.get()
    re_password = re_password_register.get()
    username = user_name_register.get()
    if name == '':
        ms.showerror("Error","Please enter your name")
    else:
        if lastname == '':
            ms.showerror("Error","Please enter your lastname")
        else:        
            if username == '':
                ms.showerror("Error","Please choose a username")
            else:
                main_cursor.execute("SELECT username FROM malt.users where username = %s;", username)
                temp_data = main_cursor.fetchone()
                temp = is_empty(temp_data)
                if temp == False:
                    ms.showerror("Error", "Username has been taken")
                else:
                    if password == '':
                        ms.showerror('Error','Please choose a password')
                    else:
                        if password == re_password:
                            if len(password) >= 4:
                                name = name.lower()
                                lastname = lastname.lower()
                                a = (username,password ,name,lastname)
                                main_cursor.execute("INSERT INTO `malt`.`users` (`username`, `password`, `name`, `lastname`) VALUES (%s, %s, %s, %s);",a)
                                main_database.commit()
                                ms.showinfo("Registered Successfully", "You are registered ruccessfully")
                                user_name_register.delete(0,END)
                                password_register.delete(0,END)
                                re_password_register.delete(0,END)
                                register_window.withdraw()
                                root.deiconify()
                                btn_register['state'] = 'disabled'
                            else:
                                ms.showerror("Error", "Your password should be at least 4 characters")
                        else:
                            ms.showerror("Error", "Password does not match")

# <<commends>>
create_database = "CREATE DATABASE IF NOT EXISTS malt;"
create_table = "CREATE TABLE IF NOT EXISTS `malt`.`users` (`id`INT NOT NULL AUTO_INCREMENT,`username` VARCHAR(25) NOT NULL,`password` VARCHAR(25) NOT NULL,`name` VARCHAR(30) NOT NULL,`lastname` VARCHAR(30) NOT NULL,PRIMARY KEY (`id`),UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);"

# sql
try:
    main_database = sql.connect(host='localhost' , user='root',password='root')
    main_cursor = main_database.cursor()
    main_cursor.execute(create_database)
    main_cursor.execute(create_table)
except:
    ms.showerror("Error", "Connection not established")

# config
myconfig = {'font':('Abril Fatface',12,'bold'),'bg':'#D2302C', 'fg':'#F7F7F9'}
myconfig_btn =  {'font':('Abril Fatface',12,'bold')
                ,'bg':'#F7F7F9', 'fg':'#D2302C'
                ,'activebackground':'#F7F7F9'
                ,'activeforeground':'#D2302C' ,'border':0.7}

# root
root = Tk()
root.geometry('400x400+300+100')
root.configure(bg='#D2302C')
root.title("Malt Bank")
root.resizable(0,0)

# toplevel
register_window = Toplevel(root)
register_window.geometry('400x400+300+100')
register_window.configure(bg='#D2302C')
register_window.title("Malt Bank")
register_window.resizable(0,0)
register_window.withdraw()

# image
logo = ImageTk.PhotoImage(Image.open("logo.png").resize((250,100), Image.ANTIALIAS))

# entry
user_name_login = Entry(root, width=25,fg='#D2302C')
password_login = Entry(root,show='*', width=25,fg='#D2302C')

# label
Label(root,image=logo,border=0).place(relx = 0.5, rely = 0.2, anchor = CENTER)
Label(root,text='Username:',cnf=myconfig).place(relx = 0.19, rely = 0.4, anchor = CENTER)
Label(root,text='Password:',cnf=myconfig).place(relx = 0.19, rely = 0.48, anchor = CENTER)

# button
btn_login = Button(root,text='Login',width=10,cnf=myconfig_btn,command=login)
btn_register = Button(root,text='Register',width=10,cnf=myconfig_btn,command=move_to_register_window)
btn_exit = Button(root,text='Exit',width=10,cnf=myconfig_btn,command=root.destroy)

# place
user_name_login.place(relx = 0.5, rely = 0.4, anchor = CENTER)
password_login.place(relx = 0.5, rely = 0.48, anchor = CENTER)
btn_login.place(relx = 0.5, rely = 0.6, anchor = CENTER)
btn_register.place(relx = 0.5, rely = 0.7, anchor = CENTER)
btn_exit.place(relx = 0.5, rely = 0.8, anchor = CENTER)

# entry_register_window
user_name_register = Entry(register_window, width=25,fg='#D2302C')
password_register = Entry(register_window, width=25,fg='#D2302C')
re_password_register = Entry(register_window, width=25,fg='#D2302C')
name_register = Entry(register_window, width=25,fg='#D2302C')
lastname_register = Entry(register_window, width=25,fg='#D2302C')

# label_register_window
Label(register_window,image=logo,border=0).place(relx = 0.5, rely = 0.2, anchor = CENTER)
Label(register_window,text='Name:',cnf=myconfig).place(relx = 0.23, rely = 0.38, anchor = CENTER)
Label(register_window,text='Lastname:',cnf=myconfig).place(relx = 0.19, rely = 0.46, anchor = CENTER)
Label(register_window,text='Username:',cnf=myconfig).place(relx = 0.19, rely = 0.54, anchor = CENTER)
Label(register_window,text='Password:',cnf=myconfig).place(relx = 0.19, rely = 0.62, anchor = CENTER)
Label(register_window,text='Rep-Password:',cnf=myconfig).place(relx = 0.15, rely = 0.7, anchor = CENTER)

# button_register_window
btn_register_window2 = Button(register_window,text='Register',width=10,cnf=myconfig_btn,command=register)
btn_exit_winsow2 = Button(register_window,text='Exit',width=10,cnf=myconfig_btn,command=root.destroy)

# place_register_window
name_register.place(relx = 0.5, rely = 0.38, anchor = CENTER)
lastname_register.place(relx = 0.5, rely = 0.46, anchor = CENTER)
user_name_register.place(relx = 0.5, rely = 0.54, anchor = CENTER)
password_register.place(relx = 0.5, rely = 0.62, anchor = CENTER)
re_password_register.place(relx = 0.5, rely = 0.7, anchor = CENTER)
btn_register_window2.place(relx = 0.5, rely = 0.8, anchor = CENTER)
btn_exit_winsow2.place(relx = 0.5, rely = 0.9, anchor = CENTER)
mainloop()
