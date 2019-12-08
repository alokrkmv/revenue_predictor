from datetime import datetime
from helpers.normalizer import Normalizers
def convertor(request_dict):
    response_dict = {
            'OpenDays':0,
            'Big Cities':0, 
            'Other':0, 
            'DT':0, 
            'FC':0, 
            'IL':0,
            'P2':0, 
            'P3':0, 
            'P22':0, 
            'P20':0,
            'P24':0, 
            'P28':0, 
            'P26':0
    }

    response_dict["OpenDays"] = (datetime.strptime(request_dict.get("OpenDays"), '%Y-%m-%d')-datetime.now()).days
    if(request_dict.get("CityGroup")=="BigCity"):
        response_dict["Big Cities"] = 1
    else:
        response_dict["Other"] = 1

    if(request_dict.get("RestaurantType")=="DT"):
        response_dict["DT"] = 1
    elif request_dict.get("RestaurantType")=="IL":
        response_dict["IL"] = 1
    else:
        response_dict["FC"] = 1

    norm_obj = Normalizers(population = int(request_dict.get("Population")),area = int(request_dict.get("Area")),pu_below_30 = int(request_dict.get("Population_below_30")))
    norm_population,norm_area,norm_pu_below_30 = norm_obj.normalize_data()

    response_dict["P2"] = norm_population
    response_dict["P3"] = norm_pu_below_30
    response_dict["P20"] = norm_area
    response_dict["P22"] = int(request_dict.get("Gender Ratio"))
    response_dict["P24"] = int(request_dict["Development Index"])
    response_dict["P28"] = int(request_dict["No_of_points_of_interest_nearby"])
    response_dict["P26"] = int(request_dict["CarParkArea"])
    
    return response_dict

    




