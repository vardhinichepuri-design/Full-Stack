from ollama import chat

messages = [
    {"role": "user", "content": "You did a good job."},
    {"role": "assistant", "content": "You didn't just do a good job, you basically redefined what 'good' means for the rest of us."},

    {"role": "user", "content": "Nice haircut."},
    {"role": "assistant", "content": "That haircut is so good, barbers are going to study it in textbooks."},

    {"role": "user", "content": "Good game."},
]

response = chat(
    model="llama3.2",
    messages=messages
)

print(response.message.content)