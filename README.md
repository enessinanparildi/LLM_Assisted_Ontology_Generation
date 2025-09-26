# LLM_Assisted_Ontology_Generation

An automated pipeline for generating domain-specific ontologies from PDF documents using Large Language Models and the Ontogenia methodology. For the competency question (CQ) generation component, we referred to "A RAG Approach for Generating Competency Questions in Ontology Engineering. (Pan et al., 2024)". In addition, we drew on the work presented in "Ontogenia: Ontology generation with metacognitive prompting in large language models." (Lippolis et al., 2024), which outlines an effective prompting strategy called Ontogenia for ontology construction.

This project is still in its early stages. More comprehensive ontology evaluation metrics are required to validate the proposed methodology. Moreover, the methodology needs to be tested on a larger set of raw text instances.

## Overview

This project transforms unstructured PDF content into structured OWL ontologies through a multi-stage process:

1. **PDF Parsing**: Extracts raw text from PDF documents using LlamaParse
2. **Competency Question Generation**: Creates domain-specific questions using Google's Gemini LLM
3. **Ontology Generation**: Builds OWL ontologies using the Ontogenia prompting methodology
4. **Validation & Visualization**: Validates the generated ontology and creates visual representations

## Features

- **Automated PDF Processing**: Parse complex PDF documents with high accuracy
- **Intelligent Question Generation**: Generate competency questions tailored to cybersecurity threat reports
- **Ontogenia Methodology**: Leverage proven ontology construction techniques
- **OWL Format Output**: Generate standard Web Ontology Language files
- **Validation Pipeline**: Ensure ontology correctness with SHACL validation
- **Visual Representation**: Create GraphViz diagrams of the ontology structure

## Requirements

### Python Dependencies

```
llama-parse
llama-index
google-generativeai
rdflib
owlready2
pyshacl
graphviz
```

### API Keys Required

- **LlamaParse API Key**: For PDF parsing capabilities
- **Google Gemini API Key**: For LLM-powered question and ontology generation

##  Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd llm-ontology-generation
   ```

2. **Install dependencies**:
   ```bash
   pip install llama-parse llama-index google-generativeai rdflib owlready2 pyshacl graphviz
   ```

3. **Set up API keys**:
   ```python
   # In create_cqs.py
   llama_parse_api_key = "your_llama_parse_api_key"
   gemini_api_key_2 = "your_gemini_api_key"
   ```

4. **Prepare directory structure**:
   ```
   project/
   ├── data/
   │   ├── pdf_example.pdf
   │   └── procedure.txt
   ├── owl_files/
   └── scripts/
   ```

## Usage

### Basic Workflow

1. **Place your PDF** in the `./data/` directory as `pdf_example.pdf`

2. **Generate Competency Questions**:
   ```python
   from create_cqs import prompt_llm
   
   filtered_list, thema_question_dict, full_str_with_titles = prompt_llm()
   ```

3. **Generate Ontology**:
   ```python
   python ontogenia.py
   ```

4. **Validate and Visualize**:
   ```python
   python run_validation.py
   ```

### Advanced Configuration

#### Customizing LLM Parameters

```python
# In create_cqs.py - get_llamaindex_gemini()
llm_gemini = GoogleGenAI(
    model_name="models/gemini-2.5-pro",
    api_key=gemini_api_key_2,
    temperature=0.01,  # Adjust for creativity vs consistency
    safety_settings=SAFE
)
```

#### Modifying Competency Question Templates

The competency question generation uses a structured prompt template that can be customized in `create_cqs.py`:

```python
template = (
    "You are an expert in cybersecurity threat analysis and ontology construction.\n"
    "You have the following text describing a cybersecurity threat report: \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "I would like you to come up with a set of competency questions..."
)
```

## Project Structure

```
├── create_cqs.py          # Competency question generation
├── ontogenia.py           # Main ontology generation pipeline  
├── run_validation.py      # Validation and visualization
├── data/
│   ├── pdf_example.pdf    # Input PDF document
│   └── procedure.txt      # Ontogenia methodology instructions
├── owl_files/
│   └── output.owl         # Generated ontology files
└── README.md
```

## Core Components

### 1. PDF Processing (`create_cqs.py`)

- **Function**: `get_raw_content()`
- **Purpose**: Extracts and cleans text from PDF documents
- **Output**: Merged string of document content

### 2. Competency Question Generation (`create_cqs.py`)

- **Function**: `prompt_llm()`
- **Purpose**: Generates domain-specific questions for ontology scoping
- **Output**: Categorized questions dictionary and formatted strings

### 3. Ontology Generation (`ontogenia.py`)

- **Function**: Main execution pipeline
- **Purpose**: Creates OWL ontology using Ontogenia methodology
- **Output**: Valid OWL/XML formatted ontology file

### 4. Validation & Visualization (`run_validation.py`)

- **Functions**: `create_graphviz_file()`, validation pipeline
- **Purpose**: Ensures ontology validity and creates visual representations
- **Output**: GraphViz diagrams and validation reports

## Output Examples

### Generated Competency Questions

```
**Threat Actor Identification**
1. What threat groups are associated with APT41?
2. What are the primary motivations behind APT41 operations?

**Attack Techniques**
1. What attack vectors does APT41 commonly employ?
2. What tools and malware are used by APT41?
```

### OWL Ontology Structure

```xml
<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:owl="http://www.w3.org/2002/07/owl#">
    
    <owl:Class rdf:about="#ThreatActor"/>
    <owl:Class rdf:about="#AttackTechnique"/>
    <owl:ObjectProperty rdf:about="#uses"/>
    
</rdf:RDF>
```

## ⚙️ Configuration

### Safety Settings

The project includes comprehensive safety settings for the Gemini API:

```python
SAFE = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    # ... additional safety configurations
]
```
## Validation

The system includes multiple validation layers:

1. **XML Format Validation**: Ensures proper OWL/XML structure
2. **RDFLib Parsing**: Validates RDF graph construction  
3. **SHACL Validation**: Checks ontology constraints and consistency
4. **Ontology Statistics**: Reports classes, properties, and individuals countle for details.

## Acknowledgments

- **LlamaParse**: For robust PDF parsing capabilities
- **Google Gemini**: For advanced language model integration
- **Ontogenia Methodology**: For systematic ontology construction approach
- **OWL/RDF Standards**: For semantic web compatibility

## Roadmap

- Interactive ontology editing interface
- Export to different ontology formats (TTL, N3, etc.)
- Integration with ontology repositories

---
## Citations
- Pan, Xueli, et al. "A rag approach for generating competency questions in ontology engineering." Research Conference on Metadata and Semantics Research. Cham: Springer Nature Switzerland, 2024.
- Lippolis, Anna Sofia, et al. "Ontogenia: Ontology generation with metacognitive prompting in large language models." European Semantic Web Conference. Cham: Springer Nature Switzerland, 2024.




