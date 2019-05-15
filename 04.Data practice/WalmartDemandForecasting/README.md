# Study "Demand forecasting" by following winner's code and comment
- original code is R
- hence I study his code by python by myself

# ! Article below is all the Winner's comments. 
# ! I hightlight and re-order sentences to understand easier
---
## Winner code and comments: https://github.com/davidthaler/Walmart_competition_code
- SVD + stlf/ets - this model applied SVD to the training data as preprocessing, and then forecast each series with stlf(), using an exponential smoothing model (ets) for the non-seasonal forecast.
- SVD + stlf/arima - the same, but with an arima model for the non-seasonal forecast
- Standard scaling + stlf/ets + averaging - like (1), but SVD was not used. Instead, the data were standard scaled, and a correlation matrix was computed. Then forecasts were made and several of the closely correlated series were averaged together, before restoring the original scale.
- SVD + seasonal arima - This used auto.arima() from the forecast package. These models were actually all (p, d, q)(0, 1, 0)[52], essentially non-seasonal arima errors 
on a seasonal naive model.
- non-seasonal arima with Fourier series terms as regressors - This also used auto.arima(), **but as a non-seasonal arima model, with the seasonality captured in the regressors.**
- Average of simple models - there were three of these: a linear regression model with seasonal(weekly) dummy variables, a seasonal naive model, and a product model, which predicts a weekly average times a store average 

---

## Winner's description: https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/discussion/8125#latest-357454

This post is a revised version of my earlier one, that was well down-thread under Sriok's post. I wanted to put it in its own thread so people could find it. Also, the code is now up on Github.

My final model was **an average of 6 components, 5 time series models plus an average of 3 simple models,** which are also solely time-based, and are described in detail elsewhere (simple models). I did not use the features at all. Most of the models came out of the forecast package in R, which is excellent. In particular, 3 of the models, including the best single model, used the stlf() function, **which does an STL decomposition and then makes a non-seasonal forecast** over the **seasonally adjusted data, before adding back the naively extended seasonal component.** The other two time series models used auto.arima() directly, which is an automatic arima model forecasting function from the forecast package.

To make each set of predictions, I iterated over the departments, producing a data matrix of Weekly_Sales values of dimension (number of weeks) x (number of stores). This allowed for **pooling of data across the stores, within the same department.** One way that I did that was by performing singular value decomposition on the data matrix and then **replacing the data with a reduced-rank approximation of itself before forecasting.** Another pooling method that I used was **to forecast the standard-scaled series and then average together several of the most closely correlated series before rescaling.** Note that in some cases, the most closely correlated series were not all that closely correlated. In that case, the prediction got flattened out. **With both SVD and averaging, the intuition is that features that are shared across different stores are probably signal, while those that are not are more likely to be noise.**

---
- **SVD + stlf/ets** - this model applied SVD to the training data as preprocessing, and then forecast each series with stlf(), using an exponential smoothing model (ets) for the non-seasonal forecast.
- **SVD + stlf/arima** - the same, but with an arima model for the non-seasonal forecast
Standard scaling + stlf/ets + averaging - like (1), but SVD was not used. Instead, the data were standard scaled, and a correlation matrix was computed. Then forecasts were made and several of the closely correlated series were averaged together, before restoring the original scale.
- **SVD + seasonal arima** - This used auto.arima() from the forecast package. These models were actually all (p, d, q)(0, 1, 0)[52], essentially non-seasonal arima errors on a seasonal naive model.
non-seasonal arima with Fourier series terms as regressors - This also used auto.arima(), but as a non-seasonal arima model, with the seasonality captured in the regressors.
- **Average of simple models** - there were three of these: a linear regression model with seasonal(weekly) dummy variables, a seasonal naive model, and a product model, which predicts a weekly average times a store average 

---
All of the models got the holiday-period shift explained in more detail elsewhere (key adjustment). Briefly, in many of the departments, there is a bulge of sales in the days leading up to Christmas, and a different number of those days fall into the same week as Christmas in the test set than in the training set years. Therefore, if there was a bulge, I shifted some of the sales around by 2 or 2.5 days, depending on whether the model involved used only the last year of the training data, or both years. This adjustment matters a lot, because **the week of Christmas is up-weighted and that part of the year has high sales levels in many departments.**

The best performing single model was model the SVD + stlf/ets. **With a 2.5 day shift (because it uses both years of data)**, it gets 2348 on the final leaderboard, enough to win this competition by itself. The runAll() script available in the repository runs all of the models, and then generates a submission out of the average of them. It actually gets 2303 (not 2301) on the final leaderboard, so I must have changed a parameter value somewhere.

I'd like to thank Rob Hyndman and the forecast package team for their great work. Also, thanks again to Hyndman and to George Athana­sopou­los for their very helpful online book Forecasting: principles and practice, which I highly recommend as a practitioner-level introduction to the subject.

---

## Winner's key adjustment: https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/discussion/8028

In this competition, we had weekly input and weekly output, so I used almost exclusively weekly models, with a 52-week year. For the most part that worked well. The data is short, so the weeks line up pretty well. In particular, if you label the **start of the training data as week 5 of 2010**, then **the Super Bowl is always in week 6, Thanksgiving is always in week 47**, and **Christmas is always in week 52**. Labor Day is not in the test set, so it doesn't matter much here. Furthermore, the Super Bowl is always on a Sunday and Thanksgiving is always on a Thursday, so those events have a fixed relationship to the week boundaries.  

- 참고로 데이터의 주차는 금요일 기준으로 split
- 토요일부터 n+1주차로 계산

Christmas is different, it occurs on a fixed date so its day of the week changes, and it has a big sales bulge associated with it, so it matters a lot here. In the **first year** of the training data, it occurs on a **Saturday (with weeks ending on Friday).즉 2010 크리스마스는 52주차에 있는데 그로인한 수요발생은 51주차 ** That causes all of its sales bulge to fall into the week before. In the **second year** of the training data, it occurs on a **Sunday**, so there is one pre-Christmas shopping day in **week 52. 즉 2011년 크리스마스는 52주차 일요일에 있으므로 52주차에 수요발생 일수는 단 하루**. The **test** set has Christmas for 2012, which is a leap year. That puts **Christmas on a Tuesday**, **with 3 pre-Christmas shopping days in its week. 즉 test데이터에서 크리스마스는 52주차 화요일에 있으니, 월 일 토 이렇게 52주차에 수요 일수 3일이 발생**   

In the training data, if you look at departments that exhibit a bulge in sales around Christmas, you see that **week 52**, **the week with Christmas in it**, looks pretty normal. Also, **week 48**, the week after Thanksgiving, does too.(*즉, training 데이터에서 48, 52주차는 매우 평범하다. but! test에서는 그러하지 않을 것! 수요발생일이 무려 3일!*) So I implemented a **post-forecast adjustment** that said that **if, in a given department, the average sales for weeks 49, 50 and 51(*즉, 2010(52주차 수요 발생일 0), 2011(52: 1) 나머지는 51주차)* were at least 10% higher than for weeks 48 and 52,** then I would circularly shift a particular fraction of the sales from **weeks 48 through 52 into the next week** (and **from 52 back to 48**). If the underlying model was based only on the last year, **I shifted 2/7 of the sales**; if it used **both years of training data**, I **shifted 2.5/7**. This is because **the test year shifts 2 days with respect to the second year of the training data**, but **3 days with respect to the first year.** 즉 수요발생일 2010 X, 2011 토, 2012 토일월 -> 따라서 test 52주차는 vs 2010: 3 shift, vs 2011: 2 shift)  

I added this adjustment with about 3 weeks to go in the competition. I gained about 200 points and took over 1st place. Some of my individual models gained almost 300 points. It was the largest gain I had in the whole competition.
