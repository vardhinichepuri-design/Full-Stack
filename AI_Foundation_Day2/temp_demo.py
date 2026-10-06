from ollama import chat
prompt = "Give me a single one-line tagline for my coffee shop.Answer in 1 line.Only the tagline/"
for t in [0,0.7,1.5]:
    print(f"Temp: {t}")
    for run in range(3):
        response = chat(
            model= "llama3.2",
            messages=[
                {
                    "role" : "user",
                    "content" : prompt
                    }
                ],
            options = {"temperature" : t}

          )
        print(f"Run{run + 1}:{response.message.content}")
    print()