import os
import json
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API = os.getenv("OPENAI_API_KEY")


class RealEstateGPT():
    def __init__(self, openai_api_key=OPENAI_API, one_shot=True):
        """Setting up necessary components for chatbot with open_api_key and instruction prompts for agent. 
        Args:
            openai_api_key: user's Open AI API Key 
            one_shot (default = True): Instructions tell the model what to do, how to use the provided information, 
            what to do with the query, and how to construct the output. If one_shot = True, then it plays role_playing_prompt. 
            If not, it uses conversatonal_prompt. Feel free to change these prompts to instruct agent on other roles/duties. 
        Returns:
            Returns agent responses.
        """

        #set up openAI API Key and load file to use prompts. 
        os.environ["OPENAI_API_KEY"] = openai_api_key
        file_path = 'prompts.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        self.role_playing_prompt = data['one_shot_prompt']
        self.conversational_prompt = data['conversational_prompt']
        self.conversation_history = []
        self.one_shot = one_shot

        # Initialize the agent with scraped dataset
        initial_context = self.role_playing_prompt if one_shot else self.conversational_prompt
        self.agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
            'data/redfin_sales_080924.csv',
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            initial_context=initial_context)


    def ask_real_estate_question(self, query):
        if not self.one_shot:
            # Update the conversational prompt dynamically based on the conversation history
            dynamic_prompt = self.conversational_prompt + "\n\n" + self._format_conversation_history() + f"\nClient: {query}"
        else:
            # For one-shot interactions, use the static role-playing prompt with the current query
            dynamic_prompt = f"{self.role_playing_prompt}\n\nClient: {query}"

        try:
            response = self.agent.run(dynamic_prompt)
            print(response)
            # Update the conversation history with the new exchange
            if not self.one_shot:
                self.conversation_history.append({'Client': query, 'AI': response})
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def _format_conversation_history(self):
        # Format the conversation history for inclusion in the dynamic prompt
        formatted_history = ""
        for exchange in self.conversation_history:
            formatted_history += f"Client: {exchange['Client']}\nAI: {exchange['AI']}\n"
        return formatted_history
