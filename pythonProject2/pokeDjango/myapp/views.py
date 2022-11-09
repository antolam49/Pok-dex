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
    for x in range(0, len(pokemonTeam)):
        listPoke = []
        infoPoke = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(pokemonTeam[x]) + '/').json()
        poke = models.Pokemon(infoPoke['id'], infoPoke['name'], infoPoke['sprites']['front_shiny'])
        for y in range(0, len(infoPoke['abilities'])):
            poke.addAbility(
                models.Ability(getAbilityId(infoPoke['abilities'][y]['ability']['url']),
                               infoPoke['abilities'][y]['ability']['name'])
            )
        listPoke.append(poke)
        context = {
            'listPoke': listPoke
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
    poke_fr = models.Pokemon_fr(infoPoke['id'], infoPoke['name'], infoPoke['sprite'], infoPoke['stats']['HP'],
                                infoPoke['stats']['attack'], infoPoke['stats']['defense'], infoPoke['stats']['special_attack'],
                                infoPoke['stats']['special_defense'], infoPoke['stats']['speed'], preId, nextId, infoShiny['sprites']['front_shiny'], infoShiny['sprites']['back_shiny'], infoShiny['sprites']['back_default'])

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



def setListPokemon (request, b: bool):
    if(b == 1):
        setList_fr()
    else:
        setList()





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
        else:
            listPoke = allPokemon

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
            return pokemon(request, poke_fr.id)

    else:
        global allPokemon
        if not allPokemon:
            listPoke_fr = setList_fr()
            allPokemon = listPoke_fr
        else:
            listPoke_fr = allPokemon

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
    typ = models.Type(infoType['name'], infoType['image'])

    context = {'type': typ}
    return render(request, 'type.html', context)
def setList():
    finalList = []
    ListPokemon = requests.get('https://pokeapi.co/api/v2/pokemon?limit=898').json()['results']

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
