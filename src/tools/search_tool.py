from duckduckgo_search import DDGS


def search_recipes(query: str) -> str:
    """
    Searches the web for specific recipes or cooking techniques.

    Args:
        query: The search string (e.g., '10 minute chicken recipes').

    Returns:
        str: A summary of the top 3 search results.
    """
    try:
        results = DDGS().text(keywords=query, max_results=3)
        summary = ""
        for r in results:
            summary += f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}\n\n"
        return summary
    except Exception as e:
        return f"Error searching for recipes: {str(e)}"