import tkinter as tk
import tkinter.ttk as ttk

class Calculadora:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora")
        self.master.geometry("330x300+100+100")
        self.master.resizable(0, 0)
        self.master.config(bg="#0A122A")
        self.master.iconbitmap("icon_calc.ico")
        
        self.first_num = 0
        self.var_op = None
        self.var_num = tk.StringVar()
        self.var_num.set('0')
        self.solved = False
        
        frm = tk.Frame(self.master, bg="#0A122A")
        frm.pack(padx=10, pady=10)
        
        # Widgets de la calculadora
        self.entDisplay = tk.Entry(frm, width=15, font='"Digital-7 Mono" 20', 
                                   textvariable=self.var_num, justify=tk.RIGHT, 
                                   bg="#e6e4d9", bd=3)
        self.btn0 = tk.Button(frm, text="0", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('0'))
        self.btn1 = tk.Button(frm, text="1", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('1'))
        self.btn2 = tk.Button(frm, text="2", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('2'))
        self.btn3 = tk.Button(frm, text="3", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('3'))
        self.btn4 = tk.Button(frm, text="4", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('4'))
        self.btn5 = tk.Button(frm, text="5", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('5'))
        self.btn6 = tk.Button(frm, text="6", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('6'))
        self.btn7 = tk.Button(frm, text="7", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('7'))
        self.btn8 = tk.Button(frm, text="8", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('8'))
        self.btn9 = tk.Button(frm, text="9", width=4, font="Arial 16", bg='#A9A9F5', 
                              command=lambda: self.add_num_display('9'))
        self.btnPoint = tk.Button(frm, text=".", width=4, font="Arial 16", bg='#A9A9F5', 
                                  command=lambda: self.add_num_display('.'))
        self.btnEqual = tk.Button(frm, text="=", width=4, font="Arial 16", bg='#A9A9F5', 
                                  command=self.solve)
        self.btnAdd = tk.Button(frm, text="+", width=4, font="Arial 16", bg='#5858FA', 
                                command=lambda: self.set_operation('+'))
        self.btnSub = tk.Button(frm, text="-", width=4, font="Arial 16", bg='#5858FA', 
                                command=lambda: self.set_operation('-'))
        self.btnMul = tk.Button(frm, text="x", width=4, font="Arial 16", bg='#5858FA', 
                                command=lambda: self.set_operation('x'))
        self.btnDiv = tk.Button(frm, text="/", width=4, font="Arial 16", bg='#5858FA', 
                                command=lambda: self.set_operation('/'))
        self.btnDel = tk.Button(frm, text="DEL", width=4, font="Arial 16", bg='#FE2E64', 
                                command=self.clear_display)
        
        self.entDisplay.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        self.btn0.grid(row=4, column=0, padx=5, pady=5)
        self.btn1.grid(row=3, column=0, padx=5, pady=5)
        self.btn2.grid(row=3, column=1, padx=5, pady=5)
        self.btn3.grid(row=3, column=2, padx=5, pady=5)
        self.btn4.grid(row=2, column=0, padx=5, pady=5)
        self.btn5.grid(row=2, column=1, padx=5, pady=5)
        self.btn6.grid(row=2, column=2, padx=5, pady=5)
        self.btn7.grid(row=1, column=0, padx=5, pady=5)
        self.btn8.grid(row=1, column=1, padx=5, pady=5)
        self.btn9.grid(row=1, column=2, padx=5, pady=5)
        self.btnPoint.grid(row=4, column=1, padx=5, pady=5)
        self.btnEqual.grid(row=4, column=2, padx=5, pady=5)
        self.btnAdd.grid(row=1, column=3, padx=5, pady=5)
        self.btnSub.grid(row=2, column=3, padx=5, pady=5)
        self.btnMul.grid(row=3, column=3, padx=5, pady=5)
        self.btnDiv.grid(row=4, column=3, padx=5, pady=5)
        self.btnDel.grid(row=0, column=0, padx=5, pady=5)
        
        
    def add_num_display(self, num):
        if self.solved:
            self.clear_display()
            self.solved = False
            
        if self.var_num.get() == '0' or self.var_num.get() == "E":
            self.var_num.set('')
        
        if num == '.' and self.var_num.get() == '':
            self.var_num.set("0.")
        
        if len(self.var_num.get()) < 12:
            if num == '.' and self.var_num.get().count('.') > 0:
                return None
            
            self.var_num.set(self.var_num.get() + num)
        
        
    def set_operation(self, op):
        if self.var_op == None:
            self.var_op = op
            self.first_num = float(self.var_num.get())
            self.clear_display()
        
        
    def solve(self):
        # Si es que se ha seleccionado previamente +, -, x, /...
        if self.var_op == '+':
            result =self.first_num + float(self.var_num.get())
        elif self.var_op == '-':
            result =self.first_num - float(self.var_num.get())
        elif self.var_op == 'x':
            result =self.first_num * float(self.var_num.get())
        elif self.var_op == '/':
            # TODO: Division entre cero
            try:
                result =self.first_num / float(self.var_num.get())
            except ZeroDivisionError:
                result = "E"

        self.var_op = None
        self.var_num.set(str(result)[:12])
        self.solved = True
                
        
    def clear_display(self):
        self.var_num.set('0')
        
    
def main():        
    root = tk.Tk()     # TopLevel
    app = Calculadora(root)
    root.mainloop()

# python calculator.py (__name__ : "__main__") desde el interprete
# import calculator.py (__name__ : "calculator.py")
if __name__ == "__main__":
    main()