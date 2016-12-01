
import tkinter
import re
import pyautogui
import time
 
class ClarifyClarity(tkinter.Frame):
 
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
 
        self._initialize()  

        #print('{}, {}'.format(self.screenWidth, self.screenHeight))
        parent.geometry('{}x{}'.format(round(self.screenWidth/2), round(self.screenHeight/2)))

 
    def _initialize(self):

        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        #Create all GUI objects
        textBoxLabel1 = tkinter.Label(text='Reason Calling', bg='gold', fg='red')
        textBoxLabel1.grid(row=0, column=0, sticky='SNEW')

        self.textBox1 = tkinter.Text(height=4, width= 100)
        self.textBox1.grid(row=1, column=0, sticky='SNEW')

        textBoxLabel2 = tkinter.Label(text='Attempted Steps', bg='blue', fg='white')
        textBoxLabel2.grid(row=2, column=0, sticky='SNEW')

        self.textBox2 = tkinter.Text( height=10, width=100)
        self.textBox2.grid(row=3, column=0, sticky='SNEW')
        
        textBoxLabel3 = tkinter.Label(text='Resolution Steps', bg='black', fg='white')
        textBoxLabel3.grid(row=4, column=0, sticky='SNEW')

        self.textBox3 = tkinter.Text(height=10, width=100)
        self.textBox3.grid(row=5, column=0, sticky='SNEW')
        

        self.button_ClearAll = tkinter.Button(text="Clear All Fields", command=self._delete_all_text)
        self.button_ClearAll.grid(row=6, column=0, sticky='SW')

        self.button_SendClarify = tkinter.Button(text='Send To Clarify', command = self._send_to_clarify)
        self.button_SendClarify.grid(row= 6, column=0, sticky='SE')

        self.button_RefreshClarify = tkinter.Button(text='Refresh Clarify', command = self._refresh_clarify)
        self.button_RefreshClarify.grid(row=6, column=0, sticky='S' )

        self._locateClarify()        

        self.columnconfigure(0, weight=1)
        for i in range(0,7):
            self.rowconfigure(i, weight=1)
        self.update()

      
    def _locateClarify(self):
        ####NEED TO CONFIRM WORKS ON ALL SCREEN SIZES#####
        ##################################################
        self.regionLeftX = 0
        self.regionTopY = round(self.screenHeight* .957)
        self.regionWidth = round(self.screenWidth* (.863 ))
        self.regionHeight = round(self.screenHeight* (1-.957))
        self.region = self.regionLeftX, self.regionTopY, self.regionWidth, self.regionHeight
        self.clarifyLocation = pyautogui.locateCenterOnScreen('clarifyicon.png', region=self.region, grayscale=True)


    def _delete_all_text(self):
        print("Deleting Texts!")
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
        for i in range(0, (int(self.textBox3.index('end').split('.')[0]) - 1)): #gets total line count
            self.textBox3.insert(i+1.0, "- ")    

        ####Save formatted text to temp var#############
        ################################################
        text_reason_calling = self.textBox1.get(1.0, 'end') 
        text_attempted_steps = self.textBox2.get(1.0, 'end')
        text_resolution_steps = self.textBox3.get(1.0, 'end')

    def _setup_ticket(self):
        #####NEEDS FINISH#######
        ########################
        print("stuff")

    def _refresh_clarify(self):

        if self.clarifyLocation is None:

            pyautogui.alert(text='UNABLE TO LOCATE CLARIFY, REATTEMPTING', title='ERROR# 100', button='ok' )
            self._locateClarify()

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
    root.update()

    application = ClarifyClarity(root)
    application.grid()
    application.mainloop()