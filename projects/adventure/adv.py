from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue
from graph import Graph

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
reverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
map_history = Graph()
all_rooms = world.rooms.keys()
visited = []


def move_player(direction):
    '''
    moves player to new room, and adds direction took to traversal path
    '''
    player.travel(direction)
    traversal_path.append(direction)


def track_player_move(exit):
    '''
    moves player, and records exit taken to which room
    in map_history for prev_room, and the next_room
    '''
    prev_room = player.current_room.get_room_id()
    move_player(exit)
    current_room = player.current_room.get_room_id()
    print(
        f'\nprev_room: {prev_room}\ndirection_took: {exit}\ncurrent_room: {current_room}')

    # adds history for movement, and it's inverse
    map_history.add_edge(prev_room, exit, current_room)
    print('new map entry: ', prev_room, map_history.visited_rooms[prev_room])
    map_history.add_edge(current_room, reverse_directions[exit], prev_room)
    track_unexplored_exits(current_room)
    print('inverse map entry: ', current_room,
          map_history.visited_rooms[current_room])


def track_unexplored_exits(current_room):
    for exit in player.current_room.get_exits():
        if exit not in map_history.get_tracked_exits(current_room).keys():
            map_history.add_edge(current_room, exit, "?")


def traverse_map(direction):
    prev_room = player.current_room.get_room_id()
    track_player_move(direction)
    current_room = player.current_room.get_room_id()
    visited.append(prev_room)

    if "?" not in map_history.get_tracked_exits(current_room).values():
        # move back to previous room
        print('\nbacktracking...\n')
        back_track()

    for exit, room in map_history.get_tracked_exits(current_room).items():
        if room is '?':
            traverse_map(exit)


def back_track():
    if len(visited) > 0:
        prev_room = visited.pop()
        print('popped: ', prev_room)
        for direction, room in map_history.get_tracked_exits(player.current_room.id).items():
            if room is prev_room:
                move_player(direction)
                for exit, room in map_history.get_tracked_exits(player.current_room.id).items():
                    if room is '?':
                        traverse_map(exit)


def find_path():
    current_room = player.current_room.get_room_id()
    visited.append(current_room)
    # q = Queue()

    # initializes map_history for starting room
    if current_room not in map_history.get_visited_rooms():
        map_history.add_room(current_room)
        track_unexplored_exits(current_room)

    for exit, room in map_history.get_tracked_exits(current_room).items():
        if room is '?':
            # q.enqueue(exit)
            print('exit: ', exit)
            traverse_map(exit)

    # while q.size() > 0:
    #     direction = q.dequeue()
    #     traverse_map(direction)


find_path()
print('VISITED: ', visited)
# print('path: ', traversal_path)
# print('path: ', visited)
print('explored rooms: ', map_history.visited_rooms)

'''
so we have access to the
    - room's id
    - room's exits
    - player can travel to one room at a time.
    - my graph can take in making a map history

input: starting room
output: a list of directions to travel to each room in the map

visited rooms are the graphs keys,
unexplored directions are held by '?'
'''


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
