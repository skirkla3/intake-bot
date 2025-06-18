# Deploy FastAPI on Render
# Intake Bot

Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.
This project contains a small FastAPI service that handles Twilio voice calls and records caller information using AI. It can optionally use Relevance AI for call analysis, look up customer data from a public API, and log results to a CRM. Deploy the service on [Render](https://render.com) or any container platform.

See https://render.com/docs/deploy-fastapi or follow the steps below:
## Deploy to Render

## Manual Steps
1. Create a new **Web Service** on Render and point it to this repository.
2. Render installs dependencies from `requirements.txt` automatically.
3. Set the **Start Command** to:

1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
2. Create a new Web Service on Render.
3. Specify the URL to your new repository or this repository.
4. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
5. Specify the following as the Start Command.
```bash
uvicorn server:app --host 0.0.0.0 --port $PORT
```

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
4. Add the required environment variables under the **Environment** tab.
5. Deploy the service and point your Twilio phone number webhook to `https://YOUR-SERVICE.onrender.com/incoming`.

6. Click Create Web Service.
## Environment Variables

Or simply click:
Create a `.env` file (not committed) with at least the following keys and their values:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)
```
OPENAI_API_KEY=-svcacct-LZ2p9TGRYrbs17FPsnnjmyG1Wm-HuJtoSFHYaCth-pw0TP7u9se3m_jr6EUNJgOLhGHyFI2PXWT3BlbkFJ5QXSzAp97ddGok2xwynOR79dQ4mS9oke9-4XH6qDSc3xHwCT2Ofak9XuyEL-r61i03FH3brEoA
RELEVANCEAI_API_KEY=-NmNlMzA1ZjUtZWRkYy00MzVmLWFiYzAtMjk5ODdmNTg3NTAx  
RELEVANCEAI_PROJECT=bac27f8f6347-47c5-aed6-7800db3809e1         
RELEVANCEAI_REGION=bcbe5a           
DATA_API_KEY=your-data-lookup-key         # optional
CRM_API_KEY=your-crm-key                  # optional
CRM_URL=https://crm.example.com/leads     # optional
```
The optional keys enable enhanced features like Relevance AI parsing, customer
intel lookup, and CRM logging.

## Thanks
## License

Thanks to [Harish](https://harishgarg.com) for the [inspiration to create a FastAPI quickstart for Render](https://twitter.com/harishkgarg/status/1435084018677010434) and for some sample code!
This project is licensed under the [MIT License](LICENSE).
