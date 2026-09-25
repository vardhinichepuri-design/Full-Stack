from ollama import chat
messages = [
    {"role" : "system","content" : "Identify sentiment as positive, negative, neutral."
    "reply with one word only."},
    {"role" : "user","content": "Great Movie!"},
    {"role" : "system","content": "Positive"},
    {"role" : "user","content": "Waste of money."},
    {"role" : "system","content": "Negative"},
    {"role" : "user","content": "It was okay."},
    {"role" : "system","content": "Neutral"},
    {"role" : "user","content": "Loved the acting but the ending was dull."},

]
response = chat(
    model= "llama3.2",
    messages=messages
)
print(response.message.content)