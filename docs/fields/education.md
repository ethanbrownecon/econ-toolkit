# Economics of education

The economics of education studies how schooling is produced and what it is worth: class sizes, teachers, school funding, college access and the returns to a degree.

## Big questions

- Does more school spending raise student achievement?
- Do smaller classes help?
- How much do good teachers matter?
- Is college worth the cost, and for whom?
- Why do achievement gaps open up between groups of children?

## Methods you will use

[Randomized experiments](../econometrics/glossary.md#pr) · [regression discontinuity](../econometrics/rd.md) at test-score and enrollment cutoffs · [instrumental variables](../econometrics/iv.md) · [panel fixed effects](../econometrics/panel.md) for teachers and schools

## Data

| Source | What it has |
|---|---|
| [NCES Common Core of Data](https://nces.ed.gov/ccd/) | Every US public school and district: enrollment, staff, finances |
| [College Scorecard](https://collegescorecard.ed.gov/data/) | Costs, graduation rates and graduates' earnings for every college |
| [Opportunity Insights](https://opportunityinsights.org/data/) | Intergenerational mobility by college and neighborhood |
| [IPEDS](https://nces.ed.gov/ipeds/) | College admissions, enrollment and finances |

## Projects on this site

- [Instrumental variables](../econometrics/iv.md): the return to schooling, using distance to college
- [Project 1: Wages and education](../projects/wages.md)

## Starter project: does school spending raise test scores?

`meap93` has 408 Michigan high schools in 1993. Do schools that spend more per student have higher math pass rates?

| Variable | Meaning |
|---|---|
| `math10` | Percentage of 10th graders passing the state math test |
| `lexpend` | Log spending per student |
| `lnchprg` | Percentage of students in the school lunch program (a poverty measure) |
| `lenroll` | Log school enrollment |

=== "Stata"

    ```stata
    bcuse meap93, clear                   // ssc install bcuse
    regress math10 lexpend, vce(robust)
    regress math10 lexpend lnchprg lenroll, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("meap93", package = "wooldridge")

    simple   <- feols(math10 ~ lexpend, data = meap93, vcov = "hetero")
    controls <- feols(math10 ~ lexpend + lnchprg + lenroll, data = meap93, vcov = "hetero")
    etable(simple, controls)
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    meap93 = wooldridge.data("meap93")
    simple = pf.feols("math10 ~ lexpend", data=meap93, vcov="hetero")
    controls = pf.feols("math10 ~ lexpend + lnchprg + lenroll", data=meap93, vcov="hetero")
    pf.etable([simple, controls])
    ```

**Check:**

| Model | `lexpend` coefficient |
|---|---:|
| Spending only | 11.16 |
| With poverty and size | 7.75 (standard error 3.83) |

Spending is in logs, so a 10% increase in spending goes with a pass rate about 0.8 percentage points higher, after controls. Controlling for poverty shrinks the estimate by a third, because richer areas both spend more and have higher scores. The remaining estimate is only marginally significant and could still reflect other differences between schools. Michigan's 1994 school finance reform (Proposal A) changed spending sharply for some districts, a natural experiment researchers have used.

## More project ideas

1. **Class size.** Read about Tennessee's Project STAR, a randomized class-size experiment, in Krueger (1999).
2. **Is college worth it?** Use the College Scorecard to relate graduates' earnings to cost, by major and type of college.
3. **Enrollment cutoffs.** Some countries cap class size at 40, so a school with 41 students splits into two small classes. Read Angrist and Lavy (1999) for this [regression discontinuity](../econometrics/rd.md).
4. **Funding and poverty.** Use NCES district data to compare spending per student in high- and low-poverty districts in your state.

## Classic papers

- Krueger (1999), "Experimental Estimates of Education Production Functions", *Quarterly Journal of Economics*
- Angrist and Lavy (1999), "Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement", *Quarterly Journal of Economics*
- Chetty, Friedman and Rockoff (2014), "Measuring the Impacts of Teachers II: Teacher Value-Added and Student Outcomes in Adulthood", *American Economic Review*
