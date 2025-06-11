from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template = (
    "Extract the specific information from this text: {dom_content}\n"
    "Follow these rules:\n"
    "1. Only output what matches the description: {parse_description}\n"
    "2. No extra text or comments.\n"
    "3. If nothing matches, output empty string.\n"
)


model = OllamaLLM(model="llama3:8b", max_tokens=512, temperature=0.3)

def chunk_text(text, max_length=1000):
    """
    Metni kelime bazında max_length kelime olacak şekilde parçalara böler.
    """
    words = text.split()
    for i in range(0, len(words), max_length):
        yield " ".join(words[i:i+max_length])


def parse_with_ollama(cleaned_html, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    
    chunks = list(chunk_text(cleaned_html, max_length=1000))

    for i, chunk in enumerate(chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed chunk {i}/{len(chunks)}")
        parsed_results.append(response)

    
    return "\n".join(parsed_results)
