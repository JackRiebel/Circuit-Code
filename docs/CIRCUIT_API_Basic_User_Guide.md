[Skip to main content](javascript:;)

[*](https://wwwin.cisco.com/)

[ SharePoint ](https://cisco.sharepoint.com/_layouts/15/sharepoint.aspx?&login_hint=jariebel@cisco.com)

* *

Jack Riebel (jariebel)

JR

Sign in

[ ](https://cisco.sharepoint.com/sites/CIRCUIT)

[CIRCUIT](https://cisco.sharepoint.com/sites/CIRCUIT)

[ Home ](https://cisco.sharepoint.com/sites/CIRCUIT/) [ Learn ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Learning-Resources.aspx) [ AI Agents ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/AI-Agents.aspx) [ Connectors ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/MCP-Connectors.aspx) [ API ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx) [ Data ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Data-in-CIRCUIT.aspx)

[Cisco Confidential Site](javascript:)

* Not following

** Share **

**

[*](https://cisco.sharepoint.com/sites/CIRCUIT)

[CIRCUIT](https://cisco.sharepoint.com/sites/CIRCUIT)

[ Home ](https://cisco.sharepoint.com/sites/CIRCUIT/) [ Learn ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Learning-Resources.aspx) [ AI Agents ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/AI-Agents.aspx) [ Connectors ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/MCP-Connectors.aspx) [ API ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx) [ Data ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Data-in-CIRCUIT.aspx)

CIRCUIT API Basic User Guide

-

## Overview
[ *](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#overview)

Welcome to the Cisco CIRCUIT API Basic User Guide. This platform provides access to advanced Generative AI capabilities, enabling general chat completions using various Large Language Models (LLMs).

Whether you're looking to integrate AI-powered Q&A into your applications or leverage state-of-the-art chat models, this guide will walk you through the necessary steps from obtaining access to making your first API calls.

Kindly complete the [API Request Form](https://go2.cisco.com/circuit-api) to begin your request for access to the service.

[Requesting an AppKey](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#2.-getting-started) | [Generating an Access Token](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#3.-authentication-api-keys) | [API Reference](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#4.-chat-completions-api-reference) | [Supported Models](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#5.-supported-models-api-versions) | [Code Snippets](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#6.-code-examples-%28python%29) | [Questions and Support](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#have-questions-or-need-support)

## 2. Getting Started
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#2.-getting-started)

To begin using the CIRCUIT API, you will need an `appkey` for identifying your application.

**

### 2.1 Requesting an AppKey
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#2.1-requesting-an-appkey)

An `appkey` is a **REQUIRED** element for all API interactions and helps distinguish your application's chat sessions.

1. **Access the CIRCUIT API Portal**: Navigate to the API request form on the [CIRCUIT API Portal](https://go2.cisco.com/circuit-api). Ensure you are connected to the Cisco VPN to access the site.

2. **Request New Key**: Use the "Request New Key" option.

-

Draft Feature: Allows intermediate saving before final submission.
-

Approval Timeline: Approval typically takes a few days.
- Tier Selection: Choose between "Free Tier" and "Paid Tier".
- Paid Tier: Requires additional justification fields, including an email from a Financial Analyst in your reporting chain confirming approval for usage costs. Refer to the [CIRCUIT API Portal](https://go2.cisco.com/circuit-api) for monthly input and completion token pricing.

3. **Manage Your AppKey** (Portal Options):

-

View: See full key details (Client Secret is masked but can be revealed).
- Edit: Update certain key information or upgrade from Free to Paid Tier.
- Test it out: Generate an API token via a GUI for testing purposes.
- Usage Details: View appkey usage statistics (prompt, completion, total tokens) by month, week, or minute per model.

## **3. Authentication & API Keys**
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#3.-authentication-api-keys)

Access to the CIRCUIT API requires an access token (also referred to as an `api-key` or `token`), which is obtained via the OAuth2 authentication flow using your Okta credentials (`client_id` and `client_secret`). This token is valid for one hour and must be refreshed periodically.

Here are several methods to generate your access token:

**

### 3.1 Via CIRCUIT API Portal
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#3.1-via-circuit-api-portal)

1. Click the "Test it out" button next to your desired `AppKey` in the [CIRCUIT API Keys Portal](https://ai-chat.cisco.com/bridgeit-platform/home).

*

2. Click "Generate Access Token." Your Client ID and Client Secret will be displayed.

3. Upon success, a message "Access token generated successfully. The generated access token will be valid for one hour" will appear. You can copy the token or download it.

4. Optionally, click "Next" to explore the Chat Completion API directly within the portal. You can choose a model from the dropdown and enter in a sample prompt, and click “Test” to get a prompt response.

*

### 3.2 Via cURL Request (Linux/Windows)
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#3.2-via-curl-request-(linux-windows))

You will need your `client_id` and `client_secret` (your Okta credentials):

**Method 1: Using Base64 Encoding**

First, encode your `client_id` and `client_secret` into a Base64 string:

* # Linux Example *

* client_id=<your client id> *

* client_secret=<your client secret> *

* base64_value=$(echo -n "${client_id}:${client_secret}" | base64) *

* echo “$base64_value” *

Then, use the Base64 value in your cURL request:

* curl --location --request POST 'https://id.cisco.com/oauth2/default/v1/token' \ *
* --header 'Accept: */*' \ *
* --header 'Content-Type: application/x-www-form-urlencoded' \ *
* --header "Authorization: Basic ${base64_value}" \ *
* --data-urlencode ‘grant_type=client_credentials’ *

**Method 2: Using cURL Basic Auth Shorthand (-u)**

This method directly passes the `client_id` and `client_secret` without manual Base64 encoding.

* **# Linux Example** *
* **client_id=<your client id>** *
* **client_secret=<your client secret>** *

* **curl -X POST "https://id.cisco.com/oauth2/default/v1/token" \** *
* **-d "grant_type=client_credentials" \** *
* **-u "$client_id:$client_secret" \** *
* **-H "Content-Type: application/x-www-form-urlencoded" \** *
* **-H "Accept: */*"** *

* **# Windows Example** *
* **set client_id=<your client id>** *
* **set client_secret=<your client secret>** *

* **curl -X POST "https://id.cisco.com/oauth2/default/v1/token" ^** *
* **-d "grant_type=client_credentials" ^** *
* **-u "%client_id%:%client_secret%" ^** *
* **-H "Content-Type: application/x-www-form-urlencoded" ^** *
* **-H “Accept: */*”** *

**

### 3.3 Via Postman
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#3.3-via-postman)

-

Method: `POST`
-

URL: `https://id.cisco.com/oauth2/default/v1/token`
-

Authorization Tab:

-

Type: Basic Auth
-

Username: Your `client_id`
-

Password: Your `client_secret`

-

Headers:

-

`Content-Type`: `application/x-www-form-urlencoded`
-

`Accept`: `*/*`

-

Body (x-www-form-urlencoded):

-

`grant_type`: `client_credentials`

-

Click "Send" to receive the `access_token` in the JSON response.

*

*

### 3.4 Via Python Requests Program
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#3.4-via-python-requests-program)

* **import requests** *
* **import base64** *
* **import os** *
* **from dotenv import load_dotenv** *

* **load_dotenv() # Loads client_id and client_secret from .env file** *

* **client_id = os.environ.get('BRIDGE_API_CLIENT_ID') # Or your specific env var name** *
* **client_secret = os.environ.get('BRIDGE_API_CLIENT_SECRET') # Or your specific env var name** *

* **url = "https://id.cisco.com/oauth2/default/v1/token"** *
* **payload = "grant_type=client_credentials"** *
* **value = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')** *

* **headers = {** *
* ** "Accept": "*/*",** *
* ** "Content-Type": "application/x-www-form-urlencoded",** *
* ** "Authorization": f"Basic {value}"** *
* **}** *

* **response = requests.post(url, headers=headers, data=payload)** *
* **response.raise_for_status() # Raise an exception for HTTP errors** *
* **token_data = response.json()** *
* **api_key = token_data.get('access_token')** *

* **print("Access Token:", api_key)** *

## 4. Chat Completions API Reference
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#4.-chat-completions-api-reference)

The CIRCUIT API offers functionalities for general chat completions.

This API allows you to interact with various LLMs for generating chat responses.

**• Endpoint:** https://chat-ai.cisco.com/openai/deployments/<model name>/chat/completions

**

### 4.1 Request Parameters
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#4.1-request-parameters)

**Parameter** **Type** **Description** messages Array An array of message objects, each with a role ("user" or "assistant") and content. user String A JSON string containing your appkey (required), and optional session_id (for conversational history) and user (Cisco CEC ID). stop Array An array used to specify stop sequences for chat completion (e.g., `["< api-key Header Your access_token obtained through the authentication process.

**

### 4.2 cURL Example for Chat Completion
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#4.2-curl-example-for-chat-completion)

**access_token=<your_access_token>**

**appkey=<your_app_key>**

**model_name=gpt-4o-mini # Example model**

**curl --location 'https://chat-ai.cisco.com/openai/deployments/'"${model_name}"'/chat/completions' \**

**--request POST \**

**--header 'Content-Type: application/json' \**

**--header 'Accept: application/json' \**

**--header "api-key: ${access_token}" \**

**--data '{**

** "messages": [**

** {**

** "role": "system",**

** "content": "You are a chatbot"**

** },**

** {**

** "role": "user",**

** "content": "What is the capital of France?"**

** }**

** ],**

** "user": "{\"appkey\":\"'"${appkey}"'\"}",**

** "stop": ["<|im_end|>"]**

**}'**

**

### 4.3 Postman Example for Chat Completion
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#4.3-postman-example-for-chat-completion)

- **Method:** POST
- **URL:** https://chat-ai.cisco.com/openai/deployments/{MODEL_NAME}/chat/completions?api-version=2025-04-01-preview
- **Authorization Tab:**

- **Type:** API Key
- **Key:** api-key
- **Value:** Your access_token
- **Add to:** Header

- **Headers:**

- Content-Type: application/json

-

**Body (raw - JSON):** * **{** *
* ** "user": "{\"appkey\": \"<your_app_key>\"}",** *
* ** "messages": [** *
* ** {"role": "system", "content": "You are a helpful assistant."},** *
* ** {"role": "user", "content": "What is the capital of France?"}** *
* ** ]** *
* **}** *
- Click “Send.”

*

## 5. Supported Models & API Versions
[ *](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#5.-supported-models-api-versions)

The list of supported models is continually updated. Please reference [this page](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx#basic-api-tiers) under basic API tiers for an up-to-date list.

**

### 5.1 Basic API Tiers Table
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#5.1-basic-api-tiers-table)

**Model Name**

**API Version**

**Context Windows**

**Available in Free Tier (**[**Restrictions Apply**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx#basic-api-tiers)**)**

**gpt-4.1**

**2025-04-01-preview**

**120K Tokens (Free Tier)**

**1M Tokens - Pay-as-you-use-tier**

**Yes**

**gpt-4o-mini**

**2025-04-01-preview**

**120K Tokens**

**Yes**

**gpt-4o**

**2025-04-01-preview**

**120K Tokens**

**Yes**

o4-mini

2025-04-01-preview

200k Tokens

No

o3

2025-04-01-preview

200k Tokens

No

gemini-2.5-flash

2025-04-01-preview

1M Tokens

No

gemini-2.5-pro

2025-04-01-preview

1M Tokens

No gpt-5 2025-04-01-preview 270k Tokens

No gpt-5 chat 2025-04-01-preview 120k Tokens

No gpt-5-mini 2025-04-01-preview 1M Tokens

No gpt-5-nano 2025-04-01-preview 1M Tokens

No

gpt-4.1-mini

2025-04-01-preview

1M Tokens

No

claude-sonnet-4-5

2025-04-01-preview

1M Tokens

No

claude-sonnet-4

2025-04-01-preview

1M Tokens

No

claude-opus-4-1

2025-04-01-preview

200k Tokens

No

claude-opus-4-5

2025-04-01-preview

200k Tokens

No

claude-haiku-4-5

2025-04-01-preview

200k Tokens

No

***Note**: The following models are deprecated and no longer available: gpt-4, gpt-35-turbo, gpt-35-turbo-16k*

## 6. Code Examples (Python)
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#6.-code-examples-(python))

These are extra snippets of code that may be of use for uploading a file to GCS, publishing metadata to Pub/Sub, using the requests library, and other useful information.

**

### 6.1 Chat Completions (Python Requests Library)
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#6.1-chat-completions-(python-requests-library))

This example demonstrates an interactive chat session using the *requests *library:

**import json**
**import os**
**import requests**
**from dotenv import load_dotenv**

**load_dotenv(override=True) # Load env vars, .env takes precedence**

**APPKEY = os.getenv("BRIDGE_API_APP_KEY")**
**api_key = os.getenv("AZURE_OPENAI_API_KEY") # This is your access token**

**MODEL_NAME = "gpt-4o"**
**API_URL = f"https://chat-ai.cisco.com/openai/deployments/{MODEL_NAME}/chat/completions?api-version=2025-04-01-preview"**

**def chat_with_circuit():**
** print("Cisco CircuIT GPT Chatbot (type 'exit' to quit)")**
** messages = [{"role": "system", "content": "You are a helpful assistant."}]**
** headers = {**
** 'Content-Type': 'application/json',**
** 'api-key': api_key**
** }**

** while True:**
** user_input = input("You: ")**
** if user_input.lower() in {"exit", "quit"}:**
** break**

** messages.append({"role": "user", "content": user_input})**

** payload = {**
** "user": json.dumps({"appkey": APPKEY}),**
** "messages": messages**
** }**

** try:**
** response = requests.post(API_URL, json=payload, headers=headers)**
** response.raise_for_status()**
** data = response.json()**
** reply = data["choices"]["message"]["content"]**
** messages.append({"role": "assistant", "content": reply})**
** print("AI:", reply.strip())**

** except requests.exceptions.HTTPError as e:**
** print("API request error:", e)**
** print("Status code:", e.response.status_code)**
** print("Response content:", e.response.text)**
** except requests.exceptions.RequestException as e:**
** print("API request error:", e)**
** break**
** except (KeyError, IndexError) as e:**
** print("Unexpected response format:", e)**
** break**

**if __name__ == "__main__":**
** chat_with_circuit()**

**

### 6.2 Chat Completions (AzureOpenAI Library)
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#6.2-chat-completions-(azureopenai-library))

When using Azure, this uses the OpenAI Python SDK specifically for Azure-hosted models:

**import os**
**from openai import AzureOpenAI**
**from dotenv import load_dotenv**

**load_dotenv()**
**appkey = os.getenv("BRIDGE_API_APP_KEY")**
**access_token = os.getenv("AZURE_OPENAI_API_KEY") # Your access token**

**client = AzureOpenAI(**
** azure_endpoint = 'https://chat-ai.cisco.com/',**
** api_key = access_token, # Can also be set via AZURE_OPENAI_API_KEY env var**
** api_version="2025-04-01-preview", # Can also be set via OPENAI_API_VERSION env var**
**)**
**messages = [**
** {"role": "system", "content": "You are a helpful assistant."}**
**]**

**user_input = input("You: ")**
**messages.append({"role": "user", "content": user_input})**

**response = client.chat.completions.create(**
** model="gpt-4o", # Model name**
** messages = messages,**
** temperature = 0,**
** user=f'{{"appkey": "{appkey}", "user": "ddamerji@cisco.com"}}' # Optional user ID**
**)**

**print(response.choices.message.content)**

**

### 6.3 Chat Completions (AzureChatOpenAI / LangChain) Wrapper

[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#6.3-chat-completions-(azurechatopenai-langchain)-wrapper)

This LangChain wrapper provides a tailored experience for conversational AI applications:

* **from langchain_openai import AzureChatOpenAI** *
* **from langchain.schema import HumanMessage, SystemMessage** *
* **import os** *
* **from dotenv import load_dotenv** *

* **load_dotenv()** *
* **app_key = os.getenv("BRIDGE_API_APP_KEY")** *
* **userid = os.getenv("CISCO_BRAIN_USER_ID") # Your Cisco CEC ID** *
* **access_token = os.getenv("AZURE_OPENAI_API_KEY") # Your access token** *

* **model = AzureChatOpenAI(** *
* ** model="gpt-4.1", # Model name** *
* ** azure_endpoint = 'https://chat-ai.cisco.com',** *
* ** api_version="2024-12-01-preview",** *
* ** openai_api_key=access_token, # Pass the access token** *
* ** model_kwargs=dict(** *
* ** user = f'{{"appkey": "{app_key}", "user": "{userid}"}}'** *
* ** )** *
* **)** *

* **msgs = [** *
* ** SystemMessage(content="You are a helpful assistant."),** *
* ** HumanMessage(content="Translate to French: Hello, how are you?")** *
* **]** *

* **print (model.invoke(msgs)) # Recommended approach** *
* **print (model.invoke("Tell me who is the president of USA for 2024"))** *

### Have questions or need support?
[**](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/Basic-Api-Guide.aspx#have-questions-or-need-support)

Contact the [ CIRCUIT API Support Webex space ](https://eurl.io/#2PnHT3YSf) and visit [ our full FAQ ](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/FAQs.aspx).

** Like

** 2530 Views

** Save for later

Contact us

Terms of use

Privacy Policy

Legal

Site map

CIRCUIT

...

2.1 Requesting an AppKey section expanded

3.1 Via CIRCUIT API Portal section expanded

3.2 Via cURL Request (Linux/Windows) section expanded

3.3 Via Postman section expanded

3.4 Via Python Requests Program section expanded

4.1 Request Parameters section expanded

4.2 cURL Example for Chat Completion section expanded

4.3 Postman Example for Chat Completion section expanded

5.1 Basic API Tiers Table section expanded

6.1 Chat Completions (Python Requests Library) section expanded

6.2 Chat Completions (AzureOpenAI Library) section expanded

6.3 Chat Completions (AzureChatOpenAI / LangChain) Wrapper
section expanded

Currently not following the site, click to follow

CIRCUIT