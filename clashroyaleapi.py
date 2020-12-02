
import requests
import json
import urllib.request
import matplotlib.pyplot as plt
import tweepy

#game info
challenge_towers = [4008,[2534,2534]]
challenge_towers_hp = [4008,5068]


#Clash Royale/Twitter API URL
base_URL = "https://api.clashroyale.com/v1/"

#Twitter API keys
consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 

#authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

West =

Apartment =

#headers
headers = {
    "Accept":"application/json",
    "authorization":"Bearer
    code"
}

#country codes
def country_codes(base_URL, headers):
    response = requests.get(base_URL+"locations/", headers = headers)
    codes = response.json()
    return codes



#request top x players/tags in Aruba and URL encodes the tags
def r_top_players(base_URL, headers, limit, cc):
    response = requests.get(base_URL+"locations/" + cc + "/rankings/players/", headers=headers, params = {"limit":limit})
    top_players = response.json()["items"]
    player_tags = []
    for t in top_players:
        player_tags.append(urllib.parse.quote(t["tag"]))
    return top_players, player_tags


#request players favorite card
def fav_card(player_tags, base_URL, headers):
    fav_cards = []
    for tag in player_tags:
        response = requests.get(base_URL+"players/" + tag + "/", headers = headers)
        player_info =  response.json()
        fav_cards.append(player_info["currentFavouriteCard"]["name"])
    return fav_cards


#returns top_players decks
def r_decks(player_tags, base_URL, headers):
    decks = []
    for tag in player_tags:
        response = requests.get(base_URL+"players/" + tag + "/", headers = headers)
        player_info =  response.json()
        cur_deck = player_info["currentDeck"]
        deck = []
        for cn in cur_deck:
            deck.append(str(cn["name"]))
        decks.append(deck)
    return decks

#build dict of all the cards
def cards_dict(base_URL, headers):
    response = requests.get(base_URL+"cards/", headers = headers)
    card_info = response.json()["items"]
    cards = {}
    for c in card_info:
        cards[c["name"]] = 0
    return cards



#build list of all the cards
def cards_list(base_URL,headers):
    cards = []
    response = requests.get(base_URL+"cards/", headers = headers)
    card_info = response.json()["items"]
    for c in card_info:
        cards.append(c["name"])
    return cards

#dict of cards with list values
def other_cards_dict(base_URL, headers):
    response = requests.get(base_URL+"cards/", headers = headers)
    card_info = response.json()["items"]
    cards = {}
    for c in card_info:
        cards[c["name"]] = [0,0]
    return cards

#fill in cards for top player decks
def f_decks(decks, cards, d_card, dd_card):
    for d in decks:
        for card in d:
            for c in cards:
                if card == c and card != d_card and card != dd_card:
                    cards[c] += 1
    return cards

#fill dict with current cards
def cards_used(cur_cards, yes):
    total_cards = sum(cur_cards.values())
    zeros = []
    for c in cur_cards:
        if cur_cards[c] == 0:
            zeros.append(c)
    for z in zeros:
        if z in cur_cards:
            del cur_cards[z]
    #percentage
    if yes == True:
        for c in cur_cards:
            cur_cards[c] = (cur_cards[c]/total_cards)*100
    return cur_cards

#builds library of players battlelogs
def user_battlelogs(player_tags, base_URL, headers):
    battle_logs = []
    for tag in player_tags:
        response = requests.get(base_URL+"players/" + tag + "/battlelog/", headers=headers)
        battle_log = response.json()
        battle_logs.append(battle_log)
    return battle_logs

#battlelogs for battle of specific type
def battle_of_spec_type(battle_logs, type):
    spec_type_battle_logs = []
    for log in battle_logs:
        length = len(log)
        for i in range(length - 1):
            if log[i]["type"] == type:
                spec_type_battle_logs.append(log[i])
    return spec_type_battle_logs

#Decks with specific card
def spec_deck(d_card, decks):
    deckswithcard = []
    for deck in decks:
        if d_card in deck:
            deckswithcard.append(deck)
    return deckswithcard


#pull decks from battlelogs
def battle_log_decks(spec_type_b_logs):
    decks = []
    for logs in spec_type_b_logs:
        deck = []
        for card in logs["team"][0]["cards"]:
            deck.append(card["name"])
        decks.append(deck)
    return decks

#battlelogs wins or losses
def winloss(spec_type_b_logs):
    winlosses = []
    for logs in spec_type_b_logs:
        if logs["team"][0]["crowns"] > logs["opponent"][0]["crowns"]:
            winlosses.append(True)
        else:
            winlosses.append(False)
    return winlosses

#list of decks containing two cards
def decks_with_both(decks, combo, winloss, dict_combo):
    #all combos in combo
    for c in combo:
        #specific cards inside the combo
        card_one = c[0]
        card_two = c[1]
        #all decks saved from battlelogs
        for deck in decks:
            #checks if cards are in the specific deck
            if card_one in deck and card_two in deck:
                dict_combo[card_one+card_two].append(winloss[decks.index(deck)])
    zeros = []
    for d in dict_combo:
        if len(dict_combo[d]) < 100:
            zeros.append(d)
    for z in zeros:
        del(dict_combo[z])
    for d in dict_combo:
        dict_combo[d] = sum(dict_combo[d])/len(dict_combo[d])*100
    return dict_combo

#dictionary of two card combos
def dict_combos(combos):
    dict_combo = {}
    for c in combos:
        dict_combo[c[0]+c[1]] = []
    return dict_combo


#combos of two cards in game
def combos(cards):
    big_list = []
    for c in cards:
        for a in cards:
            lists = []
            if c != a:
                lists.append(c)
                lists.append(a)
            big_list.append(lists)
        cards.remove(c)
    big_list = [x for x in big_list if x != []]
    return big_list



#returns the players deck, time of the game, and the damage done to the towers
def hitpoints(spec_type_b_logs,tower_hp):
    game_stats = []
    stats = []
    decks = []
    print(len(spec_type_b_logs))
    for logs in spec_type_b_logs:
        cards_used = []
        if "princessTowersHitPoints" in logs["opponent"][0].keys():
            king_tower_hp = tower_hp[0] - logs["opponent"][0]["kingTowerHitPoints"]
            princess_tower_hp = tower_hp[1] - sum(logs["opponent"][0]["princessTowersHitPoints"])
            battle_time = logs["battleTime"]
            for card in logs["team"][0]["cards"]:
                cards_used.append(card["name"])
            decks.append(cards_used)
            stats = [king_tower_hp, princess_tower_hp, battle_time,cards_used]
            game_stats.append(stats)
            cards_used = []
        else:
            if "kingTowerHitPoints" in logs["opponent"][0].keys():
                king_tower_hp = tower_hp[0] - logs["opponent"][0]["kingTowerHitPoints"]
                princess_tower_hp = tower_hp[1]
                battle_time = logs["battleTime"]
                for card in logs["team"][0]["cards"]:
                    cards_used.append(card["name"])
                decks.append(cards_used)
                stats = [king_tower_hp, princess_tower_hp, battle_time,cards_used]
                game_stats.append(stats)
            else:
                king_tower_hp = tower_hp[0]
                princess_tower_hp = tower_hp[1]
                battle_time = logs["battleTime"]
                for card in logs["team"][0]["cards"]:
                    cards_used.append(card["name"])
                decks.append(cards_used)
                stats = [king_tower_hp, princess_tower_hp, battle_time,cards_used]
                game_stats.append(stats)
        if "princessTowersHitPoints" in logs["team"][0].keys():
            king_tower_hp = tower_hp[0] - logs["team"][0]["kingTowerHitPoints"]
            princess_tower_hp = tower_hp[1] - sum(logs["team"][0]["princessTowersHitPoints"])
            battle_time = logs["battleTime"]
            for card in logs["opponent"][0]["cards"]:
                cards_used.append(card["name"])
            decks.append(cards_used)
            stats = [king_tower_hp, princess_tower_hp, battle_time,cards_used]
            game_stats.append(stats)
        else:
            if "kingTowerHitPoints" in logs["team"][0].keys():
                king_tower_hp = tower_hp[0] - logs["team"][0]["kingTowerHitPoints"]
                princess_tower_hp = tower_hp[1]
                battle_time = logs["battleTime"]
                for card in logs["opponent"][0]["cards"]:
                    cards_used.append(card["name"])
                decks.append(cards_used)
                stats = [king_tower_hp, princess_tower_hp, battle_time,cards_used]
                game_stats.append(stats)
            else:
                king_tower_hp = tower_hp[0]
                princess_tower_hp = tower_hp[1]
                battle_time = logs["battleTime"]
                for card in logs["opponent"][0]["cards"]:
                    cards_used.append(card["name"])
                decks.append(cards_used)
                stats = [king_tower_hp, princess_tower_hp, battle_time,cards_used]
                game_stats.append(stats)
    print(len(game_stats))
    return game_stats

#takes the a players game statistics and a dictionary of cards in the game and fills the dict with the number of time a card is played and tower damage in that game
def dict_game_stats(player_games, card_dict):
    zeros = []
    for games in player_games:
        for c in games[3]:
          if c in card_dict.keys():
              card_dict[c][0] += 1
              card_dict[c][1] += (games[0] + games[1])
    for c in card_dict:
        if card_dict[c][0] == 0:
            zeros.append(c)
    #
    for z in zeros:
        if z in card_dict:
            del card_dict[z]
    #
    return card_dict

######################

#print(country_codes(base_URL, headers))
#player_data = r_top_players(base_URL, headers, 10, "57000018")
#decks of top players
#decks = r_decks(player_data[1], base_URL, headers)
#decks with specific cards in them
#spec_decks = spec_deck("Valkyrie", decks))
#empty dictionary of cards
#cards = cards_dict(base_URL, headers)
#fill cards for top players decks
#cur_cards = f_decks(decks,cards)
#builds card data library
#u_cards = cards_used(cur_cards, False)
#print(top_cards(player_data[1], base_URL, headers))
##########################

#create graph of data
#plt.bar(range(len(u_cards)), list(u_cards.values()), align='center')
#plt.xticks(range(len(u_cards)), list(u_cards.keys()), fontsize = 6, rotation='vertical')
#plt.savefig("plot.png")
#plt.show()

###########################

#update the status on twitter
#tweet = "graph of cards used decks from top 100 players in Aruba."
#status = api.update_with_media("plot.png", tweet)
#api.update_status(status = tweet)
