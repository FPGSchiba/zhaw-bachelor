
rm(list=ls())




# Exercise 1: white noise interval forecasts

# 1.1 xhat=mu
mu<-10
len<-101
set.seed(1)
anzsim<-1000
number_outside<-0
# rnorm generates standardized Gaussian noise: sigma=1
sigma<-2
# Quantile for standard Gaussian distribution
z<-1.96
plot_T<-F
for (i in 1:anzsim)
{  
  x<-mu+sigma*rnorm(len)
# Point forecast: neither too high nor too low i.e. right in the middle  
  xhat<-mu
  mat<-cbind(x,c(rep(NA,len-1),xhat))
  colnames(mat)<-c("Series","Forecast")
  if (x[len]>xhat+z*sigma|x[len]<xhat-z*sigma)
    number_outside<-number_outside+1
  if (plot_T)
  {  
    plot(x,type="l",col="black",ylim=c(mu-3,mu+3))
    lines(c(rep(NA,len-1),xhat+z*sigma),type="b",col="blue")
    lines(c(rep(NA,len-1),xhat-z*sigma),type="b",col="blue")
    abline(v=len-1) 
  }
}
# Proportion
number_outside/anzsim

set.seed(1)
# New point forecast  
xhat<-9
for (i in 1:anzsim)
{  
  x<-mu+sigma*rnorm(len)
  if (x[len]>xhat+z*sigma|x[len]<xhat-z*sigma)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim

# For identical widths the forecast interval centered around mu is better than that centered around 9 since 
# the former includes more (future) observations. The latter is slightly 'off-centered' (sub-optimal)



#------------------------------------------
# 1.4 assessing the forecast interval
sigma<-1
mu<-10
len<-101
set.seed(1)
anzsim<-1000
# Here we change the width of the forecast interval: 1.6 roughly corresponds to 10% interval i.e. 
# roughly 100-10=90% of observations of a Gaussian random variable with mean mu and variance sigma^2 lie in 
# the interval [mu-1.6*sigma,mu+1.6*sigma]
z<-1.6
number_outside<-0
for (i in 1:anzsim)
{  
  x<-mu+rnorm(len)
# Point forecast: use data up to len-1 for forecasting x_len one-step ahead  
  xhat<-mean(x[1:(len-1)])
# Empirical sd  
  sigmahat<-sd(x[1:(len-1)])
  mat<-cbind(x,c(rep(NA,len-1),xhat))
  colnames(mat)<-c("Series","Forecast")
  if (F)
  {
    plot(x,type="l",col="black",ylim=c(mu-3,mu+3))
    lines(c(rep(NA,len-1),xhat+z*sigmahat),type="b",col="blue")
    lines(c(rep(NA,len-1),xhat-z*sigmahat),type="b",col="blue")
    abline(v=len-1) 
  }
  if (x[len]>xhat+z*sigmahat|x[len]<xhat-z*sigmahat)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim

# To judge the 95%-interval one must set z<-1.96 and look at (one of) the plot in the plot-window


#------------------------------------------------------
# Exercise 3: MA(1)


#-------------------------------------------------
# Exercise 4
# 4.1
set.seed(12)
len<-112
# Generate random-walk
x<-cumsum(rnorm(len))

# 4.2: mean is baaaad!
ts.plot(x)
abline(h=mean(x))


#--------------------------------------------

