import os
import tiktoken
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def load_chat_model():
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
    TEMPERATURE = os.environ.get("TEMPERATURE", "0.1")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    return init_chat_model(OPENAI_MODEL, model_provider="openai", base_url=OPENAI_API_BASE, temperature=float(TEMPERATURE))

def messages_token_count(messages, model="gpt-4-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0

    for message in messages:
        content = message.content if message.content else ""
        num_tokens += len(encoding.encode(content))
    return num_tokens

def token_count(text, model_name="gpt-4o"):
    # Initialize the encoder for the specified model
    encoder = tiktoken.encoding_for_model(model_name)
    # Encode the text into tokens
    tokens = encoder.encode(text)
    # Return the number of tokens
    return len(tokens)

def read_prompt(state: str) -> str:
    try:
        file_path = f"./src/prompts/{state}_prompt.txt"
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def read_file_prompt(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def reasoning_prompt(prompt_path: str, **input_vars):
    prompt_templ = read_file_prompt(prompt_path)
    prompt = PromptTemplate(
        template=prompt_templ, input_variables=list(input_vars.keys()),
    )
    message = prompt.format_prompt(**input_vars)
    return message.to_string()

def get_last_k_human_messages(messages, k=1):
    return [message for message in reversed(messages) if isinstance(message, HumanMessage)][:k]

def get_latest_human_message(messages):
    return get_last_k_human_messages(messages, 1)[0].content
