import requests,json

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_phi3(user_text, command_map):
    prompt = f"""
    You are a command parser. Use only the following actions:
    {json.dumps(command_map, indent=2)}
    Return only a JSON object with the matching action.
    User: "{user_text}"
    Output: action in dict as python
    """
    try:
        r = requests.post(OLLAMA_URL, json={"model": "phi3:mini", "prompt": prompt, "stream": False})
        raw_string = r.json().get("response", "").strip()
        json_data = json.loads(raw_string)
        return json_data.get("action", "unknown")
    except Exception as e:
        print("Phi-3 error:", e)
        print("Raw output:", raw_string)
        return "unknown"

# if __name__ == "__main__":
#     user_input = input("You: ")
#     reply = chat_with_mistral(user_input)
#     print("Mistral:", reply)