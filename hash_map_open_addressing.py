# Author: Elliott Larsen
# Date: 3/23/2022
# Description: Hash Map implementation in Python.  Dynamic Array is used to store the hash table and quadratic probing is used to store values (open addressing).

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
        This method clears the contents of the hash map without changing its underlying capacity.
        """
        # Traverse the hash map and if the bucket has a value, set it to None and update the hash map's size.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            if bucket is None:
                continue
            else:
                self.buckets.set_at_index(i, None)
                self.size -= 1

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
        The method takes a key as parameter and returns True if the given key is in the hash map.  Otherwise, it returns False.  Quadratic probing is used.
        """
        # Empty hash map.
        if self.size == 0:
            return False

        # Establish hashed key and initial index.
        hashed_key = self.hash_function(key)
        initial_index = hashed_key % self.capacity
        bucket = self.buckets.get_at_index(initial_index)

        iteration = 1
        rehash_index = self.quad_prob(initial_index, 0)

        # Run the loop until either matching key value is found or an empty bucket is encountered.
        while bucket is not None:
            
            # If the bucket's key matches the input key and it is not a tombstone.
            if bucket.key == key and bucket.is_tombstone is not True:
                return True
            # Continue with quadratic probing.
            else:
                rehash_index = self.quad_prob(initial_index, iteration)
                bucket = self.buckets.get_at_index(rehash_index)
                iteration += 1

        # Went through the entire hash map and did not find the key.
        return False

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        # Go through the hash map and increment the counter whenever an empty bucket is found.
        counter = 0
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            if bucket is None:
                counter += 1
            else:
                continue
        
        return counter


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
        This method returns a Dynamic Array with all the keys from the hash map in it.
        """
        return_arr = DynamicArray()
        
        # Append values to return_arr.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            # If the bucket is empty.
            if bucket is None:
                continue
            # If the bucket is occupied and it is not a tombstone.
            elif bucket is not None and bucket.is_tombstone is False:
                return_arr.append(bucket.key)
            # The bucket is occupied but it is a tombstone.
            else:
                continue

        return return_arr

#--------
# Tests 
#--------

if __name__ == "__main__":

    # Empty_buckets example 1
    # -----------------------------
    # 100 0 100
    # 99 1 100
    # 98 2 100
    # 98 2 100
    # 97 3 100

    print("\nEmpty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    # Empty_buckets example 2
    # -----------------------------
    # 49 1 50
    # 69 31 100
    # 139 61 200
    # 109 91 200
    # 279 121 400

    print("\nEmpty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    # Table_load example 1
    # --------------------------
    # 0.0
    # 0.01
    # 0.02
    # 0.02

    print("\nTable_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    # Table_load example 2
    # --------------------------
    # 0.02 1 50
    # 0.22 11 50
    # 0.42 21 50
    # 0.31 31 100
    # 0.41 41 100

    print("\nTable_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    # Clear example 1
    # ---------------------
    # 0 100
    # 2 100
    # 0 100

    print("\nClear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    # Clear example 2
    # ---------------------
    # 0 50
    # 1 50
    # 2 50
    # 2 100
    # 0 100

    print("\nClear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    # Put example 1
    # -------------------
    # 25 0.5 25 50
    # 50 0.5 50 100
    # 125 0.375 75 200
    # 100 0.5 100 200
    # 275 0.3125 125 400
    # 250 0.375 150 400

    print("\nPut example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    # Put example 2
    # -------------------
    # 36 0.1 4 40
    # 33 0.175 7 40
    # 30 0.25 10 40
    # 26 0.35 14 40
    # 23 0.425 17 40

    print("\nPut example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    # Contains_key example 1
    # ----------------------------
    # False
    # True
    # False
    # True
    # True
    # False

    print("\nContains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    # Contains_key example 2
    # ----------------------------
    # 50 150
    # True

    print("\nContains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    # Get example 1
    # -------------------
    # None
    # 10

    print("\nGet example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    # Get example 2
    # -------------------
    # 15 150
    # 200 2000 True
    # 201 None False
    # 221 2210 True
    # 222 None False
    # 242 2420 True
    # 243 None False
    # 263 2630 True
    # 264 None False
    # 284 2840 True
    # 285 None False 

    print("\nGet example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # Remove example 1
    # ----------------------
    # None
    # 10
    # None

    print("\nRemove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    # Resize example 1
    # ----------------------
    # 1 20 10 True
    # 1 30 10 True

    print("\nResize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    # Resize example 2
    # ----------------------
    # 77 300
    # 111 True 77 222 0.35
    # 228 True 77 228 0.34
    # 345 True 77 345 0.22
    # 462 True 77 462 0.17
    # 579 True 77 579 0.13
    # 696 True 77 696 0.11
    # 813 True 77 813 0.09
    # 930 True 77 930 0.08

    print("\nResize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    # Get_keys example 1
    # ------------------------
    # ['160', '170', '180', '190', '100', '110', '120', '130', '140', '150']
    # ['160', '170', '180', '190', '100', '110', '120', '130', '140', '150']
    # ['200', '110', '120', '130', '140', '150', '160', '170', '180', '190']

    print("\nGet_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
