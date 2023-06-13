from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import sys
import time

WINDOW = 20

def translate(content):
    translated_text = ""

    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

    template = """
    Your are an expert on translating movie subtitles. Translate the following text to 
    portuguese keeping the subtitle format:
    {chunk}
    """

    prompt = PromptTemplate(
        input_variables=["chunk",],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    while len(content) > 0:
        chunk = []
        while len(content) > 0:
            line = content.pop(0)
            chunk.append(line)
            if line.strip().isnumeric():
                if len(chunk) > WINDOW:
                    content.insert(0, line)
                    chunk.pop()
                    break
        time.sleep(1)
        response = chain.run(''.join(chunk))
        translated_text += f"{response}\n"
        
    return translated_text


if __name__ == '__main__':
    if len(sys.argv) > 0:
        with open(sys.argv[1], encoding='utf-8-sig') as file:
            content = file.readlines()
        try:
            translated_text = translate(content)
            print(translated_text)
        except Exception as ex:
            print(ex)
    else:
        print("usage: main.py <file to translate>")
