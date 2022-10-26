from player_list import \
    longoria_era, \
    eyraud_era, \
    labrune_era, \
    diouf_dassier_era, \
    bouchet_era, \
    rld_era, \
    l2_era, \
    tapie_era
from player import Player
import csv

all_players = list(set(longoria_era + eyraud_era + labrune_era + diouf_dassier_era + bouchet_era + rld_era + l2_era + tapie_era))
players = [Player(player) for player in all_players]

with open("players.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    for player in players:
        data = [player.name, player.views, player.position, player.pob]
        writer.writerow(data)