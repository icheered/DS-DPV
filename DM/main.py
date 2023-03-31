import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pyreadstat import read_sav

# Import the data
data, meta = read_sav('voorbeeld7_1.sav')
chol1 = pd.DataFrame(data)

# Scatter plot with regression line
plt.figure()
sns.lmplot(x='leeftijd', y='chol', data=chol1, fit_reg=True)
plt.title('Scatter plot of cholesterol and age')
plt.subplots_adjust(top=0.9)
plt.savefig('2_6_scatterplot.png')

# Fit the linear model
fit1 = smf.ols('chol ~ leeftijd', data=chol1).fit()
print("Summary of the linear model:")
print(fit1.summary())

# Fit the second linear model
fit2 = smf.ols('chol ~ leeftijd + bmi + sekse + alcohol', data=chol1).fit()
print("Summary of the second linear model:")
print(fit2.summary())

# Determine significant factors from fit2
print("\n// Significant factors (p < 0.05):")
print(fit2.pvalues[fit2.pvalues < 0.05])

# Add the residuals to the table
chol1['residuals'] = fit2.resid
plt.figure()
# Plot a histogram of the residuals
plt.hist(chol1['residuals'], bins='auto')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of residuals')
# plt.subplots_adjust(top=0.9)
plt.savefig('2_6_histogram.png')