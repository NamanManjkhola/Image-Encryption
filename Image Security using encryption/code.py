# author - Naman Manjkhola
import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import cv2

#Key generation
def key_generator(a, x, size, row, column, height):
    key = np.zeros((row, column, height), np.uint8)

    for i in range(row):
        for j in range(column):
            for k in range(height):
                a = x * a * (1 - a)
                key[i][j][k] = int(a*pow(10,16) % 256)
    return key

def xor_bindata(filename,password1,password2):
    file = open(filename, "rb")
    bindata = file.read()
    file.close()

    bindata = bytearray(bindata)
    for index, value in enumerate(bindata):
        if index%2==0:
            bindata[index] = value ^ password1
        else:
            bindata[index] = value ^ password2

    file = open(filename, "wb")
    file.write(bindata)
    file.close()


#Encryption
def encrypt(filename,password1,password2):
    img = cv2.imread(filename)
    r,c,d= img.shape

    # Create random key using key_generator()
    key = key_generator(0.01, 3.915, r * c * d, r, c, d)

    # Encryption (XOR pixels)
    encrypted_image = np.zeros((r, c, d), np.uint8)
    for row in range(r):
        for column in range(c):
            for height in range(d):
                encrypted_image[row, column, height] = img[row, column, height] ^ key[row, column, height]

    en_filename = file_path+'/encrypted_img.bmp'
    # saving file
    cv2.imwrite(en_filename, encrypted_image)

    # Encryption (XOR binary data)
    xor_bindata(en_filename,password1, password2)
    encryption_success()

#Decryption
def decrypt(filename,password1,password2):
    # Decryption (XOR binary data)
    xor_bindata(filename, password1, password2)

    enimg = cv2.imread(filename)
    r,c,d = enimg.shape

    # Generate keys using key_generator()
    key = key_generator(0.01, 3.915, r * c * d, r, c, d)

    # Decryption(XOR pixels)
    decrypted_image = np.zeros((r, c, d), np.uint8)
    for row in range(r):
        for column in range(c):
            for height in range(d):
                decrypted_image[row, column, height] = enimg[row, column, height] ^ key[row, column, height]

    # saving file
    cv2.imwrite(filename, decrypted_image)
    decryption_success()

#-----------------------------------
# GUI ALERTS
#-----------------------------------
def pass_alert():
    messagebox.showinfo("Key Alert", "Please enter the keys.")

def keylen_alert():
    messagebox.showinfo("Invalid key", "Please enter the keys between 1-255")

def distinctkey_alert():
    messagebox.showinfo("Invalid keys", "Please enter distinct keys between 1-255")

def encryption_success():
    messagebox.showinfo("Successfully Encrypted", "Encryption Done!")

def decryption_success():
    messagebox.showinfo("Successfully Decrypted", "Decryption Done!")


# Encryption button event listener
def select_image():
    global file_path
    if inputBox.get()=="" or inputBox2.get()=="":
        pass_alert()
    password1 = int(inputBox.get())
    password2 = int(inputBox2.get())

    if (password1<=0 or password1>255) or (password2<=0 or password2>255):
        keylen_alert()
    elif password1 == password2:
        distinctkey_alert()
    else:
        filename = filedialog.askopenfilename()
        file_path = os.path.dirname(filename)
        encrypt(filename,password1,password2)

# Decryption button event listener
def select_cipher():
    global file_path
    if inputBox.get() == "" or inputBox2.get() == "":
        pass_alert()
    password1 = int(inputBox.get())
    password2 = int(inputBox2.get())

    if (password1<=0 or password1>255) or (password2<=0 or password2>255):
        keylen_alert()
    elif password1 == password2:
        distinctkey_alert()
    else:
        filename = filedialog.askopenfilename()
        file_path = os.path.dirname(filename)
        decrypt(filename,password1,password2)

class Application:
  def __init__(self, master):
      appName = "Image Encryption Tool"
      developerName = "Developed by - Naman Manjkhola"
      global inputBox,inputBox2

      title = Label(master, text=appName)
      title.pack()
      title.config(font = ("Trajan Pro",25, 'bold'), pady=10)
      title2 = Label(master, text=developerName)
      title2.pack()
      title2.config(font=("Trajan Pro",10), pady=10)
      mylabel = Label(master, text="Enter Encryption / Decryption keys(1-255)")
      mylabel.pack()
      mylabel.config(font=("Trajan Pro",11), pady=10)
      inputBox = Entry(master, width=20, selectbackground='green')
      inputBox.pack()
      inputBox2 = Entry(master, width=20, selectbackground='green')
      inputBox2.pack()
      self.encrypt = Button(master, text="Encrypt", padx=20, pady=5, command=select_image)
      self.encrypt.pack(side=LEFT)
      self.decrypt = Button(master, text="Decrypt", padx=20, pady=5, command=select_cipher)
      self.decrypt.pack(side=RIGHT)



# ------------------------#
#        MAIN             #
#-------------------------#
root = Tk()
root.wm_title("Image Encryption")
root.geometry('400x250')
p1 = PhotoImage(file = 'C:/Users/asus/Downloads/enicon.png')
root.iconphoto(False, p1)
app = Application(root)
root.mainloop()