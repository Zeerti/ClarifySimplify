
#Added error function to display error messages in a new window
#Added in defer window to set defer time
#Added in close window to set closing codes
#Added in function to close child window(s)




#BUGS#
'''
    Refresh Clarify doesn't always work correctly. Correct field in clarify must be selected first. Investigate how to select that field.
'''


import tkinter       #GUI
#import re           #Unused right now
import pyautogui     #Automate keyboard and mouse evetns
import pyperclip     #Send text to clipboard
import time          #get current times and sleep function
import os            #Fetch File Path
 
class ClarifySimplify(tkinter.Frame):
 
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
 
        self._initialize()  
        parent.geometry('{}x{}'.format(round(self.screenWidth/1.5), round(self.screenHeight/1.5)))

 
    def _initialize(self):

        self.filePath = os.path.dirname(__file__)
        self.iconFilePath = os.path.join(self.filePath, 'clarifyicon.png')

        self.defaultFont = ('Times', '16', 'bold')
        self.textWidgetFont = ('Times', '12')

        self.colorDarkBackground = '#263238'
        self.colorBlueText = '#82AAE0' #130 170 224
        self.colorPurpleText = '#C792EA' #199 146 234
        self.colorOrangeText = '#F78C6C' #247 140 108
        self.colorRedText = '#FF5366' #255 83 102
        self.colorLimeBorderHighlight = '#A4D409' #164 212 9
        self.colorLimeText = '#C3E88D' #195 232 141

        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.clarifyIconQueue = self._makeRegion(0, 0, round(self.screenWidth*.288), round(self.screenHeight/2))

        textBoxLabel1 = tkinter.Label(text='Reason Calling', bg=self.colorDarkBackground, fg=self.colorLimeText, font = self.defaultFont)
        textBoxLabel1.grid(row=0, column=0, sticky='SNEW')

        self.textBox1 = tkinter.Text(height=4, width= 100)
        self.textBox1.grid(row=1, column=0, sticky='SNEW')
        self.textBox1.configure(font = self.textWidgetFont, selectbackground = self.colorLimeBorderHighlight, highlightbackground = self.colorLimeText, highlightthickness=2, background=self.colorDarkBackground, foreground=self.colorLimeText)

        textBoxLabel2 = tkinter.Label(text='Attempted Steps', font = self.defaultFont, bg=self.colorDarkBackground, fg=self.colorPurpleText, pady = 5)
        textBoxLabel2.grid(row=2, column=0, sticky='SNEW')

        self.textBox2 = tkinter.Text( height=10, width=100)
        self.textBox2.grid(row=3, column=0, sticky='SNEW')
        self.textBox2.configure(font = self.textWidgetFont, selectbackground = self.colorLimeBorderHighlight, highlightbackground = self.colorPurpleText, highlightthickness=2, background=self.colorDarkBackground, foreground=self.colorPurpleText)
        
        textBoxLabel3 = tkinter.Label(text='Resolution Steps', font = self.defaultFont, bg=self.colorDarkBackground, fg=self.colorOrangeText, pady = 5)
        textBoxLabel3.grid(row=4, column=0, sticky='SNEW')

        self.textBox3 = tkinter.Text(height=10, width=100)
        self.textBox3.grid(row=5, column=0, sticky='SNEW')
        self.textBox3.configure(font = self.textWidgetFont, selectbackground = self.colorLimeBorderHighlight,highlightbackground = self.colorOrangeText, highlightthickness=2, background=self.colorDarkBackground, foreground=self.colorOrangeText)
        

        self.button_ClearAll = tkinter.Button(text="Clear All Fields", command=self._delete_all_text)
        self.button_ClearAll.grid(row=6, column=0, sticky='SW')

        self.button_SendClarify = tkinter.Button(text='Send To Clarify', command = self._send_to_clarify)
        self.button_SendClarify.grid(row= 6, column=0, sticky='SE')

        self.button_RefreshClarify = tkinter.Button(text='Refresh Clarify', command = self._refresh_clarify)
        self.button_RefreshClarify.grid(row=6, column=0, sticky='S' )

        self.checkCloseTicket = None
        self.checkBox_CloseTicket = tkinter.Checkbutton(text='Close Ticket', variable=self.checkCloseTicket, onvalue="True", offvalue="False", bg=self.colorDarkBackground, fg=self.colorOrangeText, font=self.defaultFont)
        self.checkBox_CloseTicket.grid(column=1, row=2)

        self.checkDeferTicket = None
        self.checkBox_DeferTicket = tkinter.Checkbutton(text='Defer Ticket', variable=self.checkDeferTicket, onvalue="True", offvalue="False", bg=self.colorDarkBackground, fg=self.colorOrangeText, font=self.defaultFont, highlightbackground=self.colorDarkBackground, command=self._defer_ticket)
        self.checkBox_DeferTicket.grid(column=1, row=4)

   
        self._locateClarify(True)

        self.columnconfigure(0, weight=1)
        for i in range(0,7):
            self.rowconfigure(i, weight=1)

        self.update()

      
    ##Search Taskbar for pixelicon.png##  =======Consider Removing, slow/doesn't work right==========
    ####################################
    def _locateClarify(self, iconSearch):
        if iconSearch == True:
            self.taskBarRegion = self._makeRegion(0, round(self.screenHeight* .957), round(self.screenWidth*.863), self.screenHeight)
            self.clarifyLocation = pyautogui.locateCenterOnScreen(str(self.iconFilePath), region=self.taskBarRegion)
            print(self.clarifyLocation)

        else:
            self.windowLocateClarify = tkinter.Toplevel()
            self.windowLocateClarify.title("Locating Clarify...")
            self.windowLocateClarify.grid()
            self.windowLocateClarify.bind_all('<Control-Key-1>', self._keyboard_handler)
            self.windowLocateClarify.geometry("{}x{}+{}+{}".format(round(self.screenWidth/1.5), 50, round(self.screenWidth/2-(self.screenWidth/3)), round(self.screenHeight/2)))
            self.windowLocateClarify.configure(bg=defaultbg)

            message = tkinter.Label(self.windowLocateClarify, text="Please move the mouse cursor to the Clarify Icon and press Control and 1 at the same time", bg=self.colorDarkBackground, fg=self.colorRedText, font = self.defaultFont)
            message.grid(column=0, row = 0, sticky='NSEW')
            self.windowLocateClarify.columnconfigure(0, weight=1)
            self.windowLocateClarify.rowconfigure(0, weight=1)
            

    def _makeRegion(self, regionMostLeft, regionMostTop, regionWidth, regionHeight):
        self.newRegion = regionMostLeft, regionMostTop, regionWidth, regionHeight
        return self.newRegion


    def _keyboard_handler(self, event):
        if event.keysym == '1':
            self.clarifyLocation = pyautogui.position()
            self.windowLocateClarify.destroy()
        else:
            print(event)
            print(event)
            print(event)
        


    def _delete_all_text(self):
        self.textBox1.delete(1.0, 'end')
        self.textBox2.delete(1.0, 'end')
        self.textBox3.delete(1.0, 'end')
 

    def _send_to_clarify(self):
        
        self._insert_ticket_schema()
        self._setup_ticket()
        if self.checkBox_CloseTicket==True: #Check which checkbox is active
            self._close_ticket()
        else:
            return

        if self.checkBox_DeferTicket==True: #Check which checkbox is active
            self._defer_ticket()
        else:
            return


    def _setup_ticket(self):
        pyautogui.click(self.clarifyLocation) #Ensure clarify is focused window
        pyautogui.hotkey('ctrl', 'h')
        time.sleep(.5)
        pyautogui.click(self.screenWidth*.5, self.screenHeight*.6) #Select correct text box for tab positioning

        for i in range(0,6):
            pyautogui.press('tab')
        pyautogui.press('down') #Change from incoming to outgoing

        for i in range(0,3):
            pyautogui.press('tab')
        
        #paste in all fields from this program
        pyperclip.copy(self.text_reason_calling)
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy(self.text_attempted_steps)
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy(self.text_resolution_steps)
        pyautogui.hotkey('ctrl', 'v')

        for i in range(0,2): #3 tabs to hit hangup
            pyautogui.press('tab')
        pyautogui.press('space') #press hangup


    def _close_ticket(self):
        print("UNFINISHED CLOSE TICKET FUNCTION")
    
        # Checkbox checked
        # create new window
        # Have basic closure codes
        # include 'Not one of these'
        # Have a checkbox for closure reason
        # when box is checked close window
        # run close functions


        #  #CLOSE CALL 15 tabs to close case from main section
        
        # for i in range(0,16):
        #     pyautogui.press('tab')
        # pyautogui.press('enter')
        # pyautogui.press('esc')
        # for i in range(0,4)
        #     pyautogui.press('enter')
        # pyautogui.hotkey('control', 'v')
        # for i in range(0,10)
        #     pyautogui.press('tab') #Restoral date
        # enter x2
        # tabx3 closing codes

        #Verifone Reboot Close codes
        #       h, h, e, e, e, h, 3, 3, p 
        #Online Ordering restart
        #       h, s, o, h, px6, p
        #Smart Receipt
        #       h, s, c, h, px6, p
        #Generic Open/Close
        #       h, o, o, o, h, cx4, p
        #NTOCB
        #       h, o, n, h, cx4, p



        # tabx6
        # enter

        # Need to figure out how to check if it will     
        

    def _defer_ticket(self):

        self._window_defer_time()
        print("UNFINISHED DEFER TICKET FUNCTION")
        
        # defer checked
        # create new window
        # Have a defer time
        # have a defer reason
        # okay button to confirm


        # for i in range(0,19):  
        #     pyautogui.press('tab')
        # pyautogui.press('space')
        # time.sleep(5)
        # pyautogui.press('enter')
        # pyautogui.hotkey('ctrl', 'd')

        # pyautogui.typewrite('pix')
        # #pyautogui.press('enter') 


        # ---------- DEFER -------------
        #     Tab x3 Defer (Might be 12?)
        #     Space
        #     Grab Defer Time (Set to 5 second pause)
        #     Enter
        #     Defer Reason - i range(0-7)
        #     down x(i)
        #     enter
        #     Control + d
        #     'pix'
        #     Enter
    
        
    def _insert_ticket_schema(self):
        #########Format All text to conform to ticket standards#######
        ##############################################################

        self.textBox1.insert(1.0, "===============\nREASON CALLING\n===============\n")
        for i in range(0, (int(self.textBox1.index('end').split('.')[0]) - 1)):
            self.textBox1.insert(i+1.0, "@ ")
        self.textBox1.insert('end', "\n\n")

        self.textBox2.insert(1.0, "================\nATTEMPTED STEPS\n================\n")
        for i in range(0, (int(self.textBox2.index('end').split('.')[0]) - 1)):
            self.textBox2.insert(i+1.0, "! ")
        self.textBox2.insert('end', "\n\n")

        self.textBox3.insert(1.0, "=================\nRESOLUTION STEPS\n=================\n")
        for i in range(0, (int(self.textBox3.index('end').split('.')[0]) - 1)):
            self.textBox3.insert(i+1.0, "- ") 
        self.textBox3.insert('end', "\n\n")   

        self.text_reason_calling = self.textBox1.get(1.0, 'end') 
        self.text_attempted_steps = self.textBox2.get(1.0, 'end')
        self.text_resolution_steps = self.textBox3.get(1.0, 'end')


    def _refresh_clarify(self):

        #Ensure clarify taskbar icon coords are saved via pixelsearching or explicitly
        if self.clarifyLocation is None:
            self._locateClarify(False)

        if self.clarifyLocation is not None:
            currentMousePosition = pyautogui.position()
            clarifyRefreshColumnLocation = (self.screenWidth * .2), (self.screenHeight * .4)
            pyautogui.click(self.clarifyLocation)
            pyautogui.click(clarifyRefreshColumnLocation)
            pyautogui.moveTo(currentMousePosition) ###ONLY MOVES WITHIN PRIMARY MONITOR##
            pyautogui.press('p')
            pyautogui.press('p')
            time.sleep(.25)
            pyautogui.hotkey('alt', 'tab') #return to this program# -- Doesn't seem to work 100% of the time.

    def _window_error(self, errorMessage):
        self.windowError = tkinter.Toplevel()
        self.windowError.resizable(0,0)
        self.windowError.title('!#!ERROR!#!')
        self.windowError.grid()
        self.errorLabel = tkinter.Label(self.windowError, fg = self.colorPurpleText, font=self.textWidgetFont, text=errorMessage)
        self.errorLabel.grid(column=0, row=0)

        self.buttonOkay = tkinter.Button(self.windowError, text='Close', command=self._destroy_window(self.windowError))
        self.buttonOkay.grid(row=1, column=0)

        print("UNFINISHED FUNCTION")

    def _window_closure_code(self):
        print("UNFINISHED FUNCTION")

    def _window_defer_time(self):
        self.windowDeferTime = tkinter.Toplevel()
        print(self.windowDeferTime)
        print("SEPARATE")
        self.windowDeferTime.title("Set a defer time")
        self.windowDeferTime.grid()
        #self.windowDeferTime.bind_all(('tab', self._keyboard_handler))

        #All input fields
        self.dayInput = tkinter.Entry(self.windowDeferTime, fg = self.colorPurpleText, font=self.defaultFont)
        self.dayInput.grid(column=0, row=0, sticky='W')

        self.monthInput = tkinter.Entry(self.windowDeferTime, fg=self.colorPurpleText, bg=self.colorDarkBackground)
        self.dayInput.grid(column=0, row=0)

        self.yearInput = tkinter.Entry(self.windowDeferTime, fg=self.colorPurpleText, bg=self.colorDarkBackground)
        self.dayInput.grid(column=0, row=0, sticky='E')

        self.hourInput = tkinter.Entry(self.windowDeferTime, fg=self.colorPurpleText, bg=self.colorDarkBackground)
        self.dayInput.grid(column=0, row=1, sticky='W')

        self.minuteInput = tkinter.Entry(self.windowDeferTime, fg=self.colorPurpleText, bg=self.colorDarkBackground)
        self.dayInput.grid(column=0, row=1)

        self.buttonClose = tkinter.Button(self.windowDeferTime) 
        self.buttonClose.grid(column=0, row=2, sticky='S')
        #Error checking for not digit
        if str.isdigit(self.dayInput.get()) == False:
            self._window_error('Day is incorrect, Please input a value between 1-31')

        elif str.isdigit(self.monthInput.get()) == False:
            self._window_error('Month is incorrect, Please input a value between 1-31')

        elif str.isdigit(self.yearInput.get()) == False:
            self._window_error('Year is incorrect, Please input a value between 1-31')

        elif str.isdigit(self.hourInput.get()) == False:
            self._window_error('Hour is incorrect, Please input a value between 1-31')

        elif str.isdigit(self.minuteInput.get()) == False:
            self._window_error('Minute is incorrect, Please input a value between 1-31')

        


        print("UNFINISHED FUNCTION")

    def _destroy_window(self, window):
        print(window)
        window.destroy()

            

 
 
if __name__ == "__main__":
    root = tkinter.Tk()
    
    root.title("Clarify Clarity Feather Edition")

    root.columnconfigure(0, weight=1)
    for i in range(0,7):
        root.rowconfigure(i, weight=1)
    defaultbg = '#263238'
    root.configure(bg=defaultbg)
    root.update()


    application = ClarifySimplify(root)
    application.grid()
    application.mainloop()


