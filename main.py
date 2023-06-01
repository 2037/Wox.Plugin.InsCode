# encoding=utf8

# utility module is credit to https://github.com/jianbing/wox-python-plugins
from util import WoxEx, WoxAPI, load_module, Log

# load modules
with load_module():
    import time
    import re
    import os
    import openai
    import requests
    from settings import *
    from inscode import InsCode
    import pyperclip

# only run once; setup numexpr to avoid warning by Wox
import os
if 'NUMEXPR_NUM_THREADS' not in os.environ:
    os.environ['NUMEXPR_MAX_THREADS'] = str(os.cpu_count())
    os.environ['NUMEXPR_NUM_THREADS'] = str(os.cpu_count())


class Main(WoxEx):
    # Get API key from system environment
    api_key = os.getenv("OPENAI_API_KEY")
    # ---initialize
    Bot = InsCode(api_key=api_key)

    def request(self, url):
        # If the user has configured the proxy, it can be set here.
        # self.proxy comes from a Wox encapsulated object
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))}
            return requests.get(url, proxies=proxies)
        else:
            return requests.get(url)

    def query(self, keyword):
        question = keyword
        results = list()
        results.append({
            'Title': 'Question to Openai',
            'SubTitle': 'Preset: {}; Your question: {}'.format(self.Bot.preset_selected, keyword),
            'IcoPath': 'Images/openai.png',
            'JsonRPCAction': {
                'method': 'openai_query',
                'parameters': [keyword],
                'dontHideAfterAction': False,
            }
        })
        return results

    def openai_query(self, keyword):
        answer = self.Bot.get_answer(question=keyword)
        pyperclip.copy(answer)

    # settings preset.json by user
    def open_preset(self):
        preset_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "presets.json")
        os.system("start "+preset_path)

    def reload_preset(self):
        self.Bot.reload_presets()


    def select_preset(self, preset_selected):
        self.Bot.set_preset(preset_selected)

    def show_preset_list(self):
        pass

    def open_openai_option(self):
        preset_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "preference.json")
        os.system("start "+preset_path)

    def context_menu(self, ctx_data):
        results = [
            {
                "Title": "Edit Preset Prompts",
                'JsonRPCAction': {
                    'method': 'open_preset',
                    'parameters': [],
                },
            },
            {
                "Title": "Edit Preference",
                'JsonRPCAction': {
                    'method': 'open_openai_option',
                    'parameters': [],
                },
            },
            {
                "Title": "Select preset prompts from below",
                'JsonRPCAction': {
                    'method': 'show_preset_list',
                    'parameters': [],
                },
            },
        ]
        preset_list = [
            {"Title": preset_title,
             'JsonRPCAction': {
                 'method': 'select_preset',
                 'parameters': [preset_title]
             }
             }
            for preset_title in self.Bot.presets
        ]
        results = results+preset_list
        return results


if __name__ == "__main__":
    Main()
