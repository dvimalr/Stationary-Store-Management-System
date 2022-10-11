from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import re
import socket
mydb = mysql.connector.connect(host= "localhost",user = "root",password="abc456")
my_cursor = mydb.cursor()
##############################################################################################
my_cursor.execute("drop database if exists Store")
my_cursor.execute("create database if not exists Store")
my_cursor.execute("use Store")
#my_cursor.execute("drop table if exists stationary")
my_cursor.execute("create table if not exists stationary(item_name VARCHAR(20) not null unique, item_price INTEGER(10), item_quantity INTEGER(10), item_discount float(3),grand_total float(5))")
##############################################################################################
root = Tk() 
root.title("Stationary Shop Management System")
root.configure(width=1500,height=600,bg="White")


buttoncolor = "#49D810"
buttonfg = "black"
total = 0.0


#All functions

def additem():
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        try:
                e1=entry1.get()
                if e1 == "":
                        raise Exception("Item Name is Empty!!!")
                if e1.isdigit():
                        raise Exception("Item Name cannot be Digits!!")
                if len(e1) <=1 or e1.isdigit():
                        raise Exception("Invalid Item name")
                if not (special_char.search(e1) == None):
                        raise Exception("Can't contains Special Characters!!")

                e2=entry2.get()
                if e2 == "":
                        raise Exception("Item Price is Empty!!")
                if e2.isalpha():
                        raise Exception("Item Price cannot be Characters!!")
                e2 = int(e2)
                if e2 <= 0:
                        raise Exception("Item Price cannot be less than 0 or equal to 0!!")
			
                e3=entry3.get()
                if e3 == "":
                        raise Exception("Item Quantity is Empty!!")
                if e3.isalpha():
                        raise Exception("Item Quantity annot be Characters!!")
                e3 = int(e3)
                if e3 <= 0:
                        raise Exception("Item Quantity cannot be less than 0 or equal to 0!!")
		#e4=entry4.get()
		#if e4 == "":
		#	raise Exception("Item Category is Empty!!")
		#if e4.isdigit():
		#	raise Exception("Item Category can be characters not digits")
		#if len(e4) <=1 or e4.isdigit():
		#	raise Exception("Invalid Item Category!!")
                e5=entry5.get()
                if e5 == "":
                        raise Exception("Item Disount is Empty!!")
                if e5.isalpha():
                        raise Exception("Item Discount cannot be characters it has to be digits")
                e5 = int(e5)
                if e5 < 0:
                        raise Exception("Item Discount cannot be less than 0")
        except ValueError as e:
                 messagebox.showerror("Error","Record already exists or You entered Wrong!!!!")	
        except (mysql.connector.Error,mysql.connector.Warning):
                messagebox.showerror("Duplicate Data","You are trying to insert a item which is already present in database")	
        except Exception:
                if e1 == "":
                        messagebox.showerror("Invalid name","Item Name is Empty!!")
                elif e1.isdigit():
                        messagebox.showerror("Invalid name","Item name cannot be Digits!!")
                elif len(e1) <=1 or e1.isdigit():
                        messagebox.showerror("Invalid name","Invalid Item name")
                elif not(special_char.search(e1) == None):
                        messagebox.showerror("Invalid name","Can't contains Special Characters!!")

                elif e2 == "":
                        messagebox.showerror("Invalid price","Item Price Empty!!")
                elif str(e2).isalpha():
                        messagebox.showerror("Invalid quantity","Item Price cannot be Characters")
                elif int(e2) <= 0:
                        messagebox.showerror("Invalid price","Item Price cannot be 0 or less than 0 or Characters")
                elif e3 == "":
                        messagebox.showerror("Invalid quantity","Item Quanity is Empty!!")
                elif str(e3).isalpha():
                        messagebox.showerror("Invalid quantity","Item Quantity cannot be Characters!!")
                elif int(e3) <= 0:
                        messagebox.showerror("Invalid quantity","Item Quantity cannot be 0 or less than 0")
		#elif e4 == "":
		#	messagebox.showerror("Invalid category","Item Category is Empty!!")
		#elif e4.isdigit():
		#	messagebox.showerror("Invalid category","Item Category can be characters not digits!!")
		#elif len(e4) <=1 or e4.isdigit():
		#	messagebox.showerror("Invalid name","Invalid Item Category!!")
	
                elif e5 == "":
                        messagebox.showerror("Invalid discount","Item Discount is Empty!!")
                elif str(e5).isalpha():
                        messagebox.showerror("Invalid discount","Item Discount cannot be characters but digits!!")
                elif e5 < 0:
                        messagebox.showerror("Invalid discount","Discount cannot be less than 0")
                elif e5 < 0:
                        messagebox.showerror("Invalid discount","Discount cannot be less than 0")
                else:
                        messagebox.showerror("Error","Bad entry")
                        entry1.delete(0, END)
                        entry2.delete(0, END)
                        entry3.delete(0, END)
                        #entry4.delete(0, END)
                        entry5.delete(0, END)
		
        else:
                sql = "INSERT INTO stationary (item_name, item_price, item_quantity, item_discount) VALUES (%s, %s, %s, %s)"
                val = (str(e1),e2,e3,e5)
                my_cursor.execute(sql,val)
                mydb.commit()
                entry1.delete(0, END)
                entry2.delete(0, END)
                entry3.delete(0, END)
                #entry4.delete(0, END)
                entry5.delete(0, END)
                messagebox.showinfo(" ADD ITEM ", "ITEM ADDED SUCCESSFULLY")
        finally:
                pass

def delete1():
    e6 = entry6.get()
    if e6 == "":
        messagebox.showinfo("Warning","Enter the item in search bar first")
    elif e6.isdigit():
                messagebox.showwarning("Warning","Item Name cannot be Digits!!")
    elif len(e6) <=1 or e6.isdigit():
                messagebox.showerror("Invalid name","Invalid Item name")
    else:
        my_cursor.execute("delete from stationary where item_name = '{0}'".format(str(e6)))
        mydb.commit()
        messagebox.showinfo("DELETE ITEM", "ITEM DELETED SUCCESSFULLY")
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        #entry4.delete(0, END)
        entry5.delete(0, END)
        entry6.delete(0, END)

def showdatabase():
    total = 0.0
    total1 = 0.0
    total2 = 0.0
    quantity = 0
    i = 0
    root1 = Tk()
    root1.title("Stationary Store Management Database")
    root1.configure(width=2000,height=800,bg="White")
    my_cursor.execute("select * from stationary")
    mytext1 = my_cursor.fetchall()
    mytext = Text(root1,width=100,height= 30 ,bg= "White",fg="black", font=("Times", 12))
    mytext.insert(END," Item_Name \t\tItem_Price \t\tItem_Quantity \t\tItem_Discount \t\tTotal Amount \n")
    mytext.insert(END," ------------ \t\t----------\t\t--------------\t\t---------------\t\t---------------\n")
    for row in mytext1:
        i += 1
        mytext.insert(END,"       {0} \t\t     {1} \t\t         {2} \t\t          {3} \t\t          {4}\n".format(row[0],row[1],row[2],row[3],(float(row[1])-float(row[3]))*float(row[2])))   
        total = total + (float(row[1])-float(row[3]))*float(row[2])
        total1 = total*(18/100)
        total2 = total + total1
        quantity = quantity + row[2]
    mytext.insert(END," ------------ \t\t----------- \t\t-------------- \t\t--------------- \t\t---------------\n")
    #mytext.insert(END,"       {0} \t\t     {1} \t\t         {2} \t\t   {3} \t\t          {4}\n".format(i,"None",quantity,"None","None",total))
    mytext.insert(END,"                                                                                                                                      {5}\n".format(i,"None",quantity,"None","None",total2))
    mytext.pack(side = LEFT)

def searchitem():
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        #entry4.delete(0, END)
        entry5.delete(0, END)
        e6 = entry6.get()
        if e6 == "":
                messagebox.showwarning("Warning","Please first enter item name for search")
        elif e6.isdigit():
                messagebox.showwarning("Warning","Item Name cannot be Digits!!")
        elif len(e6) <=1 or e6.isdigit():
                messagebox.showerror("Invalid name","Invalid Item name")
        else:
                my_cursor.execute("select * from stationary where item_name = '{0}'".format(str(e6)))
                mytext1 = my_cursor.fetchone()
                try:
                        if mytext1[0] == None:
                               messagebox.showwarning("Warning","Item not found!!")
                        else:
                                entry1.insert(0,mytext1[0])
                                entry2.insert(0,mytext1[1])
                                entry3.insert(0,mytext1[2])
                                #entry4.insert(0,mytext1[3])
                                entry5.insert(0,mytext1[3])
                except Exception as e:
                                messagebox.showinfo("Message","Founded!!")
		
def update():
	e6 = entry6.get()
	if e6 == "":
		messagebox.showerror("Warning","Enter the item in search bar first")

	else:
		my_cursor.execute("select * from stationary where item_name = '{0}'".format(str(e6)))
		line = my_cursor.fetchone()
		if line != None:
			iname = line[0]
			iprice = line[1]
			iquantity = line[2]
			#icategory = line[3]
			idiscount = line[3]

			root2 = Tk()
			root2.title("Update Records")
			root2.configure(width=900,height=600,bg="White")

			def actualupdate():
				try:
					e1 = uentry1.get()
					if e1 == "":
						raise Exception("Item Name is Empty!!")
					if e1.isdigit():
						raise Exception("Item name cannot be Digits!!")
					if len(e1) <=1 or e1.isdigit():
						raise Exception("Invalid Item name!!")
					e2 = uentry2.get()
					if e2 == "":
						raise Exception("Item Price is Empty!!")
					if e2.isalpha():
						raise Exception("Item Price cannot be Characters!!")
					e2 = int(e2)
					if e2 <= 0:
						raise Exception("Item Price cannot be less than or equal to 0")
					e3 = uentry3.get()
					if e3 == "":
						raise Exception("Item Quantity is Empty!!")
					if e3.isalpha():
						raise Exception("Item Quantity cannot be Characters!!")	
					e3 = int(e3)
					if e3 <= 0:
						raise Exception("Item Quantity cannot be less than or equal to 0")
					
					#e4 = uentry4.get()
					#if e4 == "":
					#	raise Exception("Item Category is Empty!!")
					#if e4.isdigit():
					#	raise Exception("Item Category can be characters not digits!!")
					e5 = uentry5.get()
					if e5 == "":
						raise Exception("Item Discount is Empty!!")
					if e5.isalpha():
						raise Exception("Item Discount cannot be characters but digits")
					e5 = int(e5)
					if e5 < 0:
						raise Exception("Discount cannot be less than 0")
					
					
				
					if e1!="Update" or e1!="":
						iname=e1
					if e2!="Update" or e1!="":
						iprice=e2
					if e3!="Update" or e1!="":
						iquantity=e3
					#if e4!="Update" or e1!="":
					#	icategory=e4
					if e5!="Update" or e1!="":
						idiscount=e5
				except ValueError as e:
					messagebox.showerror("Error","Can't Contains Special Characters or Digits!!")
				except (mysql.connector.Error,mysql.connector.Warning):
					messagebox.showerror("Duplicate Data","You are trying to insert a item which is already present in database")
				except Exception:
					if e1 == "":
						messagebox.showerror("Invalid name","Item Name is Empty!!")
					elif e1.isdigit():
						messagebox.showerror("Invalid name","Item Name cannot be Digits!!")
					elif len(e1) <=1 or e1.isdigit():
						messagebox.showerror("Invalid name","Invalid Item name")
					elif e2 == "":
						messagebox.showerror("Invalid price","Item Price is Empty!!")
					elif str(e2).isalpha():
						messagebox.showerror("Invalid price","Item Price cannot be Characters!!")
					elif int(e2) <= 0:
						messagebox.showerror("Invalid price","Item Price cannot be 0 or less than 0")	
					elif e3 == "":
						messagebox.showerror("Invalid quantity","Item Quantity is Empty!!")
					elif str(e3).isalpha():
							messagebox.showerror("Invalid quantity","Item Quantity cannot be Characters!!")
					elif int(e3) <= 0:
						messagebox.showerror("Invalid quantity","Item Quantity cannot be 0 or less than 0")	
					#elif e4 == "":
					#	messagebox.showerror("Invalid category","Item Category is Empty!!")
					#elif e4.isdigit():
					#	messagebox.showerror("Invalid category","Item Category can be characters not digits!!")
					elif e5 == "":
						messagebox.showerror("Invalid discount","Item Discount is Empty!!")
					elif str(e5).isalpha():
							messagebox.showerror("Invalid discount","Item Discount cannot be characters but digits")
					elif int(e5) < 0:
						messagebox.showerror("Invalid discount","Item Discount cannot be less than 0")
					else:
						messagebox.showerror("Error","Bad entry")
						entry1.delete(0, END)
						entry2.delete(0, END)
						entry3.delete(0, END)
						#entry4.delete(0, END)
						entry5.delete(0, END)
				else:
					sql = "update stationary set item_name = %s, item_price = %s, item_quantity = %s, item_discount = %s  where item_name = %s"
					val = (str(iname),iprice,iquantity,idiscount,str(e6))
					my_cursor.execute(sql,val)
					mydb.commit()
					messagebox.showinfo("UPDATE ITEM", "ITEM UPDATED SUCCESSFULLY")
					uentry1.delete(0, END)
					uentry2.delete(0, END)
					uentry3.delete(0, END)
					#uentry4.delete(0, END)
					uentry5.delete(0, END)
					root2.destroy()
				finally:
					pass

			def clearuitem():
				uentry1.delete(0, END)
				uentry2.delete(0, END)
				uentry3.delete(0, END)
				#uentry4.delete(0, END)
				uentry5.delete(0, END)



			#Labels, Entries and button for root2 window.
			button8 = Button(root2,activebackground="green", text="UPDATE ITEM",bd=4, bg=buttoncolor, fg=buttonfg, width=25, font=("Times", 12),command=actualupdate)
			button9 = Button(root2,activebackground="green", text="CLEAR",bd=4, bg=buttoncolor, fg=buttonfg, width=25, font=("Times", 12),command=clearuitem)
			button10 = Button(root2,activebackground="red", text="BACK",bd=4, bg="#FF0000", fg="#EEEEF1", width=25, font=("Times", 12),command=home)
			ulabel0 = Label(root2,text="UPDATE RECORD",bg="Black",fg="#F9FAE9",font=("Times", 30),width=23)
			ulabel1 = Label(root2,text="ENTER ITEM NAME",bg="black",relief="ridge",fg="white",bd=2,font=("Times", 12),width=25)
			uentry1 = Entry(root2, font=("Times", 14),bd=4,width=25,bg="white")
			ulabel2 = Label(root2, text="ENTER ITEM PRICE",relief="ridge",height="1",bg="black",bd=2,fg="white", font=("Times", 12),width=25)
			uentry2 = Entry(root2, font=("Times", 14),bd=4,width=25,bg="white")
			ulabel3 = Label(root2, text="ENTER ITEM QUANTITY",relief="ridge",bg="black",bd=2,fg="white", font=("Times", 12),width=25)
			uentry3 = Entry(root2, font=("Times", 14),bd=4,width=25,bg="white")
			#ulabel4 = Label(root2, text="ENTER ITEM CATEGORY",relief="ridge",bg="black",bd=2,fg="white", font=("Times", 12),width=25)
			#uentry4 = Entry(root2, font=("Times", 14),bd=4,width=25,bg="white")
			ulabel5 = Label(root2, text="ENTER ITEM DISCOUNT",bg="black",relief="ridge",fg="white",bd=2, font=("Times", 12),width=25)
			uentry5 = Entry(root2, font=("Times", 14),bd=4,width=25,bg="white")
			ulabel0.grid(columnspan=6, padx=10, pady=10)
			ulabel1.grid(row=1,column=0, padx=10, pady=10)
			ulabel2.grid(row=2,column=0, padx=10, pady=10)
			ulabel3.grid(row=3,column=0, padx=10, pady=10)
			#ulabel4.grid(row=4,column=0, padx=10, pady=10)
			ulabel5.grid(row=5,column=0, padx=10, pady=10)
			uentry1.grid(row=1,column=1, padx=10, pady=10)
			uentry2.grid(row=2,column=1, padx=10, pady=10)
			uentry3.grid(row=3,column=1, padx=10, pady=10)
			#uentry4.grid(row=4,column=1, padx=10, pady=10)
			uentry5.grid(row=5,column=1, padx=10, pady=10)
			button8.grid(row=6,column=1, padx=10, pady=10)
			button9.grid(row=6,column=0,padx=10,pady=10)
			button10.grid(row=7,column=0,padx=10,pady=10)
						

			uentry1.insert(0,iname)
			uentry2.insert(0,iprice)
			uentry3.insert(0,iquantity)
			#uentry4.insert(0,icategory)
			uentry5.insert(0,idiscount)
			entry6.insert(0,"SEARCH")

			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			#entry4.delete(0, END)
			entry5.delete(0, END)
			entry6.delete(0, END)
		else:
			messagebox.showinfo("Error","Element does not exist.")

def clearitem():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    #entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def qExit():
    qExit= messagebox.askyesno("Quit System","Do you want to quit ?")
    if qExit > 0:
        root.destroy()
        return


def home():
	root.deiconify()

def graph():
	try:
		prices = []
		items = []
		#category = []
		count = 0
		my_cursor.execute("select * from stationary")
		mytext1 = my_cursor.fetchall()
		for row in mytext1:
			prices.append(row[1])
			items.append(row[0])
			#category.append(row[3])
			count += 1
		x = np.arange(len(items))
		#category = set(category)
		if count == 0:
			raise Exception("Row count is 0")
	except Exception:
		if count == 0:
			messagebox.showerror("Table empty","there are no entries in the table")
		else:
			messagebox.showerror("something went wrong")
	else:
		plt.bar(x,prices,label="Prices of items",width=0.30)
		plt.xticks(x,items)
		plt.title('Prices of items in the Store')
		plt.xlabel('Items',fontsize = 10)
		plt.ylabel('Prices',fontsize = 10)
		plt.legend()
		plt.grid()
		plt.show()
	finally:
		pass
	

#All labels Entrys Button grid place
label0 = Label(root,text="STATIONARY STORE MANAGEMENT SYSTEM ",bg="White",fg="Black",font=("Times", 27),width=39)
label1 = Label(root,text="ENTER ITEM NAME :",fg="White",bg="black",bd=2,font=("Times", 12),width=23)
entry1 = Entry(root , font=("Times", 14),bd=4,width=25,bg="white")
label2 = Label(root, text="ENTER ITEM PRICE :",bg="black",fg="white", font=("Times", 12),width=23)
entry2 = Entry(root, font=("Times", 14),bd=4,width=25,bg="white")
label3 = Label(root, text="ENTER ITEM QUANTITY :",bg="black",bd=2,fg="white", font=("Times", 12),width=23)
entry3 = Entry(root, font=("Times", 14),bd=4,width=25,bg="white")
#label4 = Label(root, text="ENTER ITEM CATEGORY :",relief="ridge",bg="black",bd=2,fg="white", font=("Times", 12),width=23)
#entry4 = Entry(root, font=("Times", 14),bd=4,width=25,bg="white")
label5 = Label(root, text="ENTER ITEM DISCOUNT :",bg="black",fg="white",bd=2, font=("Times", 12),width=23)
entry5 = Entry(root, font=("Times", 14),bd=4,width=25,bg="white")
label6 = Label(root, text="Note : This Discount is per item in Rs",fg="Red", font=("Times", 20),width=30)
label7 = Label(root, text="Note : GST of 18% added on Total Bill",fg="Red", font=("Times", 20),width=30)

button1 = Button(root,activebackground="green", text="ADD ITEM",bd=4, bg=buttoncolor, fg=buttonfg, width=25, font=("Times", 12),command=additem)
button2 = Button(root,activebackground="green", text="DELETE ITEM",bd=4, bg=buttoncolor, fg=buttonfg, width =25, font=("Times", 12),command=delete1)
button3 = Button(root,activebackground="green", text="VIEW ITEM",bd=4, bg=buttoncolor, fg=buttonfg, width =25, font=("Times", 12),command=showdatabase)
button4 = Button(root,activebackground="green", text="SEARCH ITEM",bd=4, bg=buttoncolor, fg=buttonfg, width =25, font=("Times", 12),command=searchitem)
button5 = Button(root,activebackground="green", text="CLEAR SCREEN",bd=4, bg=buttoncolor, fg=buttonfg, width=25, font=("Times", 12),command=clearitem)
button6 = Button(root,activebackground="red", text="EXIT",bd=4, bg="#FF0000", fg="#EEEEF1", width=25, font=("Times", 12),command=qExit)
entry6 = Entry(root, font=("Times", 14),justify='left',bd=4,width=25,bg="#EEEEF1")
entry6.insert(0,"")
button7 = Button(root,activebackground="green", text="UPDATE ITEM",bd=4, bg=buttoncolor, fg=buttonfg, width=25, font=("Times", 12),command=update)
button8 = Button(root,activebackground="green", text="GRAPH",bd=4, bg=buttoncolor, fg=buttonfg, width=25, font=("Times", 12),command=graph)

########POSITION OF ALL BUTTONS AND ENTRY
label0.grid(columnspan=6, padx=10, pady=10)
label1.grid(row=1,column=0, padx=10, pady=10)
label2.grid(row=2,column=0, padx=10, pady=10)
label3.grid(row=3,column=0, padx=10, pady=10)
#label4.grid(row=4,column=0, padx=10, pady=10)
label5.grid(row=4,column=0, padx=10, pady=10)
label6.grid(row=5, column=1, padx=10, pady=10)
label7.grid(row=6, column=1, padx=10, pady=10)
entry1.grid(row=1,column=1, padx=10, pady=10)
entry2.grid(row=2,column=1, padx=10, pady=10)
entry3.grid(row=3,column=1, padx=10, pady=10)
#entry4.grid(row=4,column=1, padx=10, pady=10)
entry5.grid(row=4,column=1, padx=10, pady=10)
entry6.grid(row=1,column=2, padx=10, pady=10)
button1.grid(row=7,column=0, padx=10, pady=10)
button2.grid(row=7,column=1, padx=10, pady=10)
button3.grid(row=3,column=2, padx=10, pady=10)
button4.grid(row=2,column=2, padx=10, pady=10)
button5.grid(row=4,column=2, padx=10, pady=10)
button6.grid(row=7,column=2, padx=10, pady=10)
button7.grid(row=5,column=2, padx=10, pady=10)
button7.grid(row=5,column=2, padx=10, pady=10)
button8.grid(row=6,column=2, padx=10, pady=10)


root.mainloop()
