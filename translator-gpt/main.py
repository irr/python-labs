from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import sys

WINDOW = 99

def translate(content):
    translated_text = ""

    llm = OpenAI(temperature=0, model='text-davinci-003')

    template = """
    Translate the following text to portuguese keeping the subtitle format:
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
        response = chain.run(chunk)
        translated_text += f"{response}\n"
        
    return translated_text


if __name__ == '__main__':
    if len(sys.argv) > 0:
        with open(sys.argv[1], encoding='utf-8-sig') as file:
            content = file.readlines()
        translated_text = translate(content)
        print(translated_text)
    else:
        print("usage: main.py <file to translate>")
