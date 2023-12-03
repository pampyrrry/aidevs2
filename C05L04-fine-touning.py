from openai import OpenAI

gptapi = "__your_api_key__"
client = OpenAI(api_key=gptapi)


#step1 - to najlepiej wykonac cURL'em.

#openai.api_key = gptapi

#
#client.files.create(
#  file=open("C05L04-data_to-fine_tuning", "rb"),
#  purpose="fine-tune")
#

#step2
client.fine_tuning.jobs.create(
  training_file="name_of_file_-response_from_step1",
  model="gpt-3.5-turbo"
)

print(client)
