air <- read.csv("C:/Users/Paul/Desktop/air.csv")
Pass=air$Passengers
## Begin 1a
tsPass<-ts(Pass, frequency=1)  
m=10;k=20;n=length(tsPass)  
plot(tsPass,type="b",xlim=c(0,n+k))
MApass<-filter(tsPass, filter=rep(1/m,m), method = "convolution", sides = 1)
Passhat=c(NA,MApass,rep(MApass[n],k-1))  #fits and forecasts
lines(Passhat,col="red")
##End 1a
##
##Begin 1b
tsPass<-ts(Pass, frequency=1)  
alpha=0.25;k=20;n=length(tsPass)  
plot(tsPass,type="b",xlim=c(0,n+k))
EWMApass<-alpha*filter(tsPass, filter=1-alpha, method = "recursive", sides = 1, init=tsPass[1]/alpha)
Epasshat=c(NA,EWMApass,rep(EWMApass[n],k-1))
lines(Epasshat,col="red")
#repeat for alpha = 1, 0.2, 0.05
##the prediction is always a horizontal line from passhat's 144th place
##It's hard to choose an "optimal" alpha because this method is bad for seasonal data
##As we'll see below, Holt-Winters chooses 0.9999339 for alpha when it is allowed to choose an optimal value.
##End 1b
##
##Begin 1c
##Holt-Winters with k=24
tsPass<-ts(Pass, frequency=1)  
k=24;n=length(tsPass)
Holtpass<-HoltWinters(tsPass, seasonal = "additive", gamma = FALSE) 
HoltpassPred<-predict(Holtpass, n.ahead=k, prediction.interval = T, level = 0.95)
plot(Holtpass,HoltpassPred,type="b")
HoltpassPred
Holtpass
##HoltpassPred is the set of predictions and bounds for 1c. The function chooses alpha=0.9999339 and Beta=FALSE
##End 1c
##
##Begin 1d
##Holt-Winters additive to account for seasonality
tsPass<-ts(Pass, deltat=1/12) 
k=24;n=length(tsPass)  
HWApass<-HoltWinters(tsPass, seasonal = "additive") 
HWApassPred<-predict(HWApass, n.ahead=k, prediction.interval = T, level = 0.95)
plot(HWApass,HWApassPred,type="b",)
HWApassPred
HWApass
##HoltWinters()chooses a=0.25,b=0.035,g=1.
##It looks like a pretty good prediction.
##End 1d
##
##Begin 1e
##same code, change "additive" to "multiplicative".
tsPass<-ts(Pass, deltat=1/12)  #sampling interval corresponds to 1/12 the seasonality period. Could instead specify frequency = 12
k=24;n=length(tsPass)  #k = prediction horizon
HWMpass<-HoltWinters(tsPass, seasonal = "multiplicative") 
HWMpassPred<-predict(HWMpass, n.ahead=k, prediction.interval = T, level = 0.95)
plot(HWMpass,HWMpassPred,type="b")
HWMpassPred
HWMpass
## a=0.28,b=0.033,g=0.87.
##End 1e
##
##Begin 1f
##Frankly, both the additive and the multiplicative look good. 
##Consulting the notes, the multiplicative is the correct model to choose.
##This conclusion is based on slide 8 of the time series notes.
plot(Pass)
lines(Pass)
##plotting the time series alone, it appears that the seasonality is proportional to the trend. 
##Thus, multiplicative is the correct method.
##end 1f
##
##
##begin 2a
tsPass<-ts(Pass, deltat=1/12)
k=24;n=length(tsPass)
Decpass<-decompose(tsPass, type = "additive") 
plot(Decpass,type="b")
Decpass
tsPasshat<-Decpass$trend+Decpass$seasonal
plot(tsPass,type="b")
lines(tsPasshat,col="red")
## this last plot demonstrates that the additive model is incorrect: the "hat" line overshoots the peaks and troughs at the low end, and undershoots them at the high end
##End 2A
##
##Begin 2B
##As before. Change 1 flag.
tsPass<-ts(Pass, deltat=1/12) 
k=24;n=length(tsPass)  
Mdecpass<-decompose(tsPass, type = "multiplicative") 
plot(Mdecpass,type="b")
Mdecpass
tsPasshat<-Mdecpass$trend*Mdecpass$seasonal
plot(tsPass,type="b")
lines(tsPasshat,col="red")
##And this time the red line is essentially perfect.
##Multiplicative is a better match for this data.
##End 2b
