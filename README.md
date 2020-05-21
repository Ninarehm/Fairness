# Fairness- Statistical Equity: A Fairness Classification Objective

Code implementation for Statistical Equity: A Fairness Classification Objective

## Fairness Gain
To run the code with the equity objective for fairness gain results:

```bash
python equity.py --loss_type equity --beta 0.5
```

To run the code with the equality objective for fairness gain results:

```bash
python equity.py --loss_type equality --beta 0.5
```

To run the code for fairness gain results with basic classifier objective set the beta value to be zero :

```bash
python equity.py --beta 0.0
```
## Feedback Loop
To run the feedback loop experiments use:
```bash
python equity_feedback_loop.py --loss_type equity --beta 0.5
```
```bash
python equity_feedback_loop.py --loss_type equality --beta 0.5
```
```bash
python equity_feedback_loop.py --loss_type classifier --beta 0.0
```

## Citation
The paper for this Github:
https://arxiv.org/pdf/2005.07293.pdf
Please cite the paper when using the code in this GitHub repository.
 ```
@article{mehrabi2020statistical,
  title={Statistical Equity: A Fairness Classification Objective},
  author={Mehrabi, Ninareh and Huang, Yuzhong and Morstatter, Fred},
  journal={arXiv preprint arXiv:2005.07293},
  year={2020}
}
 ```


The Adult dataset is coming from:
http://archive.ics.uci.edu/ml/datasets/Adult
Please cite the dataset sources for using the dataset.
