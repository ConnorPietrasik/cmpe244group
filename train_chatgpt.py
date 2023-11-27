from openai import OpenAI
from time import sleep
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
file_upload = client.File.create(file=open("training_data.jsonl", "rb"), purpose="fine-tune")

while True:
    file_handle = client.File.retrieve(id=file_upload.id)
    if len(file_handle) and file_handle.status == "processed":
        break
    sleep(60)

job = client.FineTuningJob.create(training_file=file_upload.id, model="gpt-3.5-turbo")
print(f"Job created with id: {job.id}")