# i4X-CPM-Model-Backend

### [Main training notebook](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/drafting_notebook.ipynb)

This repo is for developing and maintaining the backend for our predictive model which we are building for the UCSD Capital Program Management through the i4X (Innovation for Change) program. Our goal is to build a model that takes in CSV files containing columns for cost data (Gross Sq Footage, Projected Budget,	Projected Commitments,	Estimate at Completion,	Actuals To Date,	Actuals + Projections) and generate an S-cost projection and accompanying table showing the cost/month over a fixed span of time. 

With my current configuration I have achieved a median R^2 score (comparing the predicted S-curves with the actuals) of about 0.55, which is OKAY ot start but should be better. The #1 way to improve it is... you guessed it! More data! Having Gross Sq Footage as an input is essential both as a feature of the software as well as for the functioning of the model (RMSE for the growth rate parameter skyrockets when you remove it, even on a dataset of double the size), but not enough of the projects available for us on eBuilder have Gross Sq Footage data. Currently the models are being trained on only like 50 datasets, which is a tiny pool.

Anyone in the group is welcome to tweak what I did here and optimize the models further. I am sure that better performance is somehow possible from the model side.

Next steps would be to express data concerns to Chris and see what he can do for us, and then we need to start thinkng about how this is going to get integrated with the frontend. Also we need to think about what the UI is going to look like.

![WhatsApp Image 2026-03-26 at 21 04 57](https://github.com/user-attachments/assets/124c1149-4690-4903-9e1b-c39e890e367e)

[Link to login to e-Builder](https://app.e-builder.net/auth)
