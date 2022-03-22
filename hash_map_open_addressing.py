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

    def quad_prob(self, initial, iteration):
        """
        This is a helper method for quadratic probing.  It takes an initial value and nth iteration as parameters and calculates/returns the rehashed index.
        """
        return (initial + (iteration * iteration)) % self.capacity

    def calculate_size(self):
        """
        This method calculates/updates the current size of the hash map.
        """
        counter = 0
        # Travers the hash map and count the number of elements.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            if bucket is None:
                continue
            # If the bucket is not empty and is not a tombstone.
            elif bucket.is_tombstone == False:
                counter += 1
            
            else:
                continue

        self.size = counter

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def get(self, key: str) -> object:
        """
        This method takes a key as parameter and returns its associated value.  If the key is not in the hash table, the method returns None.  Quadratic probing is used.
        """
        # Establish the hashed key and initial index.
        hashed_key = self.hash_function(key)
        initial_index = hashed_key % self.capacity
        bucket = self.buckets.get_at_index(initial_index)

        iteration = 1
        rehash_index = self.quad_prob(initial_index, 0)

        # Loop until either the value is found or we find an empty bucket.
        while bucket is not None:
            # If the matching key is found and it is not a tombstone, return its value.
            if bucket.key == key and bucket.is_tombstone is not True:
                return bucket.value 
            # Otherwise, keep on searching using quadratic probing.
            else:
                rehash_index = self.quad_prob(initial_index, iteration)
                bucket = self.buckets.get_at_index(rehash_index)
                iteration += 1
        
        # The key is not in the hash map.
        return None

    def put(self, key: str, value: object) -> None:
        """
        This method takes a key and value as parameters and updates the hash map.  If the given key already exists in the hash map, its associated value is replaced with the new value.  The table is resized to double its current capacity when the current load factor is greater than or equal to 0.5.  Quadratic probing is used.
        """
        self.calculate_size()

        # Check if resize_table() needs to be called.
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        # Establish hashed key as well as initial index.
        hashed_key = self.hash_function(key)
        initial_index = hashed_key % self.capacity
        bucket = self.buckets.get_at_index(initial_index)

        # If the bucket is not occupied.
        if bucket is None:
            self.buckets.set_at_index(initial_index, HashEntry(key, value))
            self.size += 1
        # If the bucket is already occupied.
        else:
            # If the key already exists in the hash map, replace its value.
            if bucket.key == key:
                self.buckets.set_at_index(initial_index, None)
                self.buckets.set_at_index(initial_index, HashEntry(key, value))            
            # Start quadratic probing.
            else:
                iteration = 1
                rehash_index = self.quad_prob(initial_index, 0)
                # Continue probing until an empty bucket is found.
                while bucket is not None:
                    if bucket.key == key:
                        break
                    # quad_prob() is a helper method for quadratic probing.
                    rehash_index = self.quad_prob(initial_index, iteration)
                    bucket = self.buckets.get_at_index(rehash_index)
                    iteration += 1

                self.buckets.set_at_index(rehash_index, HashEntry(key, value))
                self.size += 1
        
        self.calculate_size()

    def remove(self, key: str) -> None:
        """
        This method takes a key as parameter and removes its associated value from the hash map by setting it to a tombstone. Quadratic probing is used.
        """
        # Establish hashed_key and initial index.
        hashed_key = self.hash_function(key)
        initial_index = hashed_key % self.capacity
        bucket = self.buckets.get_at_index(initial_index)

        iteration = 1
        rehash_index = self.quad_prob(initial_index, 0)

        # Start quadratic probing.
        while bucket is not None:
            # If the key is found.
            if bucket.key == key:
                bucket.is_tombstone = True
                break 
            else:
                # Continue with quadratic probing.
                rehash_index = self.quad_prob(initial_index, iteration)
                bucket = self.buckets.get_at_index(rehash_index)
                iteration += 1

        self.calculate_size()

        return

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
        Thie method takes a new capacity as parameter and changes the capacity of the internal hash map.  All existing key/value pairs are rehashed.
        """
        self.calculate_size()

        if new_capacity < 1 or new_capacity < self.size:
            return
        
        # Create a temporary list (linked list) to store values.
        temp_list = LinkedList()

        # Traverse the hash map backwards so that when temp_list is rehashed later, it is in the correct order (because insert() method puts the node at the beginning of the linked list).
        for i in range(self.capacity - 1, -1, -1):
            bucket = self.buckets.get_at_index(i)
            if bucket is None:
                continue
            # If the bucket has the value and it is not a tombstone.
            elif bucket is not None and bucket.is_tombstone is not True:
                temp_list.insert(bucket.key, bucket.value)
            # If the bucket has a value but it is a tombstone.
            else:
                continue

        # Reset/clear out the hash map.
        self.buckets = DynamicArray()
        for i in range(new_capacity):
            self.buckets.append(None)
        self.size = 0
        self.capacity = new_capacity

        # Repopulate the hash map.  Rehashing is done by put().
        for node in temp_list:
            self.put(node.key, node.value)

        self.calculate_size()

    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        pass
