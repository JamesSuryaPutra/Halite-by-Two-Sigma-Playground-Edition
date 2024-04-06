# Import helper function
from kaggle_environments.envs.halite.helpers import *
from random import choice

# Return the player's direction to move from current position (fromPos) to another position (toPos)
def getDirTo(fromPos, toPos, size):
    fromX, fromY = divmod(fromPos[0], size), divmod(fromPos[1], size)
    toX, toY = divmod(toPos[0], size), divmod(toPos[1], size)
    if fromY < toY:
        return ShipAction.NORTH
    if fromY > toY:
        return ShipAction.SOUTH
    if fromX < toX:
        return ShipAction.EAST
    if fromX > toX:
        return ShipAction.WEST

# Assign the player's direction
directions = [ShipAction.NORTH, ShipAction.EAST, ShipAction.SOUTH, ShipAction.WEST]

# Will keep track of whether the drone is collecting halite or carrying cargo to the shipyard
ship_states = {}

# Returns the commands per drones and shipyards
def agent(obs, config):
    size = config.size
    board = Board(obs, config)
    me = board.current_player
    
    # If no drones present, use the first shipyard to spawn a drone
    if len(me.ships) == 0 and len(me.shipyards) > 0:
        me.shipyards[0].next_action = ShipyardAction.SPAWN
    
    # If no shipyards present, convert the first drone into shipyard
    if len(me.shipyards) == 0 and len(me.ships) > 0:
        me.ships[0].next_action = ShipAction.CONVERT
    
    # Convert the board into two-dimensional array
    def get_map(obs):
        game_map = []
        for x in range(config.size):
            game_map.append([])
            for y in range(config.size):
                game_map[x].append(obs.halite[config.size * y + x])
        return game_map
    
    for ship in me.ships:
        if ship.next_action == None:
            
            ### 1st part: Set the player's state
            if board.step > 390:
                ship_states[ship.id] = "DEPOSIT"
            if ship.halite < 200:
                ship_states[ship.id] = "COLLECT"
            if ship.halite > 5000:
                ship_states[ship.id] = "DEPOSIT"
            
            ### 2nd part: Use the player's state to determine actions
            if ship_states[ship.id] == "COLLECT":
                position = ship.position
                game_map = get_map(obs)
            
            try:
                possiblecells = [
                    ship.cell.north.halite + game_map[position[0]][position[1]+2],
                    ship.cell.east.halite + game_map[position[0]+2][position[1]],
                    ship.cell.south.halite + game_map[position[0]][position[1]-2],
                    ship.cell.west.halite + game_map[position[0]-2][position[1]]
                ]
            
            except IndexError:
                possiblecells = [
                    ship.cell.north.halite,
                    ship.cell.east.halite,
                    ship.cell.south.halite,
                    ship.cell.west.halite
                ]
            
            best = max(range(len(possiblecells)), key=possiblecells.__getitem__)
            ship.next_action = directions[best]
            
            if ship_states[ship.id] == "DEPOSIT":
                direction = getDirTo(ship.position, me.shipyards[0].position, size)
                if direction: ship.next_action = direction
    
    return me.next_actions
