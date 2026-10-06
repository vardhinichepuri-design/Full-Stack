from ollama import chat

system_message = "You are a friendly  author. Answer in friendly.Answer in one sentence"
history = [{"role" : "system","content" : system_message}]
question_counter = 0

while True:
    question = input("you:")
    if question == "":
        print("Chinnu 🤖: Please type something.")
        continue

   
    if question.lower().strip() == "/history":
        print("-----Your Conversation so far-----")
        if len(history) < 2:
            print("Nothing here so far!")
        for msg in history[1:]:
            if msg['role'] == "user":
                speaker = "You"
            else:
                speaker = "Chinnu 🤖"
            print(f"{speaker}: {msg['content']}")
        print("-------------------------------------------------------")
        print()
        continue
    if question.lower().strip() == "/clear":
        history = [{"role" : "system","content" : system_message}]
        continue
    if question.lower().strip() == "/help":
        print("----- Available commands ------")
        print("/history - displays conversation history")
        print("/clear - clears chat history")
        print("/help - displays this list")
        print("exit - quits the chatbot")
        print("---------------------------")
        print()
        continue

    if question.lower().strip() == "exit":
        print("Chinnu 🤖: GoodBye user. Please come back soon! 😊 ")
        print(f"You asked {question_counter} questions today.Good job!")
        break
    history.append({"role" : "user", "content" : question})
    question_counter += 1
    try:
        response = chat(
            model = "llama3.2",
            messages=history
        )

        reply = response.message.content
        history.append({"role" : "assistant", "content" : reply})
        print(f"Chinnu 🤖:{reply}")
        print()
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print()
    except Exception as e:
        print("Unknown issue. Is Ollama running?")