import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

# Maximum pages to crawl (to avoid infinite crawling)
MAX_PAGES = 20

visited = set()
transition_graph = {}

def is_internal_link(base_url, link):
    """Check if link belongs to the same website"""
    return urlparse(base_url).netloc == urlparse(link).netloc

def crawl(url, base_url):
    if url in visited or len(visited) >= MAX_PAGES:
        return

    print(f"Crawling: {url}")
    visited.add(url)
    transition_graph[url] = []

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup.find_all("a", href=True):
            link = urljoin(url, tag["href"])

            # Remove fragments (#section)
            link = link.split("#")[0]

            if is_internal_link(base_url, link):
                transition_graph[url].append(link)

                if link not in visited:
                    crawl(link, base_url)

    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

if __name__ == "__main__":
    start_url = "https://www.calculator.net/" 
    ""  
    crawl(start_url, start_url)

    # Save transition graph to JSON
    with open("transition.json", "w", encoding="utf-8") as f:
        json.dump(transition_graph, f, indent=4)

    print("\nCrawling completed!")
    print("Transition graph saved as transition.json")





























# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import networkx as nx
# import matplotlib.pyplot as plt
# from pyvis.network import Network

# def is_valid(url, domain):
#     """Check if the URL is valid and belongs to the same domain."""
#     parsed = urlparse(url)
#     return bool(parsed.netloc) and parsed.netloc == domain

# def get_links(url, domain):
#     """Fetch all internal links from a given URL."""
#     internal_links = set()
#     try:
#         response = requests.get(url, timeout=5)
#         if response.status_code != 200:
#             return internal_links
        
#         soup = BeautifulSoup(response.text, 'html.parser')
#         for a_tag in soup.find_all("a", href=True):
#             href = a_tag.get("href")
#             full_url = urljoin(url, href)
#             # Clean URL (remove fragments/query params for cleaner nodes)
#             clean_url = full_url.split('#')[0].rstrip('/')
            
#             if is_valid(clean_url, domain):
#                 internal_links.add(clean_url)
#     except Exception as e:
#         print(f"Error crawling {url}: {e}")
    
#     return internal_links

# def build_transition_graph(start_url, max_depth=2):
#     domain = urlparse(start_url).netloc
#     G = nx.DiGraph()
#     visited = set()
#     queue = [(start_url, 0)]  # (url, current_depth)

#     while queue:
#         current_url, depth = queue.pop(0)
        
#         if depth >= max_depth or current_url in visited:
#             continue
            
#         print(f"Crawling: {current_url} (Depth: {depth})")
#         visited.add(current_url)
        
#         links = get_links(current_url, domain)
#         for link in links:
#             G.add_edge(current_url, link)
#             if link not in visited:
#                 queue.append((link, depth + 1))
                
#     return G

# # --- Execution ---
# seed_url = "https://www.geeksforgeeks.org/"  # Replace with your target
# web_graph = build_transition_graph(seed_url, max_depth=2)

# # --- Visualization ---
# plt.figure(figsize=(12, 8))
# pos = nx.spring_layout(web_graph, k=0.5)
# nx.draw(web_graph, pos, with_labels=True, node_size=50, font_size=8, arrows=True)
# plt.title(f"Website Transition Graph for {seed_url}")
# plt.show()