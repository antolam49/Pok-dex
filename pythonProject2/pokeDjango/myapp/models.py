import string

from django.db import models


# Create your models here.
class Pokemon(models.Model):
    id: int
    name: string
    img: string
    abilities: list

    def __init__(self, id, name, img):
        self.id = id
        self.name = name
        self.img = img
        self.abilities = []

    def addAbility(self, ability):
        self.abilities.append(ability)

class Pokemon_fr(models.Model):
    id: int
    name: string
    img: string
    #type: string

    def __init__(self, id, name, img):
        self.id = id
        self.name = name
        self.img = img

class Ability(models.Model):
    id: int
    name: string
    effect: string

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Team(models.Model):
    listPokemon: list

    def addPokemon(self, pokemon):
        self.listPokemon.append(self, pokemon)

    def suppPokemon(self, pokemon):
        self.listPokemon.remove(self, pokemon)
