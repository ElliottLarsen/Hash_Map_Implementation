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
        This method takes a key and value as parameters and adds the node to the hash map.  If the given key already exists in the hash map, its associated value is replaced with the new value.
        """
        # Hash the key and locate the bucket that matches the hashed key.
        hashed_val = self.hash_function(key)
        hashed_index = hashed_val % self.buckets.length()
        bucket = self.buckets.get_at_index(hashed_index)

        # If the bucket is empty, add the kay/value pair.
        if bucket.length() == 0:
            bucket.insert(key, value)
            self.size += 1

        # If the bucket is already occupied but it is not the same key, insert the node at the beginning of the linked list.
        elif bucket.length() != 0 and bucket.contains(key) is None:
            bucket.insert(key, value)
            self.size += 1

        # If the bucket is already occupied and the key is the same, replace the value.
        elif bucket.length() != 0 and bucket.contains(key) is not None:
            bucket.remove(key)
            bucket.insert(key, value)
            # No need to update self.size.
        
        else:
            return

    def remove(self, key: str) -> None:
        """
        This method takes a key as parameter and removes its associated value from the hash map.  If the key is not in the hash map, the method does nothing.
        """
        # If the hash map is empty, return.
        if self.size == 0:
            return

        # Hash the key and locate the bucket that matches the hashed key.
        hashed_val = self.hash_function(key)
        hashed_index = hashed_val % self.buckets.length()
        bucket = self.buckets.get_at_index(hashed_index)

        # If the bucket is occupied.
        if bucket.length != 0:
            # If the key is found in the bucket, remove the node.
            if bucket.contains(key) is not None:
                bucket.remove(key)
                self.size -= 1

        return

    def contains_key(self, key: str) -> bool:
        """
        This method takes a key as parameter and searches it in the hash map.  If the given key is in the hash map, it returns True.  Otherwise, it returns False.
        """
        # If the hash map is empty, return False.
        if self.size == 0:
            return False
        
        # Hash the key and locate the bucket that matches the hashed key.
        hashed_val = self.hash_function(key)
        hashed_index = hashed_val % self.buckets.length()
        bucket = self.buckets.get_at_index(hashed_index)

        # If the key is found in the bucket.
        if bucket.contains(key) is not None:
            return True
        
        else:
            return False

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