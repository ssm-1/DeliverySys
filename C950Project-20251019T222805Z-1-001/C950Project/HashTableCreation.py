# This class implements a basic hash map (hash table) data structure
# The hash map allows efficient storage and retrieval of key-value pairs
# Note: Code adapted from WGU Code Repository


class HashMapCreation:
    def __init__(self, initial_cap=30):
        """
        Initializes the hash map with a given initial capacity.
        The hash map is implemented as a list of lists (buckets).
        """
        self.list = []  # List to hold the buckets
        for i in range(initial_cap):
            self.list.append([])  # Initialize each bucket as an empty list

    def insert(self, key, item):
        """
        Inserts a key-value pair into the hash map.
        If the key already exists, updates the existing entry with the new item.
        """
        bucket = hash(key) % len(self.list)  # Determine the appropriate bucket index
        list_in_bucket = self.list[bucket]    # Get the list (bucket) for the calculated index

        # Check if the key already exists in the bucket
        for i, kv in enumerate(list_in_bucket):
            if kv[0] == key:  # Key found in the bucket
                list_in_bucket[i] = (key, item)  # Update the value associated with the key
                return True  # Return True indicating successful update

        # Key does not exist, so add a new key-value pair to the bucket
        list_in_bucket.append((key, item))  # Append the pair to the bucket
        return True  # Return True indicating successful insertion

    def lookup(self, key):
        """
        Retrieves the item associated with a given key.
        Returns None if the key is not found.
        """
        bucket_index = hash(key) % len(self.list)  # Determine the appropriate bucket index
        list_in_bucket = self.list[bucket_index]    # Get the list (bucket) for the calculated index

        # Search for the key in the bucket
        for pair in list_in_bucket:
            if key == pair[0]:  # Key found
                return pair[1]  # Return the value associated with the key
        
        return None  # Return None if the key is not found
    
    def update(self, package):
        """
        Updates an existing package in the hash table.
        """
        bucket_index = hash(package.parcel_id) % len(self.list)
        list_in_bucket = self.list[bucket_index]
        for i, kv in enumerate(list_in_bucket):
            if kv[0] == package.parcel_id:
                list_in_bucket[i] = [package.parcel_id, package]
                return
        # If package not found, you might want to consider adding it (optional)
        list_in_bucket.append([package.parcel_id, package])

    def remove_item(self, key):
        """
        Removes the key-value pair associated with the given key from the hash map.
        If the key is not found, no action is taken.
        """
        slot = hash(key) % len(self.list)  # Determine the appropriate bucket index
        final_dest = self.list[slot]        # Get the list (bucket) for the calculated index

        # Search and remove the key-value pair from the bucket if found
        for kv in final_dest:
            if kv[0] == key:  # Key found in the bucket
                final_dest.remove(kv)  # Remove the key-value pair from the bucket
                return  # Exit after removal
