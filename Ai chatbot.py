from transformers import pipeline

chatbot = pipeline('text-generation', model='microsoft/DialoGPT-medium')

user_input = 'Hello, how are you?'
response = chatbot(user_input, max_length=50)
print(response[0]['generated_text'])
