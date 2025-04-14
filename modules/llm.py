import ollama
from modules.prompts import prompts

LLM_MODEL_NAME = "llama3.2"
MAX_SIZE = 100
global mem, prompt
prompt = prompts[0]['prompt'] 
mem = [{"role": "system", "content": prompt}]

def choose_prompt():
    print("Choose a prompt:")
    for i, p in enumerate(prompts):
        print(f"{i+1}. {p['title']}")
    while True:
        try:
            choice = input("Enter the number of your choice('q':exit): ")
            if choice == 'q':
                print("Exiting.")
                return False
            choice = int(choice) - 1   
            if choice < 0 or choice >= len(prompts):
                print("Out of range. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
    
    global prompt, mem
    prompt = prompts[choice]['prompt']
    mem = [{"role": "system", "content": prompt}]
    return True


def chat_no_mem(user_input):
    response = ollama.chat(
        model = LLM_MODEL_NAME, 
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}], 
        stream = False)
    return response["message"]["content"]

def chat_init():
    return chat('it is your turn to speak')

def chat(user_input):
    mem.append({"role": "user", "content": user_input})
    if len(mem) > MAX_SIZE: mem.pop(0)
    response = ollama.chat(
        model = LLM_MODEL_NAME, 
        messages = mem, 
        stream = False)
    mem.append({"role": "assistant", "content": response["message"]["content"]})
    if len(mem) > MAX_SIZE: mem.pop(0)
    # print(mem)
    return response["message"]["content"]

