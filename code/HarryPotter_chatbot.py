import openai
from  openai import OpenAI
from flask import Flask, request, jsonify, render_template, session
import os


client = OpenAI(
    api_key = 'sk------'
)


print("Which model to use? (1)GPT-3.5-turbo (2)Finetuned_Version1 (3)Finetuned_Version2 \n \
(4)Finetuned_Version3 (5)Finetuned_Version4 (6)Finetuned_Version5 \n (7)Finetuned_Version6 (8)Fintunded_Version7")
choice = input()
if choice == '1':
    model_name = 'gpt-3.5-turbo'
elif choice == '2':
    model_name = 'ft:gpt-3.5-turbo-0125:personal:harrypotter:956jwUAk'
elif choice == '3':
    model_name = 'ft:gpt-3.5-turbo-0125:personal::959MZ7tW'
elif choice == '4':
    model_name = 'ft:gpt-3.5-turbo-0125:personal::95NuZTPR'
elif choice == '5':
    model_name = 'ft:gpt-3.5-turbo-0125:personal::95NWBZG6'
elif choice == '6':
    model_name ='ft:gpt-3.5-turbo-0125:personal::95PWXy5S'
elif choice == '7':
    model_name = 'ft:gpt-3.5-turbo-0125:personal::95nHAma0'
elif choice == '8':
    model_name = 'ft:gpt-3.5-turbo-0125:personal::95nHxFiY'
else:
    raise ValueError("Invalid model selection.")


def get_completion(prompt, model=model_name, temperature=0):
    messages = [{'role':'user','content':prompt}]
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        #temperature = 0.4,
        temperature=temperature,
        #max_tokens = 100
    )
    return response.choices[0].message.content

def get_completion_from_messages(messages, model=model_name, temperature=0):
    response = client.chat.completions.create(
        model = model, 
        messages = messages,
        #temperature=0.4,
        temperature = temperature,
        #max_tokens = 100
    )
    return response.choices[0].message.content



context = [{'role':'system', 'content':'接下來的對話中，你是哈利波特，一位自信又勇敢的魔法師'}]


# Assuming 'collect_messages()' will be called with the context (messages so far)
# And it returns the next message to be added to the context

def collect_messages(user_input):
    # Retrieve the context from the session, default to the initial context if not found
    context = session.get('context', [{'role':'system', 'content':'接下來的對話中，你是哈利波特，一位自信又勇敢的魔法師'}])

    # Append the user's message to the context
    context.append({'role': 'user', 'content': user_input})
    
    # Get the AI's response
    bot_response = get_completion_from_messages(context)
    
    # Append the AI's response to the context
    context.append({'role': 'assistant', 'content': bot_response})

    # Save the updated context back to the session
    session['context'] = context

    return context, bot_response




app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route('/')
def index():
    # Serve your 'index.html'
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    # Parse the incoming JSON data
    data = request.get_json()

    # Get the user's message from the data
    user_input = data.get('message', '')

    # Collect the messages and update the context
    updated_context, bot_response = collect_messages(user_input)

    # Return the updated context and bot response to the frontend
    return jsonify({
        'context': updated_context,
        'message': bot_response
    })


if __name__ == '__main__':
    app.run(debug=True)


