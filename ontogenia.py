from llama_index.core import PromptTemplate
from rdflib import Graph

from create_cqs import get_llamaindex_gemini, prompt_llm

import datetime


def read_procedure(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def prompt_format(procedure_str: str, CQs: str) -> str:
    template  = ("Read the following instructions: '{procedure}'. \n"
                 "Based on the procedure, design an ontology that comprehensively answers the following competency questions categorized by several titles.\n"
                 "---------------------\n"
                 "{CQs}"
                 "\n---------------------\n"
                 "Use the titles as a guide to design the ontology."
                 "Do not repeat classes, object properties, data properties, restrictions, etc. if they have been addressed in the previous output. \n"
                 "When you're done send me only the whole ontology you've designed in OWL format, without any comment outside the OWL.\n"
                 "Output should be a valid xml format, do not add any character.")


    qa_template = PromptTemplate(template)
    prompt = qa_template.format(procedure=procedure_str, CQs = CQs)
    return prompt


if __name__ == "__main__":
    # Reading the procedure and patterns from files
    filtered_list, thema_question_dict, full_str_with_titles = prompt_llm()

    procedure_content = read_procedure('./data/procedure.txt')
    full_prompt = prompt_format(procedure_content, full_str_with_titles)

    llm_gemini = get_llamaindex_gemini()

    out = llm_gemini.complete(full_prompt)
    outtext = out.text[7:-3]
    print(outtext)

    date_str = datetime.datetime.now().strftime("%Y%m%d")
    output_file_name = f"output_{1}_{date_str}_trial{1}.owl"

    output_path = "./" + output_file_name
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(outtext)

    # Validate the format
    g = Graph()
    g.parse(data=outtext, format='xml')

    # Save to file in different formats
    g.serialize('./owl_files/output.owl', format='xml')