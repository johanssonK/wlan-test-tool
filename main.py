import tkinter
from tkinter import ttk
import customtkinter as ctk
from PIL import Image

"""
Copyright (C) 2024 Karl Johansson xmoontool@protonmail.com

Two different layout methods, supported by tKinter, are used:
Place is used for the Left/right frames.
Grid is used inside the left and right menus.

The navigation frame style is inspired from: https://github.com/TomSchimansky/CustomTkinter/blob/master/documentation_images/image_example_dark_Windows.png 
The layout and object oriented style is inspired from: https://github.com/clear-code-projects/tkinter-complete/blob/main/2%20layout/2_9_classes.py

All icons are downloaded from: https://www.iconsdb.com/
A Custom hex color is choosen on all icons #3B8ED0
They are downloaded as 64x64 ico files
"""

# System definitions
band = ['2G4', '5G']
standard = ['a', 'b', 'g', 'n', 'ac']
rate = ['1', '2', '5.5', '11']
channel = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
bw = ['20', '40', '80']
core = ['1', '2', 'MIMO']
countries = ['ALL', 'DE', 'US'] # list of county codes that are supported
fw = ['MFG', 'STD']


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
		self.left_frame = ctk.CTkFrame(master=self, corner_radius=0)
		self.left_frame.place(x=0, y=0, relwidth=0.35, relheight=1) # relwidth here must match the remainder of the Rightmenu relwidth
		self.create_left_widgets()
		self.menuRight = RightMenu(self)

		# initial state is with COM tab open
		self.callback_button1()

		# run 
		self.mainloop()

	def create_left_widgets(self):
		# create images
		self.logo_image = ctk.CTkImage(Image.open('wifi-64.ico'), size=(32, 32))
		self.com_image= ctk.CTkImage(Image.open('settings.ico'), size=(20, 20))
		self.tx_image= ctk.CTkImage(Image.open('data-transfer-upload-64.ico'), size=(20, 20))
		self.rx_image= ctk.CTkImage(Image.open('data-transfer-download-64.ico'), size=(20, 20))
		self.console_image= ctk.CTkImage(Image.open('console-64.ico'), size=(20, 20))

		# create the top label
		self.logo_label = ctk.CTkLabel(self.left_frame, text='WLTRX for noobs', image=self.logo_image, 
								 	compound='top', font=ctk.CTkFont(size=15, weight='bold'))
		
		# create the push buttons 
		self.menu_button1 = ctk.CTkButton(self.left_frame, text='General', corner_radius=0, height=40, border_spacing=10, 
									fg_color='transparent', text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
									image=self.com_image, anchor="w", command=self.callback_button1,
									font=ctk.CTkFont(size=15, weight='normal'))
		self.menu_button2 = ctk.CTkButton(self.left_frame, text='Tx', corner_radius=0, height=40, border_spacing=10, 
									fg_color='transparent', text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
									image=self.tx_image, anchor="w", command=self.callback_button2,
									font=ctk.CTkFont(size=15, weight='normal'))
		self.menu_button3 = ctk.CTkButton(self.left_frame, text='Rx', corner_radius=0, height=40, border_spacing=10, 
									fg_color='transparent', text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
									image=self.rx_image, anchor="w", command=self.callback_button3,
									font=ctk.CTkFont(size=15, weight='normal'))
		self.menu_button4 = ctk.CTkButton(self.left_frame, text='Dbg', corner_radius=0, height=40, border_spacing=10, 
									fg_color='transparent', text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
									image=self.console_image, anchor="ws", command=self.callback_button4,
									font=ctk.CTkFont(size=15, weight='normal'))

		# place the widgets with grid technique
		self.columnconfigure(0, weight=1, uniform='a')
		self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
		self.logo_label.grid(row=0, column=0, sticky="", padx=20, pady=20)
		self.menu_button1.grid(row=1, column=0, sticky="ew")
		self.menu_button2.grid(row=2, column=0, sticky="ew")
		self.menu_button3.grid(row=3, column=0, sticky="ew")
		# add separator before dbg button
		#sep = ttk.Separator(self,orient='horizontal')
		#sep.grid(row=4, column=0, sticky="new")
		#self.empty_label=ctk.CTkLabel(self.left_frame, text="") #add empty label to get spacing between separator and console button
		#self.empty_label.grid(row=5, column=0)
		self.menu_button4.grid(row=4, column=0, sticky="ew")
		

	def callback_button1(self):
		""" General """
		self.menuRight.COM.show_menu()
		self.menuRight.TX.hide_menu()
		self.menuRight.RX.hide_menu()
		self.reset_button_style()
		self.menu_button1.configure(fg_color=['gray75', 'gray25'])
	
	def callback_button2(self):
		""" TX """
		self.menuRight.COM.hide_menu()
		self.menuRight.TX.show_menu()
		self.menuRight.RX.hide_menu()
		self.reset_button_style()
		self.menu_button2.configure(fg_color=['gray75', 'gray25'])
		#print(self.menu_button2.cget(attribute_name="fg_color")) #['#3B8ED0', '#1F6AA5']
		#print(self.menu_button2.cget(attribute_name="border_spacing"))
	
	def callback_button3(self):
		""" RX """
		self.menuRight.COM.hide_menu()
		self.menuRight.TX.hide_menu()
		self.menuRight.RX.show_menu()
		self.reset_button_style()
		self.menu_button3.configure(fg_color=['gray75', 'gray25'])
	
	def callback_button4(self):
		""" DEBUG CONSOLE """
		DebugWindow(self)
	
	def reset_button_style(self):
		self.menu_button1.configure(fg_color='transparent')
		self.menu_button2.configure(fg_color='transparent')
		self.menu_button3.configure(fg_color='transparent')


class RightMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)
		self.place(relx=0.35, y=0, relwidth=0.65, relheight=1)
		self.COM = COMMenu(self)
		self.TX =TxMenu(self)
		self.RX =RxMenu(self)


class TxMenu(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(master=parent)

		# define system
		

		# define the labels
		label_band = ctk.CTkLabel(self, text="Frequency Band")
		label_standard = ctk.CTkLabel(self, text="WLAN Standard")
		label_rate = ctk.CTkLabel(self, text="Data Rate")
		label_channel = ctk.CTkLabel(self, text="Channel")
		label_bw = ctk.CTkLabel(self, text="Bandwith")
		label_core = ctk.CTkLabel(self, text="Tx Core")
		"""
		Add country code here instead of COM menu
		"""
		
		# define the combo boxes
		combo_band = ctk.CTkComboBox(self, values=band, command=self.get_band)
		combo_standard = ctk.CTkComboBox(self, values=standard, command=self.get_standard)
		combo_rate = ctk.CTkComboBox(self, values=rate, command=self.get_rate)
		combo_channel = ctk.CTkComboBox(self, values=channel, command=self.get_channel)
		combo_bw = ctk.CTkComboBox(self, values=bw, command=self.get_bw)
		combo_core = ctk.CTkComboBox(self, values=core, command=self.get_core)

		# define buttons
		button_start = ctk.CTkButton(self, text="Start", command=self.callback_start)
		button_stop = ctk.CTkButton(self, text="Stop", command=self.callback_stop)

		# place the widgets with grid technique
		self.columnconfigure((0, 1), weight=1, uniform='a')
		self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
		label_band.grid(row=0, column=0, sticky="e", padx=10)
		label_standard.grid(row=1, column=0, sticky="e", padx=10)
		label_rate.grid(row=2, column=0, sticky="e", padx=10)
		label_bw.grid(row=3, column=0, sticky="e", padx=10)
		label_channel.grid(row=4, column=0, sticky="e", padx=10)
		label_core.grid(row=5, column=0, sticky="e", padx=10)

		combo_band.grid(row=0, column=1, sticky="ew", padx=10)
		combo_standard.grid(row=1, column=1, sticky="ew", padx=10)
		combo_rate.grid(row=2, column=1, sticky="ew", padx=10)
		combo_bw.grid(row=3, column=1, sticky="ew", padx=10)
		combo_channel.grid(row=4, column=1, sticky="ew", padx=10)
		combo_core.grid(row=5, column=1, sticky="ew", padx=10)

		button_stop.grid(row=6, column=0)
		button_start.grid(row=6, column=1)
	
	def callback_start(self):
		print("someone pressed start")
	
	def callback_stop(self):
		print("someone pressed stop")

	def get_band(self, band):
		print(f"band={band}")
	
	def get_standard(self, standard):
		print(f"standard={standard}")

	def get_rate(self, rate):
		print(f"rate={rate}")

	def get_channel(self, channel):
		print(f"channel={channel}")

	def get_bw(self, bw):
		print(f"bw={bw}")

	def get_core(self, core):
		print(f"core={core}")
	
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

		# define the widgets
		label_ip = ctk.CTkLabel(self, text="IP")
		#label_country = ctk.CTkLabel(self, text="Country Code")
		label_fw = ctk.CTkLabel(self, text="FW")
		entry_ip = ctk.CTkEntry(self, placeholder_text="192.168.xx.xxx")
		#combo_country = ctk.CTkComboBox(self, values=countries, command=self.get_country)
		combo_fw = ctk.CTkComboBox(self, values=fw, command=self.get_fw)
		"""
		radio_button_frame = ctk.CTkFrame(self)
		radio_button_label = ctk.CTkLabel(master=radio_button_frame, text='Firmware')
		self.radio_var = tkinter.IntVar(value=0)
		radio_button1 = ctk.CTkRadioButton(master=radio_button_frame, variable=self.radio_var, value=0, text='MFG')
		radio_button2 = ctk.CTkRadioButton(master=radio_button_frame, variable=self.radio_var, value=1, text='STD')
		"""
		button_load = ctk.CTkButton(self, text="Load FW", command=self.callback_load_fw)
		
		# define the grid (use uniform='a' to avoid that empty cells takes up less space than cells with widgets)
		self.columnconfigure(0, weight=1, uniform='a')
		self.columnconfigure(1, weight=2, uniform='a')
		self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a') # same number of rows as in TxMenu otherwise it looks too big

		# place the widgets
		label_ip.grid(row=1, column=0, sticky='e', padx=10)
		entry_ip.grid(row=1, column=1, sticky='ew', padx=20)
		#label_country.grid(row=2, column=0, sticky='e', padx=10)
		#combo_country.grid(row=2, column=1, sticky='ew', padx=20)
		label_fw.grid(row=2, column=0, sticky='e', padx=10)
		combo_fw.grid(row=2, column=1, sticky='ew', padx=20)

		#radio_button_frame.grid(row=3, column=1, rowspan=2, columnspan=1, padx=20, pady=10, sticky='new')
		#radio_button_label.grid(row=0, column=1, padx=20, sticky="w")
		#radio_button1.grid(row=1, column=1, padx=20, pady=10, sticky="e")
		#radio_button2.grid(row=2, column=1, padx=20, pady=10, sticky="e")
		button_load.grid(row=3, column=1, sticky='ew', padx=20)

	def callback_load_fw(self):
		print("load FW")

	def get_country(self, country):
		print(f"country={country}")
	
	def get_fw(self, fw):
		pass

	def show_menu(self):
		self.pack(side='left', expand=True, fill='both')
	
	def hide_menu(self):
		self.pack_forget()


class DebugWindow(ctk.CTkToplevel):
     
    def __init__(self, master=None):
         
        super().__init__(master=master)
        self.title("DEBUG")
        self.geometry("600x200")

 


if __name__ == "__main__":
	App('WLAN Test Tool', (500,400))
