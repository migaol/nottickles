from abc import ABC, abstractmethod
from helpers import constants
import math
import pandas as pd
from typing import Callable, Union, List

class AbstractPaginatedTable(ABC):
    """Abstract interface for a paginated table.
    """
    page: int = 0
    total_pages: int = 0

    @abstractmethod
    def page_footer(self) -> str:
        pass
    
    @abstractmethod
    def num_page_first_entry(self) -> int:
        pass

    @abstractmethod
    def num_page_last_entry(self) -> int:
        pass

    @abstractmethod
    def jump_page(self, offset: int) -> pd.DataFrame:
        pass

    def can_pprev(self) -> bool:
        """Check whether the pprev button can be pressed

        Args: None
        
        Returns:
            - bool: True if the pprev button callback would remain within the table bounds;
                False otherwise
        
        Raises: None
        """
        return False if self.page + constants.Format.SIZE_PPREV < 0 else True
    
    def can_prev(self) -> bool:
        """Check whether the prev button can be pressed

        Args: None
        
        Returns:
            - bool: True if the prev button callback would remain within the table bounds;
                False otherwise
        
        Raises: None
        """
        return False if self.page + constants.Format.SIZE_PREV < 0 else True

    def can_next(self) -> bool:
        """Check whether the next button can be pressed

        Args: None
        
        Returns:
            - bool: True if the next button callback would remain within the table bounds;
                False otherwise
        
        Raises: None
        """
        return False if self.page + constants.Format.SIZE_NEXT >= self.total_pages else True
    
    def can_nnext(self) -> bool:
        """Check whether the nnext button can be pressed

        Args: None
        
        Returns:
            - bool: True if the nnext button callback would remain within the table bounds;
                False otherwise
        Raises: None
        """
        return False if self.page + constants.Format.SIZE_NNEXT >= self.total_pages else True
    
    def get_page_no(self) -> int:
        """Get the current page number of the PaginatedTable

        Args: None
        
        Returns:
            - int: The current page number, where 1 represents the first page
        
        Raises: None
        """
        return self.page+1

class PaginatedDF(AbstractPaginatedTable):
    """Paginated table modeled on a pandas DataFrame.
    Displays data in entriesdirectly from the DataFrame.
    """
    page: int = 0
    per_row: int = 0
    total_entries: int = 0
    total_pages: int = 0
    meta: dict = None
    data: Union[dict, pd.DataFrame] = None
    title_function: Callable = None
    parse_function: Callable = None

    def __init__(self, meta: dict, data: Union[list, pd.DataFrame], title_function: Callable, parse_function: Callable):
        """Create a PaginatedDF.

        Args:
            - meta (dict): metadata, either user-created or from a URL
            - data: (list | pd.Dataframe): table contents, indexed by axes for a pd.DataFrame
                or by position for a list
            - title_function (Callable): callable object for generating the title of the current page;
                can pass in meta and data as arguments
            - parse_function (Callable): callable object for generating text to display the current page data;
                can pass in meta and data as arguments
        """
        self.page = 0
        self.per_row = constants.Format.DEFAULT_PAGE_SIZE
        self.meta = meta
        self.data = data
        self.total_entries = meta['count']
        self.total_pages = math.ceil(self.total_entries / self.per_row)
        self.title_function = title_function
        self.parse_function = parse_function

    def page_footer(self) -> str:
        """Create a page footer for the PaginatedDF.
        Displays the current and total page numbers and entries.

        Args: None
        
        Returns:
            - str: the text to display in an embed footer
        
        Raises: None
        """
        return (
            f"Showing page {self.page+1} of {self.total_pages} " +
            f"({self.num_page_first_entry()+1}-{self.num_page_last_entry()+1} of {self.total_entries} results)"
        )
    
    def num_page_first_entry(self) -> int:
        """Get the row index for the first entry in the current page.

        Args: None
        
        Returns:
            - int: row index of the first entry in the current page
        
        Raises: None
        """
        return self.page*self.per_row

    def num_page_last_entry(self) -> int:
        """Get the row index for the last entry in the current page.

        Args: None
        
        Returns:
            - int: row index of the last entry in the current page
        
        Raises: None
        """
        return min((self.page+1)*self.per_row, self.total_entries) - 1

    def jump_page(self, offset: int) -> pd.DataFrame:
        """Go forward or back the specified amount of pages.

        Args:
            - offset (int): the number of pages to jump forward or backward
        
        Returns:
            - pd.DataFrame: a pandas DataFrame containing data for the new current page
        
        Raises: None
        """
        self.page += offset
        return self.data.iloc[self.num_page_first_entry() : self.num_page_last_entry()+1]
    
class CustomPaginatedDF(AbstractPaginatedTable):
    """Paginated table with a custom model.
    Allows displaying data depending on the current page.
    """
    page: int = 0
    total_pages: int = 0
    meta: dict = None
    data: Union[list, pd.DataFrame] = None
    title_function: Callable = None
    parse_function: Callable = None
    subtitles: list = []

    def __init__(self, meta: dict, data: Union[list, pd.DataFrame], title_function: Callable, parse_function: Callable):
        """Create a CustomPaginatedDF.

        Args:
            - meta (dict): metadata, either user-created or from a URL
            - data: (list | pd.Dataframe): table contents, indexed by axes for a pd.DataFrame
                or by position for a list
            - title_function (Callable): callable object for generating the title of the current page;
                can pass in meta and data as arguments
            - parse_function (Callable): callable object for generating text to display the current page data;
                can pass in meta and data as arguments
        """
        self.page = 0
        self.meta = meta
        self.data = data
        self.total_pages = len(data)
        self.title_function = title_function
        self.parse_function = parse_function

    def page_footer(self) -> str:
        """Create a page footer for the PaginatedDF.
        Displays the current and total page numbers.

        Args: None
        
        Returns:
            - str: the text to display in an embed footer
        
        Raises: None
        """
        return (
            f"Showing page {self.page+1} of {self.total_pages}"
        )

    def jump_page(self, offset: int) -> pd.DataFrame:
        """Go forward or back the specified amount of pages.

        Args:
            - offset (int): the number of pages to jump forward or backward
        
        Returns:
            - pd.DataFrame: a pandas DataFrame containing data for the new current page
        
        Raises: None
        """
        self.page += offset
        return self.data[self.page]
        
    def num_page_first_entry(self) -> int:
        """Does nothing for a CustomPaginatedDF.
        """
        pass
        
    def num_page_last_entry(self) -> int:
        """Does nothing for a CustomPaginatedDF.
        """
        pass