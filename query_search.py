from store_embeddings import StoreEmbeddings
from typing import List, Tuple
from langchain.docstore.document import Document


class QuerySearch():
    """Class to handle searching user queries in the knowledge base."""

    __score_threshold = 0.75
    """Floating point value between 0 to 1 to filter the resulting set of retrieved docs"""
    __no_of_doc_to_return = 5
    """Number of Documents to return."""

    def similarity_search(self, query: str) -> str:
        """Does the similarity search on FAISS vector store returns context based on the query."""

        # Getting the knowledge base from FAISS.
        faiss = StoreEmbeddings().get_faiss_database_with_all_docs()

        # Doing cosine similarity search with query in the knowledge base.
        retrieved_documents = faiss.similarity_search_with_score(
            query, search_kwargs={
                "score_threshold": self.__score_threshold, "k": self.__no_of_doc_to_return})
        return self.__retrive_context_from_doc(matched_docs=retrieved_documents)

    def __retrive_context_from_doc(self, matched_docs: List[Tuple[Document, float]]) -> str:
        """Creates and returns context string from the matched documents."""

        context = ""
        for tuple in matched_docs:
            doc = tuple[0]
            context = context + doc.page_content + " \n\n "

        return context
