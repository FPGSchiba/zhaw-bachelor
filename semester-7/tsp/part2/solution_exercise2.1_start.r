
# Exercise 1

# Simulation MA(1)- and MA(5)-Processes
set.seed(71)
len<-100

# First possibility

eps<-rnorm(len)
x<-eps[2:len]-0.7*eps[1:(len-1)]
y<-eps[6:len]+0.5*eps[1:(len-5)]
par(mfrow=c(2,1))
ts.plot(x,lty=1:2)
ts.plot(y,lty=1:2)
mean(y)
acf(x)
acf(y)


set.seed(71)
# Second possibility
x<-arima.sim(list(ma=-0.7),n=len)
y<-arima.sim(list(ma=c(rep(0,4),0.5)),n=len,sd=10)



#------------------------------------------
# Exercise 2

# True processes at the end of the script file



# Read the data

ma50<-read.table(paste(getwd(),"/Data/ma50.txt",sep=""))
ma300<-read.table(paste(getwd(),"/Data/ma300.txt",sep=""))

ts.plot(ma50,lty=1:4)

x<-ma50[,1]
x<-ma300[,1]

par(mfrow=c(2,2))
ts.plot(x)
acf(x)
acf(x,type="partial")

