from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
import time
import re


# ===============Input Validation===============

def validate_name(P):
    if P == "":         # Allow empty input
        return True
    if re.match("^[A-Za-z\s]{0,20}$", P) is not None:
        return True
    return False


def validate_contact(P):
    if re.match("^\d{0,10}$", P) is not None:
        return True
    return False


def validate_quantity(P):
    if re.match("^\d{0,3}$", P) is not None:
        return True
    return False


# ===============Menu Categories===============

menu_category = ["Tea & Coffee", "Beverages",
                 "Fast Food", "Starters", "Main Course", "Dessert"]

menu_category_dict = {"Tea & Coffee": "1 Tea & Coffee.txt", "Beverages": "2 Beverages.txt", "Fast Food": "3 Fast Food.txt",
                      "Starters": "4 Starters.txt", "Main Course": "5 Main Course.txt", "Dessert": "6 Dessert.txt"}

order_dict = {}
for i in menu_category:
    order_dict[i] = {}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ===============Loading Functions===============

def load_menu():
    menuCategory.set("")
    menu_tabel.delete(*menu_tabel.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file, "r")
        category = ""
        while True:
            line = f.readline()
            if line == "":
                menu_tabel.insert('', END, values=["", "", ""])
                break
            elif line == "\n":
                continue
            elif line[0] == '#':
                category = line[1:-1]
                name = "\t\t" + line[:-1]
                price = ""
            elif line[0] == '*':
                name = "\t" + line[:-1]
                price = ""
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ") + 1:-3]

            menu_tabel.insert('', END, values=[name, price, category])


def load_order():
    order_tabel.delete(*order_tabel.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for list in order_dict[category].values():
                order_tabel.insert('', END, values=list)
    update_total_price()


def load_item_from_menu(event):
    cursor_row = menu_tabel.focus()
    contents = menu_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")


def load_item_from_order(event):
    cursor_row = order_tabel.focus()
    contents = order_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])


# ===============Buttons===============

def show_button_operation():
    category = menuCategory.get()
    if category not in menu_category:
        tmsg.showinfo("Error", "Please select valid Choice")
    else:
        menu_tabel.delete(*menu_tabel.get_children())
        f = open("Menu\\" + menu_category_dict[category], "r")
        while True:
            line = f.readline()
            if line == "":
                break
            if line[0] == '#' or line == "\n":
                continue
            if line[0] == '*':
                name = "\t" + line[:-1]
                menu_tabel.insert('', END, values=[name, "", ""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ") + 1:-3]
                menu_tabel.insert('', END, values=[name, price, category])


def update_menu_button_operation():
    update_menu_prices()
    load_menu()


def add_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if name in order_dict[category].keys():
        tmsg.showinfo("Error", "Item already exist in your order")
        return
    list = [name, rate, quantity, str(int(rate) * int(quantity)), category]
    order_dict[category][name] = list
    load_order()


def remove_button_operation():
    name = itemName.get()
    category = itemCategory.get()

    if category == "":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    del order_dict[category][name]
    load_order()


def update_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get().lstrip('0')

    if category == "":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    if order_dict[category][name][2] == quantity:
        tmsg.showinfo("Error", "No changes in Quantity")
        return
    order_dict[category][name][2] = quantity
    order_dict[category][name][3] = str(int(rate) * int(quantity))
    load_order()


def clear_button_operation():
    itemName.set("")
    itemRate.set("")
    itemQuantity.set("")
    itemCategory.set("")


def bill_button_operation():
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names) == 0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    if customer_name == "" or customer_contact == "":
        tmsg.showinfo("Error", "Customer Details Required")
        return
    if len(customer_contact) < 10:
        tmsg.showinfo("Error", "Invalid contact number")
        return
    if not customerContact.get().isdigit():
        tmsg.showinfo("Error", "Invalid Customer Contact")
        return
    ans = tmsg.askquestion("Generate Bill", "Are You Sure to Generate Bill?")
    if ans == "yes":
        bill = Toplevel()
        bill.title("Bill")
        bill.geometry("670x500+300+100")
        bill_text_area = Text(bill, font=("arial", 12))
        st = "\t\t\t\tGarg's Cafe\n"
        st += "\t\t\t\tHaryana, India \n"
        st += "\t\t\tGST.NO:- XXXXXXXXXXXXXXXX\n"
        st += "-" * 61 + "BILL" + "-" * 61 + "\nDate:- "

        # Date, Time, Name, Contact and Description for Bill
        t = time.localtime(time.time())
        week_day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                         3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        st += " " * 10 + \
            f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

        st += f"\nCustomer Name:-    {customer_name}\nCustomer Contact:- {customer_contact}\n"
        st += "-" * 130 + "\n" + " " * 4 + \
            "DESCRIPTION\t\t\t\t\tRATE\tQUANTITY\t\tAMOUNT\n"
        st += "-" * 130 + "\n"

        # List of Items
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st += name + "\t\t\t\t\t" + rate + "\t      " + \
                    quantity + "\t\t  " + price + "\n\n"
        st += "-" * 130

        st += f"\n\t\t\tTotal price : {totalPrice.get()}\n"
        st += "-" * 130

        # display bill in a new window
        bill_text_area.insert(1.0, st)

        # Write into file
        folder = f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}"
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")
        file = open(
            f"Bill Records\\{folder}\\{customer_name + customer_contact}.txt", "w")

        st_2 = "\t\t\t\t\t\t\t\t\t\tGarg's Cafe\n"
        st_2 += "\t\t\t\t\t\t\t\t\t  Haryana, India \n"
        st_2 += "\t\t\t\t\t\t\t\t\tGST.NO:- XXXXXXXXXXXXXXXX\n"
        st_2 += "-" * 41 + "BILL" + "-" * 41 + "\nDate:- "

        # Date, Time, Name, Contact and Description for Bill
        t = time.localtime(time.time())
        week_day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                         3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        st_2 += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} \
            ({week_day_dict[t.tm_wday]})"
        st_2 += " " * 10 + \
            f"\t\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"
        st_2 += f"\nCustomer Name:-    {customer_name}\n\
            Customer Contact:- {customer_contact}\n"
        st_2 += "-" * 90 + "\n" + " " * 4 + "DESCRIPTION\t\t\t\t\t\t\t\
            RATE\tQUANTITY\t\tAMOUNT\n"
        st_2 += "-" * 90 + "\n"

        # List of Items
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st_2 += name + "\t\t\t\t\t\t\t" + rate + \
                    "\t      " + quantity + "\t\t  " + price + "\n\n"
        st_2 += "-" * 90

        st_2 += f"\n\t\t\t\t\tTotal price : {totalPrice.get()}\n"
        st_2 += "-" * 90

        file.write(st_2)
        file.close()

        # Clear operations
        order_tabel.delete(*order_tabel.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()
        customerName.set("")
        customerContact.set("")

        bill_text_area.pack(expand=True, fill=BOTH)
        bill.focus_set()
        bill.protocol("WM_DELETE_WINDOW", lambda: close_bill_window(bill))


def generate_pdf():
    customer_name = customerName.get()
    customer_contact = customerContact.get()

    if not customer_name or not customer_contact:
        tmsg.showinfo("Error", "Customer details are required.")
        return

    t = time.localtime(time.time())
    folder = f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}"
    week_day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                     3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

    pdf_file_path = f"Bill Records/{folder}/{customer_name}_{customer_contact}.pdf"

    ans = tmsg.askquestion("Generate Bill", "Are You Sure to Generate Bill?")
    if ans == "yes":
        # Create a PDF document
        pdf = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        styles = getSampleStyleSheet()

        # Add content to the PDF
        elements = []

        # Title and Address 
        elements.append(Paragraph("Garg's Cafe", styles['Title']))
        elements.append(Paragraph("Haryana, India ", styles['Title']))
        elements.append(
            Paragraph("GST.NO:- XXXXXXXXXXXXXXXX", styles['Title']))

        # Bill Information
        elements.append(Spacer(1, 12))
        elements.append(
            Paragraph("-" * 35 + "BILL" + "-" * 34, styles['Title']))
        elements.append(Paragraph("Date:- " + f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
                                  + "&nbsp;" * 10 + f"Time:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}", styles['Title']))
        elements.append(Paragraph(
            f"Customer Name:-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{customer_name}", styles['BodyText']))
        elements.append(Paragraph(
            f"Customer Contact:-&nbsp;&nbsp;{customer_contact}", styles['BodyText']))

        # Order Details
        elements.append(Spacer(1, 12))
        data = [["DESCRIPTION", "RATE", "QUANTITY", "AMOUNT"]]

        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                data.append([name, rate, quantity, price])

        table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                  ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                  ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                  ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                  ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                                  ])

        order_table = Table(data)
        order_table.setStyle(table_style)
        elements.append(order_table)

        elements.append(
            Paragraph(f"Total price : {totalPrice.get()}", styles['BodyText']))

        # Build the PDF document
        pdf.build(elements)

        success_window = Toplevel()
        success_window.title("Success")
        success_window.geometry("300x150+500+300")

        success_label = Label(success_window, text="PDF Generated Successfully!", font=(
            "arial", 16, "bold"), pady=20)
        success_label.pack()
    else:
        return

    # Clear operations
    order_tabel.delete(*order_tabel.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()
    customerName.set("")
    customerContact.set("")


def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names) == 0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
    if ans == "no":
        return
    order_tabel.delete(*order_tabel.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()


def update_total_price():
    price = 0
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("Rs. " + str(price) + "  /-")


def close_bill_window(bill):
    tmsg.showinfo("Thanks", "Thanks for using our service")
    bill.destroy()


# ===============Backend Functions===============

def update_menu_prices():
    selected_item_name = item_name.get()
    selected_item_category = itemCategory.get()

    if not selected_item_name or not selected_item_category or selected_item_name.startswith("\t"):
        tmsg.showinfo("Error", "Please select an item from the menu.")
        return

    # Open a new window for entering the new price
    update_price_window = Toplevel()
    update_price_window.title("Update Menu Price")
    update_price_window.geometry("400x200+500+300")

    new_price_label = Label(
        update_price_window, text=f"Enter new price for {selected_item_name} from Section ({selected_item_category})", font=("arial", 12), wraplength=350)
    new_price_label.pack(pady=10)

    new_price_var = StringVar()
    new_price_entry = Entry(update_price_window,
                            font="arial 12", textvariable=new_price_var)
    new_price_entry.pack(pady=10)

    update_button = ttk.Button(update_price_window, text="Update Price", command=lambda: update_menu_price(
        selected_item_category, selected_item_name, new_price_var.get().lstrip('0'), update_price_window, new_price_var))
    update_button.pack(pady=10)

    # Validate the new price entry to accept only integer values less than 1000
    vcmd_new_price = (update_price_window.register(validate_quantity), "%P")
    new_price_entry.config(validate="key", validatecommand=vcmd_new_price)


def update_menu_price(category, item_name, new_price, update_price_window, new_price_var):
    # Check if the new price is empty
    if not new_price:
        tmsg.showinfo("Error", "Please enter a new price.")
        return

    # Check if the new price is the same as the previous one
    with open("Menu\\" + menu_category_dict[category], "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith('*') or line[0] == '#' or line == "\n":
            continue

        name, price = line.split(" ", 1)
        if name == item_name and price.strip() == f"{new_price}/-":
            tmsg.showinfo(
                "Error", "You entered the same price as the previously saved one.")
            return

    # Update the price
    with open("Menu\\" + menu_category_dict[category], "r") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if lines[i].startswith('*') or lines[i][0] == '#' or lines[i] == "\n":
            continue

        name = lines[i][:lines[i].rfind(" ")]
        if name == item_name:
            # Update the price
            lines[i] = f"{name} {new_price}/-\n"
            break

    # Write the updated lines back to the file
    with open("Menu\\" + menu_category_dict[category], "w") as file:
        file.writelines(lines)

    # Close the update price window
    update_price_window.destroy()

    # Reload the menu to reflect the changes
    load_menu()
    tmsg.showinfo("Success", f"Price for {item_name} updated successfully.")


# ===============Frontend===============

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Welcome to Billing System")


# ==========Title==========

style_button = ttk.Style()
style_button.configure("TButton", font=(
    "arial", 10, "bold"), background="lightgreen")

title_frame = Frame(root, bd=8, bg="yellow", relief=GROOVE)
title_frame.pack(side=TOP, fill="x")

title_label = Label(title_frame, text="Garg's Cafe", font=(
    "times new roman", 20, "bold"), bg="yellow", fg="red", pady=5)
title_label.pack()


# ==========Customer==========

customer_frame = LabelFrame(root, text="Customer Details", font=(
    "times new roman", 15, "bold"), bd=8, bg="grey", relief=GROOVE)
customer_frame.pack(side=TOP, fill="x")

customer_name_label = Label(customer_frame, text="Name", font=(
    "arial", 14, "bold"), bg="grey", fg="white")
customer_name_label.grid(row=0, column=0)
customerName = StringVar()
customerName.set("")
vcmd_name = (customer_frame.register(validate_name), "%P")
customer_name_entry = Entry(customer_frame, width=20, font="arial 15", bd=5,
                            textvariable=customerName, validate='key', validatecommand=vcmd_name)
customer_name_entry.grid(row=0, column=1, padx=50)

customer_contact_label = Label(customer_frame, text="Contact", font=(
    "arial", 15, "bold"), bg="grey", fg="white")
customer_contact_label.grid(row=0, column=2)
customerContact = StringVar()
customerContact.set("")
vcmd_contact = (customer_frame.register(validate_contact), "%P")
customer_contact_entry = Entry(customer_frame, width=20, font="arial 15", bd=5,
                               textvariable=customerContact, validate="key", validatecommand=vcmd_contact)
customer_contact_entry.grid(row=0, column=3, padx=50)


# ==========Menu==========

menu_frame = Frame(root, bd=8, bg="lightgreen", relief=GROOVE)
menu_frame.place(x=0, y=125, height=585, width=680)

menu_label = Label(menu_frame, text="Menu", font=(
    "times new roman", 20, "bold"), bg="lightgreen", fg="red", pady=0)
menu_label.pack(side=TOP, fill="x")

menu_category_frame = Frame(menu_frame, bg="lightgreen", pady=10)
menu_category_frame.pack(fill="x")

combo_lable = Label(menu_category_frame, text="Select Type", font=(
    "arial", 12, "bold"), bg="lightgreen", fg="blue")
combo_lable.grid(row=0, column=0, padx=10)
menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame, values=menu_category,
                          textvariable=menuCategory, state="readonly")
combo_menu.grid(row=0, column=1, padx=30)

show_button = ttk.Button(menu_category_frame, text="Show",
                         width=10, command=show_button_operation)
show_button.grid(row=0, column=2, padx=10)

show_all_button = ttk.Button(
    menu_category_frame, text="Show All", width=10, command=load_menu)
show_all_button.grid(row=0, column=3)

update_menu_button = ttk.Button(
    menu_category_frame, text="Update Price", width=15, command=update_menu_prices)
update_menu_button.grid(row=0, column=4, padx=10)


# ==========Menu Table==========

menu_tabel_frame = Frame(menu_frame)
menu_tabel_frame.pack(fill=BOTH, expand=1)

scrollbar_menu_x = Scrollbar(menu_tabel_frame, orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_tabel_frame, orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview.Heading", font=("arial", 13, "bold"))
style.configure("Treeview", font=("arial", 12), rowheight=25)

menu_tabel = ttk.Treeview(menu_tabel_frame, style="Treeview", columns=("name", "price", "category"),
                          xscrollcommand=scrollbar_menu_x.set, yscrollcommand=scrollbar_menu_y.set)

menu_tabel.heading("name", text="Name")
menu_tabel.heading("price", text="Price")
menu_tabel["displaycolumns"] = ("name", "price")
menu_tabel["show"] = "headings"
menu_tabel.column("price", width=50, anchor='center')

scrollbar_menu_x.pack(side=BOTTOM, fill=X)
scrollbar_menu_y.pack(side=RIGHT, fill=Y)

scrollbar_menu_x.configure(command=menu_tabel.xview)
scrollbar_menu_y.configure(command=menu_tabel.yview)

menu_tabel.pack(fill=BOTH, expand=1)
load_menu()
menu_tabel.bind("<ButtonRelease-1>", load_item_from_menu)


# ==========Item Frame==========

item_frame = Frame(root, bd=8, bg="lightgreen", relief=GROOVE)
item_frame.place(x=680, y=125, height=230, width=680)
item_title_label = Label(item_frame, text="Item", font=(
    "times new roman", 20, "bold"), bg="lightgreen", fg="red")
item_title_label.pack(side=TOP, fill="x")

item_frame2 = Frame(item_frame, bg="lightgreen")
item_frame2.pack(fill=X)
item_name_label = Label(item_frame2, text="Name", font=(
    "arial", 12, "bold"), bg="lightgreen", fg="blue")
item_name_label.grid(row=0, column=0)

itemCategory = StringVar()
itemCategory.set("")

itemName = StringVar()
itemName.set("")
item_name = Entry(item_frame2, font="arial 12",
                  textvariable=itemName, state=DISABLED, width=25)
item_name.grid(row=0, column=1, padx=10)

item_rate_label = Label(item_frame2, text="Rate", font=(
    "arial", 12, "bold"), bg="lightgreen", fg="blue")
item_rate_label.grid(row=0, column=2, padx=40)

itemRate = StringVar()
itemRate.set("")
item_rate = Entry(item_frame2, font="arial 12",
                  textvariable=itemRate, state=DISABLED, width=10)
item_rate.grid(row=0, column=3, padx=10)

item_quantity_label = Label(item_frame2, text="Quantity", font=(
    "arial", 12, "bold"), bg="lightgreen", fg="blue", )
item_quantity_label.grid(row=1, column=0, padx=30, pady=15)
itemQuantity = StringVar()
itemQuantity.set("")
vcmd_quantity = (item_frame2.register(validate_quantity), "%P")
item_quantity = Entry(item_frame2, font="arial 12", width=10,
                      textvariable=itemQuantity, validate='key', validatecommand=vcmd_quantity)
item_quantity.grid(row=1, column=1)

item_frame3 = Frame(item_frame, bg="lightgreen")
item_frame3.pack(fill=X)

add_button = ttk.Button(item_frame3, text="Add Item",
                        command=add_button_operation)
add_button.grid(row=0, column=0, padx=40, pady=30)

remove_button = ttk.Button(
    item_frame3, text="Remove Item", command=remove_button_operation)
remove_button.grid(row=0, column=1, padx=40, pady=30)

update_button = ttk.Button(
    item_frame3, text="Update Quantity", command=update_button_operation)
update_button.grid(row=0, column=2, padx=40, pady=30)

clear_button = ttk.Button(item_frame3, text="Clear",
                          width=8, command=clear_button_operation)
clear_button.grid(row=0, column=3, padx=40, pady=30)


# ==========Order Frame==========

order_frame = Frame(root, bd=8, bg="lightgreen", relief=GROOVE)
order_frame.place(x=680, y=335, height=370, width=680)

order_title_label = Label(order_frame, text="Your Order", font=(
    "times new roman", 20, "bold"), bg="lightgreen", fg="red")
order_title_label.pack(side=TOP, fill="x")


# ==========Order Table==========

order_tabel_frame = Frame(order_frame)
order_tabel_frame.place(x=0, y=40, height=260, width=680)

scrollbar_order_x = Scrollbar(order_tabel_frame, orient=HORIZONTAL)
scrollbar_order_y = Scrollbar(order_tabel_frame, orient=VERTICAL)

order_tabel = ttk.Treeview(order_tabel_frame, columns=("name", "rate", "quantity", "price", "category"),
                           xscrollcommand=scrollbar_order_x.set, yscrollcommand=scrollbar_order_y.set)

order_tabel.heading("name", text="Name")
order_tabel.heading("rate", text="Rate")
order_tabel.heading("quantity", text="Quantity")
order_tabel.heading("price", text="Price")
order_tabel["displaycolumns"] = ("name", "rate", "quantity", "price")
order_tabel["show"] = "headings"
order_tabel.column("rate", width=100, anchor='center', stretch=NO)
order_tabel.column("quantity", width=100, anchor='center', stretch=NO)
order_tabel.column("price", width=100, anchor='center', stretch=NO)

order_tabel.bind("<ButtonRelease-1>", load_item_from_order)

scrollbar_order_x.pack(side=BOTTOM, fill=X)
scrollbar_order_y.pack(side=RIGHT, fill=Y)

scrollbar_order_x.configure(command=order_tabel.xview)
scrollbar_order_y.configure(command=order_tabel.yview)

order_tabel.pack(fill=BOTH, expand=1)


# ==========Price, Bill, Cancel Lable/Button==========

total_price_label = Label(order_frame, text="Total Price", font=(
    "arial", 12, "bold"), bg="lightgreen", fg="blue")
total_price_label.pack(side=LEFT, anchor=SW, padx=20, pady=10)

totalPrice = StringVar()
totalPrice.set("")
total_price_entry = Entry(order_frame, font="arial 12",
                          textvariable=totalPrice, state=DISABLED, width=10)
total_price_entry.pack(side=LEFT, anchor=SW, padx=0, pady=10)

bill_button = ttk.Button(order_frame, text="Bill(txt)",
                         width=8, command=bill_button_operation)
bill_button.pack(side=LEFT, anchor=SW, padx=20, pady=10)

pdf_button = ttk.Button(order_frame, text="Bill(pdf)", command=generate_pdf)
pdf_button.pack(side=LEFT, anchor=SW, padx=20, pady=10)

cancel_button = ttk.Button(
    order_frame, text="Cancel Order", command=cancel_button_operation)
cancel_button.pack(side=LEFT, anchor=SW, padx=20, pady=10)

root.mainloop()
