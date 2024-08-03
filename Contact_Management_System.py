from tkinter import *
from PIL import Image,ImageTk
import mysql.connector
import tkinter.messagebox as tmsg
from tabulate import tabulate

# Function to add a new contact to the database
def add_contact():
    first_name=first_name_value.get()
    last_name=last_name_value.get()
    day=day_value.get()
    month=month_value.get()
    year=year_value.get()
    phone_number=phone_number_value.get()
    email_id=email_id_value.get()
    gender=gender_value.get()
    
    # Check if all fields are filled
    if not all([first_name,last_name,day,month,year,phone_number,email_id,gender]) or day=="Date" or month=="Month" or year=="Year":
        tmsg.showerror("Input Error","All Fields Are Required !!")
        return
    
    dob=f"{year}-{month}-{day}"
    
    try:
        # Insert new contact into the database
        cursor.execute("""INSERT INTO contacts(FirstName,LastName,DOB,PhoneNumber,EmailID,Gender) VALUES(%s,%s,%s,%s,%s,%s)""",(first_name,last_name,dob,phone_number,email_id,gender))
        db.commit()
        tmsg.showinfo("Success","Contact Added Successfully !!")
        clear_entries()
    except mysql.connector.IntegrityError as e:
        tmsg.showerror("Database Error",f"Phone Number Already Exists !!")
    except Exception as e:
        tmsg.showerror("Database Error",f"Error Adding Contact To Database :- {e}")

# Function to delete a contact from the database
def delete_contact():
    phone_number=phone_number_value.get()
    if not phone_number:
        tmsg.showerror("Input Error","Phone Number Is Required To Delete The Contact !!")
    try:
         # Delete contact from the database
        cursor.execute("DELETE FROM contacts WHERE PhoneNumber=%s",(phone_number,))
        if cursor.rowcount==0:
            tmsg.showwarning("No Record Found","No Record Found With The Provided Number !!")
        else:
            db.commit()
            tmsg.showinfo("Success","Contact Deleted Successfully !!")
            clear_entries()
    except Exception as e:
        tmsg.showerror("Database Error",f"Error Deleting Contact From Database :- {e}")

# Function to extract contact details from the database
def extract_contact():
    phone_number=phone_number_value.get()
    if not phone_number:
        tmsg.showerror("Input Error","Phone Number Is Required To Extract The Contact !!")
        return
    try:
        # Fetch contact details from the database
        cursor.execute("SELECT * FROM contacts WHERE PhoneNumber=%s",(phone_number,))
        contact=cursor.fetchone()
        if contact:
            first_name_value.set(contact[0])
            last_name_value.set(contact[1])
            dob=contact[2].strftime("%Y-%m-%d").split("-")
            year_value.set(dob[0])
            month_value.set(dob[1])
            day_value.set(dob[2])
            email_id_value.set(contact[4])
            gender_value.set(contact[5])
        else:
            tmsg.showwarning("No Record Found","No Record Found With The Provided Number !!")
            clear_entries()
    except Exception as e:
        tmsg.showerror("Database Error",f"Error Extracting Contact From Database :- {e}")

# Function to update contact details in the database
def update_contact():
    first_name=first_name_value.get()
    last_name=last_name_value.get()
    day=day_value.get()
    month=month_value.get()
    year=year_value.get()
    phone_number=phone_number_value.get()
    email_id=email_id_value.get()
    gender=gender_value.get()

    # Check if all fields are filled
    if not all([first_name,last_name,day,month,year,phone_number,email_id,gender]) or day=="Date" or month=="Month" or year=="Year":
        tmsg.showerror("Input Error","All Fields Are Required !!")
        return
    
    dob=f"{year}-{month}-{day}"
    try:
        # Fetch current contact details from the database
        cursor.execute("SELECT * FROM contacts WHERE PhoneNumber=%s",(phone_number,))
        current_contact=cursor.fetchone()
        if current_contact:
            if(first_name!=current_contact[0] or last_name!=current_contact[1] or dob!=current_contact[2].strftime("%Y-%m-%d") or email_id!=current_contact[4] or gender!=current_contact[5]):
                # Update contact details in the database
                cursor.execute("UPDATE contacts SET FirstName=%s, LastName=%s,DOB=%s,EmailID=%s,Gender=%s WHERE PhoneNumber=%s",(first_name,last_name,dob,email_id,gender,phone_number))
                db.commit()

                if cursor.rowcount==0:
                    tmsg.showwarning("No Record Found","No Record Found With The Provided Number !!")
                else:
                    tmsg.showinfo("Success","Contact Updated Successfully !!")
                    clear_entries()
            else:
                tmsg.showinfo("No Changes","No Changes Detected In The Contact Details !!")
        else:
            tmsg.showinfo("No Record Found","No Record Found With The Provided Number !!")
    except mysql.connector.IntegrityError as e:
        tmsg.showerror("Database Error","Phone Number Or Email ID Already Exists !!")
    except Exception as e:
        tmsg.showerror("Database Erro",f"Error Updating Contact In Database :- {e}")

# Function to display all contacts
def display_contacts():
    contact_box.config(state=NORMAL)
    contact_box.delete(1.0,END)
    try:
        # Fetch all contacts from the database
        cursor.execute("SELECT * From contacts")
        rows=cursor.fetchall()
        headers=["First Name","Last Name","Date Of Birth","Phone Number","Email ID","Gender"]
        table=tabulate(rows,headers=headers,tablefmt="grid")
        contact_box.insert(END,table)
    except Exception as e:
        tmsg.showerror("Database Error",f"Error Fetching Contacts :- {e}")
    contact_box.config(state=DISABLED)

# Function to clear all input fields
def clear_entries():
    first_name_value.set("")
    last_name_value.set("")
    day_value.set("Date")
    month_value.set("Month")
    year_value.set("Year")
    email_id_value.set("")
    phone_number_value.set("")
    gender_value.set(NONE)

# Function to show a specific frame
def show_frame(frame):
    frame.tkraise()

# Function to go back to the main menu
def go_back():
    show_frame(main_frame)

root=Tk()

root.title("Contact Management System")
root.wm_iconbitmap("phone-book.ico")

# Center the window on the screen
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
window_width=500
window_height=750
center_x=int(screen_width/2-window_width/2)
center_y=int(screen_height/2-window_height/2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False,False)

# Connect to the MySQL database
try:
    # Enter Your Username And Password Of MySQL Database
    db = mysql.connector.connect(host="localhost", user="", password="", database="contact_management_system")
    cursor = db.cursor()
    tmsg.showinfo("Success", "Database Connected Successfully!")

    # Create contacts table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            FirstName VARCHAR(50) NOT NULL,
            LastName VARCHAR(50) NOT NULL,
            DOB DATE NOT NULL,
            PhoneNumber VARCHAR(15) PRIMARY KEY NOT NULL UNIQUE,
            EmailID VARCHAR(100) NOT NULL UNIQUE,
            Gender VARCHAR(15) NOT NULL
        )
    """)
    db.commit()
except Exception as e:
    tmsg.showerror("Database Error", f"Error Connecting To Database: {e}")

# Load button images
delete_button=Image.open("delete_button.png")
delete_button=delete_button.resize((40,40),Image.LANCZOS)
delete_button=ImageTk.PhotoImage(delete_button)

back_button=Image.open("back_button.png")
back_button=back_button.resize((40,40),Image.LANCZOS)
back_button=ImageTk.PhotoImage(back_button)

# Create frames for different sections
main_frame=Frame(root)
add_frame=Frame(root)
delete_frame=Frame(root)
update_frame=Frame(root)
contact_frame=Frame(root)

for frame in (main_frame,add_frame,delete_frame,update_frame,contact_frame):
    frame.grid(row=0,column=0,sticky="nsew")

# Main menu
Label(main_frame,text="Contact Management System",font="helvetica 26 bold").pack(pady=20)
Button(main_frame,text="Add Contacts",command=lambda:show_frame(add_frame),width=20,font="helvetica 15 bold").pack(pady=10)
Button(main_frame,text="Delete Contacts",command=lambda:show_frame(delete_frame),width=20,font="helvetica 15 bold").pack(pady=10)
Button(main_frame,text="Update Contacts",command=lambda:show_frame(update_frame),width=20,font="helvetica 15 bold").pack(pady=10)
Button(main_frame,text="Display Contacts",command=lambda:[show_frame(contact_frame),display_contacts()],width=20,font="helvetica 15 bold").pack(pady=10)

first_name_value = StringVar()
last_name_value = StringVar()
day_value = StringVar()
month_value = StringVar()
year_value = StringVar()
email_id_value = StringVar()
phone_number_value = StringVar()
gender_value = StringVar()
gender_value.set(None)

# Add contact form
Label(add_frame,text="Add Contacts",font="helvetica 26 bold").grid(row=0,column=1,pady=20)
Button(add_frame,image=back_button,command=go_back).grid(row=1,column=0,pady=20)

first_name = Label(add_frame, text="First Name :- ")
first_name.grid(row=2, column=0, sticky="w", pady=10)
last_name = Label(add_frame, text="Last Name :- ")
last_name.grid(row=3, column=0, sticky="w", pady=10)
dob = Label(add_frame, text="Date Of Birth :- ")
dob.grid(row=4, column=0, sticky="w", pady=10)
email_id = Label(add_frame, text="Email-ID :- ")
email_id.grid(row=5, column=0, sticky="w", pady=10)
phone_number = Label(add_frame, text="Phone Number :- ")
phone_number.grid(row=6, column=0, sticky="w", pady=10)
gender = Label(add_frame, text="Gender :- ")
gender.grid(row=7, column=0, sticky="w", pady=10)

first_name_entry = Entry(add_frame, textvariable=first_name_value, width=40)
first_name_entry.grid(row=2, column=1, sticky="w")
last_name_entry = Entry(add_frame, textvariable=last_name_value, width=40)
last_name_entry.grid(row=3, column=1, sticky="w")
email_id_entry = Entry(add_frame, textvariable=email_id_value, width=40)
email_id_entry.grid(row=5, column=1, sticky="w")
phone_number_entry = Entry(add_frame, textvariable=phone_number_value, width=40)
phone_number_entry.grid(row=6, column=1, sticky="w")

days = list(range(1, 32))
months = list(range(1, 13))
years = list(range(1950, 2024))

day_value.set("Date")
month_value.set("Month")
year_value.set("Year")

dob_frame = Frame(add_frame)
dob_frame.grid(row=4, column=1, sticky="w")

day_menu = OptionMenu(dob_frame, day_value, *days)
day_menu.grid(row=0, column=0, sticky="w")

month_menu = OptionMenu(dob_frame, month_value, *months)
month_menu.grid(row=0, column=1, sticky="w")

year_menu = OptionMenu(dob_frame, year_value, *years)
year_menu.grid(row=0, column=2, sticky="w")

Radiobutton(add_frame, text="Male", variable=gender_value, value="Male").grid(row=7, column=1, sticky="w")
Radiobutton(add_frame, text="Female", variable=gender_value, value="Female").grid(row=8, column=1, sticky="w")
Radiobutton(add_frame, text="Other", variable=gender_value, value="Other").grid(row=9, column=1, sticky="w")
Button(add_frame,text="Add Contact",command=add_contact).grid(row=11,column=1,pady=20)

# Delete contact form
Label(delete_frame,text="Delete Contacts",font="helvetica 26 bold").grid(row=0,column=1,pady=20)
Button(delete_frame,image=back_button,command=go_back).grid(row=1,column=0,pady=20)

phone_number=Label(delete_frame,text="Phone Number :- ")
phone_number.grid(row=2,column=0,sticky="w",pady=10)

phone_number_entry = Entry(delete_frame, textvariable=phone_number_value, width=40)
phone_number_entry.grid(row=2, column=1, sticky="w")

Button(delete_frame,image=delete_button,command=delete_contact).grid(row=3,column=1,pady=20)

# Update contact form
Label(update_frame,text="Update Contacts",font="helvetica 26 bold").grid(row=0,column=1,pady=20)
Button(update_frame,image=back_button,command=go_back).grid(row=1,column=0,pady=20)

phone_number=Label(update_frame,text="Phone Number :- ")
phone_number.grid(row=2,column=0,sticky="w",pady=10)

phone_number_entry=Entry(update_frame,textvariable=phone_number_value,width=40)
phone_number_entry.grid(row=2,column=1,sticky="w")

Button(update_frame,text="Extract",command=extract_contact).grid(row=3,column=1,pady=20)

first_name = Label(update_frame, text="First Name :- ")
first_name.grid(row=4, column=0, sticky="w", pady=20)
last_name = Label(update_frame, text="Last Name :- ")
last_name.grid(row=5, column=0, sticky="w", pady=10)
dob = Label(update_frame, text="Date Of Birth :- ")
dob.grid(row=6, column=0, sticky="w", pady=10)
email_id = Label(update_frame, text="Email-ID :- ")
email_id.grid(row=7, column=0, sticky="w", pady=10)
gender = Label(update_frame, text="Gender :- ")
gender.grid(row=8, column=0, sticky="w", pady=10)

first_name_entry = Entry(update_frame, textvariable=first_name_value, width=40)
first_name_entry.grid(row=4, column=1, sticky="w")
last_name_entry = Entry(update_frame, textvariable=last_name_value, width=40)
last_name_entry.grid(row=5, column=1, sticky="w")
email_id_entry = Entry(update_frame, textvariable=email_id_value, width=40)
email_id_entry.grid(row=7, column=1, sticky="w")

days = list(range(1, 32))
months = list(range(1, 13))
years = list(range(1950, 2024))

day_value.set("Date")
month_value.set("Month")
year_value.set("Year")

dob_frame = Frame(update_frame)
dob_frame.grid(row=6, column=1, sticky="w")

day_menu = OptionMenu(dob_frame, day_value, *days)
day_menu.grid(row=0, column=0, sticky="w")

month_menu = OptionMenu(dob_frame, month_value, *months)
month_menu.grid(row=0, column=1, sticky="w")

year_menu = OptionMenu(dob_frame, year_value, *years)
year_menu.grid(row=0, column=2, sticky="w")

Radiobutton(update_frame, text="Male", variable=gender_value, value="Male").grid(row=8, column=1, sticky="w")
Radiobutton(update_frame, text="Female", variable=gender_value, value="Female").grid(row=9, column=1, sticky="w")
Radiobutton(update_frame, text="Other", variable=gender_value, value="Other").grid(row=10, column=1, sticky="w")
Button(update_frame,text="Update Contact",command=update_contact).grid(row=11,column=1,pady=20)

# Display contacts form
Label(contact_frame,text="Contact List",font="helvetica 26 bold").grid(row=0,column=1,pady=20)
Button(contact_frame,image=back_button,command=go_back).grid(row=1,column=0,pady=20)

contact_scroll_bar_x=Scrollbar(contact_frame,orient=HORIZONTAL)
contact_scroll_bar_x.grid(row=3,column=1,sticky="ew")

contact_scroll_bar_y=Scrollbar(contact_frame,orient=VERTICAL)
contact_scroll_bar_y.grid(row=2,column=2,sticky="ns")

contact_box=Text(contact_frame,height=30,width=50,wrap=NONE,xscrollcommand=contact_scroll_bar_x.set,yscrollcommand=contact_scroll_bar_y.set)
contact_box.grid(row=2,column=1,pady=10)
contact_scroll_bar_x.config(command=contact_box.xview)
contact_scroll_bar_y.config(command=contact_box.yview)

show_frame(main_frame)

root.mainloop()