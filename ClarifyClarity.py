
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
import time
 
class ClarifySimplify(tkinter.Frame):
 
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
 
        self._initialize()  

        #print('{}, {}'.format(self.screenWidth, self.screenHeight))
        parent.geometry('{}x{}'.format(round(self.screenWidth/1.5), round(self.screenHeight/1.5)))

 
    def _initialize(self):

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

      
    ##Search Taskbar for pixelicon.png##
    ####################################
    def _locateClarify(self, iconSearch):
        if iconSearch == True:
            self.regionLeftX = 0
            self.regionTopY = round(self.screenHeight* .957)
            self.regionWidth = round(self.screenWidth* (.863 ))
            self.regionHeight = round(self.screenHeight* (1-.957))
            self.region = self.regionLeftX, self.regionTopY, self.regionWidth, self.regionHeight
            self.clarifyLocation = pyautogui.locateCenterOnScreen('clarifyicon.png', region=self.region, grayscale=True)
            
            return
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
            return


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

        self.textBox2.insert(1.0, "================\nATTEMPTED STEPS\n================\n")
        for i in range(0, (int(self.textBox2.index('end').split('.')[0]) - 1)):
            self.textBox2.insert(i+1.0, "! ")

        self.textBox3.insert(1.0, "=================\nRESOLUTION STEPS\n=================\n")
        for i in range(0, (int(self.textBox3.index('end').split('.')[0]) - 1)):
            self.textBox3.insert(i+1.0, "- ")    

        ####Save formatted text to temp var#############
        ################################################
        text_reason_calling = self.textBox1.get(1.0, 'end') 
        text_attempted_steps = self.textBox2.get(1.0, 'end')
        text_resolution_steps = self.textBox3.get(1.0, 'end')

    def _setup_ticket(self):
        print("stuff")
        ####################
        ##UNFINISHED#########
        #####################

    def _refresh_clarify(self):

        if self.clarifyLocation is None:
            self._locateClarify(False)

        if self.clarifyLocation is not None:
            currentMousePosition = pyautogui.position()
            pyautogui.click(self.clarifyLocation)
            pyautogui.moveTo(currentMousePosition) ###ONLY MOVES WITHIN PRIMARY SCREEN##
            pyautogui.press('p')
            time.sleep(.5)
            pyautogui.press('p')
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