# i4X-CPM-Model-Backend

# Deployed app:
### 👉 [Simple version](https://i4x-cpm-s-curve-generator.streamlit.app/)
### 👉 [Full version](https://ucsd-project-capital-analytics.vercel.app/)

This is a web app tool for Capital Program Management at UC San Diego, which utilizes machine learning models to predict a cumulative cost for a planned project given only Projected Budget, Projected Commitments, Estimate at Completion, and Gross Sq Footage - the user can choose between Total Cost and Line 6 Cost.

***How it works:***
Users can engage with the app in two ways - they can upload a Cash Flow CSV for a given project directly from Unity Construct, OR simply type in the Projected Budget, Projected Commitments, Estimate at Completion, and Gross Sq Footage values manually. Then, an ensemble of machine learning models will quickly generate an S-curve, as well as display the estimated duration in months, growth rate of the curve, and the estimated midpoint of the curve. Hover over the curve to see the projected cumulative cost at any given month in the project cycle!

<img width="979" height="637" alt="Screenshot 2026-05-02 at 5 39 30 PM" src="https://github.com/user-attachments/assets/a98e4882-8540-4902-a35d-34ded9834d93" />

The machine learning models were trained on ~200 projects we are up to a top accuracy of:

**-Total Cost Curves: R^2 = 0.622**
**-Line 6 Curves: R^2 = 0.7558**

**[Main training notebook (totals)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/training_notebook_totals.ipynb)**
**[Main training notebook (Line 6)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/training_notebook_line6.ipynb)**
**[Curve Creator™️ (totals)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/curve_creator_totals.ipynb)**
**[Curve Creator™️ (Line 6)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/curve_creator_line6.ipynb)**

[Link to login to e-Builder](https://app.e-builder.net/auth)






