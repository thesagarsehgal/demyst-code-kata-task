from pydantic import BaseModel, Field

# request schema
class BusinessRegisterRequestSchema(BaseModel):
    name: str
    year_of_establishment: int  

class FindBusinessRequestSchema(BaseModel):
    name: str
    
# response schema
class BusinessRegisterResponseSchema(BaseModel):
    business_uuid: str 
    name: str 
    year_of_establishment: int  

class BusinessDetails(BaseModel):
    business_uuid: str 
    name: str 
    year_of_establishment: int  

    
class FindBusinessResponseSchema(BaseModel):
    all_businesses: list[BusinessDetails]
