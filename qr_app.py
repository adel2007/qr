import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet
from PIL import Image
import cv2
import threading
from pyzbar import pyzbar
import qrcode
from PIL import Image, ImageTk

class QRCodeDecryptorApp:

    #ui structure
    def __init__(self, root):

        self.root = root
        self.root.title("QR Code Decryptor")
        self.qr_code_file_path = tk.StringVar()
        self.key_file_path = tk.StringVar()
        self.decrypted_data = tk.Text(self.root, wrap="word", height=2, width=50)

        self.create_widgets()

    #creating fild and buttons
    def create_widgets(self):
        
        #set this page as first
        self.page = 1

        #create lable
        self.lable_manul_input  = ttk.Label(self.root, text="Manual Input:")
        self.lable_manul_input.pack()

        #create button
        self.btn_paste = ttk.Button(self.root, text="Paste", command=self.paste_text)
        self.btn_paste.pack(pady=10)
        self.manual_input = tk.Entry(self.root)
        self.manual_input.pack()

        # New section for QR code scanning
        self.lable_scan = ttk.Label(self.root, text="Scan QR Code with Webcam:")
        self.lable_scan.pack(pady=5)

        #create button
        self.btn_scan = ttk.Button(self.root, text="Start Scan", command=self.start_qr_scan)
        self.btn_scan.pack(pady=10)

        self.lable_file = ttk.Label(self.root, text="Select QR Code File:")
        self.lable_file.pack(pady=5)

        self.btn_browse = ttk.Button(self.root, text="Browse", command=self.browse_qr_code)
        self.btn_browse.pack(pady=5)

        self.lable_filename = ttk.Label(self.root, textvariable=self.qr_code_file_path)
        self.lable_file.pack()

        self.btn_decrypt = ttk.Button(self.root, text="Decrypt", command=self.decrypt_qr_code)
        self.btn_decrypt.pack(pady=10)

        self.lable_data = ttk.Label(self.root, text="Decrypted Data:")
        self.lable_data.pack(pady=5)
        self.decrypted_data.pack()

        self.button_next_page = ttk.Button(self.root, text="generate", command=self.next_page)
        self.button_next_page.place(x=10, y=10)

        #create button
        self.btn_pastee = ttk.Button(self.root, text="Paste", command=self.paste_text)


        self.gen_input = ttk.Entry(self.root)
        self.btn_gen = ttk.Button(self.root, text="generate QR", command=self.create_qr_code)

    def next_page(self):
        # صفحه فعلی را بررسی می‌کنیم
        if self.page == 1:
            # اگر صفحه اول باشیم، به صفحه دوم منتقل می‌شویم
            self.page = 2
            self.manual_input.pack_forget()
            self.lable_manul_input.pack_forget()
            self.btn_paste.pack_forget()
            self.lable_scan.pack_forget()
            self.btn_scan.pack_forget()
            self.lable_file.pack_forget()
            self.btn_browse.pack_forget()
            self.lable_file.pack_forget()
            self.btn_decrypt.pack_forget()
            self.lable_data.pack_forget()
            self.decrypted_data.pack_forget()

            self.btn_paste.pack(pady=10)
            
            

            self.gen_input.pack()

            
            self.btn_gen.pack(pady=5)

            self.button_next_page.config(text="deode")  # تغییر متن دکمه به "Previous Page"
        elif self.page == 2:

            self.btn_paste.pack_forget()
            self.gen_input.pack_forget()
            self.btn_gen.pack_forget()

            # اگر صفحه دوم باشیم، به صفحه اول منتقل می‌شویم
            self.page = 1
            self.lable_manul_input.pack(pady=5)
            self.btn_paste.pack(pady=5)
            self.manual_input.pack(pady=5)
            self.lable_scan.pack(pady=5)
            self.btn_scan.pack(pady=5)
            self.lable_file.pack(pady=5)
            self.btn_browse.pack(pady=5)
            self.lable_file.pack(pady=5)
            self.btn_decrypt.pack(pady=5)
            self.lable_data.pack(pady=5)
            self.decrypted_data.pack()
            self.button_next_page.config(text="generate")  # تغییر متن دکمه به "Next Page"

    #select png file(qr)
    def browse_qr_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        self.qr_code_file_path.set(file_path)

    #decryoting qr 
    def decrypt_qr_code(self):


        qr_code_file_path = self.qr_code_file_path.get()

        if (qr_code_file_path ) or self.manual_input:
            key =  ("ZSC9Dweeq3qPtn56Ql575ub1oEEnm7nhEoJiahxRW-w=")
            data = self.manual_input.get()
            print(data)
            decrypted_data = self.read_qr_code(qr_code_file_path, key) if qr_code_file_path else self.decrypt_data(self,key)
            self.update_decrypted_data_text(decrypted_data)
        else:
            messagebox.showerror("Error", "Please select either QR Code and Key files or provide manual input.")

    #pasting button
    def paste_text(self):
        clipboard_text = self.root.clipboard_get()
        self.manual_input.delete(1.0, tk.END)
        self.manual_input.insert(tk.END, clipboard_text)

    #scanning qr using camera
    def start_qr_scan(self):
        scanning_thread = threading.Thread(target=self.qr_scan_thread)
        scanning_thread.start()

    #qr scan core
    def qr_scan_thread(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            decoded_objects = pyzbar.decode(frame)

            for obj in decoded_objects:
                encrypted_data = obj.data
                key =  ("ZSC9Dweeq3qPtn56Ql575ub1oEEnm7nhEoJiahxRW-w=")
                decrypted_data = self.decrypt_data(key, encrypted_data)
                self.update_decrypted_data_text(decrypted_data)

            cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()  # بستن تمام پنجره‌ها پس از خروج از حلقه

    #secerypt data from scanned qr
    def decrypt_data(self, key, encrypted_data):
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    #procces the qr file selected
    def read_qr_code(self, file_path, key):
        img = Image.open(file_path)
        decoded_objects = pyzbar.decode(img)

        for obj in decoded_objects:
            encrypted_data = obj.data
            decrypted_data = self.decrypt_data(key, encrypted_data)
            self.update_decrypted_data_text(decrypted_data)

            return decrypted_data

    #show the final resault in text view item
    def update_decrypted_data_text(self, result):
        self.decrypted_data.delete(1.0, tk.END)
        self.decrypted_data.insert(tk.END, result)
        num_lines = result.count('\n') + 1
        self.decrypted_data.config(height=num_lines, width=100)

    #creating qr code 
    def create_qr_code(self):
     data = self.gen_input.get()
     print("aaaaaaaaaaaaaaaaaaaa"+data)
        #set the key
     key = ("ZSC9Dweeq3qPtn56Ql575ub1oEEnm7nhEoJiahxRW-w=")
     if (data != ""):

        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data.encode())

        #create qr code
        qr = qrcode.QRCode(
            version=40,  #qr code version
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(encrypted_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("encrypted_qr_code.png")

        self.photo = ImageTk.PhotoImage(Image.open("encrypted_qr_code.png"))

        self.image_label = ttk.Label(self.root, image=self.photo)

        self.image_label.pack(padx=100, pady=100)


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeDecryptorApp(root)
    root.mainloop()
