# Author: Elliott Larsen
# Date: 
# Description: 

from SLL_DA import *

class HashEntry:
    """
    Class implementing a Hash Entry.
    """

    def __init__(self, key: str, value: object):
        """
        Init an entry for use in a hash map.
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method and returns the content of the hash map in a human-readable form.
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"

def hash_function_1(key: str) -> int:
    """
    Sample Hash function.
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash

def hash_function_2(key: str) -> int:
    """
    Another sample Hash function.
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash

class HashMap:
    """
    Class implementing a Hash Map Table.  Supported methods are: clear(), get(), put(), remove(), contains_key(), empty_buckets(), table_load(), resize_table(), and get_keys().
    """

    def __init__(self, capacity: int, function) -> None:
        """
        Init a new HashMap that uses Quadratic Probing for collision resolution.
        """
        # Create an empty dynamic array.
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method returns the contents of the hash map in a human-readable form.
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        # quadratic probing
        pass

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        # If the load factor is greater than or equal to 0.5, this method will resize the table before putting the new key/value pair.
        # quadratic probing
        pass

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        # quadratic probing
        pass

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        # quadratic probing
        pass

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """
        pass

    def table_load(self) -> float:
        """
        This method calculates and returns the current hash table load factor.
        """
        table_load_factor = self.size / self.capacity

        return table_load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        # remember to rehash non-deleted entries into new table.
        pass

    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        pass
