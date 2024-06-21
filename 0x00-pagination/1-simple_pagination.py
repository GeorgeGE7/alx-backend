#!/usr/bin/env python3
"""
A module to add the `get_page` method to the `Server` class.
"""
import csv
from typing import List, Tuple


class Server:
    """
    A class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """
        Initialize a new instance of the `Server` class.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Get the cached dataset.

        Returns:
            List[List]: The cached dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    @staticmethod
    def index_range(page: int, page_size: int) -> Tuple[int, int]:
        """
        Calculate the start and end index range for a given page and page size.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            Tuple[int, int]: The start and end index range.
        """
        start_index_next_page = page * page_size
        return start_index_next_page - page_size, start_index_next_page

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get the items for a given page number and page size.

        Args:
            page (int): The page number. Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            List[List]: The items for the given page number and page size.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        startIndex, endIndex = self.index_range(page, page_size)
        return self.dataset()[startIndex:endIndex]
