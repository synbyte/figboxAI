

from groq import Groq

g_client = Groq(api_key='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')

def g_prompt(prompt): # Feed prompt to Groq chat completion

    convo = [
        {
            'role':'user',
            'content':prompt
        }
    ]
    completion = g_client.chat.completions.create(messages=convo, model='llama3-8b-8192')
    response = completion.choices[0].message.content

    return response

def function_call(prompt): # Take prompt and determine what function needs to be called if any
    sys_msg = (
        'You are an AI function calling mode. You will determine whether extracting the users clipboard content, '
        'taking a screenshot, capturing the webcam or calling no function is best for a voice assistant to respond '
        'to the users prompt. The webcam can be assumed to be a normal laptop webcam facing the user. You will '
        'respond with only one selection from this list: ["extract clipboard", "take screenshot", "capture webcam", "None"] \n'
        'Do not repond with anything but the most logical selection for that list with no explanation. Format the '
        'function call name exactly as I listed.'
    )

    function_convo = [
        {
            'role': 'system',
            'content': sys_msg
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]

    completion = g_client.chat.completions.create(messages=function_convo, model='llama3-8b-8192')
    response = completion.choices[0].message.content
    
    return response

def web_cam_capture():
    if not web_cam.isOpened():
        print('Error: Camera didnt open successfully')
        exit()
    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    cv2.imwrite(path,frame)

    return None

def emotion_call(prompt):
    sys_msg = (
        'You are an emotional analyst AI. Your job is to look at a prompt and give it 3 emotional scores. '
        'For example, given the prompt "I finally found the place!", you would respond with: "Joy,\nExcitement,\nSatisfaction". \n'
        'You should only respond with the top 3 emotions you get from the text, nothing else.'
    )

    convo = [
        {
            'role': 'system',
            'content': sys_msg
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]

    completion = g_client.chat.completions.create(messages=convo, model='llama3-8b-8192')
    response = completion.choices[0].message.content

    return response

prompt = input('USER: ')

response = g_prompt(prompt)
function_response = function_call(prompt)
emotional_response = emotion_call(prompt)
print(emotional_response)
#print('Function Call: ',function_response)

#print(response)