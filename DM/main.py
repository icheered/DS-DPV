# Import required libraries
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# Load data from voorbeeld7_1.sav
chol1 = pd.read_spss('voorbeeld7_1.sav')

# (a) Scatter plot with regression line
sns.lmplot(x='leeftijd', y='chol', data=chol1, fit_reg=True)

# (b) Linear model fit for chol and leeftijd
fit1 = smf.ols(formula='chol ~ leeftijd', data=chol1).fit()
print("\nFit1 summary:")
print(fit1.summary())

# (c) Linear model fit for chol with leeftijd, bmi, sekse and alcohol
fit2 = smf.ols(formula='chol ~ leeftijd + bmi + sekse + alcohol', data=chol1).fit()
print("\nFit2 summary:")
print(fit2.summary())

# Determine significant factors from fit2
print("\nSignificant factors:")
print(fit2.pvalues[fit2.pvalues < 0.05])

# (d) Histogram of the residuals from fit2
residuals = fit2.resid
plt.hist(residuals, bins=20)
plt.xlabel('Residuals')
plt.show()