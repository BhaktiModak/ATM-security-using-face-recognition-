
import tkinter as tk
import time
import messagebox
import cv2

current_balance = 1000

class FaceRecognition:
    def __init__(self, controller):
        self.controller = controller
        self.saved_face = None

    def recognize_face(self):
        cap = cv2.VideoCapture(0) 
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Display the camera feed for 2 seconds to capture faces
        for i in range(2):
            ret, frame = cap.read()
            cv2.imshow(f"Capture {i+1}", frame)
            cv2.waitKey(1000)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        #start face recognition loop
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to access camera!")
                self.controller.show_frame('StartPage')
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                self.saved_face = gray[y:y+h, x:x+w]
                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                detected_face = gray[y:y+h, x:x+w]
                cv2.imshow('Detected Face', detected_face)
                
            cv2.imshow('Face Recognition', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

         # Release resources and transition to the next page
        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1000)
        self.transition_to_next_page()
        

    def transition_to_next_page(self):
        if self.saved_face is not None:
            self.controller.show_frame('MenuPage')
        else:
            self.controller.show_frame(StartPage)

    

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance':tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, WithdrawPage, DepositPage, BalancePage, TransferPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")
    

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        self.controller.title('Securitex')
        self.controller.state('zoomed')
       # self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        heading_label = tk.Label(self, text='SECURITEX ATM',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

        password_label = tk.Label(self,text='Enter your password',font=('orbitron',13),bg='#3d3d5c',fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,textvariable=my_password,font=('orbitron',12),width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black',show='*')
            
        password_entry_box.bind('<FocusIn>',handle_focus_in)

        def check_password():
           if my_password.get() == '123':
               my_password.set('')
               incorrect_password_label['text']=''
               self.face_recognition = FaceRecognition(self.controller)
               self.face_recognition.recognize_face()
               controller.show_frame('MenuPage')
           else:
               incorrect_password_label['text']='Incorrect Password'
                
        enter_button = tk.Button(self,text='Enter',command=check_password,relief='raised',borderwidth = 3,width=40,height=3)
        enter_button.pack(pady=10)

        incorrect_password_label = tk.Label(self,text='', font=('orbitron',13),fg='white',bg='#33334d',anchor='n')
        incorrect_password_label.pack(fill='both',expand=True)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\visa.png")
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\mastercard.png")
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\american-express.png")
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()
        
class FaceRecognitionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Face Recognition Page", font=("Arial", 24))
        self.label.pack(pady=20)

        self.info_label = tk.Label(self, text="Click the button to start face recognition:")
        self.info_label.pack()
        
        start_recognition_button = tk.Button(self, text="Start Face Recognition", command=self.start_recognition)
        start_recognition_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back to Password Page", command=self.back_to_password)
        self.back_button.pack(pady=10)

    def start_recognition(self):
        self.controller.face_recognition.recognize_face()
        # After face recognition, if face matches, proceed to MenuPage
        # If face doesn't match, show the Password Page
        # You'll need to implement this logic in FaceRecognition class
    def back_to_password(self):
        self.controller.show_frame("StartPage") 

class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller
   
        heading_label = tk.Label(self,text='SECURITEX ATM',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self,text='Main Menu',font=('orbitron',13), fg='white',bg='#3d3d5c')
        main_menu_label.pack()

        selection_label = tk.Label(self,text='Please make a selection',font=('orbitron',13), fg='white', bg='#3d3d5c',anchor='w')
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)

        def withdraw():
            controller.show_frame('WithdrawPage')
            
        withdraw_button = tk.Button(button_frame,text='Withdraw',command=withdraw,relief='raised',borderwidth=3,width=50,height=5)
        withdraw_button.grid(row=0,column=0,pady=5)

        def deposit():
            controller.show_frame('DepositPage')
            
        deposit_button = tk.Button(button_frame,text='Deposit',command=deposit, relief='raised',borderwidth=3,width=50,height=5)
        deposit_button.grid(row=1,column=0,pady=5)

        def balance():
            controller.show_frame('BalancePage')
            
        balance_button = tk.Button(button_frame, text='Balance', command=balance,relief='raised',borderwidth=3,width=50,
        height=5)
        balance_button.grid(row=2,column=0,pady=5)

        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame,text='Exit',command=exit,relief='raised',borderwidth=3,width=50,height=5)
        exit_button.grid(row=4,column=0,pady=5)

        def transfer():
            controller.show_frame('TransferPage')
            
        transfer_button = tk.Button(button_frame, text='Transfer', command=transfer, relief='raised', borderwidth=3, width=50, height=5)
        transfer_button.grid(row=3, column=0, pady=5)  # Adjust row and column as needed
        


        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\visa.png")
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\mastercard.png")
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\american-express.png")
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


class WithdrawPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller


        heading_label = tk.Label(self,text='SECURITEX ATM',font=('orbitron',45,'bold'), foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        choose_amount_label = tk.Label(self,text='Choose the amount you want to withdraw',font=('orbitron',13),fg='white',bg='#3d3d5c')
        choose_amount_label.pack()

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)

        def withdraw(amount):
            global current_balance
            current_balance -= amount
            controller.shared_data['Balance'].set(current_balance)
            controller.show_frame('MenuPage')
           
        twenty_button = tk.Button(button_frame,text='20', command=lambda:withdraw(20),relief='raised',borderwidth=3,width=50,height=5)
        twenty_button.grid(row=0,column=0,pady=5)

        forty_button = tk.Button(button_frame,text='40',command=lambda:withdraw(40),relief='raised',borderwidth=3,width=50,height=5)
        forty_button.grid(row=1,column=0,pady=5)

        sixty_button = tk.Button(button_frame,text='60', command=lambda:withdraw(60),relief='raised',borderwidth=3,width=50,height=5)
        sixty_button.grid(row=2,column=0,pady=5)

        eighty_button = tk.Button(button_frame, text='80', command=lambda:withdraw(80),relief='raised',borderwidth=3,
        width=50,height=5)
        eighty_button.grid(row=3,column=0,pady=5)

        one_hundred_button = tk.Button(button_frame,text='100', command=lambda:withdraw(100), relief='raised',borderwidth=3,
        width=50,height=5)
        one_hundred_button.grid(row=0,column=1,pady=5,padx=555)

        two_hundred_button = tk.Button(button_frame,text='200',command=lambda:withdraw(200), relief='raised',borderwidth=3,width=50,height=5)
        two_hundred_button.grid(row=1,column=1,pady=5)
 
        three_hundred_button = tk.Button(button_frame,text='300',command=lambda:withdraw(300),relief='raised',borderwidth=3,width=50,height=5)
        three_hundred_button.grid(row=2,column=1,pady=5)

        cash = tk.StringVar()
        other_amount_entry = tk.Entry(button_frame,textvariable=cash,width=59, justify='right')
        other_amount_entry.grid(row=3,column=1,pady=5,ipady=30)

        def other_amount(_):
            global current_balance
            current_balance -= int(cash.get())
            controller.shared_data['Balance'].set(current_balance)
            cash.set('')
            controller.show_frame('MenuPage')
            
        other_amount_entry.bind('<Return>',other_amount)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\visa.png")
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\mastercard.png")
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\american-express.png")
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()
   

class DepositPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,text='SECURITEX ATM',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,text='Enter amount', font=('orbitron',13), bg='#3d3d5c',fg='white')
        enter_amount_label.pack(pady=10)

        self.cash = tk.StringVar()
        deposit_entry = tk.Entry(self,textvariable=self.cash,font=('orbitron',12),width=22)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            global current_balance
            try:
                amount = int(self.cash.get())
                current_balance += amount
                self.controller.shared_data['Balance'].set(current_balance)
                self.controller.show_frame('MenuPage')
                self.cash.set('')
                messagebox.showinfo("Success", f"Successfully deposited {amount}!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric amount")
            
        enter_button = tk.Button(self,text='Enter',command=deposit_cash, relief='raised',borderwidth=3,width=40,height=3)
        enter_button.pack(pady=10)

        two_tone_label = tk.Label(self,bg='#33334d')
        two_tone_label.pack(fill='both',expand=True)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\visa.png")
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\mastercard.png")
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\american-express.png")
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


class BalancePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        
        heading_label = tk.Label(self,text='SECURITEX ATM',font=('orbitron',45,'bold'), foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_label = tk.Label(self,textvariable=controller.shared_data['Balance'],font=('orbitron',13),fg='white', bg='#3d3d5c', anchor='w')
        balance_label.pack(fill='x')

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)

        def menu():
            controller.show_frame('MenuPage')
            
        menu_button = tk.Button(button_frame,command=menu,text='Menu',relief='raised',borderwidth=3,width=50,height=5)
        menu_button.grid(row=0,column=0,pady=5)

        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame, text='Exit', command=exit, relief='raised',borderwidth=3,width=50,height=5)
        exit_button.grid(row=1,column=0,pady=5)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\visa.png")
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\mastercard.png")
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file=r"C:\Users\bhakt\Downloads\american-express.png")
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

valid_account_numbers = ['12345678','98564372','43567321','90856312']
class TransferPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self, text='SECURITEX ATM', font=('orbitron', 45, 'bold'), foreground='#ffffff', background='#3d3d5c')
        heading_label.pack(pady=25)

        enter_acc_label = tk.Label(self, text='Enter Account Number', font=('orbitron', 13), bg='#3d3d5c', fg='white')
        enter_acc_label.pack(pady=10)

        self.account_number = tk.StringVar()
        account_entry = tk.Entry(self, textvariable=self.account_number, font=('orbitron', 12), width=22)
        account_entry.pack(ipady=7)

        enter_amount_label = tk.Label(self, text='Enter Amount to Transfer', font=('orbitron', 13), bg='#3d3d5c', fg='white')
        enter_amount_label.pack(pady=10)

        self.transfer_amount = tk.StringVar()
        amount_entry = tk.Entry(self, textvariable=self.transfer_amount, font=('orbitron', 12), width=22)
        amount_entry.pack(ipady=7)

        transfer_button = tk.Button(self, text='Transfer', command=self.transfer, relief='raised', borderwidth=3, width=50, height=5)
        transfer_button.pack()  # Adjust layout as needed

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        # Other elements like card images and time label go here...

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()

    def transfer(self):
        global current_balance
        try:
            amount = int(self.transfer_amount.get())
            account_number = self.account_number.get()

            if account_number not in valid_account_numbers:
                messagebox.showerror("Invalid account number","Invalid account number")
                self.controller.show_frame('MenuPage')
                return 
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a valid positive amount")
            elif amount > current_balance:
                messagebox.showerror("Error", "Insufficient funds for the transfer")
            else:
                current_balance -= amount
                self.controller.shared_data['Balance'].set(current_balance)
                self.transfer_amount.set('')
                self.account_number.set('')
                self.controller.show_frame('MenuPage')
                messagebox.showinfo("Success", f"Successfully transferred {amount} to account {self.account_number.get()}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount")

        enter_button = tk.Button(self, text='Transfer', command="ransfer", relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        # Other elements like card images and time label go here...

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()