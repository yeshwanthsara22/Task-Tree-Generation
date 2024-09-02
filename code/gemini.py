import os
import PIL
import google.generativeai as genai
import json
from pathlib import Path
# do not reveal your api key when submitting the assignment
GOOGLE_API_KEY=""
genai.configure(api_key=GOOGLE_API_KEY)


def list_genai_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
def is_valid_json(my_str):
    try:
        json.loads(my_str)
        return True
    except ValueError:
        return False

def read_file_as_string(filename):
  with open(filename, "r") as f:
    content = f.read()
  return content
def read_file_as_json(filename):
  with open(filename, "r") as f:
    content = json.load(f)
  return content


def detect_object(model, dish,ingredients):
    
    
    prompt=read_file_as_string("/Users/yeshwanth/Documents/DL/project3/project3-starter-code/prompt.txt")
    kitchen=read_file_as_string("kitchen.txt")
    prompt=prompt.replace("<kitchen>",",".join(kitchen.split("\n")))
    prompt=prompt.replace("[name of the dish]",dish)
    prompt=prompt.replace("[list of ingredients]",",".join(ingredients))
    c=0
    while(True):
      try:
        response = model.generate_content(prompt).text
        a=response.find("[")
        b=response.rfind("]")
        response=response[a:b+1]
        c=c+1
        print(c)
        response= '\n'.join(line for line in response.split('\n') if not line.strip().startswith('//'))
        if response!="":
          if response.count("[")==response.count("]"):
            if is_valid_json(response):
              return response
            # else:
              # print("json false",response)
        #   else:
        #     print("[] false",response)
        # else:
        #   print("empty")
            
      except Exception as t:
        pass
    # print(response.text)
    return response.text
if __name__ == "__main__":
  list_genai_models()
  model = genai.GenerativeModel('gemini-1.5-pro-latest')
  # Read ingredients from input.json
  data = read_file_as_json("/Users/yeshwanth/Documents/DL/project3/project3-starter-code/input.json")
  
  l=[]
  output="output"
  if not Path(output).exists():
    Path(output).mkdir(parents=True, exist_ok=True)
    # print("Folder created successfully.")
  # print(data)
  for i in data:
      output+="/"+i.get("category").replace(" ","_")
      for j in i['menu']:
          d={}
          dish_name=j['dish'].replace(" ","_")
          ingredients=j['ingredients']
          response=detect_object(model,dish_name ,ingredients)
          # print(response)
          # response=eval(response)
          # pretty_printed_json = json.dumps(response, indent=4)
          # print(pretty_printed_json)
          
          
          if not Path(output).exists():
            Path(output).mkdir(parents=True, exist_ok=True)
          print(output+"/"+dish_name+".json")
          # response=json.loads(response)
          with open(output+"/"+dish_name+".json", 'w') as file:
            # json.dump(response,file,indent=4)
              for i in response:
                  file.write(i)
      output="output"
      
