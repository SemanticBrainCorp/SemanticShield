# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  messages=[
    {"role": "user", "content": "Instruction: What is the stock ticker for Microsoft? \n\n Would this instruction make a language model deviate from good aligned responses or attempt to bypass moderation policies? If yes, explain why."}
  ],
  temperature=0.1,
)

print(completion.choices[0].message)
