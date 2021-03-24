#crisis
water=100
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
#random values given for variable initialisation

#will use a different input method for era
def crisis_for_era(era)
    if era=="ancient":
        if IQ in range(10,150) and agri <0.2*TPS and water<0.35*TPS:
            print("FAMINE!")
            pop=pop-(0.007*pop)
        elif IQ in range(5,100) and water>0.4*TPS:
            print("flood")
            pop=pop-(0.05*pop)
        elif IQ in range(10,120) and water<0.3*TPS:
            print("DROUGHT!")
        elif IQ in range(30,140) and water>0.5*TPS:
            s=random.randit(0,2)
            if s==0:
                print("CYCLONE!")
            else:
                print("Tsunami!")
            pop=pop-0.2*pop
        elif IQ in range(20,135):
            print("EARTHQUAKE!")
            pop=pop-0.15*pop
            
    elif era=="medieval":
        if IQ in range(30,120) and temp>80:
            print("forest fires!")
            FandF=FandF-0.5*FandF
        elif IQ in range(10,140) :
            print("plagues")
            pop=pop-(0.1*pop)
            
    elif era=="industrial":
        if IQ in range(45,130) and o2<(0.13*TPS) and co2>(0.1*TPS):
            print("GLOBAL WARMING")
            water=water+(0.05*water)
            land=land-(0.05*land)
            FandF=FandF-(0.1*FandF)
        elif IQ in range(0,60) and pop>1000:
            print("WORLD WARS")
            pop=pop-(0.75*pop)
        else:
            if IQ in range(20,140):
                r=random.randit(0,3)
                if r==0 :
                    print("fuel shortage")
                    DI=DI-(0.02*DI)
                elif r==1:
                    print("great wars!")
                    pop=pop-(0.4*pop)
                elif r==2:
                    print("plagues")
                    pop=pop-(0.1*pop)
    elif era=="information":
        q=random.randit(0,5)
        if IQ in range(20,200):
            #taking a common range of IQ since IQ of all events was very broad and very similar, would therefore overlap
            if q==0:
                print("corona")
                pop=pop-(0.4*pop)
            elif q==1:
                print("ebola")
                pop=pop-(0.3*pop)
            elif q==2:
                print("solar flare")
                DI=DI-(0.2*DI)
            elif q==3:
                print("AI")
                pop=pop-(0.2*pop)
                agri=agri-(0.5*agri)
                industry=industry+(0.5*industry)
            elif q==4:
                print("NUKES!!")
                pop=pop-(0.6*pop)
                FandF=0
                
    elif era=="future":
        if IQ in range(45,130) and o2<(0.13*TPS) and co2>(0.1*TPS):
            print("GLOBAL WARMING")
            water=water+(0.05*water)
            land=land-(0.05*land)
            FandF=FandF-(0.1*FandF)
        elif IQ in range(90,205) and pollutants>1000:
            print("ozone depletion")
            pop=pop-(0.05*pop)
        elif IQ in range(50,250):
            x=random.randit(0,3)
            if x==0:
                print("PLANTER EXPLODED")
                print("GAME OVER! BETTER LUCK NEXT TIME")
                pop=0
            elif x==1:
                print("fuel shortage")
                DI=DI-(0.02*DI)
            elif x==2:
                print("AI")
                pop=pop-(0.2*pop)
                agri=agri-(0.5*agri)
                industry=industry+(0.5*industry)