# Author: Elliott Larsen
# Date: 
# Description: 

from SLL_DA import *

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
    Another sample hash function.
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
        Init a new HashMap based on Dynamic Array with Singly Linked List for collision resolution.
        """
        # Fill each bucket with a LinkedList() class.
        self.buckets = DynamicArray()
        
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method and returns the contents of the hash map in a human-readable form.
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
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
        pass

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
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
        pass

    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        pass