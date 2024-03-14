from openai import OpenAI 
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

name = "John"

# image with Dalle-3
print("Generating birthday card...")
prompt = """
Create a festive and heartwarming birthday card design. 
The front of the card should feature a cheerful scene depicting a group of diverse cartoon animals 
(such as 
a lion, 
an elephant, 
a giraffe, 
a flamingo, 
a penguin, 
a bear, 
a wolf, 
a fox,
a rabit,
a monkey,
a leopard,
a mouse,
a citellus,
а meerkat,
a dolphin,
a kangaroo,
a cat,
a tiger
and a leopard gecko
) wearing party hats and gathered around a large birthday cake with colorful candles. 
The cake should be on a table adorned with balloons and streamers, set against a background of a sunny sky with a few fluffy clouds. 
The animals should appear to be laughing and having a great time, symbolizing team camaraderie and joy. 
On the top of the card, in bold and colorful letters, include the text 'Happy Birthday'.
Make sure the name is present on the card and written correctly. The name is {name}.
The style should be vibrant, playful, and suitable for a professional yet friendly office environment. 
The overall tone of the card should convey warmth, inclusiveness, and celebration, reflecting the spirit of a supportive and close-knit team.
"""

prompt = prompt.format(name=name)
client = OpenAI()
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
)
image_url = response.data[0].url

# generate birthday wish
print("Generating birthday message...")
openai_api_key = os.environ.get("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in the environment variable OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key)

system = "You are birthday wish generator. You should generate a birthday wish for a birthday card."
user = """
Craft a birthday wish that conveys warmth and joy. 
The message should be concise, no more than four lines, and suitable for anyone. 
It should express heartfelt birthday greetings in a simple, yet touching manner, focusing on happiness and good wishes for the year ahead.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", user)
])

chain = prompt | llm 
wish = chain.invoke({'name': name}).content

# html page
print('Generate html page...')
with open('birthday_message_template.html', 'r', encoding='utf-8') as file:
    tmp = file.read()
tmp = tmp.replace('{{name}}', name)
tmp = tmp.replace('{{message}}', wish)
tmp = tmp.replace('{{image}}', image_url)

with open('birthday_card.html', 'w') as file:
    file.write(tmp)

print('Done')