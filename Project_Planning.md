# Chicago Crime Analysis Project Planning

## Data Preprocessing
- [X] Only keep crimes from the last 10 years
- [X] Drop unneeded columns from dataset
- [ ] Pull in Community Area Names and Regions
- [ ] Create Time of Day column based on the date of the crime (e.g. Morning, Afternoon, Evening, Night)
- [ ] Create Month and Day columns based on the date of the crime


## Data Exploration
- [ ] Display the descriptions of the columns
- [ ] Visualize the number of crimes by the different categorical variables (e.g. Year, Month, Time of Day, Description)
- [ ] Create a Choropleth Map using the locations of the crimes

## Hypothesis Testing
- [ ] More crimes occur on weekends (including Friday)
- [ ] More crimes occur on the South side
- [ ] More crimes occur during the summer and less in the winter
- [ ] More crimes occur at night
- [ ] ...

## Prediction
- [ ] Predict the number of crimes coming up
- [ ] Experiment with different regression algorithms (OLS, Ridge, Lasso, Elastic Net, Random Forest, DL)
- [ ] Determine if the model is statistically significant
- [ ] Determine which variables are statistically significant
- [ ] Determine which variables have the largest impact on the model
- [ ] Explain what the model coefficients mean
- [ ] Determine the R^2, RMSE, and MAE of the model
- [ ] Explain what the metrics above represent with regards to this dataset
- [ ] Explain the final algorithm used
- [ ] Create a script to train and store the final model


## Web App
- [ ] Create an introduction page with a description of the data, a summary of the analysis, and a short description of the different pages in the web app
- [ ] Create a page with a Choropleth map of crimes throughout the city
- [ ] Create a page with different data visualizations from the data exploration stage:
  - [ ] Bar chart showing the number of crimes per region or community area of the city
  - [ ] Bar chart showing the number of crimes per month of the year
  - [ ] Line chart showing the trends of the different regions over the last 10 years
  - [ ] Have dropdowns for the primary and secondary descriptions of crimes
- [ ] Create a page with a description of the prediction experimentation and results


## Wrapping Up
- [ ] Create a script to preprocessing the original dataset
- [ ] Write up instructions for:
  - [ ] Downloading the dataset
  - [ ] Downloading the project
  - [ ] Running the preprocessing script
  - [ ] Running the model training script
  - [ ] Running the web app
- [ ] Write up summary and tools used in README.MD
