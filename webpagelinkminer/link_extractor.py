import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
from collections import deque
from queue import Queue
import asyncio
import aiohttp


class WebPageLinkExtractor:
    """
    A class for extracting all links from a given domain.

    Attributes:
        base_url (str): The base URL to start extracting links from.
        timeout (int): The timeout for requests, in seconds. Default is 10 seconds.
        max_depth (int): The maximum depth of links to extract. Default is 3.
        parser (str): The parser to use for BeautifulSoup. Default is 'lxml'.
        algorithm (str): The algorithm to use for link extraction. Default is 'dfs'.
    """

    def __init__(self, base_url, timeout=10, max_depth=3, parser='lxml', algorithm='dfs'):
        self.base_url = base_url
        self.timeout = timeout
        self.max_depth = max_depth
        self.parser = parser
        self.algorithm = algorithm
        self.visited_urls = set()
        self.current_max_depth = 0
        parsed_url = urlparse(base_url)
        self.domain_name = parsed_url.netloc
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def _fetch_page(self, url):
        """
        Fetches the page at the given URL and returns its content, or None if an error occurs.
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Error fetching page: {url} - {e}')
            return None

    async def _fetch_page_async(self, url):
        """
        Asynchronously fetches the page at the given URL and returns its content, or None if an error occurs.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.timeout) as response:
                    response.raise_for_status()
                    return await response.text()
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError) as e:
            print(f'Error fetching page: {url} - {e}')
            return None

    def _extract_links_dfs(self, url, depth=0, links=None):
        """
        Extracts all the links from the page at the given URL using depth-first search.
        """
        if depth > self.max_depth or url in self.visited_urls:
            return

        self.visited_urls.add(url)
        print(f'Fetching links from {url} at depth {depth}')
        self.current_max_depth = max(self.current_max_depth, depth)

        page_content = self._fetch_page(url)
        if not page_content:
            return

        soup = BeautifulSoup(page_content, self.parser)
        page_links = [a['href'] for a in soup.find_all('a', href=True)]

        for link in page_links:
            full_url = urljoin(url, link)
            parsed_full_url = urlparse(full_url)
            # Ignore URL fragments
            full_url = parsed_full_url._replace(fragment='').geturl()
            if parsed_full_url.netloc == self.domain_name:
                if links is not None:
                    links.add(full_url)
                self._extract_links_dfs(full_url, depth + 1, links=links)

    async def _extract_links_dfs_async(self, url, depth=0, links=None):
        """
        Asynchronously extracts all the links from the page at the given URL using depth-first search.
        """
        if depth > self.max_depth or url in self.visited_urls:
            return

        self.visited_urls.add(url)
        print(f'Fetching links from {url} at depth {depth}')
        self.current_max_depth = max(self.current_max_depth, depth)

        page_content = await self._fetch_page_async(url)
        if not page_content:
            return

        soup = BeautifulSoup(page_content, self.parser)
        page_links = [a['href'] for a in soup.find_all('a', href=True)]

        tasks = []
        for link in page_links:
            full_url = urljoin(url, link)
            parsed_full_url = urlparse(full_url)
            # Ignore URL fragments
            full_url = parsed_full_url._replace(fragment='').geturl()
            if parsed_full_url.netloc == self.domain_name:
                if links is not None:
                    links.add(full_url)
                tasks.append(self._extract_links_dfs_async(
                    full_url, depth + 1, links=links))

        await asyncio.gather(*tasks)

    def _extract_links_bfs(self, links=None):
        """
        Extracts all the links from the base URL using breadth-first search.
        """
        queue = deque([(self.base_url, 0)])

        while queue:
            url, depth = queue.popleft()

            if depth > self.max_depth or url in self.visited_urls:
                continue

            self.visited_urls.add(url)
            print(f'Fetching links from {url} at depth {depth}')
            self.current_max_depth = max(self.current_max_depth, depth)

            page_content = self._fetch_page(url)
            if not page_content:
                continue

            soup = BeautifulSoup(page_content, self.parser)
            page_links = [a['href'] for a in soup.find_all('a', href=True)]

            for link in page_links:
                full_url = urljoin(url, link)
                parsed_full_url = urlparse(full_url)
                # Ignore URL fragments
                full_url = parsed_full_url._replace(fragment='').geturl()
                if parsed_full_url.netloc == self.domain_name:
                    links.add(full_url)
                    queue.append((full_url, depth + 1))

    def get_links(self):
        """
        Gets all the links from the base URL up to the maximum depth, using the specified algorithm.

        Returns:
            A list of all the extracted links.
        """
        links = set()
        if self.algorithm == 'dfs':
            self._extract_links_dfs(self.base_url, links=links)
        elif self.algorithm == 'dfs_multithread':
            self._extract_links_dfs_multithread(self.base_url, links=links)
        elif self.algorithm == 'bfs':
            self._extract_links_bfs(links=links)
        elif self.algorithm == 'bfs_multithread':
            self._extract_links_bfs_multithread(links=links)

        return list(links)

    async def get_links_async(self):
        """
        Asynchronously gets all the links from the base URL up to the maximum depth, using the specified algorithm.

        Returns:
            A list of all the extracted links.
        """
        links = set()
        if self.algorithm == 'dfs':
            await self._extract_links_dfs_async(self.base_url, links=links)
        else:
            print(
                f"Async version for {self.algorithm} algorithm not implemented yet. Falling back to synchronous version.")
            links = set(self.get_links())
        return list(links)
