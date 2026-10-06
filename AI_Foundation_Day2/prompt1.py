from ollama import chat
response = chat(
    model="llama3.2",
    messages=[
        {
            "role" : "user",
            "content" : "Write a gmail message to my HOD for my internship approval ."
        }
    ]
)
print(response.message.content)