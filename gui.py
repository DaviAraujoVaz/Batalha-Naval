import tkinter as tk
from tkinter import messagebox, scrolledtext

class BattleshipGUI(tk.Tk):
    def __init__(self, on_host, on_join, on_rps_choice, on_shoot, on_chat_send, on_rematch, on_quit):
        super().__init__()
        self.title("Batalha Naval UDP")
        self.geometry("900x600")
        self.configure(bg="#1E1E2E")
        self.resizable(False, False)

        self.on_host = on_host
        self.on_join = on_join
        self.on_rps_choice = on_rps_choice
        self.on_shoot = on_shoot
        self.on_chat_send = on_chat_send
        self.on_rematch = on_rematch
        self.on_quit = on_quit
        
        self.my_board_canvas = None
        self.target_board_canvas = None
        
        # UI state
        self.my_grid_rects = [[None]*10 for _ in range(10)]
        self.target_grid_rects = [[None]*10 for _ in range(10)]

        self.container = tk.Frame(self, bg="#1E1E2E")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self._build_connection_frame()
        self._build_host_frame()
        self._build_join_frame()
        self._build_rps_frame()
        self._build_game_frame()
        self._build_game_over_frame()
        
        self.show_frame("connect")

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def _build_connection_frame(self):
        frame = tk.Frame(self.container, bg="#1E1E2E")
        self.frames["connect"] = frame
        
        lbl_title = tk.Label(frame, text="Batalha Naval", font=("Arial", 28, "bold"), fg="#A6E3A1", bg="#1E1E2E")
        lbl_title.pack(pady=60)
        
        btn_host = tk.Button(frame, text="Host (Criar Partida)", font=("Arial", 16, "bold"), bg="#89B4FA", fg="#11111B", 
                             command=lambda: self.show_frame("host"), relief="flat", padx=20, pady=10, width=20)
        btn_host.pack(pady=15)
        
        btn_join = tk.Button(frame, text="Join (Entrar em Partida)", font=("Arial", 16, "bold"), bg="#F38BA8", fg="#11111B", 
                             command=lambda: self.show_frame("join"), relief="flat", padx=20, pady=10, width=20)
        btn_join.pack(pady=15)

    def _build_host_frame(self):
        frame = tk.Frame(self.container, bg="#1E1E2E")
        self.frames["host"] = frame
        
        lbl_title = tk.Label(frame, text="Criar Partida (Host)", font=("Arial", 24, "bold"), fg="#A6E3A1", bg="#1E1E2E")
        lbl_title.pack(pady=40)
        
        f_inputs = tk.Frame(frame, bg="#1E1E2E")
        f_inputs.pack(pady=10)
        
        tk.Label(f_inputs, text="Porta Local:", fg="white", bg="#1E1E2E", font=("Arial", 14)).grid(row=0, column=0, pady=10, padx=5, sticky="e")
        self.entry_host_port = tk.Entry(f_inputs, font=("Arial", 14), width=10)
        self.entry_host_port.grid(row=0, column=1, pady=10, padx=5)
        self.entry_host_port.insert(0, "5000")

        btn_start = tk.Button(frame, text="Iniciar Host", font=("Arial", 14, "bold"), bg="#89B4FA", fg="#11111B", 
                              command=self._handle_host, relief="flat", padx=20, pady=10)
        btn_start.pack(pady=20)
        
        btn_back = tk.Button(frame, text="Voltar", font=("Arial", 12), bg="#45475A", fg="white", 
                             command=lambda: self.show_frame("connect"), relief="flat", padx=20, pady=5)
        btn_back.pack()

        self.lbl_host_status = tk.Label(frame, text="", fg="#F38BA8", bg="#1E1E2E", font=("Arial", 12))
        self.lbl_host_status.pack(pady=10)

    def _handle_host(self):
        try:
            lp = int(self.entry_host_port.get())
            self.lbl_host_status.config(text="Aguardando jogador...")
            self.on_host(lp)
        except ValueError:
            messagebox.showerror("Erro", "Porta deve ser numérica.")
            self.lbl_host_status.config(text="")
        except OSError:
            messagebox.showerror("Erro", f"A porta escolhida já está em uso ou é inválida!")
            self.lbl_host_status.config(text="")

    def _build_join_frame(self):
        frame = tk.Frame(self.container, bg="#1E1E2E")
        self.frames["join"] = frame
        
        lbl_title = tk.Label(frame, text="Entrar em Partida (Join)", font=("Arial", 24, "bold"), fg="#A6E3A1", bg="#1E1E2E")
        lbl_title.pack(pady=30)
        
        f_inputs = tk.Frame(frame, bg="#1E1E2E")
        f_inputs.pack(pady=10)
        
        tk.Label(f_inputs, text="IP do Host:", fg="white", bg="#1E1E2E", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=5, sticky="e")
        self.entry_join_ip = tk.Entry(f_inputs, font=("Arial", 12), width=15)
        self.entry_join_ip.grid(row=0, column=1, pady=10, padx=5)
        self.entry_join_ip.insert(0, "127.0.0.1")

        tk.Label(f_inputs, text="Porta do Host:", fg="white", bg="#1E1E2E", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=5, sticky="e")
        self.entry_join_host_port = tk.Entry(f_inputs, font=("Arial", 12), width=10)
        self.entry_join_host_port.grid(row=1, column=1, pady=10, padx=5)
        self.entry_join_host_port.insert(0, "5000")

        tk.Label(f_inputs, text="Sua Porta Local:", fg="white", bg="#1E1E2E", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=5, sticky="e")
        self.entry_join_local_port = tk.Entry(f_inputs, font=("Arial", 12), width=10)
        self.entry_join_local_port.grid(row=2, column=1, pady=10, padx=5)
        self.entry_join_local_port.insert(0, "5001")

        btn_join = tk.Button(frame, text="Entrar", font=("Arial", 14, "bold"), bg="#F38BA8", fg="#11111B", 
                             command=self._handle_join, relief="flat", padx=20, pady=10)
        btn_join.pack(pady=20)

        btn_back = tk.Button(frame, text="Voltar", font=("Arial", 12), bg="#45475A", fg="white", 
                             command=lambda: self.show_frame("connect"), relief="flat", padx=20, pady=5)
        btn_back.pack()

    def _handle_join(self):
        try:
            hip = self.entry_join_ip.get()
            hp = int(self.entry_join_host_port.get())
            lp = int(self.entry_join_local_port.get())
            self.on_join(lp, hip, hp)
        except ValueError:
            messagebox.showerror("Erro", "Portas devem ser numéricas.")
        except OSError:
            messagebox.showerror("Erro", f"A porta local escolhida já está em uso!")

    def _build_rps_frame(self):
        frame = tk.Frame(self.container, bg="#1E1E2E")
        self.frames["rps"] = frame
        
        lbl = tk.Label(frame, text="Sorteio do Turno: Pedra, Papel ou Tesoura", font=("Arial", 18, "bold"), fg="#89B4FA", bg="#1E1E2E")
        lbl.pack(pady=40)
        
        self.lbl_rps_status = tk.Label(frame, text="Escolha a sua jogada:", fg="white", bg="#1E1E2E", font=("Arial", 14))
        self.lbl_rps_status.pack(pady=20)
        
        btn_frame = tk.Frame(frame, bg="#1E1E2E")
        btn_frame.pack(pady=20)
        
        for choice in ["PEDRA", "PAPEL", "TESOURA"]:
            btn = tk.Button(btn_frame, text=choice, font=("Arial", 12, "bold"), bg="#313244", fg="white",
                            command=lambda c=choice: self._handle_rps(c), width=10, height=3)
            btn.pack(side="left", padx=10)

    def _handle_rps(self, choice):
        self.lbl_rps_status.config(text=f"Você escolheu {choice}. Aguardando oponente...")
        self.on_rps_choice(choice)

    def _build_game_frame(self):
        frame = tk.Frame(self.container, bg="#1E1E2E")
        self.frames["game"] = frame
        
        # Top banner
        self.lbl_turn = tk.Label(frame, text="Preparando...", font=("Arial", 16, "bold"), bg="#1E1E2E", fg="#A6E3A1", pady=10)
        self.lbl_turn.pack(fill="x")
        
        # Center layout: My Board | Target Board | Chat
        center_frame = tk.Frame(frame, bg="#1E1E2E")
        center_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left: My Board
        my_frame = tk.Frame(center_frame, bg="#1E1E2E")
        my_frame.pack(side="left", padx=20)
        tk.Label(my_frame, text="Meu Tabuleiro (Sua Frota)", font=("Arial", 12), fg="white", bg="#1E1E2E").pack()
        self.my_board_canvas = tk.Canvas(my_frame, width=330, height=330, bg="#11111B", highlightthickness=0)
        self.my_board_canvas.pack(pady=10)
        self._draw_grid(self.my_board_canvas, self.my_grid_rects, is_target=False)
        
        # Middle: Target Board
        target_frame = tk.Frame(center_frame, bg="#1E1E2E")
        target_frame.pack(side="left", padx=20)
        tk.Label(target_frame, text="Tabuleiro Alvo (Tiros)", font=("Arial", 12), fg="white", bg="#1E1E2E").pack()
        self.target_board_canvas = tk.Canvas(target_frame, width=330, height=330, bg="#11111B", highlightthickness=0)
        self.target_board_canvas.pack(pady=10)
        self._draw_grid(self.target_board_canvas, self.target_grid_rects, is_target=True)
        self.target_board_canvas.bind("<Button-1>", self._handle_canvas_click)
        
        # Right: Chat
        chat_frame = tk.Frame(center_frame, bg="#1E1E2E", width=200)
        chat_frame.pack(side="right", fill="y", padx=10)
        chat_frame.pack_propagate(False)
        tk.Label(chat_frame, text="Chat", font=("Arial", 12), fg="white", bg="#1E1E2E").pack()
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, bg="#313244", fg="white", font=("Arial", 10), state="disabled", width=25, height=18)
        self.chat_display.pack(pady=5, fill="both", expand=True)
        
        entry_frame = tk.Frame(chat_frame, bg="#1E1E2E")
        entry_frame.pack(fill="x")
        self.entry_chat = tk.Entry(entry_frame, font=("Arial", 10), bg="#181825", fg="white", insertbackground="white")
        self.entry_chat.pack(side="left", fill="x", expand=True)
        self.entry_chat.bind("<Return>", lambda e: self._handle_chat_send())
        btn_send = tk.Button(entry_frame, text="Enviar", command=self._handle_chat_send, bg="#89B4FA", fg="#11111B", relief="flat")
        btn_send.pack(side="right")

    def _build_game_over_frame(self):
        frame = tk.Frame(self.container, bg="#1E1E2E")
        self.frames["game_over"] = frame
        
        self.lbl_go_title = tk.Label(frame, text="", font=("Arial", 28, "bold"), bg="#1E1E2E")
        self.lbl_go_title.pack(pady=60)
        
        self.btn_rematch = tk.Button(frame, text="Jogar Novamente", font=("Arial", 16, "bold"), bg="#89B4FA", fg="#11111B",
                                     command=self._handle_rematch, relief="flat", padx=20, pady=10)
        self.btn_rematch.pack(pady=20)
        
        btn_quit = tk.Button(frame, text="Sair", font=("Arial", 16, "bold"), bg="#F38BA8", fg="#11111B",
                             command=self.on_quit, relief="flat", padx=20, pady=10)
        btn_quit.pack(pady=10)

    def _handle_rematch(self):
        self.btn_rematch.config(text="Aguardando oponente...", state="disabled")
        self.on_rematch()

    def show_game_over(self, result, is_win):
        color = "#A6E3A1" if is_win else "#F38BA8"
        self.lbl_go_title.config(text=result, fg=color)
        self.btn_rematch.config(text="Jogar Novamente", state="normal")
        self.show_frame("game_over")

    def reset_boards(self):
        for r in range(10):
            for c in range(10):
                self.update_cell("my", r, c, "water")
                self.update_cell("target", r, c, "water")
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state="disabled")

    def _draw_grid(self, canvas, rect_matrix, is_target):
        cell_size = 30
        margin = 25
        padding = 2
        
        # Desenha as letras das colunas (A-J)
        for c in range(10):
            x = margin + c * cell_size + cell_size // 2
            canvas.create_text(x, margin // 2, text=chr(65 + c), fill="#A6E3A1", font=("Arial", 10, "bold"))
            
        # Desenha os números das linhas (1-10)
        for r in range(10):
            y = margin + r * cell_size + cell_size // 2
            canvas.create_text(margin // 2, y, text=str(r + 1), fill="#A6E3A1", font=("Arial", 10, "bold"))

        for r in range(10):
            for c in range(10):
                x1 = margin + c * cell_size + padding
                y1 = margin + r * cell_size + padding
                x2 = margin + (c + 1) * cell_size - padding
                y2 = margin + (r + 1) * cell_size - padding
                rect = canvas.create_rectangle(x1, y1, x2, y2, outline="#313244", fill="#1E1E2E", width=1)
                rect_matrix[r][c] = rect

    def _handle_canvas_click(self, event):
        # Calculate row and col
        cell_size = 30
        margin = 25
        c = (event.x - margin) // cell_size
        r = (event.y - margin) // cell_size
        if 0 <= r < 10 and 0 <= c < 10:
            self.on_shoot(r, c)

    def _handle_chat_send(self):
        msg = self.entry_chat.get()
        if msg.strip():
            self.on_chat_send(msg)
            self.append_chat(f"Você: {msg}")
            self.entry_chat.delete(0, tk.END)

    def append_chat(self, msg):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, msg + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")

    def update_cell(self, board_type, row, col, status):
        """status: 'ship', 'hit', 'miss', 'water'"""
        canvas = self.my_board_canvas if board_type == "my" else self.target_board_canvas
        rect_matrix = self.my_grid_rects if board_type == "my" else self.target_grid_rects
        
        rect_id = rect_matrix[row][col]
        colors = {
            "ship": "#89B4FA",   # Azul brilhante
            "hit": "#F38BA8",    # Vermelho
            "miss": "#45475A",   # Cinza/Azul escuro opaco (água)
            "water": "#1E1E2E"   # Cor base
        }
        canvas.itemconfig(rect_id, fill=colors.get(status, "#1E1E2E"))

    def set_turn(self, my_turn):
        if my_turn:
            self.lbl_turn.config(text="Seu Turno! Atire no tabuleiro alvo.", fg="#A6E3A1")
        else:
            self.lbl_turn.config(text="Turno do Oponente... Aguarde.", fg="#F38BA8")

    def update_rps_status(self, msg):
        self.lbl_rps_status.config(text=msg)
