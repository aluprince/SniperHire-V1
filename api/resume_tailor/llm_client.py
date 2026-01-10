import os
from groq import Groq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

model="llama-3.3-70b-versatile"


def get_llm_tailoring(prompt, context):
    chat_completion = client.chat.completions.create(
        messages=[{
            "role" : "user",
            "content": f"""{prompt}, {context}"""
        }],
        model=model
    )
    # print(chat_completion.choices[0].message.content)

    result = chat_completion.choices[0].message.content
    return result


if __name__ == "__main__":
    response = get_llm_tailoring("Hey what is your name")
    print(response)



