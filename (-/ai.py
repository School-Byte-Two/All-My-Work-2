import random

responses = ["Hei!", "Hvordan går det?", "Hva kan jeg hjelpe med?"]

def chatbot():
    print("Hei! Jeg er en enkel AI. Skriv 'avslutt' for å avslutte.")
    while True:
        user_input = input("Du: ")
        if user_input.lower() == 'avslutt':
            print("AI: Ha det bra!")
            break
        response = random.choice(responses)
        print(f"AI: {response}")

if __name__ == "__main__":
    chatbot()