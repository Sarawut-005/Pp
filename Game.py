import tkinter as tk
import random

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("เกมเป่ายิ้งฉุบในตำนาน ✌️✊✋")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e2e") # สีพื้นหลังโมเดิร์นเข้ม
        self.root.resizable(False, False)

        # ตัวแปรเก็บคะแนน
        self.player_score = 0
        self.computer_score = 0
        
        # รายชื่อตัวเลือกและอีโมจิ
        self.choices = {
            "ค้อน": "✊",
            "กระดาษ": "✋",
            "กรรไกร": "✌️"
        }

        self.setup_ui()

    def setup_ui(self):
        # 1. แผงแสดงคะแนน (Scoreboard)
        score_frame = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        score_frame.pack(fill="x")

        self.score_label = tk.Label(
            score_frame, 
            text="ผู้เล่น: 0  |  คอมพิวเตอร์: 0", 
            font=("Segoe UI", 18, "bold"), 
            bg="#1e1e2e", 
            fg="#cdd6f4"
        )
        self.score_label.pack()

        # 2. พื้นที่แสดงผลการต่อสู้ (Battle Arena)
        arena_frame = tk.Frame(self.root, bg="#252538", bd=2, relief="groove", padx=20, pady=20)
        arena_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.vs_label = tk.Label(
            arena_frame, 
            text="🆚\nพร้อมแล้วเลือกอาวุธเลย!", 
            font=("Segoe UI", 16), 
            bg="#252538", 
            fg="#a6adc8",
            justify="center"
        )
        self.vs_label.pack(expand=True)

        self.result_label = tk.Label(
            arena_frame, 
            text="เริ่มเกม!", 
            font=("Segoe UI", 22, "bold"), 
            bg="#252538", 
            fg="#f9e2af"
        )
        self.result_label.pack(pady=10)

        # 3. โซนปุ่มกดเลือกอาวุธ (Control Panel)
        btn_frame = tk.Frame(self.root, bg="#1e1e2e", pady=30)
        btn_frame.pack(fill="x")

        # สไตล์และสีของปุ่ม
        btn_styles = {
            "กรรไกร": {"bg": "#ff5555", "fg": "white"},
            "ค้อน": {"bg": "#ffb86c", "fg": "black"},
            "กระดาษ": {"bg": "#50fa7b", "fg": "black"}
        }

        # วางปุ่ม กรรไกร ค้อน กระดาษ เคียงข้างกัน
        for choice, emoji in self.choices.items():
            btn = tk.Button(
                btn_frame,
                text=f"{emoji}\n{choice}",
                font=("Segoe UI", 14, "bold"),
                width=8,
                height=3,
                bg=btn_styles[choice]["bg"],
                fg=btn_styles[choice]["fg"],
                activebackground="#44475a",
                cursor="hand2",
                bd=0,
                command=lambda c=choice: self.play_round(c)
            )
            btn.pack(side="left", expand=True, padx=10)

        # 4. ปุ่ม Reset เกม
        reset_btn = tk.Button(
            self.root,
            text="รีเซ็ตคะแนน 🔄",
            font=("Segoe UI", 10, "bold"),
            bg="#313244",
            fg="#a6adc8",
            bd=0,
            pady=5,
            command=self.reset_game
        )
        reset_btn.pack(side="bottom", pady=15)

    def play_round(self, player_choice):
        # บอสคอมพิวเตอร์สุ่มเลือกอาวุธ
        computer_choice = random.choice(list(self.choices.keys()))
        
        p_emoji = self.choices[player_choice]
        c_emoji = self.choices[computer_choice]

        # อัปเดตข้อความบนหน้าจอ Arena
        self.vs_label.config(
            text=f"คุณเลือก: {player_choice} {p_emoji}\n\nVS\n\nคอมเลือก: {computer_choice} {c_emoji}"
        )

        # ตรวจสอบกฎการแพ้ชนะ
        if player_choice == computer_choice:
            self.result_label.config(text="เสมอซะงั้น! 🤝", fg="#f9e2af")
        elif (player_choice == "ค้อน" and computer_choice == "กรรไกร") or \
             (player_choice == "กระดาษ" and computer_choice == "ค้อน") or \
             (player_choice == "กรรไกร" and computer_choice == "กระดาษ"):
            self.result_label.config(text="คุณชนะ! 🎉", fg="#50fa7b")
            self.player_score += 1
        else:
            self.result_label.config(text="คุณแพ้! 😢", fg="#ff5555")
            self.computer_score += 1

        # อัปเดตกระดานคะแนน
        self.score_label.config(text=f"ผู้เล่น: {self.player_score}  |  คอมพิวเตอร์: {self.computer_score}")

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.score_label.config(text="ผู้เล่น: 0  |  คอมพิวเตอร์: 0")
        self.vs_label.config(text="🆚\nพร้อมแล้วเลือกอาวุธเลย!")
        self.result_label.config(text="รีเซ็ตเกมแล้ว!", fg="#f9e2af")

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGame(root)
    root.mainloop()
