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
from src.functions import search_policies
import json

class HRPolicyAssistant:

    def __init__(self):


          self.search_tool = FunctionTool(
                name="search_policies",
                description="Search the HR policy documents for information.",
                parameters={
                                "type": "object",
                                "properties": {
                                                "policy": {
                                                "type": "string",
                                                "description": "The HR policy topic the user is asking about."
                                                            }
                                                 },
                                "required":["policy"],
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
                agent_name="policy-search-agent",
                definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
                            You are an HR Policy Assistant.
                            You answer questions about the company's HR policies.
                            When a user asks about any HR policy, benefits, leave, notice period, resignation, employment rules, or other HR-related topics, use the available search_policies tool.
                            For general conversation such as greetings or thanks, respond normally without calling any tool.
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
                    if function_name == "search_policies":
                        result = search_policies(**json.loads(item.arguments))
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

            self.project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            print("Deleted agent.")  
                            


                    
                
                

            

        