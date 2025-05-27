import google.generativeai as genai

genai.configure(api_key="AIzaSyDbYbmj0TWNvW0lTcXIa4-jQOEF_2N0mu4")

def chat_with_gemini(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    response =  model.generate_content(prompt)
    return response.text

print("Chào bạn, tôi có thể giúp gì về món ăn?")

while True:
    prompt = input("Bạn: ")
    if prompt.lower() == "exit":
        break
    reply = chat_with_gemini(prompt)
    print("Gemini:" ,reply, "\n")