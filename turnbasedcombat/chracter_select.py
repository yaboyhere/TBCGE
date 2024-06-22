import customtkinter as ctk
from PIL import Image, ImageTk
from clinet import GameClient  # Assuming this is the correct import

class CharacterSelectionUI:
    def __init__(self, master, player_name, character_data, on_character_selected):
        self.master = master
        self.player_name = player_name
        self.character_data = character_data
        self.on_character_selected = on_character_selected
        self.selected_character = None
        
        self.master.title(f"Character Selection - {self.player_name}")
        
        ctk.CTkLabel(master, text=f"Welcome, {self.player_name}! Choose your character:", font=("Arial", 16)).pack(pady=10)
        
        self.character_frame = ctk.CTkFrame(master)
        self.character_frame.pack(pady=10)
        
        for character in self.character_data:
            self.create_character_button(character)
        
        self.confirm_button = ctk.CTkButton(master, text="Confirm", command=self.confirm_selection)
        self.confirm_button.pack(pady=20)
        
    def create_character_button(self, character):
        image = Image.open(character['image_path'])
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        button = ctk.CTkButton(self.character_frame, image=photo, text=character['name'], compound="top", command=lambda: self.select_character(character))
        button.image = photo  # Keep a reference to avoid garbage collection
        button.pack(side="left", padx=10)
        
    def select_character(self, character):
        self.selected_character = character
        print(f"Selected character: {character['name']}")
        
    def confirm_selection(self):
        if self.selected_character:
            print(f"Player {self.player_name} selected character: {self.selected_character['name']}")
            self.master.destroy()
            self.on_character_selected(self.selected_character)

def start_character_selection():
    root = ctk.CTk()
    character_data = [
        {"name": "Warrior", "image_path": r"C:\Users\User\turnbasedcombat\images\images (1).jpeg"},
        {"name": "Mage", "image_path": r"C:\Users\User\turnbasedcombat\images\images.jpg"},
        {"name": "cleric", "image_path": r"C:\Users\User\turnbasedcombat\images\images-_2_.jpg"}
    ]
    CharacterSelectionUI(root, "Player 1", character_data, start_combat_screen)
    root.mainloop()

def start_combat_screen(selected_character):
    print(selected_character)
    client = GameClient(selected_character)
    client.connect()

if __name__ == "__main__":
    start_character_selection()