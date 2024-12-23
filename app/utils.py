import PyPDF2
from openai import OpenAI
from pgvector.django import L2Distance

from app.models import PDFEmbedding


def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


def generate_embeddings(text, model="text-embedding-ada-002"):
    client = OpenAI()
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    del client
    return response.data[0].embedding


def query_chatbot(query, user):
    client = OpenAI()
    try:
        query_embedding = generate_embeddings(query)
        results = PDFEmbedding.objects.filter(user=user).order_by(
            L2Distance("embedding", query_embedding)
        )[:2]
        result_texts = [result.text for result in results]

        context = "\n".join(result_texts)

        # Create a prompt for OpenAI LLM (e.g., GPT-4 or GPT-3.5)
        prompt = (
            f"Here are some relevant documents\n{context}\n\n"
            "Please answer the following question based on the documents: {query}"
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        response = completion.choices[0].message
        message_content = str(response.content)
        del client
        return message_content
    except Exception as e:
        return f"Error is {str(e)}"
