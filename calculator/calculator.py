from tkinter import *

class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid(padx = 5, pady = 5)
        self.create_widgets()
        self.digits=("0","1","2","3","4","5","6","7","8","9")

    def create_widgets(self):

        
        self.display=Text(self, font=("Courier", 20), state = "disabled", wrap = NONE, width = 19, height = 1)
        self.display.grid(row=1, column=0, columnspan = 6, pady = 5)
        Button(self, text = "7", command = lambda: self.add_display("7"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=2, column = 0, sticky = W, padx = 2, pady = 2)
        Button(self, text = "8", command = lambda: self.add_display("8"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=2, column = 1, sticky = W, padx = 2, pady = 2)
        Button(self, text = "9", command = lambda: self.add_display("9"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=2, column = 2, sticky = W, padx = 2, pady = 2)
        Button(self, text = "÷", command = lambda: self.add_display("/"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=2, column = 3, sticky = W, padx = 2, pady = 2)
        Button(self, text = "C", command = self.clear, background = "indian red", font=("Courier"), width =2, height = 2).grid(row=2, column = 4, sticky = W, padx = 2, pady = 2)
        Button(self, text = "CE", command = self.backspace, background = "indian red", font=("Courier"), width =2, height = 2).grid(row=2, column = 5, sticky = W, padx = 2, pady = 2)
        Button(self, text = "4", command = lambda: self.add_display("4"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=3, column = 0, sticky = W, padx = 2, pady = 2)
        Button(self, text = "5", command = lambda: self.add_display("5"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=3, column = 1, sticky = W, padx = 2, pady = 2)
        Button(self, text = "6", command = lambda: self.add_display("6"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=3, column = 2, sticky = W, padx = 2, pady = 2)
        Button(self, text = "*", command = lambda: self.add_display("*"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=3, column = 3, sticky = W, padx = 2, pady = 2)
        Button(self, text = "xⁿ",command = lambda: self.add_display("^"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=3, column = 4, sticky = W, padx = 2, pady = 2)
        Button(self, text = "√", command = lambda: self.add_display("√("), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=3, column = 5, sticky = W, padx = 2, pady = 2)
        Button(self, text = "1", command = lambda: self.add_display("1"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=4, column = 0, sticky = W, padx = 2, pady = 2)
        Button(self, text = "2", command = lambda: self.add_display("2"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=4, column = 1, sticky = W, padx = 2, pady = 2)
        Button(self, text = "3", command = lambda: self.add_display("3"), background = "gray90", font=("Courier"), width =2, height = 2).grid(row=4, column = 2, sticky = W, padx = 2, pady = 2)
        Button(self, text = "+", command = lambda: self.add_display("+"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=4, column = 3, sticky = W, padx = 2, pady = 2)
        Button(self, text = "-", command = lambda: self.add_display("-"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=4, column = 4, sticky = W, padx = 2, pady = 2)
        Button(self, command = self.equals, background = "SlateBlue1", text = "=", font=("Courier"), width =2, height = 5).grid(row=4, column = 5, rowspan = 2, sticky = W, padx = 2, pady = 2)
        Button(self, text = "0", command = lambda: self.add_display("0"), font=("Courier"), width =2, height = 2).grid(row=5, column = 0, sticky = W, padx = 2, pady = 2)
        Button(self, text = ".", command = lambda: self.add_display("."), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=5, column = 1, sticky = W, padx = 2, pady = 2)
        Button(self, text = "(", command = lambda: self.add_display("("), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=5, column = 2, sticky = W, padx = 2, pady = 2)
        Button(self, text = ")", command = lambda: self.add_display(")"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=5, column = 3, sticky = W, padx = 2, pady = 2)
        Button(self, text = "exp", command = lambda: self.add_display("E"), background = "gainsboro", font=("Courier"), width =2, height = 2).grid(row=5, column = 4, sticky = W, padx = 2, pady = 2)

    def add_display(self, text):
        self.display.config(state = "normal")
        self.display.tag_configure("right-justify", justify = "right")
        self.display.insert(END, text, "right-justify")
        self.display.config(state = "disabled")

    def clear(self):
        self.display.config(state = "normal")
        self.display.delete(0.0, END)
        self.display.config(state = "disabled")

    def backspace(self):
        self.display.config(state = "normal")
        a=str(len(self.display.get(1.0,END)) - 2) #Character index of second to last value
        b= "1." + str(a) #Full index
        self.display.delete(b, END)
        self.display.config(state = "disabled")

    def round_sig_fig(self, value, sig_fig):
    	"""Rounds input value to  input number of significant figures"""
    	value=str(value)
    	figures=len(value)
    	if figures > sig_fig:
    		value=value[:sig_fig]
    	return value

    def correct_powers(self, equation):
        """Converts string representation of equation to one which can be evaluated""" 
        equation=equation.replace("^","**") 
        for i in equation:
            skipcount = 0 #Used to account for multiple sets of brackets
            if i == "√":
                x = equation.index(i)+1
                while True:
                    x+=1
                    if equation[x] == "(":
                        skipcount += 1
                    if equation[x] == ")":
                        if skipcount > 0: 
                            skipcount -= 1
                            continue
                        else:
                            equation = equation[:x] + ")**0.5" + equation[x+1:]                            
                            equation=equation.replace("√", "",1)
                            break
        return equation

    def equals(self):
        self.display.config(state = "normal")
        equation = str(self.display.get(1.0, END))
        equation=self.correct_powers(equation)
                   
        try:  
        	answer=(eval(equation))
        	answer=self.round_sig_fig(answer,19)

        except:
        	answer = "ERROR"
        	
        self.display.delete(0.0, END)
        self.display.tag_configure("right-justify", justify = "right")
        self.display.insert(END, answer, "right-justify")
        self.display.config(state = "disabled")
               

def main():
    root = Tk() 
    root.title("Josh's Calculator")
    app = Application(root)
    root.mainloop() 

if __name__ == '__main__':
    main()

    

