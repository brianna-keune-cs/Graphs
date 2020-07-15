import random
from util import Stack, Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def get_friends(self, user_id):
        return self.friendships[user_id]

    def set_last_id(self, user_id):
        self.last_id = user_id

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for i in range(0, num_users):
            self.add_user(f"User {i}")

        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}
        q = Queue()
        q.enqueue([user_id])

        while q.size() > 0:
            current_path = q.dequeue()
            current_user = current_path[-1]

            if current_user not in visited:
                visited[current_user] = current_path
                for friend in self.get_friends(current_user):
                    if friend not in visited:
                        path_copy = current_path + [friend]
                        q.enqueue(path_copy)
        return visited


'''
Questions
    To create 100 users with an average of 10 friends each, how many times would you need to call add_friendship()? Why?
    - It called add_friendship() 500 times.
    - Because 100 * 10 / 2 = 500, and that's the range we call the function within.

    If you create 1000 users with an average of 5 random friends each, what percentage of other users will be in a particular user's extended social network? What is the average degree of separation between a user and those in his/her extended network?
    - Percentage: 99.5% because 5/1000 = 0.005 which is 0.5%
        100% - 0.5% so there's a 99.5% chance that any other user would be in my extended network.
    - Average degree is 6, because of the 6 degree seperation theory.

    I was surprised by this answer. I had no idea until I looked more into the 6 degree of seperation. For someone who doesn't have a close group of friends but a lot of helpful acquaintances I totally think it could be possible for me to successfully get a personal message to the President from someone they know on a first name basis.
'''


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
