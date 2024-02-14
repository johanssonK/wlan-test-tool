import tkinter
import customtkinter as ctk

"""
All three layout methods supported by tKinter are used:
	Place is used for the Left/right frames
	Pack is used inside the left menu
	Grid is used in the right menus
"""

class App(ctk.CTk):
	def __init__(self, title, size):
		
		# main setup
		super().__init__()
		self.wm_title(title)
		self.geometry(f'{size[0]}x{size[1]}')
		self.minsize(size[0],size[1])
		self.maxsize(size[0],size[1]) # fixed size

		# appearance
		ctk.set_default_color_theme('blue') # blue is standard
		ctk.set_appearance_mode('dark') # system is standard but might get ugly with the blue colors?
		#titlebar_icon = tkinter.PhotoImage(file='wifi.png')  
		#self.wm_iconphoto(True, titlebar_icon)
		
		# widgets
		self.left_frame = ctk.CTkFrame(master=self)
		self.left_frame.place(x=0, y=0, relwidth=0.3, relheight=0.2) # relwidth here must match the remainder of the Rightmenu relwidth
		self.create_left_widgets()
		self.menuRight = RightMenu(self)

		# initial state is with COM tab open
		self.callback_button1()

		# run 
		self.mainloop()

	def create_left_widgets(self):
		# create the push buttons 
		#image1 = ImageTk.PhotoImage(Image.open('settings.png'))
		self.menu_button1 = ctk.CTkButton(self.left_frame, text='General', corner_radius=0, command=self.callback_button1)
		self.menu_button2 = ctk.CTkButton(self.left_frame, text='TX',  corner_radius=0, command=self.callback_button2)
		self.menu_button3 = ctk.CTkButton(self.left_frame, text='RX',  corner_radius=0, command=self.callback_button3)

		# place the buttons
		self.menu_button1.pack(expand=True, fill='both', pady=0)
		self.menu_button2.pack(expand=True, fill='both', pady=0)
		self.menu_button3.pack(expand=True, fill='both', pady=0)

	def callback_button1(self):
		""" General """
		self.menuRight.COM.show_menu()
		self.menuRight.TX.hide_menu()
		self.menuRight.RX.hide_menu()
		self.reset_button_style()
		self.menu_button1.configure(fg_color=['#000000', '#3F8AC5'])
	
	def callback_button2(self):
		""" TX """
		self.menuRight.COM.hide_menu()
		self.menuRight.TX.show_menu()
		self.menuRight.RX.hide_menu()
		self.reset_button_style()
		self.menu_button2.configure(fg_color=['#000000', '#3F8AC5'])
		#print(self.menu_button2.cget(attribute_name="fg_color")) #['#3B8ED0', '#1F6AA5']
		#print(self.menu_button2.cget(attribute_name="border_spacing"))
	
	def callback_button3(self):
		""" RX """
		self.menuRight.COM.hide_menu()
		self.menuRight.TX.hide_menu()
		self.menuRight.RX.show_menu()
		self.reset_button_style()
		self.menu_button3.configure(fg_color=['#000000', '#3F8AC5'])
	
	def reset_button_style(self):
		self.menu_button1.configure(fg_color=['#3B8ED0', '#1F6AA5'])
		self.menu_button2.configure(fg_color=['#3B8ED0', '#1F6AA5'])
		self.menu_button3.configure(fg_color=['#3B8ED0', '#1F6AA5'])





class RightMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)
		self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)
		self.COM = COMMenu(self)
		self.TX =TxMenu(self)
		self.RX =RxMenu(self)


class TxMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		label = ctk.CTkLabel(self, text="TX")
		button = ctk.CTkButton(self, text="TX")

		label.pack(expand=True, fill='both')
		button.pack(expand=True, fill='both', pady=10)
	
	def show_menu(self):
		self.pack(side='left', expand=True, fill='both')
	
	def hide_menu(self):
		self.pack_forget()


class RxMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		label = ctk.CTkLabel(self, text="RX")
		button = ctk.CTkButton(self, text="RX")

		label.pack(expand=True, fill='both')
		button.pack(expand=True, fill='both', pady=10)

	def show_menu(self):
		self.pack(side='left', expand=True, fill='both')
	
	def hide_menu(self):
		self.pack_forget()


class COMMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		# list of county codes that are supported
		countries = ['ALL', 'US', 'DE']

		# define the widgets
		label_ip = ctk.CTkLabel(self, text="IP")
		label_country = ctk.CTkLabel(self, text="Country Code")
		entry_ip = ctk.CTkEntry(self, placeholder_text="192.168.xx.xxx")
		combo_country = ctk.CTkComboBox(self, values=countries, command=self.get_country)

		radio_button_frame = ctk.CTkFrame(self)
		radio_button_label = ctk.CTkLabel(radio_button_frame, text='Firmware')
		self.radio_var = tkinter.IntVar(value=0)
		radio_button1 = ctk.CTkRadioButton(master=self, variable=self.radio_var, value=0, text='MFG')
		radio_button2 = ctk.CTkRadioButton(master=self, variable=self.radio_var, value=1, text='STD')

		# define the grid (use uniform='a' to avoid that empty cells takes up less space than cells with widgets)
		self.columnconfigure((0, 1), weight=1, uniform='a')
		self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

		# place the widgets
		label_ip.grid(row=0, column=0, sticky='w', padx=20)
		entry_ip.grid(row=0, column=1, sticky='ew', padx=20)
		label_country.grid(row=1, column=0, sticky='w', padx=20)
		combo_country.grid(row=1, column=1, sticky='ew', padx=20)

		radio_button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')
		radio_button_label.grid(row=2, column=0)
		radio_button1.grid(row=2, column=0)
		radio_button2.grid(row=2, column=1)

	def get_country(self, country):
		print(f"country={country}")

	def show_menu(self):
		self.pack(side='left', expand=True, fill='both')
	
	def hide_menu(self):
		self.pack_forget()


if __name__ == "__main__":
	App('WLAN Test Tool', (600,600))
