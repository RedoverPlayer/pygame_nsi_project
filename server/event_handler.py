import game

def checkGameSearch(game_search, users, games):
    showdown_player_count = 2
    if len(game_search["showdown"]) >= showdown_player_count:
        for c in game_search["showdown"][:showdown_player_count]:
            c.send('{"type": "search_finished"}$'.encode())
        games.append(game.ShowdownGame(game_search["showdown"][:showdown_player_count], users))
        del game_search["showdown"][:showdown_player_count]
    else:
        for c in game_search["showdown"]:
            c.send(('{"type": "search_update", "player_count": "' + str(len(game_search["showdown"])) + '"}$').encode())

def event_received(data, client, users, game_search, games):
    if data["type"] == "game_search":
        if data["gamemode"] == "showdown":
            if client not in game_search["showdown"]:
                game_search["showdown"].append(client)
            checkGameSearch(game_search, users, games)
    elif data["type"] == "stop_search":
        if data["gamemode"] == "showdown":
            game_search["showdown"].remove(client)
            checkGameSearch(game_search, users, games)