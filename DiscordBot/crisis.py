import pandas as pd
#crisis
'''water=100
land=100
IQ=120
DI=100
SI=100
pop=1000
agri=100
TPS=70
FandF=100
temp=100
o2=100
co2=100
industry=100
pollutants=100
#random values given for variable initialisation'''

#will use a different input method for era
def crisis_for_era(df,i):
    era=df.loc[i,'era']
    water=df.loc[i,'water']
    land=df.loc[i,'land']
    IQ=df.loc[i,'iq']
    DI=df.loc[i,'di']
    SI=df.loc[i,'si']
    pop=df.loc[i,'population']
    agri=df.loc[i,'agriculture']
    TPS=df.loc[i,'size']
    FandF=df.loc[i,'flora']
    temp=df.loc[i,'temp']
    o2=df.loc[i,'oxygen']
    co2=df.loc[i,'co2']
    industry=df.loc[i,'factory']
    pollutants=df.loc[i,'pollutants']
    crisis=''
    if era==1:
        if IQ in range(10,150) and agri <0.2*TPS and water<0.35*TPS:
            crisis='Famine'
            pop=pop-(0.007*pop)
        elif IQ in range(5,100) and water>0.4*TPS:
            crisis='Flood'
            pop=pop-(0.05*pop)
        elif IQ in range(10,120) and water<0.3*TPS:
            crisis='Drought'
        elif IQ in range(30,140) and water>0.5*TPS:
            s=random.randit(0,2)
            if s==0:
                crisis='Cyclone'
            else:
                crisis='Tsunami'
            pop=pop-0.2*pop
        elif IQ in range(20,135):
            crisis='Earthquake'
            pop=pop-0.15*pop
            
    elif era==2:
        if IQ in range(30,120) and temp>80:
            crisis='Forest Fire'
            FandF=FandF-0.5*FandF
        elif IQ in range(10,140) :
            crisis='Plague'
            pop=pop-(0.1*pop)
            
    elif era==3:
        if IQ in range(45,130) and o2<(0.13*TPS) and co2>(0.1*TPS):
            crisis='Global Warming'
            water=water+(0.05*water)
            land=land-(0.05*land)
            FandF=FandF-(0.1*FandF)
        elif IQ in range(0,60) and pop>1000:
            crisis="World War"
            pop=pop-(0.75*pop)
        else:
            if IQ in range(20,140):
                r=random.randit(0,3)
                if r==0 :
                    crisis='Fuel Shortage'
                    DI=DI-(0.02*DI)
                elif r==1:
                    crisis='Great Wars'
                    pop=pop-(0.4*pop)
                elif r==2:
                    crisis='Plague'
                    pop=pop-(0.1*pop)
    elif era==4:
        q=random.randit(0,5)
        if IQ in range(20,200):
            #taking a common range of IQ since IQ of all events was very broad and very similar, would therefore overlap
            if q==0:
                crisis='Corona'
                pop=pop-(0.4*pop)
            elif q==1:
                crisis='Ebola'
                pop=pop-(0.3*pop)
            elif q==2:
                crisis='Solar Flare'
                DI=DI-(0.2*DI)
            elif q==3:
                crisis='AI Malfunction'
                pop=pop-(0.2*pop)
                agri=agri-(0.5*agri)
                industry=industry+(0.5*industry)
            elif q==4:
                crisis='Nukes'
                pop=pop-(0.6*pop)
                FandF=0
                
    elif era==5:
        if IQ in range(45,130) and o2<(0.13*TPS) and co2>(0.1*TPS):
            crisis='Global Warming'
            water=water+(0.05*water)
            land=land-(0.05*land)
            FandF=FandF-(0.1*FandF)
        elif IQ in range(90,205) and pollutants>1000:
            crisis='Ozone Depletion'
            pop=pop-(0.05*pop)
        elif IQ in range(50,250):
            x=random.randit(1,3)
            if x==1:
                crisis='Fuel Shortage'
                DI=DI-(0.02*DI)
            elif x==2:
                crisis='AI Malfunction'
                pop=pop-(0.2*pop)
                agri=agri-(0.5*agri)
                industry=industry+(0.5*industry)
    
    df.loc[i,'era']=era
    df.loc[i,'water']=water
    df.loc[i,'land']=land
    df.loc[i,'iq']=IQ
    df.loc[i,'di']=DI
    df.loc[i,'si']=SI
    df.loc[i,'population']=pop
    df.loc[i,'agriculture']=agri
    df.loc[i,'flora']=FandF
    df.loc[i,'temp']=temp
    df.loc[i,'oxygen']=o2
    df.loc[i,'co2']=co2
    df.loc[i,'factory']=industry
    df.loc[i,'pollutants']=pollutants

    return df,crisis