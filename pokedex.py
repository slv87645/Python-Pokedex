import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
import urllib3
from io import BytesIO
from socket import *

# Dimensions of Window
window = tk.Tk()
window.geometry("800x400")
window.title("CS361 Pokedex")
window.config(padx=10, pady=10)

# Frames as "Pages" for different information
frame_a = tk.Frame(window)
frame_b = tk.Frame(window)
frame_c = tk.Frame(window)
frame_d = tk.Frame(window)

title_label = tk.Label(master=frame_a, text="Steven's Pokedex")
title_label.config(font=('Arial', 32))
title_label.pack(padx=10, pady=10)

# Text boxes that get populated after search
pokemon_image = tk.Label(master=frame_b)
pokemon_image.pack(padx=10, pady=10)

pokemon_information = tk.Label(master=frame_b)
pokemon_information.config(font=("Arial", 20))
pokemon_information.pack(padx=10, pady=10)

pokemon_bio = tk.Label(master=frame_b)
pokemon_bio.config(font=("Arial", 20))
pokemon_bio.pack(padx=10, pady=10)

pokemon_types = tk.Label(master=frame_c)
pokemon_types.config(font=("Arial", 20))
pokemon_types.pack(padx=10, pady=10)

pokemon_abilities = tk.Label(master=frame_c)
pokemon_abilities.config(font=("Arial", 20))
pokemon_abilities.pack(padx=10, pady=10)

pokemon_stats = tk.Label(master=frame_c)
pokemon_stats.config(font=("Arial", 20))
pokemon_stats.pack(padx=10, pady=10)

confirmation = tk.Label(master=frame_d, text="Are you sure?")
confirmation.config(font=("Arial", 20))
confirmation.pack(padx=10, pady=10)


def load_pokemon():
    """
    Retrieves data from API and passes object into functions to retrieve information
    """
    # switch to "new" page to show information
    show_frame_b()
    pokemon = pypokedex.get(name=text_id_name.get(1.0, "end-1c"))

    load_image(pokemon)
    load_information(pokemon)


def load_image(pokemon):
    """
    Obtains sprite image data from object and displays image

    :param pokemon: object made from API
    """
    http = urllib3.PoolManager()
    response = http.request('GET', pokemon.sprites.front.get('default'))
    image = PIL.Image.open(BytesIO(response.data))

    img = PIL.ImageTk.PhotoImage(image)
    pokemon_image.config(image=img)
    pokemon_image.image = img


def load_information(pokemon):
    """
    Obtains basic information data from object and populates it into window

    :param pokemon: object made from API
    """
    bio = pokemon.get_descriptions()
    pokemon_information.config(text=f"No: {pokemon.dex} - {pokemon.name.title()}")
    pokemon_bio.config(text=f"Entry: {bio.get('sword')}")
    pokemon_types.config(text="Typing: " + " - ".join([t for t in pokemon.types]).title())
    pokemon_abilities.config(text="Abilities: " + " , ".join([t.name for t in pokemon.abilities]).title())
    pokemon_stats.config(text=f"{pokemon.base_stats}")


def load_random():
    """
    Utilizes partner microservice to generate random pokemon ID that will be used to load random pokemon
    and its information.
    """
    show_frame_b()
    # partner microservice
    random_number = run_client()
    pokemon = pypokedex.get(name=f"{random_number}")

    load_image(pokemon)
    load_information(pokemon)


def run_client():
    """
    Connects to a socket server and receives a random ID number.
    """
    serverPort = 9344
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('localhost', serverPort))
    print("You are now connected to the server.")
    randNum = str(clientSocket.recv(4096).decode())
    print("The random id number is: " + randNum)
    clientSocket.close()
    return randNum


def show_frame_a():
    window.geometry("800x400")
    frame_b.pack_forget()
    frame_c.pack_forget()
    frame_d.pack_forget()
    frame_a.pack()


def show_frame_b():
    window.geometry("800x600")
    frame_a.pack_forget()
    frame_c.pack_forget()
    frame_d.pack_forget()
    frame_b.pack()


def show_frame_c():
    window.geometry("1000x400")
    frame_a.pack_forget()
    frame_b.pack_forget()
    frame_d.pack_forget()
    frame_c.pack()


def show_frame_d():
    frame_a.pack_forget()
    frame_b.pack_forget()
    frame_c.pack_forget()
    frame_d.pack()


# Functional buttons that are visible to user
yes_btn = tk.Button(master=frame_d, text='Yes', command=show_frame_a)
yes_btn.config(font=("Arial", 20))
yes_btn.pack(padx=10, pady=10)

no_btn = tk.Button(master=frame_d, text='No', command=show_frame_b)
no_btn.config(font=("Arial", 20))
no_btn.pack(padx=10, pady=10)

info_load = tk.Button(master=frame_b, text='More info', command=show_frame_c)
info_load.config(font=("Arial", 20))
info_load.pack(padx=10, pady=10)

home_button = tk.Button(master=frame_b, text="Click here to search for a new pokemon", command=show_frame_d)
home_button.config(font=("Arial", 20))
home_button.pack()

back_button = tk.Button(master=frame_c, text="Return to basic information", command=show_frame_b)
back_button.config(font=("Arial", 20))
back_button.pack()

label_id_name = tk.Label(master=frame_a, text="ID or Name")
label_id_name.config(font=("Arial", 20))
label_id_name.pack(padx=10, pady=10)

text_id_name = tk.Text(master=frame_a, height=1)
text_id_name.config(font=("Arial", 20))
text_id_name.pack(padx=10, pady=10)

btn_load = tk.Button(master=frame_a, text="Search Pokemon", command=load_pokemon)
btn_load.config(font=("Arial", 20))
btn_load.pack(padx=10, pady=10)

btn_random = tk.Button(master=frame_a, text="Load Random Pokemon", command=load_random)
btn_random.config(font=("Arial", 20))
btn_random.pack(padx=10, pady=10)

show_frame_a()

window.mainloop()