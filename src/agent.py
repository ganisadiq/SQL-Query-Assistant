from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from src.config import project_endpoint, model_deployment
from src.embedding.azure_embedding_service import AzureEmbeddingService
from src.retrieval.faiss_retriever import FAISSRetriever
from azure.ai.projects.models import FunctionTool
from openai.types.responses.response_input_param import (
    FunctionCallOutput,
    ResponseInputParam,
)
from src.functions import search_database_schema
import json

class SQLQueryAssistant:

    def __init__(self):


          self.search_tool = FunctionTool(
                name="search_database_schema",
                description="""Search the database schema, relationships,
                             business rules, and SQL guidelines to help
                            generate an accurate SQL query.""",
                parameters={
                                "type": "object",
                                "properties": {
                                                "question": {
                                                "type": "string",
                                                "description": "The user's request for generating an SQL query."
                                                            }
                                                 },
                                "required":["question"],
                                "additionalProperties":False
                            },
                strict=True
                            )
          
          self.credentials = DefaultAzureCredential()
          self.project_client = AIProjectClient(
               endpoint=project_endpoint,
               credential=self.credentials
          )
          self.openai_client = self.project_client.get_openai_client()
          self.agent = self.project_client.agents.create_version(
                agent_name="sql-query-agent",
                definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
                                You are an SQL Query Assistant.

                                Your job is to generate accurate SQL queries
                                based on the database documentation.

                                Whenever a user asks for an SQL query,
                                information about tables,
                                columns,
                                relationships,
                                or business rules,
                                always use the search_database_schema tool.

                                Only use tables and columns that appear in
                                the retrieved context.

                                Never invent table names,
                                column names,
                                or relationships.

                                If the requested information is not available
                                in the retrieved documentation,
                                tell the user that the schema does not contain
                                enough information.

                                For greetings or normal conversation,
                                respond without calling any tool.

                                Return SQL only unless the user explicitly
                                asks for an explanation.
                                """,
                tools=[self.search_tool]
                ),
            )
          self.conversation = self.openai_client.conversations.create()
          self.input_list: ResponseInputParam = []
          

    def get_response(self,user_input):
            print("=" * 50)
            print("get_response() called")
            print(f"User input: {user_input}")

            self.openai_client.conversations.items.create(
                conversation_id=self.conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )



            response = self.openai_client.responses.create(
                conversation=self.conversation.id,
                extra_body={
                    "agent_reference":{"name":self.agent.name,
                                    "type":"agent_reference"}
                                                },
                input= self.input_list,
            )

            if response.status == "failed":
                print(f"Response failed: {response.error}")
                return "Sorry, something went wrong."

            
            self.input_list = []

            for item in response.output:
                if item.type == "function_call":
                    function_name = item.name
                    if function_name == "search_database_schema":
                        result = search_database_schema(**json.loads(item.arguments))
                        self.input_list.append(
                            FunctionCallOutput(
                                type="function_call_output",
                                call_id=item.call_id,
                                output=result,
                            )
                        )
            if self.input_list:

                response = self.openai_client.responses.create(
                    previous_response_id=response.id,
                    input=self.input_list,
                    extra_body={
                        "agent_reference": {
                            "name": self.agent.name,
                            "type": "agent_reference",
                        }
                    },
                )

            print(response.output_text)


            return response.output_text

            # self.project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            # print("Deleted agent.")  
                            


                    
                
                

            

        