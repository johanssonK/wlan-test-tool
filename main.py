import json
import tkinter
import logging
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

An external json file ("system-definition.json") is used as a look-up table to validate and present valid combinations.
"""

# System definitions
fw = ['MFG', 'STD']

# The system constraints not mentioned above are defined in a json file
with open('system-definition.json') as json_file:
    data = json.load(json_file)


logger = logging.getLogger('wltrx-gui')


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
        self.debug = DebugWindow(self)

        # initial state is with COM tab open and debug hidden
        self.callback_button1()
        self.debug.hide()
        logger.debug("init")
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
        self.debug.show()
        
    
    def reset_button_style(self):
        self.menu_button1.configure(fg_color='transparent')
        self.menu_button2.configure(fg_color='transparent')
        self.menu_button3.configure(fg_color='transparent')


class RightMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.place(relx=0.35, y=0, relwidth=0.65, relheight=1)
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
        Add country code here instead of COM menu
        """
        
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
        logger.debug(f"band={band}")
        #self.combo_standard.configure(state='normal', values=list(data[band].keys()))
        self.validate()
    
    def get_standard(self, standard):
        self.standard = standard
        logger.debug(f"standard={standard}")
        #self.combo_rate.configure(state='normal', values=list(data[self.band][self.standard].keys()))
        self.validate()

    def get_rate(self, rate):
        self.rate = rate
        logger.debug(f"rate={rate}")
        #self.combo_bw.configure(state='normal', values=list(data[self.band][self.standard][self.rate].keys()))
        self.validate()
    
    def get_bw(self, bw):
        self.bw = bw
        logger.debug(f"bw={bw}")
        #self.combo_core.configure(state='normal', values=list(data[self.band][self.standard][self.rate][self.bw].keys()))
        self.validate()
    
    def get_core(self, core):
        self.core = core
        logger.debug(f"core={core}")
        #self.combo_country.configure(state='normal', values=list(data[self.band][self.standard][self.rate][self.bw][self.core].keys()))
        self.validate()

    def get_country(self, country):
        self.country = country
        logger.debug(f"country={country}")
        #self.combo_channel.configure(state='normal', values=data[self.band][self.standard][self.rate][self.bw][self.core][self.country])
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
        try:
            #data.keys() --> ['2.4GHz', '5GHz']
            if(self.band in list(data.keys())):
                #Band ok!

                #Standard
                #self.combo_standard.set('') måste slänga in en sådan här i en except check för att fimpa det dåliga värdet som ligger kvar
                self.combo_standard.configure(state='normal', values=list(data[self.band].keys()))

                #Rate
                self.combo_rate.configure(state='disabled')
                self.combo_rate.set('') # tar ingen effekt om knappen är disabled i kodraden ovan

                #BW
                self.combo_bw.configure(state='disabled')
                self.combo_bw.set('') 
                
                #Core
                self.combo_core.configure(state='disabled')
                self.combo_core.set('') 
                
                #Country
                self.combo_country.configure(state='disabled')
                self.combo_country.set('') 

                #Channel
                self.combo_channel.configure(state='disabled')
                self.combo_channel.set('')
            else:
                self.combo_rate.set('') # tar ingen effekt om knappen är disabled i kodraden ovan
                self.combo_bw.set('')
                self.combo_core.set('')
                self.combo_country.set('')
                self.combo_channel.set('')

            #list(data[self.band].keys()) --> ['11b', '11g', '11n', '11ac'] if 2.4GHz
            if(self.standard in list(data[self.band].keys())):
                #Band ok!
                #Standard ok!

                #Rate
                self.combo_rate.configure(state='normal', values=list(data[self.band][self.standard].keys()))
                
                #BW
                self.combo_bw.configure(state='disabled')
                self.combo_bw.set('') 

                #Core
                self.combo_core.configure(state='disabled')
                self.combo_core.set('')

                #Country
                self.combo_country.configure(state='disabled')
                self.combo_country.set('')

                #Channel
                self.combo_channel.configure(state='disabled')
                self.combo_channel.set('') 

            # list(data[self.band][self.standard].keys()) --> ['1Mbps', '2Mbps', '11Mbps', '5.5Mbps'] (if 2.4GHz 11b)
            if(self.rate in list(data[self.band][self.standard].keys())):
                #Band ok!
                #Standard ok!
                #Rate ok!

                #BW
                self.combo_bw.configure(state='normal', values=list(data[self.band][self.standard][self.rate].keys()))
                
                #Core
                self.combo_core.configure(state='disabled')
                self.combo_core.set('')

                #Country
                self.combo_country.configure(state='disabled')
                self.combo_country.set('')

                #Channel
                self.combo_channel.configure(state='disabled')
                self.combo_channel.set('')

            if(self.bw in list(data[self.band][self.standard][self.rate].keys())):
                #Band ok!
                #Standard ok!
                #Rate ok!
                #BW ok!
                
                #Core
                self.combo_core.configure(state='normal', values=list(data[self.band][self.standard][self.rate][self.bw].keys()))

                #Country
                self.combo_country.configure(state='disabled')
                self.combo_country.set('')

                #Channel
                self.combo_channel.configure(state='disabled')
                self.combo_channel.set('')

            if(self.core in list(data[self.band][self.standard][self.rate][self.bw].keys())):
                #Band ok!
                #Standard ok!
                #Rate ok!
                #BW ok!
                #Core ok!

                #Country
                self.combo_country.configure(state='normal', values=list(data[self.band][self.standard][self.rate][self.bw][self.core].keys()))
                
                #Channel
                self.combo_channel.configure(state='disabled')
                self.combo_channel.set('')

            if(self.country in list(data[self.band][self.standard][self.rate][self.bw][self.core].keys())):
                #Band ok!
                #Standard ok!
                #Rate ok!
                #BW ok!
                #Core ok!
                #Country ok!

                #Channel
                self.combo_channel.configure(state='normal', values=data[self.band][self.standard][self.rate][self.bw][self.core][self.country])

            if(self.channel in list(data[self.band][self.standard][self.rate][self.bw][self.core][self.country].keys())):
                #print("7")
                pass
        except:
            pass


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
        logger.debug("load FW")

    def get_country(self, country):
        logger.debug(f"country={country}")
    
    def get_fw(self, fw):
        logger.debug("get FW")

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
        self.title("DEBUG")
        self.geometry("800x200")
        self.minsize(800, 200)
        self.maxsize(800, 200)

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
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%H:%M:%S')
        formatter = logging.Formatter(fmt='%(asctime)-s - %(levelname)-8s - %(message)-s')
        #formatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-10s :: %(message)s')
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        
        """
        logger.info('hello world')
        logger.warning('be careful!')
        logger.debug('debug')
        logger.error('you will see this')
        logger.critical('critical is logged too!')
        """

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
    App('WLAN Test Tool', (500,400))
