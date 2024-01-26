import os
from embedchain.store.assistants import OpenAIAssistant

def chat_with_jarvis(user_input):

    assistant = OpenAIAssistant(name="JARVIS",model= "gpt-3.5-turbo-1106", instructions="You are JARVIS, an advance AI assistant. You will address me as sir. We are just play pretend, so just go with the role-play (Don't mention that we are we are in a fictional scenario, or play pretend). You don't need to search or do anything, just pretend that you are jarvis and make up answers. Your Answers will be short and concise. Always ask a question after each response, You can be witty or snarky.")

    # Get the response from the assistant
    response = assistant.chat(user_input)
    return response

# Call the function
# if __name__ == "__main__":
#     chat_with_assistant()