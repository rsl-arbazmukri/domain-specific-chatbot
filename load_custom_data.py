from langchain.document_loaders import CSVLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader
import pandas as pd
import os
from os import walk


class LoadCustomData():
    """Class which helps in loading different types of file in loaders."""

    def load_custom_data(
        self,
        dir_path: str = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    ) -> list:
        """Loads the files available in dir_path to Langchain loaders. """

        loaders = []
        filenames = next(walk(dir_path), (None, None, []))[2]
        for file in filenames:
            file_name, file_extension = os.path.splitext(file)
            loader = self.__get_loader(
                dir_path=dir_path, filename=file_name, file_extension=file_extension)
            if (loader is not None):
                loaders.append(loader)
        return loaders

    def __get_loader(self, dir_path: str, filename: str, file_extension: str):
        """Returns the Langchain loader for the provided file_extension."""

        file_path = dir_path + filename + file_extension
        match file_extension:
            case ".docx":
                return Docx2txtLoader(file_path=file_path)
            case ".pdf":
                return PyPDFLoader(file_path=file_path)
            case ".csv":
                return CSVLoader(file_path=file_path)
            case ".xlsx":
                excel_file = pd.DataFrame(pd.read_excel(file_path))
                conveted_csv_name = dir_path + filename + ".csv"
                excel_file.to_csv(conveted_csv_name, index=None, header=True)
                return CSVLoader(file_path=conveted_csv_name)
            case ".txt":
                return TextLoader(file_path=file_path)
            case ".html":
                return UnstructuredHTMLLoader(file_path=file_path)
            case ".json":
                return JSONLoader(file_path=file_path, jq_schema=".[]", text_content=False)
            case _:
                return None
