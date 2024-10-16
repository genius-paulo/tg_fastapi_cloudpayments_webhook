# telegram-cloudpayments-webhook
A simple example of project on cloud payments, fastapi, aiogram, webhooks

## Quickstart
1. Install Dependencies
```
poetry install
```
2. Start ngrok
```shell
ngrok http 8000
```
3. Create .env file and set TOKEN, NGROK_URL, SKIP_UPDATES, and Cloud Paemtns credentials: CP_PUBLIC_ID and API_PASSWORD
4. Set up web hooks to the ngrok address in Cloud Payments
5. Start Uvicorn Server
```shell
uvicorn main:app --host localhost --port 8000
```
