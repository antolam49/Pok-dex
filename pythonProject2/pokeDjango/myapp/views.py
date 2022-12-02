import contextvars

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
from .forms import SearchForm
import random

import json

from . import models
from .models import Pokemon

pokemonTeam = []
allPokemon = []

def team(request):
    context = {}
    listPoke = []
    listPokeAdv = []
    size = [0,0,0,0,0,0]
    for x in range(0, len(size)):
        j = random.randint(1, 1000)
        infoPoke = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(j) + '/').json()
        #infoPokeFr = requests.get('https://pokebuildapi.fr/api/v1/pokemon/' + str(j) + '/').json()
        i = random.randint(1, 1000)
        infoPokeAdv = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(i) + '/').json()
        #infoPokeFrAdv = requests.get('https://pokebuildapi.fr/api/v1/pokemon/' + str(i) + '/').json()
        poke = models.Pokemon(infoPoke['id'], infoPoke['name'], infoPoke['sprites']['front_shiny'])
        pokeAdv = models.Pokemon(infoPokeAdv['id'], infoPokeAdv['name'], infoPokeAdv['sprites']['front_shiny'])
        for y in range(0, len(infoPoke['abilities'])):
            poke.addAbility(
                models.Ability(getAbilityId(infoPoke['abilities'][y]['ability']['url']),
                               infoPoke['abilities'][y]['ability']['name']))
        for z in range(0, len(infoPokeAdv['abilities'])):
            pokeAdv.addAbility(
                models.Ability(getAbilityId(infoPokeAdv['abilities'][z]['ability']['url']),
                               infoPokeAdv['abilities'][z]['ability']['name']))
        listPoke.append(poke)
        listPokeAdv.append(pokeAdv)
        context = {
            'listPoke': listPoke,
            'listPokeAdv': listPokeAdv
        }
    return render(request, 'team.html', context)

def pokemon(request, id: int):
    infoPoke = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(id) + '/').json()
    poke = models.Pokemon(infoPoke['id'], infoPoke['name'], infoPoke['sprites']['front_shiny'])
    for y in range(0, len(infoPoke['abilities'])):
        poke.addAbility(
            models.Ability(getAbilityId(infoPoke['abilities'][y]['ability']['url']),
                           infoPoke['abilities'][y]['ability']['name'])
        )
    context = {'poke': poke}
    return render(request, 'pokemon.html', context)

def pokemon_fr(request, id: int):
    infoPoke = requests.get('https://pokebuildapi.fr/api/v1/pokemon/' + str(id) + '/').json()
    infoShiny = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(id) + '/').json()
    preId = infoPoke['id'] - 1
    nextId = infoPoke['id'] + 1
    statHp = (infoPoke['stats']['HP'] * 100) / 261
    statAttack = (infoPoke['stats']['attack']  * 100) / 261
    statDefense = (infoPoke['stats']['defense']  * 100) / 261
    statAttackSpe = (infoPoke['stats']['special_attack']  * 100) / 261
    statDefenseSpe = (infoPoke['stats']['special_defense']  * 100) / 261
    statSpeed = (infoPoke['stats']['speed']  * 100) / 261

    poke_fr = models.Pokemon_fr(infoPoke['id'], infoPoke['name'], infoPoke['sprite'], infoPoke['stats']['HP'],
                                infoPoke['stats']['attack'], infoPoke['stats']['defense'], infoPoke['stats']['special_attack'],
                                infoPoke['stats']['special_defense'], infoPoke['stats']['speed'], preId, nextId, infoShiny['sprites']['front_shiny'],
                                infoShiny['sprites']['back_shiny'], infoShiny['sprites']['back_default'], statHp, statAttack,
                                statDefense, statAttackSpe, statDefenseSpe, statSpeed)

    infoType = requests.get('https://pokebuildapi.fr/api/v1/types').json()



    if infoPoke['apiEvolutions'] != []:
        infoNextPoke = requests.get(
            'https://pokebuildapi.fr/api/v1/pokemon/' + str(infoPoke['apiEvolutions'][0]['pokedexId']) + '/').json()
        infoShinyNextPoke = requests.get(
            'https://pokeapi.co/api/v2/pokemon/' + str(infoPoke['apiEvolutions'][0]['pokedexId']) + '/').json()
        poke_fr.addNextEvo(
            models.nextEvo(infoPoke['apiEvolutions'][0]['pokedexId'], infoPoke['apiEvolutions'][0]['name'], infoNextPoke['image'], infoShinyNextPoke['sprites']['front_shiny']))
    if infoPoke['apiPreEvolution'] != "none":
        infoPrePoke = requests.get(
            'https://pokebuildapi.fr/api/v1/pokemon/' + str(infoPoke['apiPreEvolution']['pokedexIdd']) + '/').json()
        infoShinyPrePoke = requests.get(
            'https://pokeapi.co/api/v2/pokemon/' + str(infoPoke['apiPreEvolution']['pokedexIdd']) + '/').json()
        poke_fr.addPreEvo(
            models.preEvo(infoPoke['apiPreEvolution']['pokedexIdd'], infoPoke['apiPreEvolution']['name'], infoPrePoke['image'], infoShinyPrePoke['sprites']['front_shiny']))

    for x in range(0, len(infoPoke['apiTypes'])):
        poke_fr.addType(
            models.Type(str(infoPoke['apiTypes'][x]['name']), str(infoPoke['apiTypes'][x]['image']))
        )

    for y in range(0, len(infoPoke['apiResistances'])):
        poke_fr.addFaiblesse(
            models.Faiblesse(infoPoke['apiResistances'][y]['name'],
                           infoPoke['apiResistances'][y]['damage_multiplier'], infoPoke['apiResistances'][y]['damage_relation'], infoType[y]['image'])
        )

    context = {'poke_fr': poke_fr}
    return render(request, 'pokemon_fr.html', context)


def name(request):
    return index(request)

def name_fr(request):
    return index_fr(request)

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            infoPoke = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(form.data['your_name'])).json()
            poke = models.Pokemon(infoPoke['id'], infoPoke['name'], infoPoke['sprites']['front_shiny'])
            return pokemon(request, poke.id)

    else:
        global allPokemon
        if not allPokemon:
            listPoke = setList()
            allPokemon = listPoke
            print("Not all Poke en")
        else:
            listPoke = allPokemon
            print("All Poke EN")


        form = SearchForm()
        context = {'listPoke': listPoke,
                   'form': form}
        return render(request, 'index.html', context)

def index_fr(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            infoPoke = requests.get('https://pokebuildapi.fr/api/v1/pokemon/' + str(form.data['your_name'])).json()
            poke_fr = models.Pokemon(infoPoke['id'], infoPoke['name'], infoPoke['image'])
            return pokemon_fr(request, poke_fr.id)

    else:
        global allPokemon
        if not allPokemon:
            listPoke_fr = setList_fr()
            allPokemon = listPoke_fr
            print("Not all Poke fr")
        else:
            listPoke_fr = allPokemon
            print("All Poke fr")

        form = SearchForm()
        context = {'listPoke_fr': listPoke_fr,
                   'form': form}
        return render(request, 'index_fr.html', context)

def ability(request, id: int):
    infoAbi = requests.get('https://pokeapi.co/api/v2/ability/' + str(id) + '/').json()
    abi = models.Ability(infoAbi['id'], infoAbi['name'])
    abi.effect = infoAbi['effect_entries'][1]['effect']
    context = {'ability': abi}
    return render(request, 'ability.html', context)

def type(request):
    infoType = requests.get('https://pokebuildapi.fr/api/v1/types').json()
    type = models.Type("null", "null")
    infoPoke = requests.get('https://pokebuildapi.fr/api/v1/pokemon/').json()
    listType = models.listType(1)
    for y in range(0, len(infoPoke)):
        for b in range(0, len(infoPoke[y]['apiTypes'])):
            if infoPoke[y]['apiTypes'][b]['name'] == "Plante":
                listType.addPlante(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Feu":
                listType.addFeu(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Eau":
                listType.addEau(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Sol":
                listType.addSol(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Vol":
                listType.addVol(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Dragon":
                listType.addDragon(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Psy":
                listType.addPsy(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Fée":
                listType.addFee(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Ténèbres":
                listType.addTenebre(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Acier":
                listType.addAcier(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Glace":
                listType.addGlace(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Roche":
                listType.addRoche(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Spectre":
                listType.addSpectre(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Combat":
                listType.addCombat(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Normal":
                listType.addNormal(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Électrik":
                listType.addElek(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Insecte":
                listType.addInsecte(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )
            if infoPoke[y]['apiTypes'][b]['name'] == "Poison":
                listType.addPoison(
                    models.Pokemon(infoPoke[y]['id'], infoPoke[y]['name'], infoPoke[y]['image'])
                )

    for x in range(0, len(infoType)):
        type.addType(
            models.Type(infoType[x]['name'], infoType[x]['image'])
        )

    context = {'type': type,
               'list': listType}
    return render(request, 'type.html', context)
def setList():
    finalList = []
    ListPokemon = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151').json()['results']

    for x in range(0, len(ListPokemon)):
        pokemonInfo = requests.get(ListPokemon[x]["url"]).json()
        finalList.append(
            models.Pokemon(pokemonInfo['id'], pokemonInfo['name'], pokemonInfo['sprites']['front_shiny']))
        for y in range(0, len(pokemonInfo['abilities'])):
            finalList[x].addAbility(
                models.Ability(getAbilityId(pokemonInfo['abilities'][y]['ability']['url']),
                               pokemonInfo['abilities'][y]['ability']['name'])
            )
    return finalList

def setList_fr():
    finalList_fr = []
    ListPokemon = requests.get('https://pokebuildapi.fr/api/v1/pokemon').json()

    for x in range(0, len(ListPokemon)):
        i = random.randint(1, 1000)
        randomPoke = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(ListPokemon[x]['id']) + '/').json()
        #pokemonInfo = requests.get(ListPokemon[x])
        finalList_fr.append(
            models.PokemonS(ListPokemon[x]['id'], ListPokemon[x]['name'], ListPokemon[x]['sprite'], i, randomPoke['sprites']['front_shiny']))
    return finalList_fr


def getAbilityId(url):
    return requests.get(url).json()['id']

def quiz(request):
    i = random.randint(1, 898)
    randomPoke = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(i) + '/').json()
    randomPokeFr = requests.get('https://pokebuildapi.fr/api/v1/pokemon/' + str(i) + '/').json()
    poke = models.Pokemon(randomPoke['id'], randomPokeFr['name'], randomPoke['sprites']['back_shiny'])
    context = {'poke': poke}

    return render(request, 'quiz.html', context)


def setTeam(request, id):
    pokemonTeam.append(id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
