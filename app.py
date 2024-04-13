
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

from bank_churn.constants import APP_HOST, APP_PORT
from bank_churn.pipline.prediction_pipeline import BankChurnData, BankChurnClassifier
from bank_churn.pipline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.credit_score: Optional[str] = None
        self.country: Optional[str] = None
        self.gender: Optional[str] = None
        self.age: Optional[str] = None
        self.tenure: Optional[str] = None
        self.balance: Optional[str] = None
        self.products_number: Optional[str] = None
        self.credit_card: Optional[str] = None
        self.active_member: Optional[str] = None
        self.estimated_salary: Optional[str] = None
        

    async def get_bankchurn_data(self):
        form = await self.request.form()
        self.credit_score = form.get("credit_score")
        self.country = form.get("country")
        self.gender = form.get("gender")
        self.age = form.get("age")
        self.tenure = form.get("tenure")
        self.balance = form.get("balance")
        self.products_number = form.get("products_number")
        self.credit_card = form.get("credit_card")
        self.active_member = form.get("active_member")
        self.estimated_salary = form.get("estimated_salary")

@app.get("/", tags=["authentication"])
async def index(request: Request):

    return templates.TemplateResponse(
            "bank_churn.html",{"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_bankchurn_data()
        
        bankchurn_data = BankChurnData(
                                credit_score= form.credit_score,
                                country = form.country,
                                gender = form.gender,
                                age = form.age,
                                tenure= form.tenure,
                                balance= form.balance,
                                products_number = form.products_number,
                                credit_card= form.credit_card,
                                active_member= form.active_member,
                                estimated_salary= form.estimated_salary,
                                )
        
        bankchurn_df = bankchurn_data.get_bankchurn_input_data_frame()

        model_predictor = BankChurnClassifier()

        value = model_predictor.predict(dataframe=bankchurn_df)[0]

        status = None
        if value == 1:
            status = "Churn-successfull"
        else:
            status = "Churn-not-successfull"

        return templates.TemplateResponse(
            "bank_churn.html",
            {"request": request, "context": status},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)