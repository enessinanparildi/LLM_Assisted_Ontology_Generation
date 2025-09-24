from typing import Any, LiteralString

from llama_parse import LlamaParse
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import PromptTemplate

llama_parse_api_key = ""
gemini_api_key_2 = ""


def get_raw_content() -> str:
    pdf_url = "./data/pdf_example.pdf"

    parser = LlamaParse(
        api_key=llama_parse_api_key,  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="text",  # "markdown" and "text" are available
        num_workers=4,  # if multiple files passed, split in `num_workers` API calls
        verbose=True,
        language="en",
    )
    parsed_documents = parser.load_data(pdf_url)
    parsed_documents.pop(4)

    merged_str = ''
    for documents in parsed_documents:
        merged_str = merged_str + "\n" + documents.text
    merged_str = merged_str.replace("R E P O R T |  M A N D I A N T APT41, A Dual Espionage and Cyber Crime Operation", " ")
    return merged_str



def get_llamaindex_gemini() -> GoogleGenAI:
    SAFE = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    max_tokens = 100000
    context_window = 10000
    llm_gemini = GoogleGenAI(model_name="models/gemini-2.5-pro", api_key=gemini_api_key_2,
                        temperature=0.01, safety_settings=SAFE)
    return llm_gemini

def prompt_llm() -> tuple[list[Any], dict[Any, Any], LiteralString | str | Any]:
    template = (
        "You are an expert in cybersecurity threat analysis and ontology construction.\n"
        "You have the following text describing a cybersecurity threat report: \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "I would like you to come up with a set of competency questions for the purpose of constructing an effective ontology for this threat report.\n"
        "Competency questions are user-oriented interrogatives that allow us to scope our ontology. In other words, they are questions that our users would want to gain answers for, through exploring and querying the ontology and its associated knowledge base."
    )

    merged_str = get_raw_content()
    qa_template = PromptTemplate(template)
    messages = qa_template.format(context_str=merged_str)

    llm_gemini = get_llamaindex_gemini()

    out = llm_gemini.complete(messages)
    output_text = out.text
    split_list = output_text.split("\n")
    filtered_list = []
    for item in split_list:
        if item != "":
            filtered_list.append(item)


    for i in range(len(filtered_list)):
        if filtered_list[i][0:2] != "**":
            filtered_list[i] = filtered_list[i][3:].strip()

    filtered_list.pop(0)
    filtered_list.pop(-1)

    for i in range(len(filtered_list)):
        filtered_list[i] = filtered_list[i].strip()

    full_str_with_titles = ""
    for item in filtered_list:
        full_str_with_titles = full_str_with_titles + "\n" + item

    thema_question_dict = dict()
    curr_key = None
    for i in range(len(filtered_list)):
        if filtered_list[i][0:2] == "**":
            thema_question_dict[filtered_list[i][2:-2]] = []
            curr_key = filtered_list[i][2:-2]

        if filtered_list[i][0:2] != "**" and curr_key is not None:
            thema_question_dict[curr_key].append(filtered_list[i])

    with open("cq_text_flash.txt", "w", encoding="utf-8") as f:
        f.write(full_str_with_titles)

    return filtered_list, thema_question_dict, full_str_with_titles







