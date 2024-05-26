#!/usr/bin/env python
# coding: utf-8

# THIS PYTHON SCRIPT DOESNT WORK ANYMORE, RIOT API CHANGED
# ESTE SCRIPT DE PYTHON NO FUNCIONA DEBIDO A CAMBIOS EN LA API DE RIOT

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cassiopeia as cp
from datetime import timedelta

# You have to request API KEY from Riot Developer Web
RIOT_API_KEY = "RGAPI-e8f63d09-d476-4864-bc92-bbb9c0298b3d"
CPConfig = cp.Settings({'global': {'version_from_match': 'latest', 'default_region': 'LAS'}})
cp.apply_settings(CPConfig)
cp.set_riot_api_key(RIOT_API_KEY)

# User and region to analyze
user = "G2 ANDREWTAT3"
region = "EUW"
summoner = cp.Summoner(name=user, region=region)


# ## Confección de las preguntas
# 
# (Tamaño de los datos en base a tus partidas)
# 
# - Campeones más jugados por el usuario y en general.
# - Campeones con el mayor y menor winrate, por el usuario y en general.
# - Campeones con promedio de KDA más alto y bajo, por el usuario y en general.
# - Posicion del usuario con mayor y menor winrate.
# 
# Otros datos menos relevantes
# - Porcentaje de campeones hombres/femeninos jugados.
# - Porcentaje de winrate por genero de campeon.
# - Winrate de amigos.
# 
# ## Questions
# 
# - Most played champions by user and general
# - Champions winrate by user and general
# - Champions KDA Mean by user and general
# - User role by best winrate
# 
# Another data
# - Percentage of female/male champions played
# - Winrate by gender of the champions
# - Friend's winrate

# Creacion de la lista df y diccionarios para entender mejor la información.
# Dataframe
df = []
# Diccionaries for listing Win Status, Spells and Female Champions
win = {False: "Loss", True: "Win"}
summonerid = {1: "Cleanse", 2: "Clarity", 3: "Exhaust", 4: "Flash", 5: "", 6: "Ghost", 7: "Heal", 14: "Ignite", 11: "Smite", 12: "Teleport", 21: "Barrier"}
females = {"Ahri", "Akali", "Anivia", "Annie", "Ashe", "Bel'Veth", "Caitlyn", "Camille", "Cassiopeia", "Diana", "Elise", "Evelynn", "Fiora", "Gwen", "Irelia",
           "Janna", "Jinx", "Kai'Sa", "Kalista", "Karma", "Katarina", "Kayle", "LeBlanc", "Leona", "Lillia", "Lissandra", "Lulu", "Lux", "Miss Fortune",
           "Morgana", "Nami", "Neeko", "Nidalee", "Nilah", "Orianna", "Poppy", "Qiyana", "Quinn", "Rell", "Renata Glasc", "Riven",
           "Samira", "Sejuani", "Senna", "Seraphine", "Shyvana", "Sivir", "Sona", "Soraka", "Syndra", "Taliyah", "Tristana", "Vayne", "Vex", "Vi",
           "Xayah", "Yuumi", "Zeri", "Zoe", "Zyra"}
# Friends diccionaries, you have to list your friends or data will be affected by them, ex: {"friend1", "friend2"}
friends = {}

# Codigo para realizar querys a la API de Riot acerca de X variables.
# Code to do querys to Riot's API about X variables listed after df.append()

for match in summoner.match_history[0:300]: # Analiza un X de partidas./ Analyze X matches
    players = match.participants
    if match.is_remake:
        pass
    elif match.duration < timedelta(minutes=15, seconds=30):
        pass
    else:
        try:
            for x in players:
                df.append((match.id, x.summoner.name, x.champion.name, "female" if x.champion.name in females else "male", x.lane.name, "friend" if x.summoner.name in friends else "user" if x.summoner.name in user else "other", x.stats.kills, x.stats.deaths, x.stats.assists, round(x.stats.kda,2),  x.runes.keystone.name, summonerid[x.summoner_spell_d.id], summonerid[x.summoner_spell_f.id], win[x.stats.win], match.queue.name))
        except KeyError:
            pass
print("Calls Done, creating Dataframe")
# Creacion del DataFrame y guardado en "leagueoflegendsdata.csv"
# Dataframe creation and saved on "leagueoflegendsdata.csv"
df = pd.DataFrame(df, columns=["Match ID", "Name", "Champion", "Champion Sex", "Role", "Type", "Deaths", "Kills", "Assists", "KDA", "Keystone", "Spell D", "Spell F", "Win", "Match Type"])
df = df.set_index("Match ID")
df.to_csv("leagueoflegendsdata.csv")

df = df[df["Match Type"] == "ranked_solo_fives"] # Modify this for filtering by Match Type

# General Played Count Graph
DATA = df[df["Type"] == "other"]["Champion"].value_counts().nlargest(10).sort_values(ascending=True)

fig, axs = plt.subplots(nrows=2, figsize=[10,6], dpi=250)
sns.lineplot(data=DATA, color="blue", ax=axs[0])

DATA = df[df["Type"] == "other"]["Champion"].value_counts().nsmallest(10).sort_values(ascending=False)

sns.lineplot(data=DATA, color="red", ax=axs[1])

axs[0].set(xlabel=None, ylabel=None)
axs[1].set(xlabel=None, ylabel=None)
fig.supylabel("Played Count", x=0.06)
fig.supxlabel("Champions")
fig.suptitle("General Champions Played Count", y=0.92)

fig.savefig("loldata/general_playedcount.png")


# User Played Count Graph
DATA = df[df["Type"] == "user"]["Champion"].value_counts().nlargest(10).sort_values(ascending=True)

fig, axs = plt.subplots(nrows=2, figsize=[10,6], dpi=250)
sns.lineplot(data=DATA, color="blue", ax=axs[0])

fch = df[(df["Type"] == "user")]["Champion"].value_counts()
fch2 = df[(df["Type"] == "user")]["Champion"].value_counts()
fch = fch[fch >= 4]
DATA = fch.nsmallest(10).sort_values(ascending=False)

sns.lineplot(data=DATA, color="red", ax=axs[1])

axs[0].set(xlabel=None, ylabel=None)
axs[1].set(xlabel=None, ylabel=None)
fig.supylabel("Played Count", x=0.06)
fig.supxlabel("Champions")
fig.suptitle("User Champions Played Count (Not counting champions played below 4 games)", y=0.92)

fig.savefig("loldata/user_playedcount.png")


# General Winrate Graph
fch = df[(df["Type"] == "other")]["Champion"].value_counts()
fch2 = df[(df["Type"] == "other")]["Champion"].value_counts()
fch = fch[fch >= 10]

xd = df[(df["Type"] == "other") & (df["Win"] == "Win")]["Champion"].value_counts() / fch

DATA = xd.nlargest(10).sort_values()

fig, axs = plt.subplots(nrows=2, figsize=[10,6], dpi=250)
sns.lineplot(data=DATA, color="blue", ax=axs[0])

DATA = xd.nsmallest(10).sort_values(ascending=False)

sns.lineplot(data=DATA, color="red", ax=axs[1])

axs[0].set(xlabel=None, ylabel=None)
axs[1].set(xlabel=None, ylabel=None)
fig.supylabel("Winrate", x=0.05)
fig.supxlabel("Champions")
fig.suptitle("General Winrate by Played Champion", y=0.92)

fig.savefig("loldata/general_winrate.png")


# Confección de tabla con el winrate, wins y partidas totales jugadas de cada campeon (excluyendo al usuario y amigos)
md = []
md = pd.DataFrame(xd, columns=["Champion","A", "B"])
md = md.rename(columns={"Champion": "Winrate", "A": "Win", "B": "Total"})
md["Win"] = df[(df["Type"] == "other") & (df["Win"] == "Win") & df["Champion"].isin(fch.index)]["Champion"].value_counts()
md["Total"] = df[(df["Type"] == "other") & df["Champion"].isin(fch.index)]["Champion"].value_counts()
md = md.sort_values(by="Winrate", ascending=False)
md = md.dropna()
md2 = md.head(10)
md2 = md2.append(md.tail(10))
md2 = md2.round(2)

ax = plt.subplot(frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

pd.plotting.table(data=md2, ax=ax, loc="center")
ax.set_title("General Winrate (Top and Lowest 10)")

plt.savefig('loldata/general_winratetable.png')


# User Winrate Graph
fch = df[(df["Type"] == "user")]["Champion"].value_counts()
fch2 = df[(df["Type"] == "user")]["Champion"].value_counts()
fch = fch[fch >= 10]

xd = df[(df["Type"] == "user") & (df["Win"] == "Win")]["Champion"].value_counts() / fch

DATA = xd.nlargest(10).sort_values()

fig, axs = plt.subplots(nrows=2, figsize=[10,6], dpi=250)
sns.lineplot(data=DATA, color="blue", ax=axs[0])

DATA = xd.nsmallest(10).sort_values(ascending=False)

sns.lineplot(data=DATA, color="red", ax=axs[1])

axs[0].set(xlabel=None, ylabel=None)
axs[1].set(xlabel=None, ylabel=None)
fig.supylabel("Winrate", x=0.05)
fig.supxlabel("Champions")
fig.suptitle("User Winrate by Played Champion", y=0.92)

fig.savefig("loldata/user_winrate.png")


# Confección de tabla con el winrate, wins y partidas totales jugadas de cada campeon (excluyendo al usuario y amigos)
md = []
md = pd.DataFrame(xd, columns=["Champion","A", "B"])
md = md.rename(columns={"Champion": "Winrate", "A": "Win", "B": "Total"})
md["Win"] = df[(df["Type"] == "user") & (df["Win"] == "Win") & df["Champion"].isin(fch.index)]["Champion"].value_counts()
md["Total"] = df[(df["Type"] == "user") & df["Champion"].isin(fch.index)]["Champion"].value_counts()
md = md.sort_values(by="Winrate", ascending=False)
md = md.dropna()
md2 = md.head(10)
md2 = md2.append(md.tail(10))
md2 = md2.round(2)

ax = plt.subplot(frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

pd.plotting.table(data=md2, ax=ax, loc="center")
ax.set_title("User Winrate (Top and Lowest 10)")

plt.savefig('loldata/user_winratetable.png')

# User role Winrate
# Filtrando rol y luego calculando winrate
fr = df[(df["Type"] == "user")]["Role"].value_counts()
fr = df[(df["Type"] == "user")]["Role"].value_counts()
fr = fr[fr >= 10]

lol = df[(df["Type"] == "user") & (df["Win"] == "Win")]["Role"].value_counts() / fr
lol = lol.sort_values()

fig = plt.figure(figsize=[10,3], dpi=250)
sns.lineplot(data=lol, color="green")
fig.suptitle("User Best Role", y=0.95)
fig.savefig("loldata/user_rolewinrate.png")


# General KDA Mean
fix1 = df.groupby("Champion")["KDA"].mean()
fix = fix1.nlargest(10).sort_values(ascending=True)

fig, axs = plt.subplots(nrows=2, figsize=[12,6], dpi=250)
sns.lineplot(data=fix, color="blue", ax=axs[0])

fix = fix1.nsmallest(10).sort_values(ascending=False)

sns.lineplot(data=fix, color="red", ax=axs[1])

axs[0].set(xlabel=None, ylabel=None)
axs[1].set(xlabel=None, ylabel=None)
fig.supylabel("KDA Mean", x=0.07)
fig.supxlabel("Champions")
fig.suptitle("General KDA Mean by Champion", y=0.92)
fig.savefig("loldata/general_kdamean.png")


# User KDA Mean
fix2 = df[df["Type"] == "user"]
fix1 = fix2.groupby("Champion")["KDA"].mean()
fix = fix1.nlargest(10).sort_values(ascending=True)

fig, axs = plt.subplots(nrows=2, figsize=[12,6], dpi=250)
sns.lineplot(data=fix, color="blue", ax=axs[0])

fix = fix1.nsmallest(10).sort_values(ascending=False)

sns.lineplot(data=fix, color="red", ax=axs[1])

axs[0].set(xlabel=None, ylabel=None)
axs[1].set(xlabel=None, ylabel=None)
fig.supylabel("KDA Mean", x=0.07)
fig.supxlabel("Champions")
fig.suptitle("User KDA Mean by Champion", y=0.92)
fig.savefig("loldata/user_kdamean.png")


# Gender Data
TOTAL = (df[df["Champion Sex"] == "male"]["Champion Sex"].value_counts().values) + (df[df["Champion Sex"] == "female"]["Champion Sex"].value_counts().values)
PIE = pd.DataFrame([df[df["Champion Sex"] == "female"]["Champion Sex"].value_counts().values,df[df["Champion Sex"] == "male"]["Champion Sex"].value_counts().values],index=["Female","Male"])
PIE = PIE / TOTAL
PIE = PIE.squeeze()
PIE = PIE.sort_index(ascending=True)

fig, axs = plt.subplots(ncols=2, figsize=[12,6], dpi=250)
axs[0].pie(x=PIE.values, labels=["Female","Male"], autopct=str, colors=["pink","lavender"])
axs[0].set_title("Played count by Gender")

DATA = df[df["Win"] == "Win"]["Champion Sex"].value_counts() / df["Champion Sex"].value_counts()
DATA = DATA.sort_index(ascending=True)

axs[1].pie(x=DATA.values, labels=["Female","Male"], autopct=str, colors=["pink","lavender"])
axs[1].set_title("Winrate by Gender")

fig.savefig("loldata/genderdata.png")


# Friends Winrate
DATA = df[(df["Type"] == "friend") & (df["Win"] == "Win")]["Name"].value_counts() / df[(df["Type"] == "friend")]["Name"].value_counts()
DATA = DATA.sort_values(ascending=True).round(2)

fig = plt.figure(figsize=[6,2], dpi=250)
ax = sns.lineplot(data=DATA, x=DATA.index, y=DATA.values)
ax.set_title("Friends Winrate when playing with User")

fig.savefig("loldata/friend_winrate.png")

print("Script Operation Done!")
