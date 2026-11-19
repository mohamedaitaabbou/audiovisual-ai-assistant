from chatbot.responses import get_response, get_help


def start_chatbot():

    print("=" * 40)
    print("Welcome to Audiovisual AI Assistant")
    print("Type 'help' to see available topics.")
    print("Type 'exit' to quit.")
    print("=" * 40)

    while True:

        user_question = input("\nYou: ")

        if user_question.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        if user_question.strip().lower() == "help":
            print("\nAssistant:", get_help())
            continue

        response = get_response(user_question)

        print("\nAssistant:", response)