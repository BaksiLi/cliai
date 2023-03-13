#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, isdir
import json
from typing import Dict,  List
import questionary as q

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".cliai")


class Preset(List[Dict]):
    """
    The individual Preset we use later, a warpper around List of dictionries 

    Currently assume it is loaded from json file or created from a Dict, with all proper keys within proper range
    """

    def __init__(self, name: str, config: Dict) -> None:

        self.name:str = name

        self.role:str = config["role"]
        self.temperature: float = float(config["temperature"])
        self.maximal_length:int = int(config["maximal_length"])
        self.top_p: float = float(config["top_p"])
        self.frequency_panalty:float = float(config["frequency_panalty"])
        self.presence_panalty:float = float(config["presence_panalty"])


class PresetsHandler:
    """
    The class to handle presets
    """

    def __init__(self, config_dir: str = DEFAULT_CONFIG_DIR) -> None:
        self.config_dir = config_dir

        if not isdir(self.config_dir):
            print(
                f"The configuration directory {self.config_dir} is not created, create one. But note this is weird and should not be happening"
            )
            os.makedirs(self.config_dir)

        self.preset_path: str = os.path.join(self.config_dir, "presets.json")

        self.presets: Dict[str, Dict] = {}

        if not isfile(self.preset_path):
            print(f"presets not found in {config_dir}, create a new one with a default")
            self.create_default_preset()

        else:
            self.load_from_config()

    def select_preset(self) -> Preset:
        """
        let the user select a preset using numbers

        :return: None
        """
        preset_keys: List[str] = list(self.presets.keys())

        preset_choices: List[str] = []
        for i, key in enumerate(preset_keys):
            preset_choices.append(key)

        preset_choices.append("create a new bot")

        choice:str = q.select(message="Please select from presets:", choices=preset_choices).ask()

        print(choice)

        # the logic for entering custom presets
        if choice == "create a new bot":
            config: Dict = {}

            role:str = q.text("Please describe the role you want AI to behave", multiline=True).ask()
            config["role"] = role

            temperature:float = float(
                q.text("Please enter the desired temperature between 0 and 1, default to ", default="1").ask()
            )
            assert 0 <= temperature <= 1, "Temperature must be between 0 and 1"
            config["temperature"] = str(temperature)

            maximal_length:int = int(q.text("Please enter the maximal_length as integer between 1 and 2048, default ",default="2048").ask())
            assert 1 <= maximal_length <= 2048, "maximal_length must be between 1 and 2048"
            config["maximal_length"] = str(maximal_length)

            top_p: float = float(q.text("Please enter the top_p as float point number between 0 and 1, default ", default="1").ask())
            assert 0 <= top_p <= 1, "top_p must be between 0 and 1"
            config["top_p"] = str(top_p)

            frequency_panalty:float = float(q.text("Please enter the frequency_panalty as float point number between 0 and 2, default to ", default="0").ask())
            assert 0 <= frequency_panalty <= 2, "frequency_panalty must be between 0 and 2"
            config["frequency_panalty"] = str(frequency_panalty)

            presence_panalty:float = float(q.text("Please enter the presence_panalty as float point number between 0 and 2, default to ",default="0").ask())
            assert 0 <= presence_panalty <= 2, "presence_panalty must be between 0 and 2"
            config["presence_panalty"] = str(presence_panalty)

            name:str = q.text("Great! Lastly, enter the name of your new bot",default="Another new bot").ask()

            preset: Preset = Preset(name, config)

            self.presets[name] = config
            with open(self.preset_path, "w+") as f:
                json.dump(self.presets, f)

            return preset

        else:
            preset :Preset = Preset(choice, self.presets[choice])
            return preset
            

    def load_from_config(self) -> None:
        with open(self.preset_path, "r") as f:
            self.presets = json.load(f)

    def create_default_preset(self)->None:

        default_preset: Dict[str, Dict] = {
            "default": {
                "role": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.",
                "temperature": "1",
                "maximal_length": "256",
                "top_p": "1",
                "frequency_panalty": "0",
                "presents_panalty": "0",
            }
        }
        self.presets = default_preset
        with open(self.preset_path, "w+") as f:
            json.dump(self.presets, f)


if __name__ == "__main__":
    presets = PresetsHandler()
    presets.select_preset()
