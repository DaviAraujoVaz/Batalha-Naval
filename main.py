import tkinter as tk
from tkinter import messagebox
from gui import BattleshipGUI
from network import NetworkManager
from game_logic import GameLogic

class BattleshipApp:
    def __init__(self):
        self.gui = BattleshipGUI(self.on_host, self.on_join, self.on_rps_choice, self.on_shoot, self.on_chat_send, self.on_rematch, self.on_quit)
        self.network = NetworkManager(self.on_message_received)
        self.game_logic = GameLogic()
        
        self.my_rps_choice = None
        self.opp_rps_choice = None
        self.my_turn = False
        self.game_started = False
        self.game_over = False
        self.my_rematch_choice = False
        self.opp_rematch_choice = False
        self.shots_fired = [[False]*10 for _ in range(10)]

    def start(self):
        # Prevent window closing without cleaning up
        self.gui.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.gui.mainloop()

    def on_closing(self):
        self.network.close()
        self.gui.destroy()

    def on_host(self, local_port):
        self.network.start_listening(local_port)
        # Host aguarda receber HELLO do Joiner

    def on_join(self, local_port, host_ip, host_port):
        self.network.start_listening(local_port)
        self.network.set_target(host_ip, host_port)
        self.network.send_message("HELLO")

    def on_rps_choice(self, choice):
        self.my_rps_choice = choice
        self.network.send_message(f"RPS {choice}")
        self.check_rps_result()

    def on_shoot(self, row, col):
        if not self.game_started or self.game_over:
            return
        if not self.my_turn:
            messagebox.showwarning("Aviso", "Não é o seu turno!")
            return
        if self.shots_fired[row][col]:
            # Já atirou nesta posição, ignora o clique
            return
        
        self.shots_fired[row][col] = True
        self.network.send_message(f"SHOOT {row} {col}")

    def on_chat_send(self, msg):
        self.network.send_message(f"CHAT {msg}")

    def on_rematch(self):
        self.my_rematch_choice = True
        self.network.send_message("REMATCH")
        self.check_rematch()

    def on_quit(self):
        self.on_closing()

    def check_rematch(self):
        if self.my_rematch_choice and self.opp_rematch_choice:
            self.reset_game()

    def reset_game(self):
        self.game_logic.reset()
        self.gui.reset_boards()
        self.my_rps_choice = None
        self.opp_rps_choice = None
        self.my_rematch_choice = False
        self.opp_rematch_choice = False
        self.game_over = False
        self.game_started = False
        self.shots_fired = [[False]*10 for _ in range(10)]
        self.gui.show_frame("rps")
        self.gui.update_rps_status("Escolha a sua jogada:")

    # --- Network Callbacks (Execute in Main Thread) ---
    def on_message_received(self, msg):
        # We need to dispatch this to tkinter's main thread safely
        self.gui.after(0, self._process_message, msg)

    def _process_message(self, msg):
        if msg == "HELLO":
            # Connected! Move to RPS frame
            self.gui.show_frame("rps")
            self.network.send_message("HELLO_ACK") # Send ack just in case they connected slightly later
            
        elif msg == "HELLO_ACK":
            self.gui.show_frame("rps")

        elif msg.startswith("RPS "):
            self.opp_rps_choice = msg.split(" ")[1]
            self.check_rps_result()

        elif msg.startswith("SHOOT "):
            if self.game_over: return
            _, r, c = msg.split(" ")
            r, c = int(r), int(c)
            hit = self.game_logic.receive_shot(r, c)
            if hit:
                self.gui.update_cell("my", r, c, "hit")
                self.network.send_message(f"REPLY_HIT {r} {c}")
                # Keep their turn, meaning it's NOT our turn
                self.set_turn(False)
            else:
                self.gui.update_cell("my", r, c, "miss")
                self.network.send_message(f"REPLY_MISS {r} {c}")
                # Missed, so it becomes our turn
                self.set_turn(True)
                
            if self.game_logic.is_game_over():
                self.network.send_message("WIN")
                self.game_over = True
                self.gui.show_game_over("Derrota! Seus navios afundaram.", False)

        elif msg.startswith("REPLY_HIT "):
            _, r, c = msg.split(" ")
            r, c = int(r), int(c)
            self.gui.update_cell("target", r, c, "hit")
            # Hit, so keep turn
            self.set_turn(True)

        elif msg.startswith("REPLY_MISS "):
            _, r, c = msg.split(" ")
            r, c = int(r), int(c)
            self.gui.update_cell("target", r, c, "miss")
            # Missed, end turn
            self.set_turn(False)

        elif msg == "WIN":
            self.game_over = True
            self.gui.show_game_over("Vitória! Frota inimiga destruída.", True)

        elif msg == "REMATCH":
            self.opp_rematch_choice = True
            self.check_rematch()

        elif msg.startswith("CHAT "):
            chat_msg = msg[5:]
            self.gui.append_chat(f"Oponente: {chat_msg}")

    def check_rps_result(self):
        if self.my_rps_choice and self.opp_rps_choice:
            m = self.my_rps_choice
            o = self.opp_rps_choice
            
            if m == o:
                self.gui.update_rps_status("Empate! Escolha novamente.")
                self.my_rps_choice = None
                self.opp_rps_choice = None
            else:
                win_conditions = {
                    "PEDRA": "TESOURA",
                    "PAPEL": "PEDRA",
                    "TESOURA": "PAPEL"
                }
                if win_conditions[m] == o:
                    # I won
                    self.start_game(first_turn=True)
                else:
                    # I lost
                    self.start_game(first_turn=False)

    def start_game(self, first_turn):
        self.game_started = True
        self.gui.show_frame("game")
        self.set_turn(first_turn)
        
        # Draw my ships
        for r in range(10):
            for c in range(10):
                if self.game_logic.board[r][c] == 1:
                    self.gui.update_cell("my", r, c, "ship")

    def set_turn(self, my_turn):
        self.my_turn = my_turn
        self.gui.set_turn(my_turn)

if __name__ == "__main__":
    app = BattleshipApp()
    app.start()
