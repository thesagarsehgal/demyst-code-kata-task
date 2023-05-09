import datetime

from constants.pre_decision_summary_config_contant import PreDecisionSummaryConfigConstant


def year_month_tuples(year, month):
    months = year * 12 + month - 1 # -1 to reflect 1-indexing
    while True:
        yield (months // 12, months % 12 + 1) # +1 to reflect 1-indexing
        months -= 1 # next time we want the previous month

def get_preassessment_score(accounting_balance_sheet_json, loan_amount_requested):
    year = datetime.date.today().year
    month = datetime.date.today().month
    prev_months = year_month_tuples(year, month)
    
    accounting_balance_sheet_json_sorted = sorted(accounting_balance_sheet_json, key=lambda k: (k["year"], k["month"]), reverse=True)
    
    total_asset_value = 0
    total_profit = 0
    
    if(len(accounting_balance_sheet_json_sorted)<PreDecisionSummaryConfigConstant.EVALUATION_MONTHS):
        raise Exception("Balance Sheet does not contain enough data")
    
    for i in range(PreDecisionSummaryConfigConstant.EVALUATION_MONTHS):
        year, month  = next(prev_months)
        # print(month, year, accounting_balance_sheet_json_sorted[i])

        if(accounting_balance_sheet_json_sorted[i]["year"]==year and accounting_balance_sheet_json_sorted[i]["month"]==month):
            total_asset_value+=accounting_balance_sheet_json_sorted[i]["assetsValue"]
            total_profit+=accounting_balance_sheet_json_sorted[i]["profitOrLoss"]
        else:
            # print(accounting_balance_sheet_json_sorted[i]["year"], year, accounting_balance_sheet_json_sorted[i]["month"], month)
            raise Exception("Balance Sheet does not contains latest data.")
    
    avg_asset = total_asset_value/PreDecisionSummaryConfigConstant.EVALUATION_MONTHS    
    
    if(total_profit>0):
        if(avg_asset>loan_amount_requested):
            return 100, total_profit
        else:
            return 60, total_profit
    else:
        return 20, total_profit
        
        
        