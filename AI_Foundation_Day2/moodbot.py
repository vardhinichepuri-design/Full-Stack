import ollama

while True:
    user_input = input("\nHow are you feeling? ")

    if user_input.lower() == "exit":
        break

    prompt = f"""
You are a Mood-Based Reply Bot.

Identify the user's mood and give recommendations.

User: {user_input}

Reply ONLY in this format:

Mood: <mood>
Song Genre: <song genre>
Snack: <snack>
Activity: <activity>
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print("\n" + response["message"]["content"])