import contextvars

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
from .forms import SearchForm

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

def setListPokemon (request, b: bool):
    if(b == true):
        setList_fr()
    else:
        setList()


def pokemon_fr(request, id: int):
    infoPoke = requests.get('https://pokebuildapi.fr/api/v1/pokemon/' + str(id) + '/').json()
    poke = models.Pokemon_fr(infoPoke['id'], infoPoke['name'], infoPoke['sprite'], infoPoke['apiTypes'])

    context = {'poke_fr': poke_fr}
    return render(request, 'pokemon.html', context)


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
            poke_fr = models.Pokemon_fr(infoPoke['id'], infoPoke['name'], infoPoke['image'])
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
        #pokemonInfo = requests.get(ListPokemon[x])
        finalList_fr.append(
            models.Pokemon_fr(ListPokemon[x]['id'], ListPokemon[x]['name'], ListPokemon[x]['sprite']))
    return finalList_fr


def getAbilityId(url):
    return requests.get(url).json()['id']


def setTeam(request, id):
    pokemonTeam.append(id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
