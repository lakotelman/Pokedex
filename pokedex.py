import requests
from pprint import pprint
from rich import print
import json
import os
import artwork

def clear(): 
   os.system("clear||cls")

class Pokemon:
    def __init__(self, name, types_, weight, height, abilities, health_points, attack_points, defense_points):
        self.name = name
        self.types_ = types_ 
        self.weight = weight 
        self.height = height 
        self.abilities = abilities 
        self.health_points = health_points
        self.attack_points = attack_points
        self.defense_points = defense_points
    
    def __repr__(self): #list Pokemon information 
        return f"Pokemon: {self.name.title()} Type:{self.types_}"

    def __dict__(self):
        print(f"""
---------- {self.name.upper()}----------
Type(s): {(", ".join(self.types_)).title()}
Weight: {self.weight}
Height: {self.height}
Abilities: {(", ".join(self.abilities)).title()}
Health Points: {self.health_points}
Attack Points: {self.attack_points}
Defense Points: {self.defense_points}
         """)

class Pokedex: 
    def __init__(self): 
        self.wholepokedex = {
            "fire": [],
            "water": [],
            "rock": [], 
            "electric": [],
            "grass":[],
            "poison": [], 
            "fairy": [], 
            "psychic": [],
            "normal": [],
            "other": []
        }

    def fetch_and_add_pokemon(self, newpokemon: str):
        for k,v in self.wholepokedex.items():
            for pokemon in v: 
                if newpokemon == pokemon.name:
                    print(f"You already have {newpokemon} in your pokedex")
                    return None
                else: 
                    continue
        try:
            api_link = f"https://pokeapi.co/api/v2/pokemon/{newpokemon}"
            self.poke_data = requests.get(api_link).json()
            self.add_pokemon(self.poke_data)
            print(f"Entered {newpokemon.title()} into your Pokedex!")
        except json.JSONDecodeError:
            print("That pokemon doesn't exist. Perhaps you misspelled it?")

    def add_pokemon(self, poke_data: dict ): 
        p = Pokemon ( 
            name = poke_data["name"],
            types_ = {item["type"]["name"] for item in poke_data["types"]},
            weight = poke_data["weight"],
            height = poke_data["height"],
            abilities = [item["ability"]["name"] for item in poke_data["abilities"]],
            health_points = poke_data["stats"][0]["base_stat"],
            attack_points = poke_data["stats"][1]["base_stat"],
            defense_points = poke_data["stats"][2]["base_stat"]
        )
        has_type_category = False
        for k in self.wholepokedex.keys(): 
            if k in p.types_:
                has_type_category = True 
                self.wholepokedex[k].append(p)
        if has_type_category == False: 
                self.wholepokedex["other"].append(p)


    def all_poke_by_type(self): 
        for k,v in self.wholepokedex.items():
            if len(v) == 0:
                continue
            just_names = [pokemon.name.title() for pokemon in v]
            just_names.sort()
            formatted_names = "- "+"\n- ".join(just_names)

            print(f""" 
---------- Type:{k.title()} ----------
{formatted_names}
            """)

    def show_poke_details(self, specific_pokemon): 
        for type_list in self.wholepokedex.values(): 
            for p in type_list:
                    if p.name == specific_pokemon: 
                        p.__dict__()
                        return None
             
        print("\nHmm. I couldn't find that one.\n ") 
                



def catchemall():
    main_dex = Pokedex()
    while True: 
        clear()
        print(artwork.yourpokedex)
        option = input("\n-----What would you like to do?-----\n \n[A]dd a pokemon? \n[V]iew the whole Pokedex by type? \n[S]ee details for a specific pokemon? \nYou can [q]uit at any time ").lower().strip()
        if option == "q": 
            print(artwork.pikachu)
            break
        elif option == "a": 
            while True:
                poke_input= input("\nWhich pokemon would you like to add?(Remember you can enter [b] to go back.) ")
                if poke_input == "b": 
                    break
                else:
                    main_dex.fetch_and_add_pokemon(poke_input)
        elif option == "v": 
            main_dex.all_poke_by_type()
            input("Press enter to continue")
        elif option =="s": 
            specific_pokemon = input("\nWhose details would you like to see? ")
            main_dex.show_poke_details(specific_pokemon)
            input("Press enter to continue")
        else: 
            print("\nI don't understand your command. Try again?")


catchemall()

