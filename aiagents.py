from agents import Agent, Runner, AsyncOpenAI, set_tracing_disabled, set_default_openai_client, enable_verbose_stdout_logging, set_default_openai_api

from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)
external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions") 

enable_verbose_stdout_logging()

WebDev: Agent = Agent(
    name= "WebDev Agent",
    instructions= "You are a helpful assistant, and a specialist in web development. You can help with any web development related questions.", 
    model= "gemini-2.0-flash-exp",
    handoff_description="WebDev Agent is a specialized agent for web development. It can assist with any web development related questions, including HTML, CSS, JavaScript, and more.",
)

MobileDev: Agent = Agent(
    name = "MobileDev Agent",
    instructions= "You are a helpful assistant, and a specialist in mobile development. You can help with any mobile development related questions.",
    model= "gemini-2.0-flash-exp",
    handoff_description="MobileDev Agent is a specialized agent for mobile development. It can assist with any mobile development related questions, including Android, iOS, and more.",
)



DevOps_agent: Agent = Agent(
    name = "DevOps Agent",
    instructions = "You are a helpful assistant, and a specialist in DevOps. You can help with any DevOps related questions.",
    handoff_description="DevOps Agent is a specialized agent for DevOps. It can assist with any DevOps related questions, including CI/CD, Docker, Kubernetes, and more.",
    model= "gemini-2.0-flash-exp",
)

OpenAISDK_agent: Agent = Agent(
    name = "OpenAI SDK Agent",
    instructions= "You are a helpful assistant, and a specialist in OpenAI SDK. You can help with any OpenAI SDK related questions.",
    handoff_description="OpenAI SDK Agent is a specialized agent for OpenAI SDK. It can assist with any OpenAI SDK related questions, including Python, JavaScript, and more.",
    model= "gemini-2.0-flash-exp",
)

orchestrator_agent: Agent = Agent(
    name = "OpenAI Agent",
    instructions= "You are a helpful assistant, and a specialist in OpenAI. You can help with any OpenAI related questions.",
    handoff_description="OpenAI Agent is a specialized agent for OpenAI. It can assist with any OpenAI related questions, including GPT-3, DALL-E, and more.",
    tools = [DevOps_agent.as_tool(
        tool_name = "DevOps Agent",
        tool_description = "DevOps Agent is a specialized agent for DevOps. It can assist with any DevOps related questions, including CI/CD, Docker, Kubernetes, and more.",
    ),
    OpenAISDK_agent.as_tool(
        tool_name = "OpenAI SDK Agent",
        tool_description = "OpenAI SDK Agent is a specialized agent for OpenAI SDK. It can assist with any OpenAI SDK related questions, including Python, JavaScript, and more.",
    ),
    ],
    model= "gemini-2.0-flash-exp",    
)
triage_agent: Agent = Agent(
    name = "PanaCloud Agent",
    instructions= "You are a helpful assistant",
    model= "gemini-2.0-flash-exp",
    handoffs= [orchestrator_agent, WebDev, MobileDev],
)

result = Runner.run_sync(triage_agent, "create a mobile application")
print(result.final_output)