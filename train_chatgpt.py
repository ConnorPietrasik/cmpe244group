from openai import OpenAI
from time import sleep
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
# file_upload = client.files.create(
#     file=open("training_data.jsonl", "rb"), 
#     purpose="fine-tune"
# )

# while True:
#     file_handle = client.files.retrieve(id=file_upload.id)
#     if len(file_handle) and file_handle.status == "processed":
#         break
#     sleep(60)

job = client.fine_tuning.jobs.create(training_file="file-4YPEq7BJO128gq1284EnJQ4w", model="gpt-3.5-turbo")
print(f"Job created with id: {job.id}")