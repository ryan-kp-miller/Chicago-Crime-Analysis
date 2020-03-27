# Chicago Crime Analysis Project Planning

## Data Preprocessing
- [X] Only keep crimes from the last 10 years
- [X] Drop unneeded columns from dataset
- [X] Clean up the text columns (Primary Type and Location Description)
- [X] Pull in Community Area Names and Regions
- [X] Create Month, day of week, time of day, and season columns based on the date of the crime
- [X] Remove Nulls from the dataset
- [X] Add in homicides data and repeat steps above
- [X] Add community area population for calculating crimes per capita

## Data Exploration
- [X] Display the descriptions of the columns
- [X] Most and least common types of crime
- [X] Regions with the most and least crime/homicides
- [X] Community Areas with the most and least crime/homicides
- [X] Visualize the number of crimes per capita by the different Date-based categorical variables (e.g. Year, Month, Time of Day, Season, Description)
- [X] Repeat visualizations with estimated crimes/homicides per capita
- [X] Visualize relationships between arrest rates and the different columns
- [X] Write short summaries for each section

## Prediction
- [X] Predict whether an arrest will be made for a crime
- [X] Experiment with different classification algorithms (Random Forest, DL, ...)
- [X] Determine which variables have the largest impact on the model

## Power BI Dashboard
- [ ] Create a page with a Choropleth map of crimes throughout the city
- [ ] Create a page with different data visualizations from the data exploration stage:
  - [ ] Bar chart showing the number of crimes per region or community area of the city
  - [ ] Bar chart showing the number of crimes per month of the year
  - [ ] Line chart showing the trends of the different regions over the last 10 years
  - [ ] Have dropdowns for the primary and secondary descriptions of crimes
  - [ ] Most and Least Common Types of Crimes
  - [ ] Most and Least Common Locations of Crimes
  - [ ] Most and Least Arrests by Community Area
  - [ ] Most and Least Arrests by Region
  - [ ] Most and Least Domestic Crimes by Community Area
  - [ ] Most and Least Domestic Crimes by Region
  - [ ] Most and Least Common Locations of Crimes
- [ ] Create Crimes/Homicides per Capita page

## Wrapping Up
- [ ] Write up summary and tools used in README.MD
