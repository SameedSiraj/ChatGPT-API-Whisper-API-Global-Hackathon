# -*- coding: utf-8 -*-
"""MyQuiz.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U5hcjxtwibHSiSPDbMaECHqtc9zC1AYp

#Quiz.AI: Experience the Trivia of Future

##**Install all Prerequisites**
"""

#Run this till it completes. Then refresh the page to make sure it is installed
!pip uninstall ffmpeg-python
!pip uninstall ffmpeg
!pip uninstall redis
!pip uninstall openai
!pip uninstall git+https://github.com/openai/whisper.git
!pip install git+https://github.com/openai/whisper.git
!pip install setuptools-rust
!pip install redis
!pip install openai
!pip install ffmpeg-python

"""
##**Driver Code**"""

#Import all Modules - DO NOT CHANGE
import whisper
import openai
import os
import random
import redis
import json

#Define Variables and API Keys - DO NOT CHANGE
model = whisper.load_model("base")
openai.api_key = "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"

num_questions = 0
correct_answers = 0
age = -1
topic = ""

#This Command asks the User his/her age

print("What is your Age? ")
'''ageDict = model.transcribe("age.m4a", fp16=False) #If you click on the folder icon located on the left side of google colaboratory, you will find the audio file 'age.m4a'. Now what I want you guys to do is upload your own recordings in their and chand the variable in this code to test if your recoding is getting converted Successfully.
age = ageDict["text"]'''
print("You are "+age+" Years old.")
while True:
  try:
    ageInt = int(input("Enter your age: "))
    if ageInt > 0:
      age=str(ageInt)
      break
    print("Invalid age entered")
  except Exception as e:
    print(e)

#This Command asks the User his/her topic
'''print("What Topic do you want the quiz to be on? ")
topicDict = model.transcribe("topic.m4a", fp16=False) #If you click on the folder icon located on the left side of google colaboratory, you will find the audio file 'Music.m4a'. Now what I want you guys to do is upload your own recordings in their and chand the variable in this code to test if your recoding is getting converted Successfully.
topic = topicDict["text"]'''
topic = input("What Topic do you want the quiz to be on? ")
print("You have chosen" + topic)

#This command asks the User how many questions do they want to answer - DO NOT CHANGE
#num_questions = int(input("How many questions would you like to Answer? "))
while True:
  try:
    num_questions = int(input("How many questions would you like to Answer? "))
    if num_questions > 0:
      break
    print("Invalid number entered")
  except Exception as e:
    print(e)

# Connect to Redis
r = redis.Redis(host='redis-14880.c15.us-east-1-2.ec2.cloud.redislabs.com', port=14880, password='b1elTNUSTLSw9MXQs3JIi3jAkV1EMrfh')

#This loop goes through the number of questions that a user wants - DO NOT CHANGE
for i in range(num_questions):
  #The following command asks the question to the user
  completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content": "Generate a random easy question that you have not asked before related to " +topic+" for a "+age+"-year-old which can be answered in one word. Don't provide the answer"}])
  question = completion.choices[0].message.content
  print(completion.choices[0].message.content)

  #The following command asks the user for an answer
  user_answer = input("Please provide me with your answer: ")

  #The following command verifies the answer with ChatGPT
  completionOne = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content": "Is "+user_answer+" a correct answer for the question: "+question+" Answer ONLY in True or False and be lenient. The answer need not be grammatically and fully correct"}])
  answer = completionOne.choices[0].message.content
  print(completionOne.choices[0].message.content)

  #The following Command checks and provides you with the score accordingly
  if (answer == 'True' or answer == 'True.'):
    correct_answers = correct_answers+1
    
  # Insert each object into Redis
  r.lpush('my_list', json.dumps({'Topic': topic, 'Age': age, 'Question': question, 'User Answer': user_answer, 'Correct Answer': answer}))

print("Hooray! You got " +str(correct_answers)+ " out of "+str(num_questions)+" answers right!")

"""**To Print Redis Database**"""

objects_from_redis = []
for i in range(r.llen('my_list')):
    obj = json.loads(r.lindex('my_list', i))
    objects_from_redis.append(obj)

print(objects_from_redis)

"""**To Refresh the Database**"""

r.flushall()