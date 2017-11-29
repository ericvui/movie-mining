import pandas as pd
import re
from addPrefixToColumn import addPrefixToColumn


def encodeActors(df):
    actors = []
    indices = []
    prefix = "actor_"
    count = 0
    for index, row in df.iterrows():
        count += 1
        actorsInRow = ""
        firstactor = True
        for actor  in re.finditer("\'name\': \'\w+(-* *\w*)*\'", row['cast']):
            if not firstactor:
                actorsInRow += "|"
            if not (actor is None):
                actorsInRow += prefix + actor.group().replace("'name': ", "").replace("'", "")
            firstactor = False
        actors.append(actorsInRow)
        indices.append(index)

    actors_encoded = pd.Series(actors, index=indices).str.get_dummies()
    actors_encoded.to_csv("../../data/interim/actors_encoded.csv", encoding='utf-8')
    return actors_encoded

def encodeActorsToOne(df, filter, threshold):
    """
    reads the first actor out of the credits.csv and onehotencodes it
    joins the encoded actors with the movie id again
    :param df: Credits DF (../../data/raw/credits.csv/credits.csv)
    :return: encodedActors + id
    """
    actors = []
    indices = []
    prefix = "actor_"
    for index, row in df.iterrows():
        actor = re.search("\'name\': \'\w+(-* *\w*)*\'", row['cast'])
        if not (actor is None):
            actor = actor.group().replace("'name': ", "").replace("'", "")
            actor = prefix + actor
            actors.append(actor)
            indices.append(index)
        else:
            actors.append("")
            indices.append(index)
    actors = pd.Series(actors,index=indices)
    actors_encoded = pd.get_dummies(actors)

    # actors_encoded['id'] = pd.Series(df['id'])
    #if (filter):
     #   actors_encoded = epc.filterWithThreshold(actors_encoded, threshold)
    # actors_encoded = epc.addPrefixToColumn(new_values_encoded, "actors")
    return actors_encoded


def actorsForHistogram(df):
    actors = []
    indices = []
    prefix = "actor_"
    for index, row in df.iterrows():
        actor = re.search("\'name\': \'\w+(-* *\w*)*\'", row['cast'])
        if not (actor is None):
            actor = actor.group().replace("'name': ", "").replace("'", "")
            actor = prefix + actor
            actors.append(actor)
            indices.append(index)
        else:
            actors.append("")
    new_values_encoded = pd.DataFrame()
    new_values_encoded['actors'] = pd.Series(actors)
    #new_values_encoded = pd.DataFrame(actors, columns=['test'])
    #new_values_encoded.rename(columns={0: 'log(gdp)'}, inplace=True)

    return  new_values_encoded
