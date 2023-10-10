from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from load_custom_data import LoadCustomData
import os
from langchain.document_loaders.base import BaseLoader
from typing import List


class StoreEmbeddings():
    """Generate and store embeddings of the domain specific knowledge base."""

    __faiss_folder_path = "data/generated/embeddings_storage"
    """Path to store the generated embeddings through FAISS."""

    def get_faiss_database_with_all_docs(self) -> FAISS:
        """Checks whether FAISS vector storage for embeddings is present in the specified path.
        If embeddings are already available, it returns the existing store; 
        otherwise, it generates embeddings from custom data and stores them in the specified path.
        """

        openai_embeddings = OpenAIEmbeddings()
        if (os.path.exists(self.__faiss_folder_path)):
        
            # Fetch locally stored embeddings from FAISS.
            docsearch_faiss = FAISS.load_local(
                folder_path=self.__faiss_folder_path, embeddings=openai_embeddings)
            return docsearch_faiss
        else:
        
            # Retrieve the knowledge base.
            custom_data_loaders = LoadCustomData().load_custom_data()
            load_all_documents = self.__get_list_of_doc_from_loaders(
                loaders=custom_data_loaders)

            # Generate embeddings of the retrieved knowledge base.
            docsearch_faiss = FAISS.from_documents(
                documents=load_all_documents, embedding=openai_embeddings)

            # Save the embeddings in local path.
            FAISS.save_local(self=docsearch_faiss,
                             folder_path=self.__faiss_folder_path)
        return docsearch_faiss

    def __get_list_of_doc_from_loaders(self, loaders: List[BaseLoader]):
        """Loads & splits the documents supplied within the loaders and returns list of 
        the loaded documents as output.
        """

        docs = []
        for loader in loaders:
            docs.extend(loader.load_and_split())

        return docs
