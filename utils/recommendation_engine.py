import os
import openai
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan(age, weight, height, body_fat_percentage, gender, activity_level, goal):
    fitness_prompt = [
        {"role": "system", "content": "You are a fitness and diet assistant."},
        {"role": "user", "content": f"Generate a comprehensive fitness training and diet plan for a {age}-year-old {gender} with a weight of {weight}kg, height of {height}cm, body fat percentage of {body_fat_percentage}%, leading a {activity_level} lifestyle, aiming to {goal}."}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=fitness_prompt
    )
    
    return response.choices[0].message['content']

