### R code from vignette source 'C:/Users/wlmr/teaching_unterricht/Time Series Prediction (TSP)/Slides/Rnw/slides_part5'

###################################################
### code chunk number 1: init
###################################################
# R-code: SARMA
library(sarima)

# Simulation examples
x <- sim_sarima(n=144, model = list(ma=0.8))               # MA(1)
x <- sim_sarima(n=144, model = list(ar=0.8))               # AR(1)

x <- sim_sarima(n=144, model = list(ar=c(rep(0,11),0.8)))  # SAR(1), 12  seasons
x <- sim_sarima(n=144, model = list(ma=c(rep(0,11),0.8)))  # SMA(1)

# more enlightened SAR(1) and SMA(1)
x <- sim_sarima(n=144,model=list(sar=0.8, nseasons=12, sigma2 = 1))  # SAR(1), 12 seasons
x <- sim_sarima(n=144,model=list(sma=0.8, nseasons=12, sigma2 = 1))  # SMA(1)

x <- sim_sarima(n=144, model = list(iorder=1, sigma2 = 1)) # (1-B)X_t = e_t (random walk)
acf(x)
acf(diff(x))

x <- sim_sarima(n=144, model = list(iorder=2, sigma2 = 1))  # (1-B)^2 X_t = e_t
x <- sim_sarima(n=144, model = list(siorder=1,
                                    nseasons=12, sigma2 = 1)) # (1-B^{12}) X_t = e_t

x <- sim_sarima(n=144, model = list(iorder=1, siorder=1,
                                    nseasons=12, sigma2 = 1))
x <- sim_sarima(n=144, model = list(ma=0.4, iorder=1, siorder=1,
                                    nseasons=12, sigma2 = 1))
x <- sim_sarima(n=144, model = list(ma=0.4, sma=0.7, iorder=1, siorder=1,
                                    nseasons=12, sigma2 = 1))

x <- sim_sarima(n=144, model = list(ar=c(1.2,-0.8), ma=0.4,
                                    sar=0.3, sma=0.7, iorder=1, siorder=1,
                                    nseasons=12, sigma2 = 1))

x <- sim_sarima(n=144, model = list(iorder=1, siorder=1,
                                    nseasons=12, sigma2 = 1),
                x = list(init=AirPassengers[1:13]))


# 1. Stationary seasonal models: D=0
set.seed(10)
# 1.1 SARMA(1,0)
x <- sim_sarima(n=144,model=list(sar=0.8, nseasons=12, sigma2 = 1))  # SAR(1), 12 seasons
ts.plot(x)
# Peaks at multiples of 12
acf(x,lag.max=36)


# Fit SAR
y<-x
y_obj<-arima(x,seasonal = list(order = c(1, 0, 0), period = 12))
# Forecasts
h<-240
ymin<-min(predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se)
ymax<-max(predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se)
ts.plot(c(y,rep(NA,h)),xlab="",ylab="",main="Multi steps ahead interval forecast",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se),
col="blue",lty=2)

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
plot_predict_func(x,h,y_obj)




# An example with a weak seasonality: sar1 is smaller (but positive) than previous model
# 1.2 SARMA(1,0)
set.seed(10)
x <- sim_sarima(n=144,model=list(sar=0.3, nseasons=12, sigma2 = 1))  # SAR(1), 12 seasons
ts.plot(x)
# Peaks at multiples of 12
acf(x,lag.max=36)

# Fit SAR
y_obj<-arima(x,seasonal = list(order = c(1, 0, 0), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)



set.seed(10)
# 1.3 SARMA(0,1): an example whose seasonality stops after one year (flat in forecast): 
# SMA instead of SAR
x <- sim_sarima(n=144,model=list(sma=0.8, nseasons=12, sigma2 = 1))  # SAR(1), 12 seasons
ts.plot(x)
# Peaks at 12 only: typical for SARMA(0,Q). But note that SARMA(1,0,0) had a similar pattern (because sar was small) 
acf(x,lag.max=36)

# Fit SMA
y_obj<-arima(x,seasonal = list(order = c(0, 0, 1), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)



# A rather unrealistic example with a negative-coefficient seasonality: seasonality in one year correlates negatively with seasonality in previous year 
# 1.4
set.seed(10)
# 1.4 SARMA(0,1)
x <- sim_sarima(n=144,model=list(sma=-0.8, nseasons=12, sigma2 = 1))  # SAR(1), 12 seasons
ts.plot(x)
# Peaks at 12 only: typical for SAMA(0,Q)
acf(x,lag.max=36)

# Fit SMA
y_obj<-arima(x,seasonal = list(order = c(0, 0, 1), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)




set.seed(10)
# 1.5 SARMA(1,1)
x <- sim_sarima(n=144,model=list(sma=0.8, sar=0.8, nseasons=12, sigma2 = 1))  # SAR(1), 12 seasons
ts.plot(x)
# Peaks at multiples of 12: inherits parsimony from ARMA-class (not really relevant in most applications)
acf(x,lag.max=36)

# Fit SARMA
y_obj<-arima(x,seasonal = list(order = c(1, 0, 1), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)




###################################################
### code chunk number 2: init
###################################################
# R-code: SARIMA(P,D,Q)



# 2. Non-stationary seasonal models: D=1
set.seed(10)
# 2.1 SARIMA(1,1,0)
len<-2000
y <- sim_sarima(n=len, model = list(sar=0.8, siorder=1,nseasons=12, sigma2 = 1))
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)

# Peaks at multiples of 12: very slowly decaying acf: infinite memory!!! In contrast stationary SARMA have finite-length memory
acf(x,lag.max=120)

# Fit SARIMA(1,1,0)
y_obj<-arima(x,seasonal = list(order = c(1, 1, 0), period = 12))
# Forecasts: very persistent pattern, width of interval spreads out (accumulating uncertainty)
h<-240
plot_predict_func(x,h,y_obj)



set.seed(10)
# 2.2 SARIMA(0,1,1)
y <- sim_sarima(n=len, model = list(sma=0.8, siorder=1,nseasons=12, sigma2 = 1))
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)

# Peaks at multiples of 12: very slowly decaying acf: infinite memory!!! In contrast stationary SARMA have finite-length memory
acf(x,lag.max=120)

# Fit SARIMA(0,1,1)
y_obj<-arima(x,seasonal = list(order = c(0, 1, 1), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)




# An example of an integrated seasonal process with a less regular pattern
set.seed(10)
# 2.3 SARIMA(0,1,1)
y <- sim_sarima(n=len, model = list(sma=-0.8, siorder=1,nseasons=12, sigma2 = 1))
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)
# All seasonal acf peaks are smaller than previous model: less regular/more noisy seasonal
acf(x,lag.max=120)

# Fit SARIMA(0,1,1)
y_obj<-arima(x,seasonal = list(order = c(0, 1, 1), period = 12))
# Forecasts: high uncertainty at the start (wide intervals from beginning)
# Width increases slowly (diverges for infinite h)
h<-240
plot_predict_func(x,h,y_obj)



# 2.4 A more extreme example of an integrated seasonal process whose forecast interval widens very slowly
set.seed(10)
# 2.4 SARIMA(0,1,1)
y <- sim_sarima(n=len, model = list(sma=-1, siorder=1,nseasons=12, sigma2 = 1))
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)

# Even more noisy seasonal
acf(x,lag.max=120)

# Fit SARIMA(0,1,0)
y_obj<-arima(x,seasonal = list(order = c(0, 1, 1), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)



# 2.5 An example of an integrated seasonal process which just replicates last year of data in the forecast
set.seed(10)
# 2.4 SARIMA(0,1,0)
y <- sim_sarima(n=len, model = list( siorder=1,nseasons=12, sigma2 = 1))
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)

#  seasonal
acf(x,lag.max=120)

# Fit SARIMA(0,1,0)
y_obj<-arima(x,seasonal = list(order = c(0, 1, 0), period = 12))
# Forecasts
h<-240
plot_predict_func(x,h,y_obj)
# Compare forecast with last year of observations
predict(y_obj,n.ahead=12)$pred
y[(length(y)-11):length(y)]



# 2.6 Another example: winters can become summers i.e. peaks and troughs of a SARIMA can change over time
set.seed(10)
# 2.4 SARIMA(0,1,0)
y <- sim_sarima(n=10000, model = list(sma=0.9, siorder=1,nseasons=12, sigma2 = 1))
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
z_1<-y[(10*120+1):(11*120)]
z_2<-y[(80*120+1):(81*120)]

# After some time the 'seasons' look very different i.e. summer could become winter and conversely
par(mfrow=c(2,1))
ts.plot(z_1,xlab="",ylab="",main="SARIMA(0,1,1): data-window from 1201:1320")
ts.plot(z_2,xlab="",ylab="",main="SARIMA(0,1,1): data-window from 9601:9720(same realization)")






###################################################
### code chunk number 3: init
###################################################
# R-code: SARIMA(p,d,q)(P,D,Q)

# 3. Non-stationary general seasonal models including short lags (within year dependence)
set.seed(10)
# 3.1 a non-realistic example
# SARIMA(2,1,1)(1,1,1): very strong stochastic trend because d+D=2 (rather unrealistic)
len<-2000
y <- sim_sarima(n=len, model = list(ar=c(1.2,-0.8), ma=0.4,
                                    sar=0.3, sma=0.7, iorder=1, siorder=1,
                                    nseasons=12, sigma2 = 1))
length(y)
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)
# Seasonal peaks are burried very slowly decaying acf due to very strong stochastic trend. Infinite memory!
acf(x,lag.max=120)

# Fit SARIMA(2,1,1)(1,1,1)
y_obj<-arima(x,order=c(2,1,1),seasonal = list(order = c(1, 1, 1), period = 12))
tsdiag(y_obj,gof.lag=36)

# Forecasts: strongly trending (baaaad) and very fast spreading out intervals due to stochastic trend
h<-240
plot_predict_func(x,h,y_obj)




# 3.2 A more realistic less trending model: SARIMA(1,0,0)(1,1,1)
set.seed(10)
len<-2000
y <- sim_sarima(n=len, model = list(ar=0.9, ma=0,
                                    sar=0.3, sma=-0.7, iorder=0, siorder=1,
                                    nseasons=12, sigma2 = 1))
length(y)
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)
# We can control for acf at smaller (within year) lags
acf(x,lag.max=120)

# Fit SARIMA(1,0,0)(1,1,1)
y_obj<-arima(x,order=c(1,0,0),seasonal = list(order = c(1, 1, 1), period = 12))
# Estimates are close to true parameters
y_obj
# Diagnostics are OK
tsdiag(y_obj,gof.lag=36)

# Forecasts: no trend and slowly spreading out intervals: better (more realistic) than previous example
h<-240
plot_predict_func(x,h,y_obj)



# 3.3 An example with a small drift/slope
set.seed(1)
len<-2000
y <- sim_sarima(n=len, model = list(ar=0, ma=-0.99,iorder=1,
                                    sar=0.3, sma=0.5,  siorder=1,
                                    nseasons=12, sigma2 = 1))
length(y)
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)
# We can control for acf at smaller (within year) lags
acf(x,lag.max=120)

# Fit SARIMA(1,1,0)
y_obj<-arima(x,order=c(0,1,1),seasonal = list(order = c(1, 1, 1), period = 12))
# Estimates are close to true parameters
y_obj
# Diagnostics are not OK
tsdiag(y_obj,gof.lag=36)

# Forecasts: no trend and slowly spreading out intervals: better than previous example
h<-240
plot_predict_func(x,h,y_obj)




###################################################
### code chunk number 4: init
###################################################
# R-code: auto.arima
# Automatic model identification  Auto.arima
# Can be poor when used without care!!!!!!!!!!!!!!!!!!!

library(forecast)


set.seed(1)
len<-2000
y <- sim_sarima(n=len, model = list(ar=0, ma=-0.99,iorder=1,
                                    sar=0.3, sma=0.5,  siorder=1,
                                    nseasons=12, sigma2 = 1))
length(y)
# Needs some initialization!!!
ts.plot(y)
# Extract last 200 observations (after initialization)
x<-y[1800:len]
ts.plot(x)
# We can control for acf at smaller (within year) lags
acf(x,lag.max=120)

# Fit SARIMA(0,1,1)(1,1,1)
y_obj<-arima(x,order=c(0,1,1),seasonal = list(order = c(1, 1, 1), period = 12))
tsdiag(y_obj,gof.lag=36)
# Forecasts: weak trend and slowly spreading out intervals
h<-240
plot_predict_func(x,h,y_obj)



fit <- auto.arima(x)
# No seasonality
fit
# Multi-step forecast rather poor: season is much more regular
plot(forecast(fit,h=20))

# Here we allow for intense search over many models by selecting stepwise=FALSE,approximation=FALSE (see help)
fit <- auto.arima(x,stepwise=FALSE,approximation=FALSE)
# No seasonality
fit
# Poor forecasts
plot(forecast(fit,h=20))

# Doesn't work either...
fit<-auto.arima(x, seasonal = T)
plot(forecast(fit,h=20))

# Define a ts-object: here we supply the additional information of seasonal length s
myts <- ts(x, start=c(2000, 1),  frequency=12)
fit<-auto.arima(myts)#, seasonal = F)
# The model orders do not match but forecasts are similar to ordinary predict above
fit
plot(forecast(fit,h=h))

# Check diagnostics: much better than true model above... 
# But true model better in forecasting
y_obj<-arima(x,order=c(0,0,2),seasonal = list(order = c(1, 1, 1), period = 12))
tsdiag(y_obj,gof.lag=36)




