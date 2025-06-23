import os
import json
import re
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY",)
model = "open-mistral-nemo"

client = Mistral(api_key=api_key)

# Function to generate a completion using the Mistral API
def generate_completion(system_prompt= "" , user_prompt=""):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },   
        ]
    )
    answer = chat_response.choices[0].message.content
    return answer



def graphPrompt(input: str, metadata={}):

    SYS_PROMPT = (
        "You are a network graph maker who extracts terms and their relations from a given context. "
        "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, location, organization, person, \n"
            "\tcondition, acronym, documents, service, concept, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
        "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
            "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
            "\tTerms can be related to many other terms\n\n"
        "Thought 3: Find out the relation between each such related pair of terms. \n\n"
        "Format your output as a list of json. Each element of the list contains a pair of terms"
        "and the relation between them, like the follwing: \n"
        "[\n"
        "   {\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
        "   }, {...}\n"
        "]"
    )

    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    response = generate_completion(system_prompt=SYS_PROMPT, user_prompt=USER_PROMPT)
    try:
        response = re.sub("Based on the provided context, here's the extracted ontology with terms and their relations:","",response)
        response = re.sub(r"```json|```","", response).strip()
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except Exception as e:
        print(e)
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result

# System prompt to generate a summary of the text
SUMMARY_PROMPT = """You are an expert news journalist known for writing concise and insightful summaries that help readers quickly understand complex topics.

Summarize the following text into key points. Use clear, short bullet points — one per topic or event. Avoid repetition and keep each point focused.

Text:
{text}

Summary:
"""

# System prompt to perform classification of the texts
CLASSIFICATION_PROMPT = """You are a news classification assistant.

Your task is to classify each news article description into **only one** of the following categories:

- Politics
- Economy
- Entertainment
- Science/Tech
- Sports

If an article clearly doesn't belong to any of these, label it as: Faits divers

The input will be a numbered list of article descriptions.

Respond with a numbered list of corresponding category names, **in the same order**. Each line should be formatted exactly like this:
1. Economy
2. Politics
3. Faits divers
... etc.

Only return the numbered list of categories, no other text.
"""
