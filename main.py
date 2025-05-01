from core.history import load_conversation_history
from core.api import chat_with_rima
from voice.speaker import speak
from voice.listener import listen

def main():
    print("Welcome to Stella! Type or say something. Say 'quit' to exit.")
    conversation_history = load_conversation_history()
    
    while True:
        mode = input("Type [t] or Speak [s]? ").strip().lower()
        if mode == "s":
            user_input = listen()
            print(f"You (spoken): {user_input}")
        else:
            user_input = input("You (typed): ")
        
        if user_input.lower() == "quit":
            break

        response = chat_with_rima(user_input, conversation_history)
        print("Stella:", response)
        speak(response)

if __name__ == "__main__":
    main()
