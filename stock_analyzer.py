from pprint import pprint
import json
import argparse
import requests
import statistics


def analyze_stock(symbol):
    credentials = json.load(open('creds.json', 'r'))
    api_key = credentials['fmp_api_key']

    # financial-growth-quarterly
    url_financial_growth_quarter = 'https://fmpcloud.io/api/v3/financial-growth/{}?period=quarter&apikey={}'.format(symbol, api_key)
    resp_financial_growth_quarter = requests.get(url=url_financial_growth_quarter)
    data_financial_growth_quarter = resp_financial_growth_quarter.json() # Check the JSON Response Content documentation below

    url_key_metrics = 'https://fmpcloud.io/api/v3/key-metrics/{}?apikey={}'.format(symbol, api_key)
    resp_key_metrics = requests.get(url=url_key_metrics)
    data_key_metrics = resp_key_metrics.json() # Check the JSON Response Content documentation below

    url_ratios = 'https://fmpcloud.io/api/v3/ratios/{}?apikey={}'.format(symbol, api_key)
    resp_ratios = requests.get(url=url_ratios)
    data_ratios = resp_ratios.json() # Check the JSON Response Content documentation below

    url_rating = 'https://fmpcloud.io/api/v3/rating/{}?apikey={}'.format(symbol, api_key)
    resp_rating = requests.get(url=url_rating)
    data_rating = resp_rating.json() # Check the JSON Response Content documentation below

    url_income_statement = 'https://fmpcloud.io/api/v3/income-statement/{}?period=quarter&apikey={}'.format(symbol, api_key)
    resp_income_statement = requests.get(url=url_income_statement)
    data_income_statement = resp_income_statement.json() # Check the JSON Response Content documentation below

    eps_growth_12=[]
    revenue_growth_12=[]
    grossProfit_growth_12=[]
    rdExp_growth_12=[]
    opCF_growth_12=[]

    i=0
    for element in data_financial_growth_quarter:
        if(i>11):
            break
        eps_growth_12.append(element['epsgrowth'])
        revenue_growth_12.append(element['revenueGrowth'])
        grossProfit_growth_12.append(element['grossProfitGrowth'])
        rdExp_growth_12.append(element['rdexpenseGrowth'])
        opCF_growth_12.append(element['operatingCashFlowGrowth'])
        i=i+1


    eps_12=[]
  
    i=0
    for element in data_income_statement:
        if(i>11):
            break
        eps_12.append(element['eps'])
        i=i+1

    # calculate mean
    eps_mean=mean_yearly(eps_growth_12)
    revenue_mean=mean_yearly(revenue_growth_12)
    grossProfit_mean=mean_yearly(grossProfit_growth_12)
    rdExp_mean=mean_yearly(rdExp_growth_12)
    opCF_growth_mean=mean_yearly(opCF_growth_12)

    eps_12_mean=mean_yearly(eps_12)

    print("\n+++++Evaluation of Stock: {}++++++\n".format(symbol))
    print("#  Explanations  #\n")
    print("All values are yearly. Not in percentage. Sorted by priority (latest most important)")


    print("#  Risk  #")
    print("grahamNumber: " + str(data_key_metrics[0]['grahamNumber']) + " [stockPrice] - Number based on the ")   
    print("RD Expense Growth: " + str(rdExp_mean) + " [<0.3] - Company solely rely on technology -> needs to invest too much")   
    print("debtToEquity: " + str(data_key_metrics[0]['debtToEquity']) + " [<3]")   
    
    # Volatility
    #Std(eps)
    #std(revenue 3 years)
    #fiveYShareholdersEquityGrowthPerShare -> wird der Growth nur durch Fremdkapital finanziert

    print("\n#  Growth  #")
    # Per Share -> I don't know... print("CF Growth/S (3y): " + str(data_financial_growth_quarter[0]['threeYOperatingCFGrowthPerShare']) + " [>0.1] - ")   
    # Per Share -> I don't know... print("Revenue Growth/S (3y): " + str(data_financial_growth_quarter[0]['threeYRevenueGrowthPerShare']) + " [>0.1] -  ")   
    print("Revenue Growth mean (3y): " + str(revenue_mean) + " [>0.1] -  ")   
    print("Gross Profit Growth mean (3y): " + str(grossProfit_mean) + " [>0.1] -  ")   
    print("EPS Growth mean (3y): " + str(eps_mean) + " [>0.1] -  ")   
    print("Operating CF Growth (3y): " + str(opCF_growth_mean) + " [>0.1] -  ")   
    
    print("EPS mean (3y): " + str(eps_12_mean) + " [>10] -  ")    # 1y

    print("\n# Prospects  #")

    print("ROE: " + str(data_key_metrics[0]['roe']) + " [>0.2] - Return on Equity (usually correlated with ROIC, ROA)")    # 1y
    print("PE: " + str(data_ratios[0]['priceEarningsRatio']) + " [<12] - Years to recoup the share price")   
    print("PEG: " + str(data_ratios[0]['priceEarningsToGrowthRatio']) + " [<1.5, ideal 1] - PE/EPS-Growth determines how fair the share price is regarding the eps growth rate ")   

    # print("\n#  Timing  #")
    # Gewinn über letzten 6 Monate/3 Moante

    print("\n# Rating  #")
    print("ratingScore: " + str(data_rating[0]['ratingScore']) + " [=5] - Rating score by other analysts ")  
    

    # print("\n# My Rating  #")
    # Formula to be developed

    # data.to_csv(f'./{symbol}_analysis.csv')

def getPercentage(decimalValue):
    return decimalValue*100

def mean_yearly(lst_quartlery):
    return mean(lst_quartlery)*4

def mean(lst): 
    return sum(lst) / len(lst) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('symbol', type=str, help="the stock symbol you want to download")

    namespace = parser.parse_args()
    analyze_stock(**vars(namespace))
