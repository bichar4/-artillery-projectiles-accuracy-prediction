class TwoPointInterceptMapper():
    """gives the slope and intercept of interpolated points """
    def __init__(self,x_array,y_array):
        self.x_array = x_array
        self.y_array = y_array
        self.a0 = []
        self.a1 = []
        self.__calc_intercepts()   
    def __calc_intercepts(self):
        for i in range(len(self.y_array)-1):
            self.a1.append((self.y_array[i+1]-self.y_array[i])/(self.x_array[i+1]-self.x_array[i]))
            self.a0.append(self.y_array[i] - (self.a1[i]*self.x_array[i]))
    def upper_range_mapper(self,array,number):
        index = -1
        for i in range(len(array)):
            if(number == array[0]):#making sure the index doesnot collide in case of intercept array
                index = 1
                break
            if(array[i]>=number):
                index = i
                break;
        return index,array[index];  
    def get_intercepts(self,number):
        index,value = self.upper_range_mapper(height,number)     
        assert(index>0),"y variable is beyond the scope of sorted range"
        index = index-1 #mapping with the intercept array
        return self.a0[index],self.a1[index]
    def getY_value(self,number):
        y,m = self.get_intercepts(number)
        return (m*number)+y
    def test(self):
        for i in range(len(self.a0)):
            print(self.a0[i],self.a1[i])