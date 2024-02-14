import customtkinter as ctk


class App(ctk.CTk):
	def __init__(self, title, size):
		
		# main setup
		super().__init__()
		self.title(title)
		self.geometry(f'{size[0]}x{size[1]}')
		self.minsize(size[0],size[1])
		self.maxsize(size[0],size[1]) # fixed size

		# widgets 
		self.menuLeft = LeftMenu(self)
		self.menuRight = RightMenu(self)

		# run 
		self.mainloop()


class LeftMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)
		self.place(x=0, y=0, relwidth=0.3, relheight=0.2)
		self.create_widgets()

	def create_widgets(self):
		
		# create the push buttons 
		menu_button1 = ctk.CTkButton(self, text='Button 1', corner_radius=0, command=self.callback_button1)
		menu_button2 = ctk.CTkButton(self, text='Button 2', corner_radius=0, command=self.callback_button2)
		menu_button3 = ctk.CTkButton(self, text='Button 3', corner_radius=0, command=self.callback_button3)

		# place the buttons
		menu_button1.pack(expand=True, fill='both', pady=1)
		menu_button2.pack(expand=True, fill='both', pady=1)
		menu_button3.pack(expand=True, fill='both', pady=1)

	def callback_button1(self):
		print("CALLBACK BUTTON 1")
		#self.menuRight.pack(self, side='left', expand=True, fill='both', padx=20, pady=20)
		#self.pack(self.menuRight, side='left', expand=True, fill='both', padx=20, pady=20)
		#TxMenu.show_menu(self)
	
	def callback_button2(self):
		print("CALLBACK BUTTON 2")
	
	def callback_button3(self):
		print("CALLBACK BUTTON 3")



class RightMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)
		self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)
		#Entry(self, 'Entry 1','Button 1','green')
		#Entry(self, 'Entry 2','Button 2','blue')
		self.COM = COMMenu(self)
		self.TX =TxMenu(self)
		self.RX =RxMenu(self)

"""
class Entry(ctk.CTkFrame):
	def __init__(self, parent, label_text, button_text, label_background):
		super().__init__(parent)

		label = ctk.CTkLabel(self, text = label_text)
		button = ctk.CTkButton(self, text = button_text)

		label.pack(expand=True, fill='both')
		button.pack(expand=True, fill='both', pady=10)

		self.pack(side = 'left', expand = True, fill = 'both', padx = 20, pady = 20)
"""


class TxMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		label = ctk.CTkLabel(self, text="TX")
		button = ctk.CTkButton(self, text="TX")

		label.pack(expand=True, fill='both')
		button.pack(expand=True, fill='both', pady=10)

		#self.pack(side='left', expand=True, fill='both', padx=20, pady=20)
		self.hide_menu()
	
	def show_menu(self):
		self.pack(side='left', expand=True, fill='both', padx=20, pady=20)
	
	def hide_menu(self):
		self.pack_forget()


class RxMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		label = ctk.CTkLabel(self, text="RX")
		button = ctk.CTkButton(self, text="RX")

		label.pack(expand=True, fill='both')
		button.pack(expand=True, fill='both', pady=10)

		#self.pack(side='left', expand=True, fill='both', padx=20, pady=20)

class COMMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		label = ctk.CTkLabel(self, text="COM")
		button = ctk.CTkButton(self, text="COM")

		label.pack(expand=True, fill='both')
		button.pack(expand=True, fill='both', pady=10)

		#self.pack(side='left', expand=True, fill='both', padx=20, pady=20)

if __name__ == "__main__":
	App('WLAN Test Tool', (600,600))
