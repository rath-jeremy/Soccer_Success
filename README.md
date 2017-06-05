(Jimmy) Hyun Jin Kim <hyunkim2015@u.northwestern.edu>  
Jeremy Rath <JeremyRath2020@u.northwestern.edu>  
EECS 349 Machine Learning  
Northwestern University

[Repository for codes and data](https://github.com/TheLordBlarg/Soccer_Success)  
[Detailed report](https://github.com/TheLordBlarg/Soccer_Success/raw/master/report/project_report.pdf)

# Motivation

Predicting the outcome of sports matches is one of the favorite topics for statisticians and
gamblers alike. It is an interesting problem where the question of the respective importance of
randomness (’luck’) and determinism (’skill’) is hotly debated. Of course, much importance also
lies in the fact that successful predictions can lead to lots of money. For soccer, previous prediction
methods mostly used team-level features while neglecting individual skills. We hypothesize
that individual skills are crucial to soccer and contain much information for predicting match
outcomes which those other methods are not utilizing. Therefore, in this project, we sought to
develop a machine learning strategy that predicts the outcomes of soccer matches based mainly
on the individual attributes of the players on each team.

# Approach

Our novel approach uses in-game stats from the Electronic Arts' celebrated game franchise FIFA, which were [painstakingly crafted by the experts](http://www.espnfc.us/blog/espn-fc-united-blog/68/post/2959703/fifa-17-player-ratings-system-blends-advanced-stats-and-subjective-scouting). Those numerical stats measuring skills falling under various categories such as attacking, defending, and goalkeeping were obtained from <https://sofifa.com>. This was then combined with the records of matches (obtained from <http://www.worldfootball.net>) to yield a dataset consisting of match outcomes and player stats. This dataset was then fed into Weka as well as a custom-made neural network algorithm for classification.

# Results

Unfortunately, our results were quite disappointing. Figure 1 shows the results of various Weka algorithms applied to the dataset. None of the algorithms performed significantly better than the ZeroR baseline, measured in terms of their 10-fold cross-validation accuracy. Logistic regression, which performed the best, only yielded a 3% improvement over the baseline. Furthermore, its test accuracy was significantly lower than the CV-accuracy, indicating that the generalization is poor.

![](report/figures/result_weka.png)
*Figure 1. Results from select algorithms in Weka*

Results 

![](report/figures/learning_curve.png)
*Figure 2. Typical learning curve for custom-made single layer neural network*

![](report/figures/result_features.png)
*Figure 3. List of select features ordered by their information gain. Full list available [in the repository](https://github.com/TheLordBlarg/Soccer_Success/blob/master/results/entropy_train.csv)*
