""" unique ID gen """
import string
import uuid


class UniqueIDGenerator:
    """ 
    A unique ID generator that guarantees the uniqueness of the ID across the instance with ability to specify the ID prefix 


    # Example usage
       ` id_generator = UniqueIDGenerator(prefix='USER', length=12)`

        `user_id = id_generator.generateID()`

        `print(f"Generated User ID: {user_id}")`
    """

    def __init__(self, prefix='', length=12, chars=string.ascii_letters + string.digits):
        self.prefix = prefix
        self.length = length
        self.chars = chars
        self.used_ids = set()

    def generateID(self):
        while True:
            # generate a random UUID
            unique_part = str(uuid.uuid4()).replace(
                '-', '')[:self.length - len(self.prefix)]

            # combine prefix and generated id
            unique_id = f"{self.prefix}{unique_part}"

            # check if the ID is unique
            if unique_id not in self.used_ids:
                self.used_ids.add(unique_id)
                return unique_id
