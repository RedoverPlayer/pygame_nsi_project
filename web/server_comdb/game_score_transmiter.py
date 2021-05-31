import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="jeupygame"
)

def communicate_game(ids :list, kills: list, deaths:list, game_mode:str, time):
    """send the score to the db, take list, player must be listed from the winner to the loser (1st to 10th)"""
    cursor = mydb.cursor()
    data_set = {
        "players_ids": ids,
        "kills": kills,
        "deaths": deaths,
        "game_mod":game_mode,
        "duration":time
        }
    json_dump = json.dumps(data_set)
    print(json_dump)
    json_object = json.loads(json_dump)
    print(json_object)
    cursor.execute(("INSERT INTO game_info (json_files) VALUES( %s)"), (json_dump,))
    upade_player_info(json_object,time)
    mydb.commit()
    cursor.close()

def upade_player_info(json,time):
    cursor = mydb.cursor()
    json_obj = json
    for i in range (len(json_obj["kills"])):
        print("id:", json_obj["players_ids"][i])
        print("kills:", json_obj["kills"][i])
        print('---')
        cursor.execute(("UPDATE accounts SET KILLS = KILLS + %s, DEATHS = DEATHS + %s, TIME_WASTED = TIME_WASTED + %s WHERE ID = %s"), (json_obj["kills"][i], json_obj["deaths"][i], time, json_obj["players_ids"][i]))
    #close the connection to the database.
    mydb.commit()
    cursor.close()

communicate_game([1,2,3,4,5],[1,2,3,5,7],[5,2,4,6,1000],"vachekiri",150)
