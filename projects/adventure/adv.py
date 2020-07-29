from room import Room
from player import Player
from world import World

import random
import sys
from ast import literal_eval
from util import Stack
from graph import Graph

sys.setrecursionlimit(10**6)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []
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

    # adds history for movement, and it's inverse
    map_history.add_edge(prev_room, exit, current_room)
    map_history.add_edge(current_room, reverse_directions[exit], prev_room)
    track_unexplored_exits(current_room)


def track_unexplored_exits(current_room):
    '''
    adds a way to track which rooms have not been explored on what possible exits there are in a room.
    '''
    for exit in player.current_room.get_exits():
        if exit not in map_history.get_tracked_exits(current_room).keys():
            map_history.add_edge(current_room, exit, "?")


def traverse_map(direction):
    '''
    uses a recursive dft to get all rooms in map
    '''
    visited.append(player.current_room.id) # adds room to a list to be able to backtrack

    track_player_move(direction)
    current_room = player.current_room.get_room_id()

    if "?" not in map_history.get_tracked_exits(current_room).values():
        back_track()

    for exit, room in map_history.get_tracked_exits(current_room).items():
        if room is '?':
            traverse_map(exit)


def back_track():
    '''
    makes player back track their path to previously known room with at least 1 unexplored room
    '''
    if len(visited) > 0:
        prev_room = visited.pop()
        for direction, room in map_history.get_tracked_exits(player.current_room.id).items():
            if room is prev_room:
                move_player(direction)
                for exit, room in map_history.get_tracked_exits(player.current_room.id).items():
                    if room is '?':
                        traverse_map(exit)
                back_track()


def find_path():
    '''
    creates a path to all rooms on the world map
    '''
    current_room = player.current_room.get_room_id()
    visited.append(current_room)
    s = Stack()

    # initializes map_history for starting room
    if current_room not in map_history.get_visited_rooms():
        map_history.add_room(current_room)
        track_unexplored_exits(current_room)

    # picks initial direction to travel in
    for exit, room in map_history.get_tracked_exits(current_room).items():
        if room is '?':
            s.push(exit)
            traverse_map(exit)

    while s.size() > 0:
        if len(map_history.visited_rooms) == len(all_rooms):
            return
        direction = s.pop()
        traverse_map(direction)


find_path()


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
