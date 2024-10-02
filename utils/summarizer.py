from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client(key, endpoint):
    ta_credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return client

def summarize_text(client, documents):
    try:
        response = client.begin_extract_summary(documents=documents, max_sentence_count=5)
        summaries = []
        for doc in response:
            if not doc.is_error:
                summary = ' '.join([sentence.text for sentence in doc.sentences])
                summaries.append(summary)
            else:
                summaries.append(f"Error: {doc.error.message}")
        return summaries
    except Exception as err:
        print(f"Encountered exception: {err}")
        return ["An error occurred during summarization."]
