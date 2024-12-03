import json
import tkinter
import logging
import re
import os
from tkinter import ttk
import customtkinter as ctk
from CTkMenuBar import *                 #pip install CTkMenuBar
from CTkMessagebox import CTkMessagebox  #pip install CTkMessagebox
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

An external json file ("system-definition.json") is used as a look-up table to validate and present valid combinations.
"""

# System definitions
fw = ['MFG', 'STD']

# The system constraints not mentioned above are defined in a json file
with open('system-definition.json') as json_file:
    data = json.load(json_file)


logger = logging.getLogger('wltrx-gui')


class App(ctk.CTk):
    def __init__(self, title, size, className):

        # main setup
        super().__init__(className=className)
        self.wm_title(title)
        
        #get center coordinates of the screen and place the window there
        self.ws = self.winfo_screenwidth() # width of the screen
        self.hs = self.winfo_screenheight() # height of the screen
        self.x = int((self.ws/2) - (size[0]/2))
        self.y = int((self.hs/2) - (size[1]/2))
        self.geometry(f'{size[0]}x{size[1]}+{self.x}+{self.y}')
        #self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1]) # fixed size

        # appearance
        ctk.set_default_color_theme('blue') # blue is standard
        ctk.set_appearance_mode('dark') # system is standard but might get ugly with the blue colors?
        
        # program icon
        self.titlebar_icon = tkinter.PhotoImage(file='./assets/wifi.png') # need to be png format
        self.wm_iconphoto(True, self.titlebar_icon)
        
        # widgets
        self.left_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.left_frame.place(x=0, y=0, relwidth=0.30, relheight=1) # relwidth here must match the remainder of the Rightmenu relwidth
        self.create_left_widgets()
        self.menuRight = RightMenu(self)
        self.debug = DebugWindow(self)

        # initial state is with COM tab open and debug hidden
        self.callback_button1()
        self.debug.hide()
        logger.debug("init")

        # Add a CTkMenuBar if clicking on the WiFi logo
        self.click_counter = 0

        # run 
        self.mainloop()

    def create_left_widgets(self):
        # create images
        self.logo_image = ctk.CTkImage(Image.open('./assets/wireless-64.ico'), size=(32, 32))
        self.com_image= ctk.CTkImage(Image.open('./assets/settings.ico'), size=(20, 20))
        self.tx_image= ctk.CTkImage(Image.open('./assets/data-transfer-upload-64.ico'), size=(20, 20))
        self.rx_image= ctk.CTkImage(Image.open('./assets/data-transfer-download-64.ico'), size=(20, 20))
        self.console_image= ctk.CTkImage(Image.open('./assets/console-64.ico'), size=(20, 20))

        # create the top label
        self.logo_label = ctk.CTkLabel(self.left_frame, text='WTT', image=self.logo_image, 
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
        self.menu_button4.grid(row=4, column=0, sticky="ew")

        # bind event to the WiFi logo --> mouse click will show menu. Hover will show tooltip
        self.logo_label.bind('<Button-1>', self.toggle_menu)
        self.logo_label.bind('<Enter>', self.show_tooltip)
        self.logo_label.bind('<Leave>', self.hide_tooltip)
    
    def show_tooltip(self, event):
        """
        Inspiration from: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
        """
        self.tooltip=tkinter.Toplevel()
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')
        self.label=tkinter.Label(self.tooltip,text="Click on the WiFi logo to toggle the menu")
        self.label.pack()

    def hide_tooltip(self,event):
        self.tooltip.destroy()

    def show_menu(self):
        #TODO: Creating a new menu every time is ugly. It should just be a hide/show. But self.config(menu=self.menu) does not work. Need to investigate
        self.menu = CTkMenuBar(self, bg_color='grey20', border_width=0)
        button_1 = self.menu.add_cascade("File")
        button_2 = self.menu.add_cascade("Help")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="Exit", command=lambda: self.destroy())

        dropdown2 = CustomDropdownMenu(widget=button_2)
        dropdown2.add_option(option="About", command=lambda: CTkMessagebox(title='About', 
                                                                           message='Need help? Send an email to Karl at: xmoontool@protonmail.com \n\nIcons by: https://icons8.com/'))
    
    def hide_menu(self):
        self.menu.destroy()

    def toggle_menu(self, event):
        self.click_counter+=1
        if(self.click_counter%2 != 0):
            self.show_menu()
        else:
            self.hide_menu()   

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
        self.debug.show()
        
    
    def reset_button_style(self):
        self.menu_button1.configure(fg_color='transparent')
        self.menu_button2.configure(fg_color='transparent')
        self.menu_button3.configure(fg_color='transparent')


class RightMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.place(relx=0.30, y=0, relwidth=0.70, relheight=1)
        self.COM = COMMenu(self)
        self.TX = TxMenu(self)
        self.RX = RxMenu(self)


class TxMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Define variables that can keep track of choosen Tx values
        self.band = [""]
        self.standard = [""]
        self.rate = [""]
        self.bw = [""]
        self.core = [""]
        self.country = [""]
        self.channel = [""]

        # define the labels
        label_band = ctk.CTkLabel(self, text="Frequency Band")
        label_standard = ctk.CTkLabel(self, text="WLAN Standard")
        label_rate = ctk.CTkLabel(self, text="Data Rate")
        label_bw = ctk.CTkLabel(self, text="Bandwith")
        label_core = ctk.CTkLabel(self, text="Tx Core")
        label_country = ctk.CTkLabel(self, text="Country Code")
        label_channel = ctk.CTkLabel(self, text="Channel")
        
        """
        Define the combo boxes
        The 'band' combo box will always be populated with data.keys(). The rest of the boxes need to
        be populated dynamically with an individual postcommand that parses the json constraints file.
        """
        self.combo_band = ctk.CTkComboBox(self, values=list(data.keys()), command=self.get_band)
        self.combo_standard = ctk.CTkComboBox(self, values=self.standard, command=self.get_standard, state='disabled')
        self.combo_rate = ctk.CTkComboBox(self, values=self.rate, command=self.get_rate, state='disabled')
        self.combo_channel = ctk.CTkComboBox(self, values=self.channel, command=self.get_channel, state='disabled')
        self.combo_bw = ctk.CTkComboBox(self, values=self.bw, command=self.get_bw, state='disabled')
        self.combo_core = ctk.CTkComboBox(self, values=self.core, command=self.get_core, state='disabled')
        self.combo_country = ctk.CTkComboBox(self, values=self.country, command=self.get_country, state='disabled')

        # set all combos to NULL initially
        self.combo_band.set('')     
        self.combo_standard.set('')
        self.combo_rate.set('')     
        self.combo_channel.set('')  
        self.combo_bw.set('')    
        self.combo_core.set('')
        self.combo_country.set('')

        # define buttons
        button_start = ctk.CTkButton(self, text="Start", command=self.callback_start)
        button_stop = ctk.CTkButton(self, text="Stop", command=self.callback_stop)

        # place the widgets with grid technique
        # Order: band -> standard -> rate -> bw -> core -> country_code -> channel
        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
        label_band.grid(row=0, column=0, sticky="e", padx=10)
        label_standard.grid(row=1, column=0, sticky="e", padx=10)
        label_rate.grid(row=2, column=0, sticky="e", padx=10)
        label_bw.grid(row=3, column=0, sticky="e", padx=10)
        label_core.grid(row=4, column=0, sticky="e", padx=10)
        label_country.grid(row=5, column=0, sticky="e", padx=10)
        label_channel.grid(row=6, column=0, sticky="e", padx=10)

        self.combo_band.grid(row=0, column=1, sticky="ew", padx=10)
        self.combo_standard.grid(row=1, column=1, sticky="ew", padx=10)
        self.combo_rate.grid(row=2, column=1, sticky="ew", padx=10)
        self.combo_bw.grid(row=3, column=1, sticky="ew", padx=10)
        self.combo_core.grid(row=4, column=1, sticky="ew", padx=10)
        self.combo_country.grid(row=5, column=1, sticky="ew", padx=10)
        self.combo_channel.grid(row=6, column=1, sticky="ew", padx=10)

        button_stop.grid(row=7, column=0)
        button_start.grid(row=7, column=1)
    
    def callback_start(self):
        logger.debug("someone pressed start")
    
    def callback_stop(self):
        logger.debug("someone pressed stop")

    # Reminder; order is: band -> standard -> rate -> bw -> core -> country_code -> channel
    def get_band(self, band):
        self.band = band
        self.standard = ''
        self.rate = ''
        self.bw = ''
        self.core = ''
        self.country = ''
        self.channel = ''
        logger.debug(f"band={band}")
        self.validate()
    
    def get_standard(self, standard):
        self.standard = standard
        self.rate = ''
        self.bw = ''
        self.core = ''
        self.country = ''
        self.channel = ''
        logger.debug(f"standard={standard}")
        self.validate()

    def get_rate(self, rate):
        self.rate = rate
        self.bw = ''
        self.core = ''
        self.country = ''
        self.channel = ''
        logger.debug(f"rate={rate}")
        self.validate()
    
    def get_bw(self, bw):
        self.bw = bw
        self.core = ''
        self.country = ''
        self.channel = ''
        logger.debug(f"bw={bw}")
        self.validate()
    
    def get_core(self, core):
        self.core = core
        self.country = ''
        self.channel = ''
        logger.debug(f"core={core}")
        self.validate()

    def get_country(self, country):
        self.country = country
        self.channel = ''
        logger.debug(f"country={country}")
        self.validate()
    
    def get_channel(self, channel):
        self.channel = channel
        logger.debug(f"channel={channel}")
        self.validate()
    
    def show_menu(self):
        self.pack(side='left', expand=True, fill='both')
    
    def hide_menu(self):
        self.pack_forget()

    def validate(self):
        """
        Validation if choosen combination is valid. System is defined in system-definition.json
        Need to enable / disable the correct buttons based on the validation result
        Also need to erase the invalid value, even if it is disabled
        """
        logger.debug(f"band={self.band}, standard={self.standard}, rate={self.rate}, bw={self.bw}, core={self.core}, country={self.country}, channel={self.channel}")
        
        # we have a nested try/except because the data[self.band][self.standard][self.rate][self.bw][self.core][self.country] is not fully populated from the beginning
        try:
            if(self.channel in list(data[self.band][self.standard][self.rate][self.bw][self.core][self.country])):
                self.check_channel_ok()
            else:
                self.check_country_ok()
        
        except:
            try:
                if(self.country in list(data[self.band][self.standard][self.rate][self.bw][self.core].keys())):
                    self.check_country_ok()
                else:
                    self.check_core_ok()
            except:
                try:
                    if(self.core in list(data[self.band][self.standard][self.rate][self.bw].keys())):
                        self.check_core_ok()
                    else:
                        self.check_bw_ok()
                except:
                    try:
                        if(self.bw in list(data[self.band][self.standard][self.rate].keys())):
                            self.check_bw_ok()
                        else:
                            self.check_rate_ok()
                    except:
                        try:
                            # list(data[self.band][self.standard].keys()) --> ['1Mbps', '2Mbps', '11Mbps', '5.5Mbps'] (if 2.4GHz 11b)
                            if(self.rate in list(data[self.band][self.standard].keys())):
                                self.check_rate_ok()
                            else:
                                self.check_standard_ok()
                        except:
                            try:
                                #list(data[self.band].keys()) --> ['11b', '11g', '11n', '11ac'] if 2.4GHz
                                if(self.standard in list(data[self.band].keys())):
                                    self.check_standard_ok()
                                else:
                                    #Here we enter when we set band first time, the try is successfull, but since standard is empty we get into this else
                                    self.check_band_ok()
                            except:
                                try:
                                    #data.keys() --> ['2.4GHz', '5GHz']
                                    if(self.band in list(data.keys())):
                                        #Band ok!
                                        self.check_band_ok()
                                except:
                                    pass
    
    def check_band_ok(self):
        #data.keys() --> ['2.4GHz', '5GHz']
        #Band ok!

        self.enable_all_combos()

        #Standard
        self.standard = ''
        self.combo_standard.set('')
        self.combo_standard.configure(state='normal', values=list(data[self.band].keys()))

        #Rate
        self.rate = ''
        self.combo_rate.set('')
        self.combo_rate.configure(state='disabled')

        #BW
        self.bw = ''
        self.combo_bw.set('')
        self.combo_bw.configure(state='disabled')
        
        #Core
        self.core = ''
        self.combo_core.set('')
        self.combo_core.configure(state='disabled')
        
        #Country
        self.country = ''
        self.combo_country.set('')
        self.combo_country.configure(state='disabled')

        #Channel
        self.channel = ''
        self.combo_channel.set('')
        self.combo_channel.configure(state='disabled')

    def check_standard_ok(self):
        #Band ok!
        #Standard ok!

        self.enable_all_combos()

        #Rate
        self.rate = ''
        self.combo_rate.set('')
        self.combo_rate.configure(state='normal', values=list(data[self.band][self.standard].keys()))
        
        #BW
        self.bw = ''
        self.combo_bw.configure(state='disabled')

        #Core
        self.core = ''
        self.combo_core.configure(state='disabled')

        #Country
        self.country = ''
        self.combo_country.configure(state='disabled')

        #Channel
        self.channel = ''
        self.combo_channel.configure(state='disabled')

    def check_rate_ok(self):
        #Band ok!
        #Standard ok!
        #Rate ok!

        self.enable_all_combos()

        #BW
        self.bw = ''
        self.combo_bw.set('')
        self.combo_bw.configure(state='normal', values=list(data[self.band][self.standard][self.rate].keys()))
        
        #Core
        self.core = ''
        self.combo_core.configure(state='disabled')

        #Country
        self.country = ''
        self.combo_country.configure(state='disabled')

        #Channel
        self.channel = ''
        self.combo_channel.configure(state='disabled')

    def check_bw_ok(self):
        #Band ok!
        #Standard ok!
        #Rate ok!
        #BW ok!
        
        self.enable_all_combos()

        #Core
        self.core = ''
        self.combo_core.set('')
        self.combo_core.configure(state='normal', values=list(data[self.band][self.standard][self.rate][self.bw].keys()))

        #Country
        self.country = ''
        self.combo_country.configure(state='disabled')

        #Channel
        self.channel = ''
        self.combo_channel.configure(state='disabled')

    def check_core_ok(self):
        #Band ok!
        #Standard ok!
        #Rate ok!
        #BW ok!
        #Core ok!

        self.enable_all_combos()

        #Country
        self.country = ''
        self.combo_country.set('')
        self.combo_country.configure(state='normal', values=list(data[self.band][self.standard][self.rate][self.bw][self.core].keys()))
        
        #Channel
        self.channel = ''
        self.combo_channel.configure(state='disabled')

    def check_country_ok(self):
        #Band ok!
        #Standard ok!
        #Rate ok!
        #BW ok!
        #Core ok!
        #Country ok!

        self.enable_all_combos()
        
        #Channel
        self.channel = ''
        self.combo_channel.set('')
        self.combo_channel.configure(state='normal', values=data[self.band][self.standard][self.rate][self.bw][self.core][self.country])

    def check_channel_ok(self):
        #if we get here, all is good
        pass

    def enable_all_combos(self):
        # if the combo box is disabled and we try combo.set(''), it has not effect. So enabling all, before updating the values in them is safer than just assume they are enabled
        self.combo_channel.configure(state='normal')
        self.combo_standard.configure(state='normal')
        self.combo_rate.configure(state='normal')
        self.combo_bw.configure(state='normal')
        self.combo_core.configure(state='normal')
        self.combo_country.configure(state='normal')
        self.combo_channel.configure(state='normal')
    

class RxMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Define variables that can keep track of choosen Tx values
        self.band = [""]
        self.core = [""]
        self.channel = [""]
        self.nbr_of_packets = [""]

        # define the labels
        label_band = ctk.CTkLabel(self, text="Frequency Band")
        label_core = ctk.CTkLabel(self, text="Rx Core")
        label_channel = ctk.CTkLabel(self, text="Channel")
        label_packets = ctk.CTkLabel(self, text="Number of packets")

        # define the combo boxes and entry box
        self.combo_band = ctk.CTkComboBox(self, values=list(data.keys()), command=self.get_band)
        self.combo_core = ctk.CTkComboBox(self, values=self.core, command=self.get_core, state='disabled')
        self.combo_channel = ctk.CTkComboBox(self, values=self.channel, command=self.get_channel, state='disabled')
        self.packet_entry = ctk.CTkEntry(self, placeholder_text="1000")

        # set all combos to NULL initially
        self.combo_band.set('')     
        self.combo_core.set('')
        self.combo_channel.set('')     

        # define buttons
        button_start = ctk.CTkButton(self, text="Start", command=self.callback_start)
        button_stop = ctk.CTkButton(self, text="Stop", command=self.callback_stop)

        # place the widgets with grid technique
        # Order: band -> core -> channel -> nbr of packets
        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
        label_band.grid(row=0, column=0, sticky="e", padx=10)
        label_core.grid(row=1, column=0, sticky="e", padx=10)
        label_channel.grid(row=2, column=0, sticky="e", padx=10)
        label_packets.grid(row=3, column=0, sticky="e", padx=10)

        self.combo_band.grid(row=0, column=1, sticky="ew", padx=10)
        self.combo_core.grid(row=1, column=1, sticky="ew", padx=10)
        self.combo_channel.grid(row=2, column=1, sticky="ew", padx=10)
        self.packet_entry.grid(row=3, column=1, sticky="ew", padx=10)

        button_stop.grid(row=6, column=0)
        button_start.grid(row=6, column=1)

    def get_band(self, band):
        pass

    def get_core(self, core):
        pass

    def get_channel(self, channel):
        pass

    def callback_start(self):
        logger.debug("someone pressed start")
    
    def callback_stop(self):
        logger.debug("someone pressed stop")

    def show_menu(self):
        self.pack(side='left', expand=True, fill='both')
    
    def hide_menu(self):
        self.pack_forget()


class COMMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # define the widgets
        label_ip = ctk.CTkLabel(self, text="IP")
        label_fw = ctk.CTkLabel(self, text="FW")
        self.entry_ip = ctk.CTkEntry(self, placeholder_text="192.168.xx.xxx")
        self.combo_fw = ctk.CTkComboBox(self, values=fw, command=self.get_fw) 
        self.button_load = ctk.CTkButton(self, text="Load FW", command=self.callback_load_fw)
        
        # define the grid (use uniform='a' to avoid that empty cells takes up less space than cells with widgets)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a') # same number of rows as in TxMenu otherwise it looks too big

        # place the widgets
        label_ip.grid(row=1, column=0, sticky='e', padx=10)
        self.entry_ip.grid(row=1, column=1, sticky='ew', padx=20)

        label_fw.grid(row=2, column=0, sticky='e', padx=10)
        self.combo_fw.grid(row=2, column=1, sticky='ew', padx=20)

        self.button_load.grid(row=3, column=1, sticky='ew', padx=20)

    def callback_load_fw(self):
        ip = self.entry_ip.get()
        logger.debug(f"load FW, IP = {ip}")
        self.set_ip(ip)
        #os.system("python3 ./dut-control/test.py")
        os.system("python3 ./dut-control/load_mfg_fw.py")

    def get_country(self, country):
        logger.debug(f"country={country}")
    
    def get_fw(self, fw):
        logger.debug("get FW")

    def set_ip(self, ip):
        """
        The config.ini contains a line with 'IP =  10.8.17.121' that needs to be replaced with the new IP. Use regexp
        """
        with open ('./dut-control/config.ini', 'r+') as f:
            file = f.read()
            file = re.sub(r'(?<=IP = ).*$' , ip, file, flags=re.MULTILINE) # change everything after 'IP = ' to the new ip argument
            f.seek(0)
            f.write(file)
            f.truncate()

    def show_menu(self):
        self.pack(side='left', expand=True, fill='both')
    
    def hide_menu(self):
        self.pack_forget()


class DebugWindow(ctk.CTkToplevel):
    """ 
    This is the debug window that pops up when pressing on dbg. It is a ctk textbox that uses the custom
    logging handler DebugHandler to show text
    A lot of inspiration from https://github.com/beenje/tkinter-logging-text-widget/blob/master/main.py 
    """
     
    def __init__(self, master=None): 
        super().__init__(master=master)

        #define window size
        self.w = 800
        self.h = 200
        
        #get center coordinates of the screen and place the window there
        self.ws = self.winfo_screenwidth() # width of the screen
        self.hs = self.winfo_screenheight() # height of the screen
        self.x = int((self.ws/2) - (self.w/2))
        self.y = int((self.hs/2) - (self.h/2))
        self.geometry(f'{self.w}x{self.h}+{self.x}+{self.y}')
        #self.geometry("800x200") # this will show up in the upper left corner

        self.title("DEBUG")

        # fully constraint the window
        self.minsize(self.w, self.h)
        self.maxsize(self.w, self.h)

        # When pressing the x button in the titlebar it hides instead of gets destroyed -> closing it will create problems trying to open it again
        self.protocol("WM_DELETE_WINDOW", self.hide)

        # place the widgets with grid technique
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # Create a textbox that takes up the full debug window
        self.text_area = ctk.CTkTextbox(self, state='disabled') # Read-only
        self.text_area.grid(row=0, column=0, sticky="nswe")
        self.text_area.configure(font=ctk.CTkFont(size=13, weight='normal'))

        # Create tags so that the different log levels get differnt colors
        self.text_area.tag_config('INFO', foreground='white')
        self.text_area.tag_config('DEBUG', foreground='gray')
        self.text_area.tag_config('WARNING', foreground='orange')
        self.text_area.tag_config('ERROR', foreground='red')
        self.text_area.tag_config('CRITICAL', foreground='red', underline=1)
        
        # Create the custom log handler so that all logger messages are automatically shown in the log window
        log_handler = DebugHandler(self.text_area)

        # Create a file log handler. Can be useful to be able to send this log for support
        file_handler = logging.FileHandler('./logs/log.txt', 'w') #overwrite old log
        # create the formatter
        formatter = logging.Formatter(fmt='%(asctime)-s - %(levelname)-8s - %(message)-s')
        
        # add formatter and handlers
        log_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.addHandler(file_handler)

    def show(self):
        self.deiconify()
    
    def hide(self):
        self.withdraw()


class DebugHandler(logging.Handler):
    """
    This class allows you to log to a Tkinter Text or ScrolledText widget
    It is inspired by: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    """

    def __init__(self, textWidget):
        logging.Handler.__init__(self)
        self.text = textWidget

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tkinter.END, msg + '\n', record.levelname)
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tkinter.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)
    App(title='WLAN Test Tool', size=(500,400), className='wtt')
