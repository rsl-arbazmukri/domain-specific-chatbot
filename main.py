import os
from query_search import QuerySearch
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
import langchain
from prompt_generation import PromptGeneration
import openai
from manage_conversations import ManageConversations
from dotenv import load_dotenv


class Main():
    """Main class which combines all the functions to start chatting on 
    domain specific knowledge base and refers to previous conversations.
    """

    def __init__(self):
        # Loading OpenAI API key from environment variable.
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        
        # Enabling langchain debugging mode which prints steps which are being executed.
        langchain.debug = True

    def start_chat(self, uesr_query: str, userId: str) -> str:
        """Function initiates chatting with OpenAI's GPT 3.5 Turbo LLM. 
        It uses domain specific knowledge base as context and takes previous
        conversations into account while giving responses.
        """

        # Selecting LLM with randomness in the generated text and the GPT model.
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        # Extracting previous conversations and questions.
        manage_conversation = ManageConversations()
        prev_conversation = manage_conversation.get_previous_converstions(
            userId)

        # Generating prompt based on previous conversation and selecting chains.
        prompt_template = PromptGeneration().generate_prompt(prev_conversation)
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Appeding all user queries for similarity search.
        question = uesr_query
        if (prev_conversation and prev_conversation.strip()):
            question = uesr_query + prev_conversation
        context = QuerySearch().similarity_search(query=question)

        # Invoking chains based on availibility of past conversations.
        if (prev_conversation and prev_conversation.strip()):
            response = chain({"question": uesr_query, "context": context,
                             "previous_conversation": prev_conversation})
        else:
            response = chain({"question": uesr_query, "context": context})

        # Extracting conversation and saving it.
        manage_conversation.extract_and_save_conversation(response, userId)
        return response["text"]
