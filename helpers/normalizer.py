import math

class Normalizers:
    def __init__(self,**kwargs):
        self.population = kwargs["population"]
        self.area = kwargs["area"]
        self.population_below_30 = kwargs["pu_below_30"]

    def population_normalizer(self,population):
        if population<=900000:
            return math.ceil(population/100000)
        else :
            return 10

    def area_normaziler(self,area):
        if area<=800:
            return math.ceil(area/800)
        else:
            return min(15,(area-800)/100+1)

    def population_below_30_normalizer(self,pu_below_30):
        return math.ceil(pu_below_30/10)

    def normalize_data(self):
        norm_population =  self.population_normalizer(self.population)
        norm_area = self.area_normaziler(self.area)
        norm_pu_below_30 = self.population_below_30_normalizer(self.population_below_30)

        return norm_population,norm_area,norm_pu_below_30




