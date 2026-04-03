# i4X-CPM-Model-Backend

### [Main training notebook (totals)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/training_notebook_totals.ipynb)
### [Main training notebook (Line 6)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/training_notebook_line6.ipynb)
### [Curve Creator™️ (totals)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/curve_creator_totals.ipynb)
### [Curve Creator™️ (Line 6)](https://github.com/tomragus/i4X-CPM-Model-Backend/blob/main/curve_creator_line6.ipynb)

This repo is for developing and maintaining the backend for our predictive model which we are building for the UCSD Capital Program Management through the i4X (Innovation for Change) program. Our goal is to build a model that takes in CSV files containing columns for cost data (Gross Sq Footage, Projected Budget,	Projected Commitments,	Estimate at Completion,	Actuals To Date,	Actuals + Projections) and generate an S-cost projection and accompanying table showing the cost/month over a fixed span of time. 

With my current configuration I have achieved a median R^2 score (comparing the predicted S-curves with the actuals) of about 0.55, which is OKAY ot start but should be better. The #1 way to improve it is... you guessed it! More data! Having Gross Sq Footage as an input is essential both as a feature of the software as well as for the functioning of the model (RMSE for the growth rate parameter skyrockets when you remove it, even on a dataset of double the size), but not enough of the projects available for us on eBuilder have Gross Sq Footage data. Currently the models are being trained on only like 50 datasets, which is a tiny pool.

Anyone in the group is welcome to tweak what I did here and optimize the models further. I am sure that better performance is somehow possible from the model side.

Next steps would be to express data concerns to Chris and see what he can do for us, and then we need to start thinkng about how this is going to get integrated with the frontend. Also we need to think about what the UI is going to look like.

![WhatsApp Image 2026-03-26 at 21 04 57](https://github.com/user-attachments/assets/124c1149-4690-4903-9e1b-c39e890e367e)

[Link to login to e-Builder](https://app.e-builder.net/auth)

------------------

### Update: Apr 3

Next big change will come with more data, but! The models for Line 6 only actually perform MUCH BETTER than the regular models (best R^2 score 0.6777) even without the full data! This surprising and really great news

Some Line 6 examples:

<img width="843" height="368" alt="Screenshot 2026-04-03 at 3 52 47 PM" src="https://github.com/user-attachments/assets/87ac6154-a3b4-4275-962e-7c80f353a376" />

<img width="842" height="371" alt="Screenshot 2026-04-03 at 3 52 06 PM" src="https://github.com/user-attachments/assets/d630a952-5f6e-43be-ae0c-c3548e0b962e" />

<img width="847" height="365" alt="Screenshot 2026-04-03 at 3 51 51 PM" src="https://github.com/user-attachments/assets/6412c55b-d8d9-4abb-a8ab-a3b3a0cf76de" />

<img width="269" height="547" alt="Screenshot 2026-04-03 at 3 55 41 PM" src="https://github.com/user-attachments/assets/7b668cde-6df1-4f07-83e1-3c6233a9045c" />



