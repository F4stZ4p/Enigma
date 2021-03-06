import urllib.parse

from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient(AsyncIOMotorClient):
    def __init__(self, config, logger, bot=None, *args, **kwargs):
        # Internal
        self.conn = None
        self.logger = logger

        # Config
        self.host = config["database"]["host"]
        self.port = config["database"]["port"]
        self.database = config["database"]["database"]
        self.username = urllib.parse.quote_plus(config["database"]["username"])
        self.password = urllib.parse.quote_plus(config["database"]["password"])
        self.replica_set = config["database"]["replica_set"]

        # URI Building
        if len(self.host) == 1:
            self.uri = f"mongodb://{self.username}:{self.password}" \
                       f"@{self.host[0]}:{self.port}"
            super(MongoClient, self).__init__(self.uri, *args, **kwargs)
        elif len(self.host) > 1:
            host_list = []
            for replica_host in self.host:
                host = f"mongodb://{self.username}:{self.password}"\
                                     f"@{replica_host}"
                host_list.append(host)

            super(MongoClient, self).__init__(
                host_list, replicaSet=f"{self.replica_set}", *args, **kwargs
            )

    async def upsert(self, entity, **states):
        """
        Updates an existing state's value. Creates a state
        if it does not exist. Also creates a database collection
        for each entity type when needed.

        :param entity: Any discord object with an id attribute
        :param states: A dict of state and possible values
        """
        if not (hasattr(entity, "id")):
            raise TypeError(f"'{entity}' is not an Entity!")

        collection = self[self.database][
            f'{entity.__class__.__name__}States']
        await collection.update(
            {f"{entity.__class__.__name__.lower()}_id": entity.id},
            {"$set": states},
            upsert=True
        )

    async def get(self, entity, state):
        """
        Grabs the value stored for an entity's state.

        :param entity: Any discord object with an id attribute
        :param state: An event passed as str
        :return: Returns the state's value if found or returns None
        """
        if not (hasattr(entity, "id")):
            raise TypeError(f"'{entity}' is not an Entity!")

        collection = self[self.database][
            f'{entity.__class__.__name__}States']
        record = await collection.find_one(
            {f"{entity.__class__.__name__.lower()}_id": entity.id})
        if record is None:
            return record
        else:
            try:
                state = record[state]
            except KeyError:
                return None
            return state

    async def increment(self, entity, state, value):
        """
        Increments an existing state's value.

        :param entity: Any discord object with an id attribute
        :param state: A state of type int
        :param value: The value to increment the state by
        """
        if not (hasattr(entity, "id")):
            raise TypeError(f"'{entity}' is not an Entity!")

        collection = self[self.database][
            f'{entity.__class__.__name__}States']
        await collection.update(
            {f"{entity.__class__.__name__.lower()}_id": entity.id},
            {"$inc": {state: value}},
        )
