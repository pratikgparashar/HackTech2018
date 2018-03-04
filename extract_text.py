import requests
import json

subscription_key = "c314cd02a604410c906666e552b8e8e1"
assert subscription_key

vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "ocr"

image_url = "http://4.bp.blogspot.com/-7KQPc9gtWTE/Wl5njfz-uuI/AAAAAAAAs8k/c7VJE_PeEzokF7aEcS-VHfT6m76ngi0DgCK4BGAYYCw/s1600/Margaret%2BCarrasco-730821.jpg"

headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
data     = {'url': image_url}
params   = {'language': 'unk', 'detectOrientation ': 'true'}
response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
response.raise_for_status()
analysis = response.json()
line_infos = [region["lines"] for region in analysis["regions"]]
word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
        	word_infos.append(word_info)
#final_sentence=""
for each in word_infos:
	final_sentence+=each["text"]+" "
print(final_sentence)

subscription_key="5d162a1f02724f6daf4489f4220413a4"
assert subscription_key
text_analytics_base_url="https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
key_phrase_api_url = text_analytics_base_url+"keyPhrases"
sentiment_api_url = text_analytics_base_url + "sentiment"

documents={'documents': [{'id': '1', 'text':'victim harassed by person with knife'}]}
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
key_phrases = response.json()
print(key_phrases['documents'][0]['keyPhrases'])
response  = requests.post(sentiment_api_url, headers=headers, json=documents)
key_phrases = response.json()
print(key_phrases['documents'][0]['score'])
