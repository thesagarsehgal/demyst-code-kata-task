### How to setup 
- install docker-compose on your system 
- run the following command build the docker images 
```
docker-compose build 
```
- run the following command bring up the docker images 
```
docker-compose up 
```
- Now you can register 2 accounting providers by hitting the following APIs (This step can be improved upon by adding the script on startup)
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/loan/accounting/providers/regsiter?name=XERO' \
  -H 'accept: application/json' \
  -d ''
```
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/loan/accounting/providers/regsiter?name=MYOB' \
  -H 'accept: application/json' \
  -d ''
```


# DB Architecture 

```
class BaseModel(Base):
    # A base class to include all these columns in every column 
    __abstract__ = True
    id = Column(Integer, primary_key=True,index = True, nullable=False, autoincrement=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow(), default=datetime.utcnow(), nullable=True)

class BusinessDetail(BaseModel):
    # A table containing details of all the businesses regsitered
    __tablename__ = "business_detail"

    business_uuid = Column(String(256), primary_key=True, index=True, nullable=False, default=generate_uuid)
    name = Column(String(256), unique=True, nullable=False)
    year_of_establishment = Column(Integer, nullable=False)

class LoanApplication(BaseModel):
    # A table containing all the loan applications submitted
    __tablename__ = "loan_application"
    
    application_uuid = Column(String(256), primary_key=True, nullable=False, default=generate_uuid)
    business_uuid = Column(String(256), nullable=False)
    accounting_provider_name = Column(String(256), nullable=True)
    loan_amount_requested = Column(Integer, nullable=True)
    
    # application_status stored over here for furture debugging purposes
    application_status = Column(String(256), default=LoanApplicationStatus.NOT_SUBMITTED.value , nullable=False)
    
    # the response of the balance sheet retrieved is stored over here .. useful for debugging purposes 
    accounting_balance_sheet_json = Column(JSON, nullable=True)
    
    pre_assessment_value = Column(JSON, nullable=True)
    amount_sanctioned = Column(Integer, nullable=True)
    
    # the response of the decision engine is stored over here .. useful for debugging purposes 
    decision_json = Column(JSON, nullable=True)


class AccountingProvider(BaseModel):
    __tablename__ = "accounting_provider"
    
    acconting_provider_name = Column(String(256), nullable=False)

    # column for future purposes, if we don't want to display an accounting proivder, due to unavailablity 
    display = Column(String(256), default=False, nullable=False)
```


# Assumptions 
- For Accounting Providers ... have hardcoded the API's with the response (as mentioned in the task) with a Mock API https://apimocha.com/demyst/xero/accounting-service, https://apimocha.com/demyst/myob/accounting-service 
- For Decision Service ... have hardcoded its response (as mentioned in the task) with a Mock API https://apimocha.com/demyst/decision-service 
- For making decision of `pre_assessment_value` ... have assumed the following 
    - matching if last 12 month data is present ... if not present ... the application would be rejected bcz of Absence of Data
    - calculating total_profit_loss, as a sum of all the all profit/loss of past 12 months 
    - ```if(total_profit_loss_last_12_months > 0):
        if(average_asset_last_12_months > loan_amount_requested):
            pre_assessment_value = 100
        else:
            pre_assessment_value = 60
    else:
        pre_assessment_value = 20
    ```
    
