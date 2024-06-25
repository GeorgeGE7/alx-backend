#!/usr/bin/python3
"""
This module implements a basic cache using a dictionary.
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    Cache implementation using a dictionary.
    """
    def put(self, key, item):
        """
        Add an item to the cache.

        Args:
            key (Hashable): The key of the item.
            item: The item to be added.
        """
        if key is not None and item is not None:
            self.cache_data.update({key: item})

    def get(self, key):
        """
        Get an item from the cache.

        Args:
            key (Hashable): The key of the item.

        Returns:
            The value of the item in the cache, or None if the item is not in
            the cache.
        """
        return self.cache_data.get(key, None)
