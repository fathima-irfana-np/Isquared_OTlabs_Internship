try:
    from langchain.retrievers import ContextualCompressionRetriever
    print("Import 1 success")
except ImportError as e:
    print(f"Import 1 failed: {e}")

try:
    from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
    print("Import 2 success")
except ImportError as e:
    print(f"Import 2 failed: {e}")
