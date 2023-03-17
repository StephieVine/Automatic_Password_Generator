import string
from tkinter import *
# from PIL import ImageTk, Image
from tkinter import messagebox
import string
import random
import sqlite3
import datetime
import pyperclip


windows = Tk()
windows.geometry('1500x1000+0+0')
windows.configure(bg='black')
windows.title("Automatic Password Generator")

currentDateTime = datetime.datetime.now()



#Validation entries
def generate():
    if usernamefield.get() == '':
        messagebox.showerror('', 'Name Cannot be Empty')
        return

    else:

        Lowercase = string.ascii_lowercase #this will return all lowercase characters
        uppercase = string.ascii_uppercase #this will return all uppercase characters
        numbers = string.digits #this will return all digits
        characters = string.punctuation #this will return all punctuation characters
        shuffle = Lowercase+uppercase+numbers+characters
        # print(shuffle)

        #for generating the given length
        passwordlength=int(length_box.get()) #this would help to collect whatever the user choses as the length and
        # stores it in the passwordlength variable

        if not option.get(): #this is to ensure that your option is not null
            messagebox.showerror('!', 'Choose an option')
            return

        elif option == 1:
            passwordfield.insert(0, random.sample(Lowercase, passwordlength))

        elif option == 2:
            passwordfield.insert(0, random.sample(Lowercase+uppercase+numbers, passwordlength))

        elif option == 3:
            passwordfield.insert(0, random.sample(shuffle, passwordlength))

        #this line of code is for generating password randomly
        password=random.sample(shuffle,passwordlength)
        passwordfield.insert(0, password)

        #connecting to the database
        con = sqlite3.connect("Automatic_password_gen.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur=con.cursor()

        con.execute("CREATE TABLE IF NOT EXISTS password_Generator_Table(Username TEXT NOT NULL, GeneratedPassword TEXT "
                    "NOT NULL, Time_stamp TIMESTAMP)")
        cur.execute("SELECT * FROM password_Generator_Table")
        # print("Table created succesfully")
        # con.commit()
        # con.close()
        selectn=("SELECT * FROM password_Generator_Table WHERE Username = ?")
        cur.execute(selectn, [(usernamefield.get())])
        if cur.fetchone():
            messagebox.showerror('!', 'This username already exist')
            usernamefield.delete(0, END)
            passwordfield.delete(0, END)
            length_box.delete(0)
            option.set(0)
        else:
            insert=str("INSERT INTO password_Generator_Table(Username, GeneratedPassword, Time_stamp) VALUES(?,?,?)")
            cur.execute(insert, (usernamefield.get(), passwordfield.get(), currentDateTime))
            messagebox.showinfo('Success', 'Password generated successfully')
            con.commit() #to make the changes
            con.close()

            msg=messagebox.askyesno("", 'Do you want to clear the fields?')
            if msg:
                option.set(0)
                passwordfield.delete(0, END)
                usernamefield.delete(0, END)
                length_box.delete(0)
                return

def copy():
    random_password=passwordfield.get()
    pyperclip.copy(random_password)
    messagebox.showinfo('', "Copied")

def reset():
    option.set(0)
    passwordfield.delete(0, END)
    usernamefield.delete(0, END)
    length_box.delete(0, END)



#THE END





Font = ('ariel', 16, 'bold')

headinglbl = Label(windows, text= 'Automatic Password Generator', font=('times new roman', 50, 'bold'), bg='black',
                   fg='springgreen2')
headinglbl.grid(pady=10, padx=200)

usernamelbl=Label(windows, text='Username:', font=Font, bg='black', fg='white')
usernamelbl.grid(pady=10)

usernamefield = Entry(windows, width=25, bd=2, font=Font)
usernamefield.grid(pady=10)

#Getting data from the entry fields and radio buttons
option = IntVar()
# option2 = IntVar()
# option3 = IntVar()

#radiobuttons
strength1= Radiobutton(windows, bg='cyan3', text='Weak Strength', value=1, variable=option, font=Font )
strength1.grid(pady=10)

strength2= Radiobutton(windows, bg='cyan3', text='Medium Strength', value=2, variable=option, font=Font )
strength2.grid(pady=10)

strength3= Radiobutton(windows, bg='cyan3', text='Strong Strength', value=3, variable=option, font=Font )
strength3.grid(pady=10)

passwordlenghtlbl= Label(windows, text='Password Length', font=Font, bg="black", fg='white')
passwordlenghtlbl.grid(pady=10)

length_box= Spinbox(windows, from_=6, to=20,  width=5, font=Font)
length_box.grid(pady=10)

generatebutton = Button(windows, text='Generate', font=Font, bg='springgreen2', cursor='hand2', command=generate)
generatebutton.grid(pady=10)

passwordfield = Entry(windows, width=25, bd=2, font=Font)
passwordfield.grid(pady=10)

copybutton = Button(windows, text='Copy', font=Font, bg='springgreen2', cursor='hand2', command=copy)
copybutton.grid(pady=5)

resetbutton = Button(windows, text='Reset', font=Font, bg='springgreen2', cursor='hand2', command=reset)
resetbutton.grid(pady=5)

usernameImage = PhotoImage(file='images (5).png')
usernameLabel= Label(windows, image=usernameImage)
usernameLabel.place(x=160, y=250)

usernameImage1 = PhotoImage(file='images (5).png')
usernameLabel1= Label(windows, image=usernameImage)
usernameLabel1.place(x=950, y=250)








windows.mainloop()
