
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
  if (plot_T)
  {  
    plot(x,type="l",col="black",ylim=c(mu-3,mu+3))
    lines(c(rep(NA,len-1),xhat+z*sigma),type="b",col="blue")
    lines(c(rep(NA,len-1),xhat-z*sigma),type="b",col="blue")
    abline(v=len-1) 
  }
  if (x[len]>xhat+z*sigma|x[len]<xhat-z*sigma)
    number_outside<-number_outside+1
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
# 1.2 xhat=mean(x)
sigma<-1
mu<-10
len<-101
set.seed(1)
anzsim<-1000
z<-1.96
number_outside<-0
for (i in 1:anzsim)
{  
  x<-mu+rnorm(len)
# Point forecast: use data up to len-1 for forecasting x_len one-step ahead  
  xhat<-mean(x[1:(len-1)])
  if (x[len]>xhat+z*sigma|x[len]<xhat-z*sigma)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim

#------------------------------------------
# 1.3 using mean and empirical standard deviation
sigma<-1
mu<-10
len<-101
set.seed(1)
anzsim<-1000
z<-1.96
number_outside<-0
sigmahat_vec<-NULL
for (i in 1:anzsim)
{  
  x<-mu+rnorm(len)
# Point forecast: use data up to len-1 for forecasting x_len one-step ahead  
  xhat<-mean(x[1:(len-1)])
# Empirical sd  
  sigmahat<-sd(x[1:(len-1)])
# collect all sds  
  sigmahat_vec<-c(sigmahat_vec,sigmahat)
  if (x[len]>xhat+z*sigmahat|x[len]<xhat-z*sigmahat)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim
# Mean interval width
z*2*mean(sigmahat_vec)
# Compare with above
z*2*sigma


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
  if (x[len]>xhat+z*sigmahat|x[len]<xhat-z*sigmahat)
    number_outside<-number_outside+1
  if (plot_T)
  {  
    
    plot(x,type="l",col="black",ylim=c(mu-3,mu+3))
    lines(c(rep(NA,len-1),xhat+z*sigmahat),type="b",col="blue")
    lines(c(rep(NA,len-1),xhat-z*sigmahat),type="b",col="blue")
    abline(v=len-1) 
  }
}
# Proportion
number_outside/anzsim

# To judge the 95%-interval one must set z<-1.96 and look at (one of) the plot in the plot-window

#-----------------------------------------------------------------
# Exercise 2: t-distribution
# 2.1 
mu<-10
len<-101
set.seed(1)
anzsim<-1000
z<-1.96
# Set degrees of freedom
df<-3
number_outside<-0
sigmahat_vec<-NULL
for (i in 1:anzsim)
{  
  x<-mu+rt(len, df)
  # Point forecast: use data up to len-1 for forecasting x_len one-step ahead  
  xhat<-mean(x[1:(len-1)])
  # Empirical sd  
  sigmahat<-sd(x[1:(len-1)])
  sigmahat_vec<-c(sigmahat_vec,sigmahat)
  if (x[len]>xhat+z*sigmahat|x[len]<xhat-z*sigmahat)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim
# Mean standard deviation (true standard deviation is sqrt{df/(df-2)})
mean(sigmahat_vec)
# True sd
sqrt(df/(df-2))



# Augment df
df<-10
set.seed(1)
number_outside<-0
sigmahat_vec<-NULL
for (i in 1:anzsim)
{  
  x<-mu+rt(len, df)
  # Point forecast: use data up to len-1 for forecasting x_len one-step ahead  
  xhat<-mean(x[1:(len-1)])
  # Empirical sd  
  sigmahat<-sd(x[1:(len-1)])
  sigmahat_vec<-c(sigmahat_vec,sigmahat)
  if (x[len]>xhat+z*sigmahat|x[len]<xhat-z*sigmahat)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim
# Mean standard deviation (true standard deviation is sqrt{df/(df-2)})
mean(sigmahat_vec)
# True sd
sqrt(df/(df-2))



# Augment df
df<-200
set.seed(1)
number_outside<-0
sigmahat_vec<-NULL
for (i in 1:anzsim)
{  
  x<-mu+rt(len, df)
  # Point forecast: use data up to len-1 for forecasting x_len one-step ahead  
  xhat<-mean(x[1:(len-1)])
  # Empirical sd  
  sigmahat<-sd(x[1:(len-1)])
  sigmahat_vec<-c(sigmahat_vec,sigmahat)
  if (x[len]>xhat+z*sigmahat|x[len]<xhat-z*sigmahat)
    number_outside<-number_outside+1
}
# Proportion
number_outside/anzsim
# Mean standard deviation (true standard deviation is sqrt{df/(df-2)})
mean(sigmahat_vec)
# True sd
sqrt(df/(df-2))


# 2.2 For larger df the percentage of observations outside the interval approaches 5% (Gaussian case) 


# 2.3 In most applications the Gaussian assumption does not hold (more outliers/heavy tails, asymmetry,...). 
# Therefore we expect the percentage of future observations lying outside the above interval forecast to exceed 5%
# Most (classic) forecast packages ignore this feature. 

#------------------------------------------------------
# Exercise 3: MA(1)

# 3.1 White noise can be replicated by setting mu=0, b1=0

# 3.2
mu<-10
b1<-0.9
len<-101
set.seed(1)
anzsim<-1000
number_outside<-0
sigmahat_vec<-NULL
for (i in 1:anzsim)
{  
  eps<-rnorm(len)
# Note that x has length len-1!  
  x<-mu+eps[2:len]+b1*eps[1:(len-1)]
# Point forecast: use data up to (length(x)-1) for forecasting x_length(x) one-step ahead  
  xhat<-mean(x[1:(length(x)-1)])
# Empirical sd  
  sigmahat<-sd(x[1:(length(x)-1)])
  sigmahat_vec<-c(sigmahat_vec,sigmahat)
  if (x[(length(x))]>xhat+z*sigmahat|x[(length(x))]<xhat-z*sigmahat)
    number_outside<-number_outside+1
}
number_outside/anzsim

# average sd
mean(sigmahat_vec)
# Average interval width: this was ~3.92 in the white noise case above
2*z*mean(sigmahat_vec)
# Next week, we shall construct a better forecast with a narrower forecast interval

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
# 4.3
# Last data point or exponential smoothing 

# 4.4
anzsim<-1000
# Weight of exponential smoother
alpha<-0.8
weight_exp<-alpha^(0:(len-1))/sum(alpha^(0:(len-1)))
#ts.plot(weight_exp)
meansquare_mean<-meansquare_last<-mean_square_exp<-0
for (i in 1:anzsim)
{
  x<-cumsum(rnorm(len+1))
# Forecast: mean  
  xhat_mean<-mean(x[1:len])
# Forecast: last data point  
  xhat_last<-x[len]
# Forecast: expoential smoother  
  xhat_exp<-x[len:1]%*%weight_exp
# Compute mean-square error  
  meansquare_mean<-meansquare_mean+(x[len+1]-xhat_mean)^2
  meansquare_last<-meansquare_last+(x[len+1]-xhat_last)^2
  mean_square_exp<-mean_square_exp+(x[len+1]-xhat_exp)^2
}  
# MS forecast errors of forecasts
meansquare_mean/anzsim
meansquare_last/anzsim
mean_square_exp/anzsim

# 4.5
set.seed(12)
len<-112
# Generate noise
x<-(rnorm(len))
ts.plot(x)
abline(h=mean(x))
anzsim<-1000
meansquare_mean<-meansquare_last<-mean_square_exp<-0
for (i in 1:anzsim)
{
  x<-(rnorm(len+1))
  xhat_mean<-mean(x[1:len])
  xhat_last<-x[len]
  xhat_exp<-x[len:1]%*%weight_exp
  
  meansquare_mean<-meansquare_mean+(x[len+1]-xhat_mean)^2
  meansquare_last<-meansquare_last+(x[len+1]-xhat_last)^2
  mean_square_exp<-mean_square_exp+(x[len+1]-xhat_exp)^2
  
}  
# MS forecast errors of forecasts: ranking is inverted (mean best and last data point worst)
meansquare_mean/anzsim
meansquare_last/anzsim
mean_square_exp/anzsim

# 4.6
set.seed(12)
len<-112
# Generate cycle+noise
x<-(rnorm(len))+2*cos(pi/6*1:len)
ts.plot(x)
abline(h=mean(x))
anzsim<-1000
meansquare_mean<-meansquare_last<-0
for (i in 1:anzsim)
{
  x<-(rnorm(len+1))+2*cos(pi/6*1:(len+1))
  xhat_mean<-mean(x[1:len])
  xhat_last<-x[len]
  xhat_exp<-x[len:1]%*%weight_exp
  
  meansquare_mean<-meansquare_mean+(x[len+1]-xhat_mean)^2
  meansquare_last<-meansquare_last+(x[len+1]-xhat_last)^2
  mean_square_exp<-mean_square_exp+(x[len+1]-xhat_exp)^2
  
}  
# MS forecast errors of forecasts: best forecast has MSE of 1!!!
meansquare_mean/anzsim
meansquare_last/anzsim
mean_square_exp/anzsim

# 4.7
# We learned that the weighting of the data (assign more weight to 
# last data point, or equal weight to all data points, or cyclically...) is
# crucial in determining a good forecast. Exponential smoothing is generally between 
# mean and last (though sometimes best) and is a good compromise in many applications. 
# We will now learn how to assign 
# optimal weights under certain (model-) assumptions


#--------------------------------------------
# Exercise 5 MA(1): Regression instead of mean point forecast

# 5.1, 5.2 and 5.3
mu<-10
b1<-0.9
len<-101
set.seed(1)
anzsim<-1000
number_outside<-number_outside_regression<-0
sigmahat_vec<-NULL
for (i in 1:anzsim)
{  
  eps<-rnorm(len)
# Note that x has length len-1!  
  x<-mu+eps[2:len]+b1*eps[1:(len-1)]
# Regression of x_t on its history: use data up to (length(x)-1) for forecasting the next observation
  lm_obj<-lm(x[2:(length(x)-1)]~x[1:(length(x)-2)])
# Make a forecast of last x
  xhat_regression<-lm_obj$coefficients[1]+lm_obj$coefficients[2]*x[len-1] 
# Classic mean forecast  
  xhat<-mean(x[1:(length(x)-1)])
# Empirical sd: we use the same interval width for both forecasts  
  sigmahat<-sd(x[1:(length(x)-1)])
  sigmahat_vec<-c(sigmahat_vec,sigmahat)
# Number of future observations outside mean rule  
  if (x[(length(x))]>xhat+z*sigmahat|x[(length(x))]<xhat-z*sigmahat)
    number_outside<-number_outside+1
# Number of future observations outside linear regression rule: both intervals are of the same width  
  if (x[(length(x))]>xhat_regression+z*sigmahat|x[(length(x))]<xhat_regression-z*sigmahat)
    number_outside_regression<-number_outside_regression+1
}

# 5.4 Percent of observations outside the interval: mean vs. regression rule
# Mean
number_outside/anzsim
# Regression: much less observations outside forecast interval (for identical width): regression-rule is better than sample mean 
# We could tighten the forecast interval so as to cover 95% of the future observations
number_outside_regression/anzsim


