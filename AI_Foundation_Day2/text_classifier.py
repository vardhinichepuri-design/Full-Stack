import ollama

while True:
    text = input("\nEnter a message: ")

    if text.lower() == "exit":
        break

    prompt = f"""
Classify the following message as either Urgent or Not Urgent.

Few-shot examples:

Message: "I need the report immediately."
Classification: Urgent

Message: "Please send the notes when you have time."
Classification: Not Urgent

Message: "This is an emergency. Please respond now."
Classification: Urgent

Message: "Can you share the assignment tomorrow?"
Classification: Not Urgent

Now classify this message:

"{text}"

Reply ONLY with:
Urgent
OR
Not Urgent
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print("Classification:", response["message"]["content"].strip())