# import json
import os
import openai
import re
import pyperclip
from settings import *
import requests


class InsCode:
    def __init__(self, api_key=None):
        if not api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")
        else:
            self.api_key = api_key
        openai.api_key = self.api_key

        with open('preference.json', 'r') as f:
            self.preference = json.load(f)
            self.preset_selected = self.preference["preset_selected"]
            self.model = self.preference["model"]
            self.is_keepitshort = self.preference["is_keepitshort"]
            self.max_tokens = self.preference["max_tokens"]
        self.presets = load_prompts()
        self.is_clipboard = True
        
        # test mode
        self.is_fakeanswer = False 

    # store preference as file since Wox terminate process after window closed
    def set_preset(self, preset):
        self.preset_selected = preset
        self.preference["preset_selected"] = preset
        with open('preference.json', 'w+') as f:
            json.dump(self.preference, f,sort_keys=True,indent=4)

    def reload_presets(self):
        self.presets = load_prompts()

    def response_fn(self, question, preset=None, model=None):
        if not preset:
            preset = self.preset_selected
        if not model:
            model = self.model

        preset_dict = self.presets.get(preset)
        if not self.is_keepitshort:
            content = preset_dict["content"]
            content = re.sub(
                r"(Remember do not include any explanations in your responses.)", "", content)
            preset_dict["content"] = content

        return_info = openai.ChatCompletion.create(
            model=model,
            max_tokens=self.max_tokens,
            messages=[preset_dict, {"role": "user", "content": question}]
        )
        return return_info

    def get_answer(self, question, **kwargs):
        # only return first codeblock, return original if failed
        if self.is_fakeanswer:
            return "This is a fake answer. \n"

        def extract_code(s):
            try:
                pos = re.search(r"(```.*\n)", s)
                poss = pos.end()
                pos2 = re.search(r"(```)", s[poss:])
                pose = pos2.start()
                return s[poss:poss+pose]
            except:
                return s

        answer_raw = self.response_fn(
            question, **kwargs)["choices"][0]["message"]['content']

        if self.is_keepitshort:
            answer = extract_code(answer_raw)
        else:
            answer = answer_raw
        if self.is_clipboard:
            pyperclip.copy(answer)
        return answer

    def test(self, question, preset_name=None, **kwargs):
        # test all
        if not preset_name:
            for key, value in self.presets.items():
                answer = self.get_answer(question=question, preset=key)
                print(key, value, "\n", answer, "\n")
        # test specific prompt
        else:
            answer = self.get_answer(question=question,
                                     preset=preset_name, **kwargs)
            print(preset_name, self.presets[preset_name], "\n", answer, "\n")



if __name__ == "__main__":
    import sys
    Bot = InsCode()
    # query mode
    # python inscode.py "your question"
    # Usage: subprocess.Popen(["python", "inscode.py", "query"])
    if len(sys.argv) > 1:
        if sys.argv[1]=="query":
            while True:
                question = sys.stdin.readline().strip()
                if not question:
                    break
                answer = Bot.get_answer(question)
                print("Received question: ", question)
                print("Get answer: ", answer)

    # interactive mode
    # python inscode.py
    else:
        import time
        start_time = time.time()
        while True:
            time_pass = time.time() - start_time
            if time_pass > 300: # 5 minutes
                break
            question = input("Enter your question: (Type quit/q to quit)\n")
            # question = input()
            print(Bot.get_answer(question))
            # print("Time pass: %d sec" % time_pass) 
            if question == "quit" or question=="q": # Exit loop if user enters "quit"
                break