import numpy as np
import pandas as pd 

class HeroStat(object):

    def __init__(self, stat_name, hero, value):
        self.stat_name = stat_name
        self.name = hero
        try:
            self.value = float(value)
        except:
            self.value = value


    def __repr__(self):
        return str(pd.Series(data=[self.stat_name, self.name, self.value]))
        return "HeroData(stat_name = %s, hero = %s, value = %f)" %(self.stat_name, self.name, self.value)


    def get_value(self):
        return self.value

    def all(self):
        """
        Get list of pair mappings of hero -> value from a HeroStat object
        """
        pass

class HerosStats(object):

    def __init__(self, stat_name, hero_and_value):
        self.stat_name = stat_name
        self.hero_and_value = hero_and_value
        self.set_values()
        self.set_heros()

        """
        Here, instantiate a HeroStat obj for every hero and value and
        store it in __dict__ where hero name is the key. 
        """

        for pair in self.hero_and_value:
            try:
                pfloat = float(pair[1])
                self.__dict__[pair[0]] = HeroStat(self.stat_name, pair[0], pfloat)
            except:
                self.__dict__[pair[0]] = HeroStat(self.stat_name, pair[0], pair[1])
        
    def __getitem__(self, item):
        return self.__dict__[item]

    def __repr__(self):
        return str(pd.DataFrame(data={self.stat_name: zip(*self.hero_and_value)[1]}, index=zip(*self.hero_and_value)[0]))
    # , index=zip(*self.hero_and_value)[0], columns=self.stat_name)
        # return "%s :: HerosStats(stat_name = %s, data = %s)" % (self.__class__, self.stat_name, self.hero_and_value)            

    def __iter__(self):
        # iterations to yield HeroStat individual objects
        for pair in self.hero_and_value:
            yield self.__dict__[pair[0]]

    def __div__(self, other):
        """
        Overload div operator for HerosStats objects to do a numpy array division on data portion of attrs. 
        """
        res = np.array(zip(*self.hero_and_value)[1]) / np.array(zip(*other.hero_and_value)[1], dtype=float)
        hero_and_value = zip(zip(*self.hero_and_value)[0], res)
        hs = HerosStats(self.stat_name, hero_and_value)
        return hs
        
    def set_values(self):
        """
        Sets this objects values attribute. 
        """
        values = []
        for pair in self.hero_and_value:
            values.append(pair[1])
        self.values = values
        
    def set_heros(self):
        """
        Set the heros attribute of this object.
        """
        heros = []
        for pair in self.hero_and_value:
            heros.append(pair[0])
        self.heros = heros
    
    def get_values(self):
        """
        :returns: list of ints
        """
        return self.values

    def get_data(self):
        """
        Method to return list of hero to value mappings for a HerosStats instance. 
        """
        return map(lambda pair: pair[1], self.hero_and_value)

    

    