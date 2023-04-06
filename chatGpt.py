import openai
import gradio as gr

openai.api_key = open('api_key.txt','r').read().strip('\n')

message_history = []

def predict(input):
    global message_history
    message_history.append({'role':'user','content':input})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )

    reply_text = completion.choices[0].message.content
    print(reply_text)
    message_history.append({'role':'assistant','content':reply_text})
    response = [(message_history[i]['content'],message_history[i+1]['content']) for i in range(0,len(message_history)-1,2)]
    return response

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder='Type Here').style(container=False)
        txt.submit(predict,txt,chatbot)
        #txt.submit(lambda: "", None, txt) You Can Use Lambda Function That Returns an Empty String
        txt.submit(None,None,txt,_js="() => {''}") # Or Adding JavaScript That Returns Empty String

demo.launch()