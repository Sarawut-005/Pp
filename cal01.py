import tkinter as tk
from tkinter import messagebox

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("เครื่องคิดเลขโมเดิร์น")
        self.root.geometry("350x550")
        self.root.configure(bg="#171c26")  # พื้นหลังตัวเครื่องสีเข้ม
        self.root.resizable(False, False)   # ล็อกขนาดหน้าต่าง

        self.expression = ""

        # ส่วนของหน้าจอแสดงผล
        self.display_var = tk.StringVar(value="0")
        self.create_display()

        # ส่วนของปุ่มกด
        self.create_buttons()
        
        # ผูกปุ่มบนคีย์บอร์ดเข้ากับฟังก์ชัน
        self.bind_keys()

    def create_display(self):
        # หน้าจอด้านบนสุด
        display_frame = tk.Frame(self.root, bg="#171c26", padx=10, pady=20)
        display_frame.pack(expand=True, fill="both")

        self.display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            anchor="e", 
            bg="#222834",      # สีหน้าจอแสดงผล
            fg="#ffffff",      # สีตัวอักษร
            font=("Segoe UI", 32, "bold"),
            padx=15,
            pady=15,
            wraplength=320
        )
        self.display_label.pack(expand=True, fill="both")

    def create_buttons(self):
        # เฟรมสำหรับวางปุ่มระบบ Grid
        buttons_frame = tk.Frame(self.root, bg="#171c26", padx=15, pady=15)
        buttons_frame.pack(expand=True, fill="both")

        # กำหนดเลย์เอาต์ปุ่ม (ข้อความ, แถว, คอลัมน์, ประเภทสี)
        buttons_layout = [
            ('C', 0, 0, 'func'), ('⌫', 0, 1, 'func'), ('%', 0, 2, 'op'), ('/', 0, 3, 'op'),
            ('7', 1, 0, 'num'),  ('8', 1, 1, 'num'),  ('9', 1, 2, 'num'),  ('*', 1, 3, 'op'),
            ('4', 2, 0, 'num'),  ('5', 2, 1, 'num'),  ('6', 2, 2, 'num'),  ('-', 2, 3, 'op'),
            ('1', 3, 0, 'num'),  ('2', 3, 1, 'num'),  ('3', 3, 2, 'num'),  ('+', 3, 3, 'op'),
            ('0', 4, 0, 'num'),  ('.', 4, 1, 'num'),  ('=', 4, 2, 'equal') # '=' จะขยายยาว 2 ช่อง
        ]

        # สีของปุ่มแต่ละประเภท
        colors = {
            'num':   {"bg": "#2d3545", "fg": "#ffffff", "active": "#3d485e"},
            'op':    {"bg": "#ff9f0a", "fg": "#ffffff", "active": "#ffb340"},
            'func':  {"bg": "#a5a5a5", "fg": "#000000", "active": "#c1c1c1"},
            'equal': {"bg": "#2ecc71", "fg": "#ffffff", "active": "#4cd985"}
        }

        # วางโครงสร้าง Grid ให้อัตราส่วนเท่ากัน
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1, minsize=65)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1, minsize=65)

        for text, row, col, btn_type in buttons_layout:
            color = colors[btn_type]
            
            # เช็คกรณีพิเศษสำหรับปุ่ม '=' ให้กว้าง 2 ช่อง
            colspan = 2 if text == '=' else 1
            
            btn = tk.Button(
                buttons_frame,
                text=text,
                bg=color["bg"],
                fg=color["fg"],
                activebackground=color["active"],
                activeforeground=color["fg"],
                font=("Segoe UI", 16, "bold"),
                borderwidth=0,
                relief="flat",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)
            
            # ใส่เอฟเฟกต์โค้งมนแบบหลอกตาด้วยการลดขอบแบน (Flat) ในระบบ Grid

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_var.set("0")
        elif char == '⌫':
            if len(self.expression) > 0:
                self.expression = self.expression[:-1]
                self.display_var.set(self.expression if self.expression else "0")
        elif char == '=':
            self.calculate_result()
        else:
            # จัดการเครื่องหมายคำนวณไม่ให้ซ้ำซ้อนกันซื่อๆ
            if char in ['+', '*', '/', '%'] and (not self.expression or self.expression[-1] in ['+', '-', '*', '/', '%']):
                if self.expression:
                    self.expression = self.expression[:-1] + char
            elif char == '-' and (not self.expression or self.expression[-1] in ['+', '-', '*', '/', '%']):
                self.expression += char
            else:
                if self.expression == "0" and char != '.':
                    self.expression = char
                else:
                    self.expression += char
                    
            self.display_var.set(self.expression)

    def calculate_result(self):
        try:
            # เปลี่ยน % ให้หาร 100 ก่อนคำนวณ
            expr_to_eval = self.expression.replace('%', '/100')
            
            if not expr_to_eval:
                return

            # คำนวณผลลัพธ์อย่างปลอดภัย
            result = eval(expr_to_eval)
            
            # ปรับทศนิยมให้ไม่ยาวเกินไป
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 8)

            self.expression = str(result)
            self.display_var.set(self.expression)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def bind_keys(self):
        # ฟังก์ชันรองรับการกดคีย์บอร์ด
        self.root.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        key = event.char
        if key in "0123456789+-*/.%" :
            self.on_button_click(key)
        elif event.keysym == "Return" or key == "=":
            self.on_button_click("=")
        elif event.keysym == "Backspace":
            self.on_button_click("⌫")
        elif event.keysym == "Escape":
            self.on_button_click("C")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()
