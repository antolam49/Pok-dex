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

class PokemonS(models.Model):
    id: int
    name: string
    img: string
    abilities: list
    random: int
    shiny: string

    def __init__(self, id, name, img, random, shiny):
        self.id = id
        self.name = name
        self.img = img
        self.abilities = []
        self.random = random
        self.shiny = shiny

    def addAbility(self, ability):
        self.abilities.append(ability)

class Pokemon_fr(models.Model):
    id: int
    name: string
    img: string
    faiblesses: list
    types: list
    hp: int
    attaque: int
    defense: int
    attaque_spe: int
    defense_spe: int
    speed: int
    nextPoke: list
    prePoke: list
    preId: int
    nextId: int
    shiny: string
    back_shiny: string
    back: string

    def __init__(self, id, name, img, hp, attaque, defense, attaque_spe, defense_spe, speed,preId, nextId, shiny, back_shiny, back):
        self.id = id
        self.name = name
        self.img = img
        self.hp = hp
        self.attaque = attaque
        self.defense = defense
        self.attaque_spe = attaque_spe
        self.defense_spe = defense_spe
        self.speed = speed
        self.faiblesses = []
        self.types = []
        self.nextPoke = []
        self.prePoke = []
        self.preId = preId
        self.nextId = nextId
        self.shiny = shiny
        self.back_shiny = back_shiny
        self.back = back

    def addNextEvo(self, nextEvo):
        self.nextPoke.append(nextEvo)
    def addPreEvo(self, preEvo):
        self.prePoke.append(preEvo)
    def addFaiblesse(self, faiblesse):
        self.faiblesses.append(faiblesse)

    def addType(self, type):
        self.types.append(type)

class Faiblesse(models.Model):
    name: string
    dmg_multiplier: int
    dmg_relation: string
    image: string

    def __init__(self, name, dmg_multiplier, dmg_relation, image):
        self.name = name
        self.dmg_multiplier = dmg_multiplier
        self.dmg_relation = dmg_relation
        self.image = image

class nextEvo(models.Model):
    id: int
    name: string
    image: string
    shiny: string
    def __init__(self, id, name, image, shiny):
        self.id = id
        self.name = name
        self.image = image
        self.shiny = shiny

class preEvo(models.Model):
    id: int
    name: string
    image: string
    shiny: string
    def __init__(self, id, name, image, shiny):
        self.id = id
        self.name = name
        self.image = image
        self.shiny = shiny

class Ability(models.Model):
    id: int
    name: string
    effect: string

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Type(models.Model):
    name: string
    image: string

    def __init__(self, name, image):
        self.name = name
        self.image = image
class Team(models.Model):
    listPokemon: list

    def addPokemon(self, pokemon):
        self.listPokemon.append(self, pokemon)

    def suppPokemon(self, pokemon):
        self.listPokemon.remove(self, pokemon)
