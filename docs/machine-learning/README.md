# Machine learning

Machine learning (ML) is a set of methods for **prediction**: given what you know about someone, what is the best guess about their outcome? Economists use it to forecast, to classify text and images, to pick control variables, and increasingly inside causal methods.

!!! info "What you will learn"
    How ML differs from econometrics · training and test data · overfitting and cross-validation · LASSO, decision trees and random forests · judging a classifier · ML for causal inference · where deep learning fits

    Examples predict whether a married woman works, using the Wooldridge `mroz` data from the [logit page](../econometrics/logit.md).

## Prediction versus causation

| | Econometrics | Machine learning |
|---|---|---|
| Main question | What is the **effect** of x on y? | What is the best **prediction** of y? |
| Focus | One coefficient, its standard error and its causal meaning | Accuracy on new data |
| Success means | A believable research design | Low error on data the model has never seen |
| Typical tools | OLS, IV, DiD, fixed effects | LASSO, random forests, boosting, neural networks |

!!! warning "A good predictor is not a causal effect"
    A random forest might find that owning a pool predicts high income. Building pools will not make anyone richer. Use ML to predict. Use the [econometrics methods](../econometrics/index.md) to estimate effects.

## The core idea: test on data the model has not seen

A flexible model can memorize its data, including the noise. It then looks great on that data and does badly on new data. This is **overfitting**.

The fix is to hold data back:

1. **Split** the data into a **training set** (often 75–80%) and a **test set**.
2. **Fit** every model on the training set only.
3. **Tune** model settings with **cross-validation** inside the training set: split it into, say, 5 folds, train on 4, check on the 5th, and rotate.
4. **Judge** the final models once, on the test set.

## Models to know

| Model | Idea | Strengths |
|---|---|---|
| **Logistic or linear regression** | The baseline | Fast, interpretable. Often hard to beat on small data. |
| **LASSO** | Regression with a penalty that shrinks weak coefficients to exactly zero | Picks variables automatically, handles many predictors |
| **Ridge** | Like LASSO, but shrinks coefficients without zeroing them | Stable when predictors are correlated |
| **Decision tree** | Splits the data into groups with yes/no questions | Easy to explain, but overfits on its own |
| **Random forest** | Averages hundreds of trees, each built on a random sample | Strong default, captures interactions automatically |
| **Gradient boosting** (XGBoost, LightGBM) | Builds trees one at a time, each fixing the last one's errors | Often the most accurate on tables of data |

## Run it

Predict whether a woman is in the labor force (`inlf`) from 13 characteristics. Compare a logit, a LASSO logit and a random forest.

=== "Python"

    ```python
    # pip install scikit-learn wooldridge
    import pandas as pd
    import wooldridge
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    mroz = wooldridge.data("mroz")
    features = ["nwifeinc", "educ", "exper", "expersq", "age", "kidslt6", "kidsge6",
                "huseduc", "husage", "unem", "city", "motheduc", "fatheduc"]
    X, y = mroz[features], mroz["inlf"]

    # 1. Split: 75% train, 25% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)

    # 2. Models (LASSO and logit need standardized predictors)
    models = {
        "Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "LASSO logistic": make_pipeline(StandardScaler(),
                                        LogisticRegression(penalty="l1", solver="liblinear", C=0.1)),
        "Random forest": RandomForestClassifier(n_estimators=500, min_samples_leaf=5, random_state=42),
    }

    # 3. Fit on training data, judge on test data
    for name, model in models.items():
        model.fit(X_train, y_train)
        prob = model.predict_proba(X_test)[:, 1]
        cv_auc = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc").mean()
        print(f"{name:20s} accuracy {accuracy_score(y_test, prob > 0.5):.3f}  "
              f"AUC {roc_auc_score(y_test, prob):.3f}  5-fold CV AUC {cv_auc:.3f}")

    # Which variables matter most to the forest?
    rf = models["Random forest"]
    pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False).head()
    ```

    `C` sets the LASSO penalty: smaller values zero out more coefficients. `LogisticRegressionCV` chooses it by cross-validation.

=== "R"

    ```r
    # install.packages(c("glmnet", "ranger", "pROC", "wooldridge"))
    library(glmnet)    # LASSO
    library(ranger)    # random forests
    library(pROC)      # AUC

    data("mroz", package = "wooldridge")
    features <- c("nwifeinc", "educ", "exper", "expersq", "age", "kidslt6", "kidsge6",
                  "huseduc", "husage", "unem", "city", "motheduc", "fatheduc")

    # 1. Split: 75% train, 25% test
    set.seed(42)
    rows  <- sample(nrow(mroz), size = 0.75 * nrow(mroz))
    train <- mroz[rows, ]
    test  <- mroz[-rows, ]
    f <- reformulate(features, response = "inlf")

    # 2. Logit
    logit   <- glm(f, data = train, family = binomial)
    p_logit <- predict(logit, newdata = test, type = "response")

    # 3. LASSO logit, penalty chosen by 10-fold cross-validation
    cv_lasso <- cv.glmnet(as.matrix(train[, features]), train$inlf, family = "binomial")
    p_lasso  <- predict(cv_lasso, newx = as.matrix(test[, features]),
                        s = "lambda.1se", type = "response")[, 1]
    coef(cv_lasso, s = "lambda.1se")      # dots are coefficients set to zero

    # 4. Random forest
    rf <- ranger(f, data = transform(train, inlf = factor(inlf)), num.trees = 500,
                 min.node.size = 5, probability = TRUE, importance = "impurity", seed = 42)
    p_rf <- predict(rf, data = test)$predictions[, "1"]

    # 5. Judge on the test set
    for (p in list(p_logit, p_lasso, p_rf)) {
      cat("accuracy", mean((p > 0.5) == test$inlf), " AUC", auc(test$inlf, p, quiet = TRUE), "\n")
    }
    sort(importance(rf), decreasing = TRUE)
    ```

=== "Stata"

    ```stata
    bcuse mroz, clear
    local x "nwifeinc educ exper expersq age kidslt6 kidsge6 huseduc husage unem city motheduc fatheduc"

    * 1. Split: 75% train (sample == 1), 25% test (sample == 2)
    set seed 42
    splitsample, generate(sample) split(0.75 0.25)

    * 2. Logit, judged on the test set
    logit inlf `x' if sample == 1
    estat classification if sample == 2      // accuracy
    lroc inlf if sample == 2                 // AUC and ROC curve

    * 3. LASSO logit, penalty chosen by cross-validation
    lasso logit inlf `x' if sample == 1, selection(cv) rseed(42)
    lassocoef                                // which variables were kept
    predict p_lasso, pr
    roctab inlf p_lasso if sample == 2       // AUC
    ```

    Stata 16 and later include `lasso`, `ridge` and `elasticnet`. For random forests, install `rforest` from SSC.

## Read the output

Results on the test set (Python version; your numbers will move a little with a different split):

| Model | Accuracy | AUC |
|---|---:|---:|
| Always guess "works" (baseline) | 0.566 | 0.500 |
| Logistic regression | 0.688 | 0.764 |
| LASSO logistic | 0.704 | 0.766 |
| Random forest | 0.720 | 0.770 |

| Measure | Meaning |
|---|---|
| **Accuracy** | Share of test cases predicted correctly. Always compare it with the baseline of guessing the most common answer. |
| **AUC** | The chance the model ranks a random working woman above a random non-working woman. 0.5 is a coin flip, 1 is perfect. |
| **Cross-validated AUC** | AUC averaged over folds of the training data. Use it to choose between models **before** touching the test set. |
| **Feature importance** | How much each variable helps the forest's predictions. Experience and other family income matter most here. Importance is not a causal effect. |

**What this shows:** with 753 observations and 13 predictors, the three models perform about the same in every language we tried. Flexible models such as random forests shine with large datasets and complicated interactions. On small, tidy data, a logit is hard to beat and far easier to explain.

**LASSO picks variables:** in the Python model, it set 5 of the 13 coefficients to exactly zero, including husband's age and education. R's cross-validated LASSO keeps only education, experience, age and young children.

## Machine learning for causal inference

ML can also help estimate causal effects, when used carefully:

| Method | What ML does | Tools |
|---|---|---|
| **Double/debiased ML** | Predicts the outcome and the treatment from many controls, then estimates the effect from what is left over | Stata `dsregress`, `poregress`; R and Python [DoubleML](https://docs.doubleml.org/) |
| **Post-double-selection LASSO** | Uses LASSO to choose which controls to include | Stata `dsregress`; R `hdm` |
| **Causal forests** | Estimate how a treatment effect varies across people | R [grf](https://grf-labs.github.io/grf/); Python [EconML](https://econml.azurewebsites.net/) |

The design still has to come first: these tools help with many controls and flexible relationships, not with an omitted variable you never measured.

## Deep learning

Deep learning uses **neural networks**: many layers of simple calculations that learn patterns in very large datasets. It powers image recognition, translation and large language models. Economists use it mostly for unstructured data: text (central bank statements, news, job ads), satellite images (night lights as a measure of economic activity) and audio.

For tables of numbers like the ones on this page, gradient boosting usually works as well or better, with far less effort.

- [Practical Deep Learning for Coders](https://course.fast.ai/): a free, hands-on course
- [PyTorch tutorials](https://pytorch.org/tutorials/): the most popular deep learning library in research

## Common mistakes

- **Testing on the training data.** It always looks good. Keep a test set aside until the end.
- **Data leakage.** Information from the test set, or from the future, sneaks into training. For example, standardizing with the mean of the full dataset, or using next month's sales to predict this month's. Use pipelines so every step learns from training data only.
- **Reading feature importance as causation.** It shows what helps prediction, not what causes the outcome.
- **Ignoring the baseline.** 90% accuracy is poor if 95% of cases are "no".
- **Reaching for complexity first.** Start with a regression, then see if anything beats it.

## Learn more

- [An Introduction to Statistical Learning](https://www.statlearning.com/): the standard first book, free, with R and Python editions
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)
- Mullainathan and Spiess (2017), "Machine Learning: An Applied Econometric Approach", *Journal of Economic Perspectives*: ML from an economist's point of view
