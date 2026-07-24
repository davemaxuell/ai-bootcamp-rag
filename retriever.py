from ingest import get_vectorstore


def retrieve(query: str, k: int = 6, level: str | None = None):
    if not query.strip():
        return []
    store = get_vectorstore()
    metadata_filter = None
    if level:
        metadata_filter = {"level": {"$in": [level, "general"]}}
    return store.similarity_search(query, k=k, filter=metadata_filter)
