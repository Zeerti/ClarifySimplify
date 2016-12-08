
#Added Colors - updated the GUI color scheme
#Revised clarifyicon searching.
    #Checks for the icon, if it can't find it, it then will ask to move the mouse over the icon and save the location




#BUGS#
'''
    Refresh Clarify doesn't always work correctly. Correct field in clarify must be selected first. Investigate how to select that field.
'''


import tkinter
import re
import pyautogui
import pyperclip
import time
import os
 
class ClarifySimplify(tkinter.Frame):
 
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
 
        self._initialize()  

        #print('{}, {}'.format(self.screenWidth, self.screenHeight))
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

        #self.clarifyIconPixel = None

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
            return

    def _delete_all_text(self):
        self.textBox1.delete(1.0, 'end')
        self.textBox2.delete(1.0, 'end')
        self.textBox3.delete(1.0, 'end')
 
    def _send_to_clarify(self):
        #########Format All text to conform to ticket standards#######
        ##############################################################

        #Format Reason Calling#
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

        ####Save formatted text to temp var#############
        ################################################
        self.text_reason_calling = self.textBox1.get(1.0, 'end') 
        self.text_attempted_steps = self.textBox2.get(1.0, 'end')
        self.text_resolution_steps = self.textBox3.get(1.0, 'end')

        self._setup_ticket()


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
        #######pyautogui.press('space') #press hangup

        #CLOSE CALL SPLIT 15 tabs to close case,
        '''
        for i in range(0,16):
            pyautogui.press('tab')
        pyautogui.press('enter')
        pyautogui.press('esc')
        for i in range(0,4)
            pyautogui.press('enter')
        pyautogui.hotkey('control', 'v')
        for i in range(0,10)
            pyautogui.press('tab') #Restoral date
        enter x2
        tabx3 closing codes

            Verifone Reboot Close codes
            h, h, e, e, e, h, 3, 3, p 
        tabx6
        enter
        '''


        
        #DEFER CALL SPLIT 18 tabs for defer
        '''
        for i in range(0,19):  
            pyautogui.press('tab')
        pyautogui.press('space')
        time.sleep(5)
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 'd')
        pyautogui.typewrite('pix')
        #pyautogui.press('enter') 
        '''



        '''
        ###### Add notes to case #####
        ======================================================
            Control + H to get into Call Log
            Click Once -- Notes Section -- CALL LOG  (50, 60) #############VERIFY WORKING ON ALL MONITORS###########
            Tab x5 to phone #
            Tab x1 to Outgoing call
            Down arrow x1 to set outgoing call
            Tab x3 back to Notes Section
            Tab x2 HangUp
            ---------- DEFER -------------
            Tab x3 Defer (Might be 12?)
            Space
            Grab Defer Time (Set to 5 second pause)
            Enter
            Defer Reason - i range(0-7)
            down x(i)
            enter
            Control + d
            'pix'
            Enter

            ---------- CLOSE ------------
            Tab x2 Close
            Space
            Enter
            Esc
            Enter x3



            #Check if closing or deferring

            I attempted to test test customers test
            verified that the test was a successful test
            changed test settings to test to fix problem.


        '''

    def _refresh_clarify(self):

        #Ensure clarify taskbar icon coords are saved
        if self.clarifyLocation is None:
            self._locateClarify(False)

        if self.clarifyLocation is not None:
            currentMousePosition = pyautogui.position()
            clarifyRefreshColumnLocation = (self.screenWidth * .2), (self.screenHeight * .4)
            pyautogui.click(self.clarifyLocation)
            pyautogui.click(clarifyRefreshColumnLocation)
            pyautogui.moveTo(currentMousePosition) ###ONLY MOVES WITHIN PRIMARY SCREEN##
            pyautogui.press('p')
            #time.sleep(.5)
            pyautogui.press('p')
            time.sleep(.25)
            pyautogui.hotkey('alt', 'tab') #return to this program#

            

 
 
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
    application.configure
    application.mainloop()


