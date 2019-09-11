# Tools and Knowledge to Detect Statistical Oddities in Published Research

This repository houses the content presented at a workshop on research evaluation at the IGGI Conference 2019. 

The aim of this workshop is to introduce knowledge and tools that may help researchers better evaluate the accuracy of reported statistics - both in their own as well as in published research. A secondary aim is to cover concepts that may help researchers avoid the statistical issues illuminated in the workshop.

## Simulations
This section aims to illustrate the inter-relation between statistical power, statistical significance, sample size and effect size through a series of simulations.  
  
 Each simulation can be performed employing the relative function contained in `statistical_power.py`, or a series of experiments can be scheduled through the simulations manager located in `AI_reserch_police.py`.  
  
The simulation functions included in this repository are:

* `play_p_value_sonata` 
Simulate a series of experiments according to a given sample size and dimension of effect. The function will produce different sounds 
according to the significance level achieved in a specific simulated experiment. 

* `simulate_experiments`
Simulate a series of experiments according to different sample sizes and dimension of effect. The function will produce two point-plots showing the ordered significance levels and observed dimension of effect for each experiment performed with each sample size.

* `simulate_correlations`
Simulate pairs of correlations according to two sample sizes and different dimensions of effect. The function will produce two scatter plots with a fitted regression line reporting the respective signifgicance levels and observed dimension of effect.

* `simulate_filedrawer`
Samples a set of effect sizes values from a normal distribution given parameters mu and sigma. From the generated distribution of effect sizes, randomly sample a set of values, for each value simulate an experiment accordingly to a given sample size and store the observed dimension of effect of only those experiment that resulted statistically significant. The function will produce a density plot comparing the distribution of 'ground truth' effect sizes and the 'reported' observed effect sizes.
  
** In this specific framework:  
**Experiment** consists in randomly sample two sets of values from two normal distributions (sigma=1) which parameters mu differ according to a specified effect size (Cohen's d) and then comparing them via an indipendent samples t-test.  
**Correltions** consists in randomly sample two sets of values from a multivariate normal distributions with mu=0 and covariance matrix=[[1, rho], [rho, 1]] and compute the strength of their relationship through Pearson product-moment correlation.

## Links to data (if any)
...

## Links to presented literature
...

## Links to original repositories of presented tools

- GRIM
- SPRITE
- (statcheck)
...

## Requirements
We recommend setting up a virtual environment to avoid any dependency conflicts as shown below:  
  
``` python
# Pipenv is a virtual environment manager
pip install pipenv

# Create a virtual environment in this directory
pipenv install

# open / activate virtual environment
pipenv shell

# install all the dependencies
pip install -r requirements.txt
# Now we are good to go....
```
  
For Windows users we **strongly** advise to install `numpy==1.17.1+mkl` and `scipy==1.3.1` (in this order) directly from the binaries distributed through https://www.lfd.uci.edu/~gohlke/pythonlibs.
