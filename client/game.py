import udp_socket

def update(camera, map, player, rplayers, pressed_keys, screen, cinematic, tick_time, udp_sock, server_ip, id, auth_token):
    tiles_rendered, foreground_tiles = map.update(camera.coords, screen, player)

    for rplayer in rplayers:
        rplayer.update(screen, camera.coords)

    player.update(pressed_keys, tiles_rendered, map.map_size, map.tile_size, tick_time, screen, camera)

    for tile in foreground_tiles:
        tile.update(screen, camera.coords)
    
    for rplayer in rplayers:
        rplayer.renderInfoBar(screen, camera.coords)

    player.renderInfoBar(screen, camera.coords)

    # ensure camera does not go to the border
    if not cinematic:
        camera.update(player.coords, map.map_size, map.tile_size)

    # add the player to the screens
    udp_socket.sendCoords(udp_sock, (server_ip, 12861), player.coords, id, auth_token)

    return tiles_rendered