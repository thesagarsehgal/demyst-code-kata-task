
from fastapi import HTTPException, status
from dao import business_dao
from model import db_model
from schema import business_schema
from sqlalchemy.orm import Session


def regsiter_business(business_regsiter_schema : business_schema.BusinessRegisterRequestSchema, db: Session):
    business_in_db = business_dao.find_all_by_name(business_regsiter_schema.name.strip(), db)
    if(len(business_in_db)>0):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT ,
            detail="Business with this name already exists"
        )
    
    business_regsiter_db = db_model.BusinessDetail(name=business_regsiter_schema.name.strip(),
                                                    year_of_establishment=business_regsiter_schema.year_of_establishment)
    business_regsiter_db = business_dao.save(business_regsiter_db, db)
    
    return business_schema.BusinessRegisterResponseSchema(
        business_uuid=business_regsiter_db.business_uuid,
        name=business_regsiter_db.name,
        year_of_establishment=business_regsiter_db.year_of_establishment
    )


def find_business(business_request_schema : business_schema.FindBusinessRequestSchema, db: Session):
    all_business_in_db = business_dao.find_all_by_name(business_request_schema.name.strip(), db)
    if(len(all_business_in_db)==0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="No business was fopund with the given name"
        )
        
    return business_schema.FindBusinessResponseSchema(
        all_businesses= [
            business_schema.BusinessDetails(
                name=business.name,
                year_of_establishment=business.year_of_establishment,
                business_uuid=business.business_uuid
            ) for business in all_business_in_db
        ]
    )
