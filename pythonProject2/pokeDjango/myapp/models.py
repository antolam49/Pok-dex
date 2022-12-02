import string

from django.db import models

class Joueur(models.Model):
    pokemons: list

    def __init__(self):
        self.pokemons = []
    def addPoke(self, pokemon):
        self.pokemons.append(pokemon)
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
    statHp: int
    statAttack: int
    statDefense: int
    statAttackSpe: int
    statDefenseSpe: int
    statSpeed: int

    def __init__(self, id, name, img, hp, attaque, defense, attaque_spe, defense_spe, speed,preId, nextId, shiny, back_shiny, back, statHp, statAttack, statDefense, statAttackSpe, statDefenseSpe, statSpeed):
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
        self.statHp = statHp
        self.statAttack = statAttack
        self.statDefense = statDefense
        self.statAttackSpe = statAttackSpe
        self.statDefenseSpe = statDefenseSpe
        self.statSpeed = statSpeed

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
    listType: list

    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.listType = []

    def addType(self, type):
        self.listType.append(type)


class listType(models.Model):
    id: int
    listFeu: list
    listEau: list
    listPlante: list
    listTénèbres: list
    listInsecte: list
    listPsy: list
    listAcier: list
    listDragon: list
    listFée: list
    listSol: list
    listRoche: list
    listPoison: list
    listÉlectrik: list
    listGlace: list
    listVol: list
    listCombat: list
    listNormal: list
    listSpectre: list

    def __init__(self, id):
        self.id = id
        self.listFeu = []
        self.listEau = []
        self.listÉlectrik = []
        self.listNormal = []
        self.listAcier = []
        self.listCombat = []
        self.listDragon = []
        self.listFée = []
        self.listGlace = []
        self.listInsecte = []
        self.listPlante = []
        self.listPoison = []
        self.listPsy = []
        self.listRoche = []
        self.listSol = []
        self.listTénèbres = []
        self.listVol = []
        self.listSpectre = []

    def addNormal(self, pokemon):
        self.listNormal.append(pokemon)
    def addFeu(self, pokemon):
        self.listFeu.append(pokemon)
    def addEau(self, pokemon):
        self.listEau.append(pokemon)
    def addPlante(self, pokemon):
        self.listPlante.append(pokemon)
    def addElek(self, pokemon):
        self.listÉlectrik.append(pokemon)
    def addGlace(self, pokemon):
        self.listGlace.append(pokemon)
    def addFee(self, pokemon):
        self.listFée.append(pokemon)
    def addDragon(self, pokemon):
        self.listDragon.append(pokemon)
    def addSol(self, pokemon):
        self.listSol.append(pokemon)
    def addRoche(self, pokemon):
        self.listRoche.append(pokemon)
    def addVol(self, pokemon):
        self.listVol.append(pokemon)
    def addPsy(self, pokemon):
        self.listPsy.append(pokemon)
    def addPoison(self, pokemon):
        self.listPoison.append(pokemon)
    def addCombat(self, pokemon):
        self.listCombat.append(pokemon)
    def addTenebre(self, pokemon):
        self.listTénèbres.append(pokemon)
    def addInsecte(self, pokemon):
        self.listInsecte.append(pokemon)
    def addAcier(self, pokemon):
        self.listAcier.append(pokemon)
    def addSpectre(self, pokemon):
            self.listSpectre.append(pokemon)


class Team(models.Model):
    listPokemon: list

    def addPokemon(self, pokemon):
        self.listPokemon.append(self, pokemon)

    def suppPokemon(self, pokemon):
        self.listPokemon.remove(self, pokemon)
