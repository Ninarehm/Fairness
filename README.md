# Fairness

To run the code with the equity objective for fairness gain results:

python equity.py --loss_type equity --beta 0.5

To run the code with the equality objective for fairness gain results:

python equity.py --loss_type equality --beta 0.5

To run the code for fairness gain results with basic classifier objective set the beta value to be zero :

python equity.py --beta 0.0

To run the feedback loop experiments use:

python equity_feedback_loop.py --loss_type equity --beta 0.5

python equity_feedback_loop.py --loss_type equality --beta 0.5

python equity_feedback_loop.py --loss_type classifier --beta 0.0


The paper for this Github:
https://arxiv.org/pdf/2005.07293.pdf
Please cite the paper when using the code in this GitHub repository.


The Adult dataset is coming from:
http://archive.ics.uci.edu/ml/datasets/Adult
Please cite the dataset sources for using the dataset.
