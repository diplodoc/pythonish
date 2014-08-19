import random
import inspect


class User:
    def __init__(self, name='', id=0):
        self.name = name
        self.id = id


class Users:
    def __init__(self):
        self.data = []

    def addUser(self, name):
        self.data.append(User(name, len(self.data)))

    def getUsers(self):
        for user in self.data:
            print user.name


class Item:
    def __init__(self, url='', title='', tags=[], id=0):
        self.id = id
        self.url = url
        self.title = title
        self.tags = tags


class Items:
    def __init__(self):
        self.data = []

    def addItem(self, title=''):
        self.data.append(Item(title=title, id=len(self.data)))

    def getItems(self):
        for item in self.data:
            print item.title


class UserActions:
    def __init__(self):
        self.data = {}

    def make_action(self, user, item, key, val):
        if user.id not in self.data:
            self.data[user.id] = {}
        if item.id not in self.data:
            self.data[user.id][item.id] = {}
        self.data[user.id][item.id][key] = val

    def like(self, user, item):
        self.make_action(user, item, 'like', 1)

    def dislike(self, user, item):
        self.make_action(user, item, 'like', -1)

    def read(self, user, item , percent):
        self.make_action(user, item, 'read', percent)


class Responder:
    def __init__(self):
        self.actionToMethodMap = {}
        self.actionToAgsMap = {}

    def register(self, action, method, **kwargs):
        if action in self.actionToMethodMap:
            self.actionToMethodMap[action].append((method, kwargs))
        else :
            self.actionToMethodMap[action] = [(method, kwargs)]

    def run(self):
        while(True):
            command_string = raw_input()
            if command_string == 'exit':
                break
            command_list = command_string.split(' ')
            if command_list[0] not in self.actionToMethodMap:
                print 'Unknown action'
                continue

            args1 = {}
            for elem in command_list[1:]:
                (arg, val) = elem.split('=')
                args1[arg] = val

            for (method, args2) in self.actionToMethodMap[command_list[0]]:
                combined_args = dict(args1.items() + args2.items())
                acceptable_params = inspect.getargspec(method)[0][1:]
                acceptable_args = []
                for param in acceptable_params:
                    if param not in combined_args:
                        print 'Wrong number of parameters'
                        continue
                    acceptable_args.append(combined_args[param])
                method(*acceptable_args)


class RecommendationAlgorithm:
    def __init__(self):
        self.index = []

    def buildIndex(self, users, items, user_actions):
        self.index = items.data

    def recommend(self, user_id):
        i = random.randint(0, len(self.index)-1)
        return [self.index[i].title]


class Combiner:
    def __init__(self):
        self.algos = []

    def addAlgo(self, algo):
        self.algos.append(algo)

    def recommend(self, user_id):
        result = []
        for algo in self.algos:
            result += algo.recommend(user_id)
        print result

    def buildIndex(self, users, items, user_actions):
        for algo in self.algos:
            algo.buildIndex(users, items, user_actions)

# create storage
users = Users()
items = Items()
user_actions = UserActions()

# create computation objects
algo = RecommendationAlgorithm()
combiner = Combiner()
combiner.addAlgo(algo)

# set up responder
responder = Responder()
responder.register('add_user', users.addUser)
responder.register('add_item', items.addItem)
responder.register('add_item', combiner.buildIndex, users=users, items=items, user_actions=user_actions)
responder.register('get_users', users.getUsers)
responder.register('get_items', items.getItems)
responder.register('recommend', combiner.recommend)

# roll it
responder.run()