import json
from typing import Dict, Any
from langchain.memory import MongoDBChatMessageHistory


class ManageConversations():
    """Class to store and extract user conversations."""

    __connection_string = "YOUR_MONGO_DB_CONNECTION_STRING"

    def extract_and_save_conversation(self, response: Dict[str, Any], userId: str):
        """Extracts key fields from the JSON obtained in the LLM response and stores
        it to MongoDB.
        """

        json_object = self.__extract_summary(response['text'])
        question = ""
        answer = ""
        if (json_object is not None):
            if "question" in json_object:
                question = json_object["question"]
            if "summary" in json_object:
                answer = json_object["summary"]

        self.__save_converstaion(question, answer, userId)

    def get_previous_converstions(self, userId: str) -> str:
        """Retrieves stored conversations from MongoDB for the given user ID."""
        message_history = MongoDBChatMessageHistory(
            connection_string=self.__connection_string, session_id=userId)
        prev_conv = ""
        for msg in reversed(message_history.messages):
            prev_conv = msg.content + prev_conv + " "

        return prev_conv

    def __save_converstaion(self, query: str, answer: str, userId: str):
        """Stores the user query and answer from LLM into MongoDB for the given 
        user ID.
        """
        message_history = MongoDBChatMessageHistory(
            connection_string=self.__connection_string, session_id=userId)
        message_history.add_user_message(query)
        message_history.add_ai_message(answer)

    def __extract_summary(self, response: str):
        """Extracts conversation JSON from LLM response."""
        firstIndexOfJson = response.rfind("{")
        lastIndexOfJson = response.rfind("}")
        if (firstIndexOfJson != -1 and lastIndexOfJson != -1):
            json_str = response[firstIndexOfJson:(lastIndexOfJson+1)]
            if (json_str.__contains__("summary")):
                return json.loads(json_str)

        return None
