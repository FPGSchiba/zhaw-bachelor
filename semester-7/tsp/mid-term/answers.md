# Midterm - Jann Erhardt

## Exercise 1

### (a)

The process is not stationary. It has an upwards trjectory.
As $1.3x_{t-1}$ will influence the series to grow over time.

### (b)

$$
E[] = ?
$$

### (c)

$$
x_{100} = x_{99} = 19
$$

$$
\hat{x}_{101} = 5 + 1.3x_{100}-0.5x_{99}+\epsilon_{101} = 5 + 1.3\times 19 - 0.5 \times 19 = 20.2
$$

### (d)

$$
\mu \plusmn 2\sigma\sqrt{1 + b_1^2} = 5 \plusmn 2 \times \sqrt{4} \times \sqrt{1 + 1.3^2} \approx 5 \plusmn 6.56
$$

No we cannot. As the confidence interval calculated above is (-1.56, 11.56). So there still is a possibility within 95% that the next observation is negative.

## Exercise 2

### (a)

Because both PACF and ACF do no longer vanish for a ARMA(1,1) process.

### (b)

Its the Bayesian Information Criterium (BIC). Its defined as:

$$
BIC(p_0, q_0) := log(\hat{\sigma^2_{p_0q_0}})+log(T)\frac{p_0+q_0}{T}
$$

The first term penalises the models error, so that it fits the data well.

The second term penalises the model complexity. So that it prefers models that fit the data well, but the model is still simple.

### (c)

An ARMA model can be used to fit arbitrary stationary time series data with less parameters, so we have parsimony.

### (d)

The second model is stationary as all its parameters are $|a| < 1$. That means it does not grow nor shrink and stays around its $\mu = 0.5$.

## Exercise 3

### Series 1

Timeseries plot:

![alt text](image.png)

You can clearly see that this series is not stationary, so differences are needed.
I can also see a small seasonal trend, so I will use `period = 12`.

PACF
![alt text](image-1.png)

ACF

![alt text](image-2.png)

From PACF and ACF we get not much information, so its clearly a more complex SARIMA Model.

After playing with the variables in the SARIMA()() model a bit I came to following conclusions:

- Second differences are needed for the non-seasonal part
- First differences are needed for the seasonal part
- The non-seasonal AR-Part needs to be higher than 2.
- The non-seasonal MA-Part needs to be higher than 1.
- The seasonal MA-Part needs to be higher than 1.

So my final model is: SARIMA(2, 2, 1)(0, 1, 1)

Diagnostics:
![alt text](image-3.png)

Forecast:
![alt text](image-4.png)

### Series 2

Timeseries Plot:
![alt text](image-5.png)

The process is clearly non-stationary, so differences are needed. Seasonality cannot really be seen by eye.

ACF
![alt text](image-7.png)

PACF
![alt text](image-6.png)

ACF says nothing at all which tells me it will be a complexer ARMA or a MA model. PACF looks like a ARIMA(0, 1, 2), so I will try that first.

Diagnistics of ARIMA(0, 1, 2):

![alt text](image-8.png)

This looks like there is seasonality in the data. (Only because I was stupid and left seasonal differences in the model, so there is no seasonality here).

After looking at some more diagnostics: The non-seasonal part appears to be a ARIMA(2, 1, 1) in despite of my previous believe. I think its due to the complexer ARIMA process I should not look at the PACF too much.

![alt text](image-10.png)

Forecast:
![alt text](image-14.png)

### Series 3

Timeseries plot:
![alt text](image-11.png)

I cannot see by eye if the time series data is stationary or not, but its clearly seasonal, so I will use `period = 12`.

ACF
![alt text](image-12.png)

ACF also clearly shows the seasonal pattern repeating at 12.

PACF
![alt text](image-13.png)

PACF shows the same picture as the ACF.

I found an interesting result. I only took the first seasonal differences and the diagnistics already look quite good:

![alt text](image-15.png)

I saw the Ljung-Box statistics around lag 4 and also the low values in the seasonality. So I updated the non-seasonal part to a ARIMA(4, 0, 0) and with the seasonal part also needing improvement I ended up with SARIMA(4, 0, 0)(0, 1, 1) as my best model.

Diagnostics:
![alt text](image-16.png)

Forecast:
![alt text](image-17.png)

## Exercise 3

### Series 4

Timeseries Plot:
![alt text](image-18.png)

Cannot say if the data is stationary or not. So I will first assume its stationary.

ACF
![alt text](image-19.png)

Slightly looks like a pattern is visible.

PACF

![alt text](image-20.png)

No pattern, only a clear negative partial correlation at lag 2. So I will first try ARIMA(2, 0, 0).

Diagnostics:
![alt text](image-21.png)

Diagnostics already looks really good so I will keep that simple MA(2) model.

Forecast:
![alt text](image-22.png)
