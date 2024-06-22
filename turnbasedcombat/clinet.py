import customtkinter as ctk
import socket
import threading
from PIL import Image, ImageTk
from characters import Character, Warrior, Mage, Cleric

background_image_path = r"C:\Users\User\turnbasedcombat\images\background.jpg"
image_path_left = r"C:\Users\User\turnbasedcombat\images\images-_1_.jpg"
is_player_turn = False  # Global variable to track if it's the player's turn

class GameClient:
    def __init__(self, selected_character, host='127.0.0.1', port=65432):
        self.selected_character = selected_character
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            self.client.send(self.selected_character['name'].encode('utf-8'))  # Send the selected character to the server

            self.connected = True
            self.listener = threading.Thread(target=self.receive_messages)
            self.listener.daemon = True
            self.listener.start()
            self.on_connected()
        except Exception as e:
            print(f"Connection failed: {e}")

    def send_message(self, message):
        if self.connected:
            try:
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Sending message failed: {e}")
                self.connected = False

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")
                    handle_server_message(message)
                else:
                    self.client.close()
                    self.connected = False
                    break
            except:
                self.client.close()
                self.connected = False
                break

    def on_connected(self):
        display_battle_window(self.selected_character)

    def close(self):
        self.connected = False
        self.client.close()

def create_status_bar(canvas, x, y, width, height, max_value, current_value, fill_color):
    # Outer black rectangle
    canvas.create_rectangle(x - 1, y - 1, x + width + 1, y + height + 1, fill='black', outline='black')
    # Background rectangle
    canvas.create_rectangle(x, y, x + width, y + height, fill='red', outline='black')
    # Foreground rectangle
    fill_width = (current_value / max_value) * width
    canvas.create_rectangle(x, y, x + fill_width, y + height, fill=fill_color, outline='black')

def perform_action(action):
    global is_player_turn
    if is_player_turn:
        if action == 'fight':
            print("Fight button clicked")
            client.send_message(f"action fight {player_character.attack_power}")
        elif action == 'special':
            print("Special Attacks button clicked")
            client.send_message("action special")
        elif action == 'run':
            print("Run button clicked")
            client.send_message("action run")
        is_player_turn = False

def update_health_and_mp(character, health_amount, mp_amount):
    character.current_health = max(0, min(character.max_health, character.current_health + health_amount))
    character.current_mp = max(0, min(character.max_mp, character.current_mp + mp_amount))
    canvas.delete("all")
    create_status_bar(canvas, 100, 50, 300, 20, player_character.max_health, player_character.current_health, 'green')
    create_status_bar(canvas, 100, 80, 300, 20, player_character.current_mp, player_character.current_mp, 'blue')
    create_status_bar(canvas, 500, 50, 300, 20, enemy_character.max_health, enemy_character.current_health, 'green')
    create_status_bar(canvas, 500, 80, 300, 20, enemy_character.current_mp, enemy_character.current_mp, 'blue')
    player_hp_label.config(text=f"{player_character.current_health}/{player_character.max_health} HP")
    player_mp_label.config(text=f"{player_character.current_mp}/{player_character.max_mp} MP")
    enemy_hp_label.config(text=f"{enemy_character.current_health}/{enemy_character.max_health} HP")
    enemy_mp_label.config(text=f"{enemy_character.current_mp}/{enemy_character.current_mp} MP")
    print(player_character.current_health)

def handle_server_message(message):
    global is_player_turn, enemy_character
    parts = message.split()
    action = parts[0]

    if action == "update_health_mp":
        character_type = parts[1]
        health_amount = int(parts[2])
        mp_amount = int(parts[3])
        if character_type == "player":
            root.after(0, update_health_and_mp, player_character, health_amount, mp_amount)
        elif character_type == "enemy":
            root.after(0, update_health_and_mp, enemy_character, health_amount, mp_amount)
    elif action == "your_turn":
        is_player_turn = True
    elif action == "enemy_selected":
        enemy_name = parts[1]
        if enemy_name == "Warrior":
            enemy_character = Warrior()
        elif enemy_name == "Mage":
            enemy_character = Mage()
        elif enemy_name == "Cleric":
            enemy_character = Cleric()
        root.after(0, update_enemy_image)
    elif action == "waiting":
        print("Waiting for another player")

def update_enemy_image():
    global enemy_character, root
    # Load the enemy character image
    enemy_image_path = enemy_character.picture_path
    original_image_right = Image.open(enemy_image_path)
    image_width, image_height = original_image_right.size
    # Resize image to fit within 400x300 while maintaining aspect ratio
    max_width, max_height = 400, 300
    if image_width > max_width or image_height > max_height:
        ratio = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * ratio), int(image_height * ratio))
        resized_image_right = original_image_right.resize(new_size, Image.Resampling.LANCZOS)
    else:
        resized_image_right = original_image_right

    logo_right = ImageTk.PhotoImage(resized_image_right)

    # Update the label to display the enemy character image
    image_label_right.config(image=logo_right)
    image_label_right.image = logo_right  # Keep a reference to the image to prevent garbage collection

def display_battle_window(selected_character):
    global canvas, player_hp_label, player_mp_label, enemy_hp_label, enemy_mp_label, root, player_character, enemy_character, image_label_right
    root = ctk.CTk()
    root.title("Turn-Based Combat Game")
    root.geometry("900x900")

    if selected_character['name'] == "Warrior":
        player_character = Warrior()
    elif selected_character['name'] == "Mage":
        player_character = Mage()
    elif selected_character['name'] == "Cleric":
        player_character = Cleric()
    # Add more character classes as needed

    enemy_character = Mage()  # Default enemy character before receiving actual enemy selection

    # Load the background image
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(background_image)
    
    # Create a background label
    background_label = ctk.CTkLabel(root, text="", image=bg_image)
    background_label.image = bg_image  # Keep a reference to the image to prevent garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load the left image
    original_image_left = Image.open(player_character.picture_path)
    image_width, image_height = original_image_left.size
    # Resize image to fit within 400x300 while maintaining aspect ratio
    max_width, max_height = 400, 300
    if image_width > max_width or image_height > max_height:
        ratio = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * ratio), int(image_height * ratio))
        resized_image_left = original_image_left.resize(new_size, Image.Resampling.LANCZOS)
    else:
        resized_image_left = original_image_left

    logo_left = ImageTk.PhotoImage(resized_image_left)

    # Create a label to display the left image
    image_label_left = ctk.CTkLabel(root, text="", image=logo_left)
    image_label_left.image = logo_left  # Keep a reference to the image to prevent garbage collection
    image_label_left.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    # Load the right image (initial enemy image, will be updated later)
    original_image_right = Image.open(player_character.picture_path)
    image_width, image_height = original_image_right.size
    if image_width > max_width or image_height > max_height:
        ratio = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * ratio), int(image_height * ratio))
        resized_image_right = original_image_right.resize(new_size, Image.Resampling.LANCZOS)
    else:
        resized_image_right = original_image_right

    logo_right = ImageTk.PhotoImage(resized_image_right)

    # Create a label to display the right image (enemy)
    image_label_right = ctk.CTkLabel(root, text="", image=logo_right)
    image_label_right.image = logo_right  # Keep a reference to the image to prevent garbage collection
    image_label_right.grid(row=0, column=3, padx=20, pady=20, sticky="e")

    canvas = ctk.CTkCanvas(root, width=900, height=200, bg='black')
    canvas.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="n")

    create_status_bar(canvas, 100, 50, 300, 20, player_character.max_health, player_character.current_health, 'green')
    create_status_bar(canvas, 100, 80, 300, 20, player_character.current_mp, player_character.current_mp, 'blue')
    create_status_bar(canvas, 500, 50, 300, 20, enemy_character.max_health, enemy_character.current_health, 'green')
    create_status_bar(canvas, 500, 80, 300, 20, enemy_character.current_mp, enemy_character.current_mp, 'blue')

    player_hp_label = ctk.CTkLabel(root, text=f"{player_character.current_health}/{player_character.max_health} HP")
    player_hp_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    player_mp_label = ctk.CTkLabel(root, text=f"{player_character.current_mp}/{player_character.max_mp} MP")
    player_mp_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")

    enemy_hp_label = ctk.CTkLabel(root, text=f"{enemy_character.current_health}/{enemy_character.max_health} HP")
    enemy_hp_label.grid(row=2, column=3, padx=20, pady=5, sticky="e")
    enemy_mp_label = ctk.CTkLabel(root, text=f"{enemy_character.current_mp}/{enemy_character.max_mp} MP")
    enemy_mp_label.grid(row=3, column=3, padx=20, pady=5, sticky="e")

    button_frame = ctk.CTkFrame(root)
    button_frame.grid(row=4, column=0, columnspan=4, pady=20)

    fight_button = ctk.CTkButton(button_frame, text="Fight", command=lambda: perform_action('fight'))
    special_button = ctk.CTkButton(button_frame, text="Special Attacks", command=lambda: perform_action('special'))
    run_button = ctk.CTkButton(button_frame, text="Run", command=lambda: perform_action('run'))

    fight_button.grid(row=0, column=0, padx=20, pady=10)
    special_button.grid(row=0, column=1, padx=20, pady=10)
    run_button.grid(row=0, column=2, padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    selected_character = {"name": "Warrior", "image_path": "path_to_warrior_image.png"}  # Example character selection
    client = GameClient(selected_character)
    client.connect()