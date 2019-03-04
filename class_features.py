import pandas as pd
import numpy as np

class Features:

    def __init__(self):
        self.X = pd.DataFrame(data=None, columns=['Age'])

    def features_clean(self, df):
        self.X = self.age(df.loc[:,['saledate','YearMade']])
        self.X = self.machine_hrs(df.loc[:,'MachineHoursCurrentMeter'])
        selected_dummies = ['UsageBand','Hydraulics','Enclosure','state',
                            'ProductSize','fiProductClassDesc','Drive_System',
                            'Stick','Transmission','Tire_Size','Track_Type',
                            'Blade_Type','Steering_Controls']
        self.X = self.dummies(df.loc[:,selected_dummies])
        return self.X

    def age(self, df):
        df['YearSale'] = pd.to_datetime(df['saledate']).dt.year
        df['YearMade'] = df['YearMade'].replace(1000,np.nan) #Set YearMade=1000 to missing value    
        self.X['Age'] = df['YearSale']-df['YearMade'] #Age of the vehicle at the time of sale
        
        age_null = self.X['Age'].mean()
        self.X['Age']=self.X['Age'].where(self.X['Age']>0,age_null)
        self.X['Age_sq']=self.X['Age']**2 
        return self.X
        
    def machine_hrs(self, df):
        self.X['machine_hrs']=df.where(df==0,1)
        return self.X
    
    def dummies(self, df):
        #Usage
        dummies_usage = pd.get_dummies(df['UsageBand'])
        self.X = pd.concat([dummies_usage, self.X], 
                           axis=1, join_axes=[self.X.index])
    
        #Hydraulics
        dummies_hydraulics = pd.get_dummies(df['Hydraulics'])
        self.X = pd.concat([dummies_hydraulics['2 Valve'],dummies_hydraulics['Standard'],
                   dummies_hydraulics['Auxiliary'],dummies_hydraulics['Base + 1 Function'],
                   dummies_hydraulics['3 Valve'],dummies_hydraulics['4 Valve'], self.X], 
                            axis=1, join_axes=[self.X.index])
    
        #Enclosure
        dummies_enclosure = pd.get_dummies(df['Enclosure'])
        self.X = pd.concat([dummies_enclosure['EROPS w AC'],dummies_enclosure['OROPS'],
                   dummies_enclosure['EROPS'], self.X], 
                            axis=1, join_axes=[self.X.index])
    
        #State
        dummies_state = pd.get_dummies(df['state'], drop_first=True)
        self.X = pd.concat([dummies_state['Florida'],dummies_state['Texas'],
                   dummies_state['California'], self.X], axis=1, join_axes=[self.X.index])
        self.X = pd.concat([dummies_state['Washington'],dummies_state['Georgia'],
                   dummies_state['Maryland'], self.X], axis=1, join_axes=[self.X.index])
        self.X = pd.concat([dummies_state['Mississippi'],dummies_state['Ohio'],
                   dummies_state['Colorado'], self.X], axis=1, join_axes=[self.X.index])
        self.X = pd.concat([dummies_state['Illinois'],dummies_state['New Jersey'],
                   dummies_state['North Carolina'], self.X], axis=1, join_axes=[self.X.index])
        self.X = pd.concat([dummies_state['Tennessee'],dummies_state['Pennsylvania'],
                   dummies_state['South Carolina'], self.X], axis=1, join_axes=[self.X.index])

        #Product size
        dummies_productSize = pd.get_dummies(df['ProductSize'])
        self.X = pd.concat([dummies_productSize, self.X], 
                           axis=1, join_axes=[self.X.index])
    
        #Product class
        dummies_productClass = pd.get_dummies(df['fiProductClassDesc'])
        df['product_class_Backhoe_Loader'] = dummies_productClass[
                            'Backhoe Loader - 14.0 to 15.0 Ft Standard Digging Depth']
        self.X = pd.concat([df['product_class_Backhoe_Loader'], self.X], 
                           axis=1, join_axes=[self.X.index])
     
        #Drive system
        dummies_driveSystem = pd.get_dummies(df['Drive_System'])
        self.X = pd.concat([dummies_driveSystem, self.X], 
                           axis=1, join_axes=[self.X.index])
    
        #Stick
        dummies_stick = pd.get_dummies(df['Stick'])
        self.X = pd.concat([dummies_stick, self.X], 
                           axis=1, join_axes=[self.X.index])

        #Transmission
        dummies_transmission = pd.get_dummies(df['Transmission'])
        self.X = pd.concat([dummies_transmission['Standard'], self.X], 
                           axis=1, join_axes=[self.X.index])
    
        #Tire size
        dummies_tireSize = pd.get_dummies(df['Tire_Size'])
        self.X = pd.concat([dummies_tireSize['20.5'], self.X], 
                           axis=1, join_axes=[self.X.index])

        #Track type
        dummies_trackType = pd.get_dummies(df['Track_Type'])
        self.X = pd.concat([dummies_trackType, self.X], 
                           axis=1, join_axes=[self.X.index])
     
        #Blade_Type
        dummies_Blade_Type = pd.get_dummies(df['Blade_Type'])
        self.X = pd.concat([dummies_Blade_Type['PAT'],dummies_Blade_Type['None or Unspecified'],
                   dummies_Blade_Type['Straight'], self.X], 
                            axis=1, join_axes=[self.X.index])

        #Steering control
        dummies_Steering_Controls = pd.get_dummies(df['Steering_Controls'])
        self.X = pd.concat([dummies_Steering_Controls['Conventional'], self.X], 
                           axis=1, join_axes=[self.X.index])
    
        return self.X
