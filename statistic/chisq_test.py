import statsmodels.api as sm
mode = "part-total"

A_1 = 175
A_T = 9115
A_0 = A_T - A_1

B_1 = 116
B_T = 16104
B_0 = B_T - B_1

if mode == "part-total":
    contingency_table=sm.stats.Table2x2([[A_1,A_0], [B_1,B_0]])
    print("Summary informationis")
    print(contingency_table.summary())
    print(f"ORvalue is{contingency_table.oddsratio},pvalue is{contingency_table.oddsratio_pvalue()}")