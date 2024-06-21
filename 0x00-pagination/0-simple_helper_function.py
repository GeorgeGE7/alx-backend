#!/usr/bin/env python3
"""
First function - For pagination 
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """index range to check index range

    Args:
        page (int): page number
        page_size (int): number of items in the page

    Returns:
        Tuple[int, int]: inputs
    """
    start_index_next_page: int = page * page_size
    return start_index_next_page - page_size, start_index_next_page
