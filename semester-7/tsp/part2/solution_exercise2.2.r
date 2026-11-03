# Exercise 1

b_1<-0.9
sigma<-2

# 1.1 MA-processes are always stationary

# 1.2 mean is zero
mu<-0
# Variance
R0<-sigma^2*(1+b_1^2)
R0

# 1.3 acf

acf_e<-rep(0,10)
acf_e[1]<-1
acf_e[2]<-b_1/(1+b_1^2)

acf_e

ARMAacf( ma = b_1, lag.max = 10, pacf = FALSE)


# -------------------------------------------------------------------------------
# Exercise 2


set.seed(10)
b_1<--0.7
b_5<-0.5

# 2.1
len<-100
x<-arima.sim(list(ma=b_1),n=len)
set.seed(10)
y<-arima.sim(list(ma=c(rep(0,4),b_5)),n=len)



# 2.2 Sample acf's
par(mfrow=c(2,1))
acf(x)
acf(y)

# 2.3 We select orders 1 and 5: estimate empirical models

x_obj<-arima(x,order=c(0,0,1))
y_obj<-arima(y,order=c(0,0,5))

x_obj$coef
y_obj$coef


# 2.4 Check diagnostics
tsdiag(x_obj)
tsdiag(y_obj)



# 2.5, 2.6 

predict(x_obj,n.ahead=10)
predict(y_obj,n.ahead=10)

# 2.7
par(mfrow=c(2,1))
x_r_for<-c(x,predict(x_obj,n.ahead=10)$pred)
ts.plot(x_r_for)
abline(v=100)
lines(c(rep(NA,100),predict(x_obj,n.ahead=10)$pred+2*predict(x_obj,n.ahead=10)$se),col="red")
lines(c(rep(NA,100),predict(x_obj,n.ahead=10)$pred-2*predict(x_obj,n.ahead=10)$se),col="red")

y_r_for<-c(y,predict(y_obj,n.ahead=10)$pred)
ts.plot(y_r_for)
abline(v=100)
lines(c(rep(NA,100),predict(y_obj,n.ahead=10)$pred+2*predict(y_obj,n.ahead=10)$se),col="red")
lines(c(rep(NA,100),predict(y_obj,n.ahead=10)$pred-2*predict(y_obj,n.ahead=10)$se),col="red")





#---------------------------------
# Exercise 3
interval_forecast<-function(x,h,q)
{
  len<-length(x)
  # Estimation of parameters
  ma_obj<-arima(x,order = c(0, 0, q))
  # Forecast multi-step ahead
  xhat<-predict(ma_obj,h)
  # Compute the forecast intervals
  x_lower<-xhat$pred-2*xhat$se
  x_upper<-xhat$pred+2*xhat$se
  return(list(x_lower=x_lower,x_upper=x_upper))
}


set.seed(12)
sigma<-sqrt(2)
q<-2
b_1<--1.7
b_2<-0.8
len<-50
mu<-0
# Number simulations
anzsim<-1000
sigma_vec<-1:anzsim
# Forecast horizon
h<-10
emp_sig<-rep(0,h)

wh<-rep(0,anzsim)

# We compute anzsim replications of length len+h of the MA(2)
for (j in 1:anzsim)#j<-1
{

# Simulate process  
  x<-mu+arima.sim(n = len+h, list( ma = c(b_1,b_2)), sd = sigma)
# The first len observations are fed to interval_forecast
  z<-x[1:len]
  int_obj<-interval_forecast(z,h,q)
  
# we verify that x[101:(100+h)] are in the forecast intervals
# If not (miss) the empirical significance level emp_sig is incremented by 1
  for (i in 1:h)#i<-1
  {
    if (x[len+i]<int_obj$x_lower[i]|x[len+i]>int_obj$x_upper[i])
    {  
      emp_sig[i]<-emp_sig[i]+1
      if (i==1)
        wh[j]<-1
    }
  }
}
# The empirical significance level should be close to 5%
# For shorter series (len=50) the empirical significance level is above 5%: too optimistic; bands too narrow (overfitting) 
#   and point forecast biased
# For longer series the effect vanishes: empirical significance levels are closer to theoretical one
emp_sig/anzsim


# Slightly more complex model: MA(4)

set.seed(12)
sigma<-sqrt(2)
q<-4
b_1<--1.7
b_2<-0.8
b_3<-1.2
b_4<--0.9
mu<-0
# Number simulations
anzsim<-1000
sigma_vec<-1:anzsim
# Forecast horizon
h<-10
emp_sig<-rep(0,h)

wh<-rep(0,anzsim)

# We compute anzsim replications of length len+h of the MA(2)
for (j in 1:anzsim)#j<-1
{
  # Simulate process  
  x<-mu+arima.sim(n = len+h, list( ma = c(b_1,b_2,b_3,b_4)), sd = sigma)
  # The first len observations are fed to interval_forecast
  z<-x[1:len]
  int_obj<-interval_forecast(z,h,q)
  
  # we verify that x[101:(100+h)] are in the forecast intervals
  # If not (miss) the empirical significance level emp_sig is incremented by 1
  for (i in 1:h)#i<-1
  {
    if (x[len+i]<int_obj$x_lower[i]|x[len+i]>int_obj$x_upper[i])
    {  
      emp_sig[i]<-emp_sig[i]+1
      if (i==1)
        wh[j]<-1
    }
  }
}
# The empirical significance level should be close to 5%
# For shorter series (len=50) the empirical significance level is above 5%: too optimistic; bands too narrow (overfitting) 
#   and point forecast biased
# For longer series the effect vanishes: empirical significance levels are closer to theoretical one
emp_sig/anzsim



