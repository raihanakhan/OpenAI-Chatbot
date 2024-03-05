import openai


def ask_openai(message):
    response = openai.chat.completions.create(
        messages=message,
        model="gpt-3.5-turbo",
        max_tokens=500,
    )

    answer = response.choices[0].message.content.strip()
    return answer


def asK_openai_streaming(message):
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message
            }
        ],
        model="gpt-3.5-turbo",
        stream=True
    )

    for chunk in response:
        print(chunk.choices[0].delta.content or "", end="")

