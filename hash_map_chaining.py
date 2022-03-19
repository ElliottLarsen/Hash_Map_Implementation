# Author: Elliott Larsen
# Date: 3/18/2022
# Description: Hash Map implementation in Python.  Dynamic Array is used to store the hash table and singly linked list is used to resolve collision (chaining).

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
        This method clears the contents of the hash map without changing the underlying hash table capacity.
        """
        # Traverse the map and empty out buckets.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            # If the bucket is occupied.
            if bucket.length() != 0:
                # Assign a new/empty linked list to the bucket.
                self.buckets.set_at_index(i, LinkedList())
                # Decrease the size accordingly.
                self.size -= bucket.length()
            else:
                continue

    def get(self, key: str) -> object:
        """
        This method receives a key as parameter and returns the value associated with the key.  If the key is not in the hash map, it returns None.
        """
        # If the key is not in the hash map.
        if self.contains_key(key) is False:
            return None
        
        # Hash the key and locate the bucket that matches the hashed key.
        hashed_val = self.hash_function(key)
        hashed_index = hashed_val % self.buckets.length()
        bucket = self.buckets.get_at_index(hashed_index)
        
        # Find the node that matches the key.
        node = bucket.contains(key)

        return node.value


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
        This method returns the number of empty buckets in the hash table.
        """
        empty_bucket_num = 0
        
        # Traverse the map and count the number of empty buckets.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)

            if bucket.length() == 0:
                empty_bucket_num += 1
        
        return empty_bucket_num

    def table_load(self) -> float:
        """
        This method calculates and returns the current hash table load factor.
        """
        table_load_factor = self.size / self.capacity

        return table_load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        This method takes new capacity as parameter and changes the capacity of the internal hash table.  All elements of the hash map will be rehashed.
        """
        # If the new capacity is less than one, return.
        if new_capacity < 1:
            return
    
        # Create a linked list where key/value pairs will be stored temporarily.
        temp_arr = LinkedList()

        # Go through the hash map and copy all the key/value pairs to temp_arr.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            # If the bucket is empty.
            if bucket.length() == 0:
                continue
            # Go through the bucket and copy all the nodes to temp_arr.
            else:
                for node in bucket:
                    temp_arr.insert(node.key,node.value)
        
        # Reset self.size and self.capacity.
        self.size = 0
        self.capacity = new_capacity

        # Reset self.buckets to an empty array of linked lists.
        self.buckets = DynamicArray()        
        for i in range(new_capacity):
            self.buckets.append(LinkedList())

        # Go through the temp_arr (linked list) and rehash/place each node in self.buckets.
        for node in temp_arr:
            self.put(node.key,node.value)
        
    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map.  
        """
        return_arr = DynamicArray()

        # Traverse each bucket of the hash map.
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            if bucket.length() == 0:
                continue
            # If the bucket is not empty, go through each node of the linked list and add their keys to return_arr.
            else:
                for node in bucket:
                    return_arr.append(node.key)

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
    # 39 31 50
    # 36 61 50
    # 33 91 50
    # 30 121 50

    print("\nEmpty_buckets example 2")
    print("-----------------------------")
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
    # 0.62 31 50
    # 0.82 41 50

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
    # 39 0.5 25 50
    # 37 1.0 50 50
    # 35 1.5 75 50
    # 32 2.0 100 50
    # 30 2.5 125 50
    # 30 3.0 150 50

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
    # 27 0.35 14 40
    # 25 0.425 17 40

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
    # 50 75
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
    # 77 75
    # 111 True 77 111 0.69
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
    # ['160', '110', '170', '120', '180', '130', '190', '140', '150', '100']
    # ['160', '110', '170', '120', '180', '130', '190', '140', '150', '100']
    # ['200', '160', '110', '170', '120', '180', '130', '190', '140', '150']

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
