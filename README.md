# WebPageLinkMiner

`WebPageLinkMiner` is a Python library for extracting all the links from a given domain.

## Features

- Extract links from any domain
- Specify maximum depth for link extraction
- Uses depth-first search or breadth-first search algorithm
- Asynchronous link extraction for faster performance

## Further use

Our Python library allows users to extract all the links within a domain by providing its base URL. Once the links are extracted, they can be loaded using Langchain's WebBaseLoader to embed the content of the website. This can be useful for deploying a Q&A chatbot that can answer questions related to the website's content.

## Installation

Since the package is not hosted on PyPi, you'll have to clone the repository and install it manually using setup.py:

1. Clone the repository to your local machine:

```
git clone https://github.com/ojasskapre/WebPageLinkMiner.git
```

2. Navigate to the repository:

```
cd WebPageLinkMiner
```

3. Install the package:

```
pip install .
```

## Usage

1. **Simple usage example:**

```
from webpagelinkminer import WebPageLinkExtractor

extractor = WebPageLinkExtractor('https://www.example.com', max_depth=3)
links = extractor.get_links()

print(f'Total links found: {len(links)}\n')
```

2. **Customizing Extraction Parameters:**

```
from webpage_link_extractor import WebPageLinkExtractor

# Create an instance of WebPageLinkExtractor with custom parameters

extractor = WebPageLinkExtractor(
  base_url='https://nextjs.org/docs',
  timeout=15, # Set the request timeout to 15 seconds
  max_depth=5, # Extract links up to a maximum depth of 5
  parser='html.parser', # Use the 'html.parser' for BeautifulSoup parsing
  algorithm='bfs' # Use breadth-first search for link extraction
)

# Get all the links using the specified algorithm and parameters

links = extractor.get_links()

# Print the extracted links

print(links)
```

3. **Asynchronous Extraction:**

```
import asyncio
from webpage_link_extractor import WebPageLinkExtractor

async def extract_links_async(): # Create an instance of WebPageLinkExtractor with the base URL
extractor = WebPageLinkExtractor('https://nextjs.org/docs')

# Get all the links asynchronously using the default algorithm
links = await extractor.get_links_async()

# Print the extracted links
print(links)

# Run the asynchronous extraction
asyncio.run(extract_links_async())
```

## Configuration Options

The `WebPageLinkExtractor` class provides several configuration options to customize the link extraction process. When creating an instance of the WebPageLinkExtractor class, you can specify the following options:

- `base_url` (str): The base URL to start extracting links from.
- `timeout` (int): The timeout for requests, in seconds. Default is `10` seconds.
- `max_depth` (int): The maximum depth of links to extract. Default is `3`.
- `parser` (str): The parser to use for BeautifulSoup. Default is `'lxml'`. Other option provided is `'html.parser'`
- `algorithm` (str): The algorithm to use for link extraction. Default is `'dfs'`. Other option is `'bfs'`

To create an instance of `WebPageLinkExtractor` with custom configuration options, use the following syntax:

```
extractor = WebPageLinkExtractor(
  base_url='https://nextjs.org/docs',
  timeout=15,
  max_depth=5,
  parser='html.parser',
  algorithm='bfs'
)
```

**Note**: The asynchronous version currently supports only the DFS algorithm.
