import os
import openai
openai.api_type = "azure"
openai.api_base = "https://datastudio-uki-openai-dev.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "09149f0a2968470b802d1641dd723f63"

response = openai.Completion.create(
  engine="Deployment1",
  prompt="sky is\n",
  temperature=1,
  max_tokens=100,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)
 
 
