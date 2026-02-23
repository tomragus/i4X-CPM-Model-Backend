# i4X-CPM-Model-Backend

This repo is for developing and maintaining the backend for our predictive model which we are building for the UCSD Capital Program Management through the i4X (Innovation for Change) program. Our goal is to build a model that takes in CSV files containing columns for cost data (Projected Budget,	Projected Commitments,	Estimate at Completion,	Actuals To Date,	Actuals + Projections) and generate an S-cost projection and accompanying table showing the cost/month over a fixed span of time. 

My current idea for how this will be done is 1) to compile a training set of project projection files with timelines spanning 2011 - 2027, 2) convert the timelines (disregarding categories, only total costs) into parameters for an associated S-curve (start date, end date, and curve-parameterization variables), 3) train the model on these data to predict the parameterization vector, and then 4) in the ouput to convert the parameterization into an S-curve (which will produce a table as a side product). The model of choice in this particular problem is probably a Gradient-Boosted Tree (XGBoost/LightGBM), and doing it this way is great because it turns this into basically a regression problem.

This would produce the S-curves for total cost, and could easily be altered to work for only the Line 6 rows (just like, using Claude Code or whatever). If we want to also add category breakdowns to the S-curve + table, we can also do this, by training a second model which instead of the parameterization vector, learns an "allocation vector" (containing the percentage of cost per each category). This allocation vector could be super-imposed on the S-curve, so that the curve/table also has a rough distribution of the categories that make up the total cost each month. 

## "What about using a pre-built model?" https://huggingface.co/ai-in-projectmanagement/ProjectManagementLLM

This is an option, but using something pre-built (aka something language-based) comes with some trade-offs. LLMs can hallucinate and might not be the most reliable, compared to a ground-up model for only this specific task, which if done right should be extremely stable. LLMs also still suck at math basically and if precision is important for CPM, it will be tough to sell. LLM cost breakdowns are almost guaranteed to not add up.

The benefit? More open-ended and adaptable, and certainly easier to use. Something that needs to be discussed in the group. I am personally not crazy about doing it this way.

## COVID?

The COVID conversation is interesting, because projects that spanned over COVID (2020-2022) are essentially stunted. The problem is that we are already kind of bottlenecked by USABLE (keyword, USABLE!) project data, and eliminating any project that touched this span of time, we are restricting our pool even further. We might end up stuck with only projcts finished before 2020, and considering we are predicting for 2026 and beyond, this might be less relevant now.

SO I think we should keep the COVID projects in the data pile. It's entirely possible that whatever stunting is caused by COVID is actually learned/observed by the model, and addressed without us even having to do anything (models can be weird like that... they notice deep details we cannot fathom). If we want to avoid getting hung up on this though, we can experiment with adding a simple "COVID: Yes/No" feature ("Yes" for projects whose spans touch the COVID window, "No" for others) and train the model on the data, including this feature. We can then compare this version to the raw model and see which performs better, and just pick the approach that works best.
