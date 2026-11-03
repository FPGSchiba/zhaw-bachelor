rm(list = ls())


library(forecast)



#----------------------------------------------------------------------------
# Exercise 1

# 1.a and 1.b

set.seed(87)
len<-100
y<-rep(NA,12*len)
a1<-0.8
sigma<-1
for (i in 1:12)
{
  x<-arima.sim(list(ar=a1),n=len,sd=sigma)
  y[i+(0:(len-1)*12)]<-x
}

ts.plot(x)

#---------------------
# 1.c
# Typical seasonal pattern
ts.plot(y)
acf(y,lag.max=48)

#-------------------------
# 1.d
y_obj<-arima(y, seasonal = list(order = c(1, 0, 0), period = 12))
# sar1 matches a1 (in 95% confidence interval)
# Indeed: x_{it}-0.6x_{it-12}=y_{it}-0.6y_{it-1}=epsilon_{it}
y_obj
tsdiag(y_obj,gof.lag=48)

#----------------------
# 1.e
# each of the generated 12 y-series corresponds to a month. Since y can be positive or negative, the sign of the 
# seasons can change i.e. winter troughs can become summer troughs and conversely 
ts.plot(x)
abline(h=0)

#----------------------
# 1.f This problem could be alleviated by adding non-vanishing means: seasonal dummies
# One possible proposal: a cosine 
month_mean<-3*cos(pi/6*1:12)

ts.plot(month_mean)

#---------------------
# 1.g
set.seed(87)
z<-rep(NA,12*len)

for (i in 1:12)
{
  x<-arima.sim(list(ar=a1),n=len,sd=sigma)
  z[i+(0:(len-1)*12)]<-x+month_mean[i]
}
# Typical seasonal pattern but now month_mean lifts systematically winters up (early and late months) and pushes 
# summers down (middle months): more in agreement with calendar data.
ts.plot(z)

acf(z,lag.max=48)
# z is more regular
ts.plot(cbind(y,z),col=c("red","blue"))


# Let's fit a standard simple seasonal model
z_obj<-arima(z, order = c(0, 0, 0),seasonal = list(order = c(1, 0, 1), period = 12))
# Check diagnostics: problem at seasonal length
tsdiag(z_obj,gof.lag=48)
# More complex
z_obj<-arima(z, order = c(0, 0, 0),seasonal = list(order = c(2, 0, 1), period = 12))
# Check diagnostics: look fine
tsdiag(z_obj,gof.lag=48)
# We deduce that SARIMA models can also fit fixed seasonals (although the model is misspecified): 
#   Strength of SARIMA models in forecast competitions!!!



#----------------
# 1.h Changing seasonal pattern could be a problem when simulating data. But in applications the model fits 
# the seasonal pattern to the (more regular fluctuations of the) data and therefore seasonal effects are stable i.e. 'winters' remain 'winters'.
# In fact forecasts of SARIMA-models simply reflect some average seasonal pattern of the data during the last couple of years


#---------------------------------------------------------------------------------
# Exercise 2
library(sarima)
library(forecast)


load(file=paste(getwd(),"/Data/exercise5",sep=""))


x<-mat[,1]
# Exercise 2.a: no trend (possibly stationary though D=1 might be possible), seasonals
ts.plot(x)
# Intrayear dependence weak/vanishing
acf(x)


# 2.b Classic estimation
x_obj<-arima(x, seasonal = list(order = c(1, 0, 1), period = 12))
x_obj
# Looks fine: might try SAR(1) which is even simpler
tsdiag(x_obj,gof.lag=48)

# Bingo
x_obj<-arima(x, seasonal = list(order = c(1, 0, 0), period = 12))
x_obj
tsdiag(x_obj,gof.lag=48)



# Forecasts: specify a predict function
plot_predict_func<-function(y,h,y_obj)
{  
  ymin<-min(min(predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se),y)
  ymax<-max(max(predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se),y)
  ts.plot(c(y,rep(NA,h)),xlab="",ylab="",main="Multi steps ahead interval forecast",
          ylim=c(ymin,ymax))
  lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred),col="blue")
  lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se),
        col="blue",lty=2)
  lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se),
        col="blue",lty=2)
}

h<-240
plot_predict_func(x,h,x_obj)
  

# 2.c Apply auto.arima

# Fit the above y: very long time series
fit <- auto.arima(x)
# No seasonality!
fit
# Multi-step forecast rather poor: season is much more regular
plot(forecast(fit,h=20))

# More comprehensive fitting
fit <- auto.arima(x,stepwise=FALSE,approximation=FALSE)
# No seasonality!
fit
# Multi-step forecast rather poor: season is much more regular
plot(forecast(fit,h=20))

# Try to enforce seasonality by imposing D=1 or start.P=1: does not help...
fit <- auto.arima(x,start.P = 1,D=1,stepwise=FALSE,approximation=FALSE)
# No seasonality!
fit
# Multi-step forecast rather poor: season is much more regular
plot(forecast(fit,h=20))

if (F)
{
# Imposing D=1 works for white noise though....  
  set.seed(1)
  foo <- ts(rnorm(60),frequency=12)
  auto.arima(foo,D=1)
}

# Does not converge in reasonable amount of time
myts <- ts(x, start=c(1900, 1),  frequency=12)
fit<-auto.arima(myts, seasonal = T)
fit
plot(forecast(fit,h=h))


#--------------
x<-mat[,2]# Series 2
# Typical seasonal pattern 
ts.plot(x)
acf(x)

# Stationary model as above
x_obj<-arima(x, seasonal = list(order = c(1, 0, 1), period = 12))
x_obj
tsdiag(x_obj,gof.lag=48)

# requires seasonal differencing because the monthly pattern
# is persistent
x_obj<-arima(x, seasonal = list(order = c(1, 1, 1), period = 12))
x_obj
tsdiag(x_obj,gof.lag=48)

# Forecasts: much more regular pattern

h<-240
plot_predict_func(x,h,x_obj)


# Apply auto.arima
# Does not converge in reasonable amount of time
myts <- ts(x, start=c(1900, 1),  frequency=12)
fit<-auto.arima(myts, seasonal = T)
fit
plot(forecast(fit,h=h))




#--------------------
# 3. series
x<-mat[,3]
# Very weak seasonal (if at all). Strong autocorrelation/dependence visible
ts.plot(x)
# acf not really informative about seasonal
acf(x)

# Fit a non-seasonal non-stationary model and check diagnostics
x_obj<-arima(x, order=c(1,1,0))
x_obj
# Seasonal: look at acf(12) of residuals
tsdiag(x_obj,gof.lag=48)

# Add a seasonal component: seasonal is weak i.e. might try a stationary specification
x_obj<-arima(x, order=c(1,1,0),seasonal = list(order = c(1, 0, 1), period = 12))
x_obj
tsdiag(x_obj,gof.lag=48)



# Forecasts: specify a predict function

h<-240
plot_predict_func(x,h,x_obj)


# Apply auto.arima
# Model similar to above one: stationary seasonal
myts <- ts(x, start=c(1900, 1),  frequency=12)
fit<-auto.arima(myts, seasonal = T)
fit
plot(forecast(fit,h=h))

#-------------------------------------------------------------------------
# exercise 3
# Define generic forecast function
forecast_plot<-function(anz_data,y,pred)
{
  h<-length(pred[,1])
  anz_data<-min(anz_data,length(y)-1)
  ymin<-min(min(y[(length(y)-anz_data):length(y)]),min(pred))
  ymax<-max(max(y[(length(y)-anz_data):length(y)]),max(pred))
  q<-ts.plot(c(y[(length(y)-anz_data):length(y)],rep(NA,h)),ylim=c(ymin,ymax),ylab="")
  q<-lines(c(rep(NA,anz_data),pred[,2]),col="blue")
  q<-lines(c(rep(NA,anz_data),pred[,1]),col="blue")
  q<-lines(c(rep(NA,anz_data),pred[,3]),col="blue")
  return(list(q=q))
}
#----------------------
# 3.a Plot
load(file=paste(getwd(),"/Data/electricity_load",sep=""))
dat<-data.frame(x)
# Non-stationary: changing level and seasonals (there is more to be discovered in this series: see later exercises)
ts.plot(x)
len<-length(x)


#-------------------------
# 3.b : fit model
# Seasonal length: 24 hours a day
s<-24

# OK model: simple, diagnostics `bad' (acf seems cyclical) but forecasts seem OK
x_obj<-arima(x, order = c(1, 0, 1),seasonal = list(order = c(1,1, 1), period = s))
# Much better diagnostics; forecasts similar to above model
x_obj<-arima(x, order = c(2, 0, 3),seasonal = list(order = c(1,1, 1), period = s))
# Less optimal diagnostics: intervals unrealistically wide (d+D=2)
x_obj<-arima(x, order = c(0, 1, 1),seasonal = list(order = c(0,1 , 1), period = s))

x_obj
# Check first three years
tsdiag(x_obj,gof.lag=36)

#------------------
# 3.c Forecasts: different combinations of d,D can have strong impact on intervall widths
h<-240
plot(forecast(x_obj,h=h))


#------------------------
# 3.d auto.arima
myts <- ts(x, start=c(1980, 1),  frequency=s)
head(myts)
fit<-auto.arima(myts, seasonal = T)
# Model orders
fit
fit$coef

# Diagnostics: look at the residuals. Can you detect a pattern?
checkresiduals(fit)
#------------------------
# 3.e Check fitted parameters with arima
x_obj<-arima(x, order = c(2, 0, 3),seasonal = list(order = c(1,1 , 1), period = s))
# Matches auto.arima: both rely on state space models
x_obj$coef
# Compute diagnostics for auto.arima based on replication of model by arima object
tsdiag(x_obj,gof.lag=36)

#------------------
# 3.f Forecasts: plausible
plot(forecast(x_obj,h=h))




