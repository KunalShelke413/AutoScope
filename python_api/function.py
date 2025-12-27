import pandas as pd
def note4bar(grouped):
    if isinstance(grouped, pd.DataFrame):
        category_totals = grouped.sum(axis=1)
    else:
        category_totals = grouped
    T3 = category_totals.sort_values(ascending=False).head(3).to_dict()
    L3 = category_totals.sort_values().head(3).to_dict()
    avg_value = category_totals.mean()
    median_value = category_totals.median()
    closest_to_avg = (
        (category_totals - avg_value)
        .abs()
        .sort_values()
        .head(2)
        .index
    )
    closest_to_avg_vals = category_totals.loc[closest_to_avg].to_dict()
    Q1 = category_totals.quantile(0.25)
    Q2 = category_totals.quantile(0.5)
    Q3 = category_totals.quantile(0.75)
    IQR = Q3 - Q1
    outliers = category_totals[
        (category_totals < Q1 - 1.5 * IQR) |
        (category_totals > Q3 + 1.5 * IQR)
    ].to_dict()
    insights = []
    top_cat, top_val = category_totals.idxmax(), category_totals.max()
    low_cat, low_val = category_totals.idxmin(), category_totals.min()
    insights.append(
        f"\nThe highest performing category is '{top_cat}' with a total value of {top_val:.2f}.\n"
    )
    insights.append(
        f"The lowest performing category is '{low_cat}' with a total value of {low_val:.2f}.\n"
    )
    insights.append(
        f"The average value across all categories is {avg_value:.2f}, with a median of {median_value:.2f}.\n"
    )
    for cat, val in closest_to_avg_vals.items():
        insights.append(
            f"The category '{cat}' ({val:.2f}) is close to the overall average.\n"
        )
    if outliers:
        insights.append(
            "Outliers detected in categories: " +
            ", ".join([f"{k} ({v:.2f})" for k, v in outliers.items()])+"\n"
        )
    else:
        insights.append("No significant outliers were detected in the data.\n")
    note=""
    for i in insights:
       note+=i
    note+="\nTop 3 Bars:\n"
    for key,value in T3.items():
        note+=f"{key} >>> {value} \n"
    note+="\nBottom 3 Bars:\n"
    for key,value in L3.items():
        note+=f"{key} >>> {value} \n"
    note+="\nFirst Quartile: "+str(Q1)+"\nThird Quartile: "+str(Q3)+"\n"
    note+="\nOutliers:\n"
    if outliers.items():
       for key,value in outliers.items():
        note+=f"{key} >>> {value} \n"
    else:
       note+="None\n"
    note+="\n"
    return note

def note4pie(grouped):
    if isinstance(grouped, pd.DataFrame):
        category_totals = grouped.sum(axis=1)
    else:  
        category_totals = grouped
    total_sum = category_totals.sum()
    percentages = (category_totals / total_sum) * 100
    T3 = percentages.sort_values(ascending=False).head(20).to_dict()
    top_cat = percentages.idxmax()
    top_val = percentages.max()
    low_cat = percentages.idxmin()
    low_val = percentages.min()
    sorted_pct = percentages.sort_values()
    near_equal = {}
    for i in range(len(sorted_pct) - 1):
        diff = abs(sorted_pct.iloc[i] - sorted_pct.iloc[i + 1])
        if diff < 2:
            near_equal[sorted_pct.index[i]] = sorted_pct.iloc[i]
            near_equal[sorted_pct.index[i + 1]] = sorted_pct.iloc[i + 1]
    note = ""
    note += "\nSlices Contributors:\n"
    for key, value in T3.items():
        note += f"{key} >>> {value:.2f}%\n"
    note += (
        f"\nThe largest share in the pie chart is '{top_cat}', contributing {top_val:.2f}% of the total.\n"
    )
    note += (
        f"The smallest slice is '{low_cat}', contributing only {low_val:.2f}%.\n"
    )
    if top_val > 50:
        note += (
            f"'{top_cat}' dominates the distribution, accounting for more than half of the total.\n"
        )
    if near_equal:
        note += "\nSome categories have nearly equal contributions:\n"
        for k, v in near_equal.items():
            note += f"{k} >>> {v:.2f}%\n"
    note += (
        "\nThis pie chart highlights how the total value is distributed across categories, "
        "making it easy to identify dominant and minor contributors.\n"
    )
    note+="\n"
    return note

def note4histogram(series):
    if series is None or series.empty:
        return "No data available to generate histogram insights.\n"
    series = pd.to_numeric(series, errors="coerce").dropna()
    if series.empty:
        return "Histogram cannot be generated due to non-numeric data.\n"
    note = ""
    min_val = series.min()
    max_val = series.max()
    mean_val = series.mean()
    median_val = series.median()
    std_val = series.std()
    Q1 = series.quantile(0.25)
    Q2 = series.quantile(0.5)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    skewness = series.skew()
    outliers = series[
        (series < Q1 - 1.5 * IQR) |
        (series > Q3 + 1.5 * IQR)
    ]
    note += (
        f"The values in this histogram range from {min_val:.2f} to {max_val:.2f}.\n"
    )
    note += (
        f"The average value is {mean_val:.2f}, with a median of {median_val:.2f}.\n"
    )
    if skewness > 0.5:
        note += "The distribution is right-skewed, with a longer tail towards higher values.\n"
    elif skewness < -0.5:
        note += "The distribution is left-skewed, with a longer tail towards lower values.\n"
    else:
        note += "The distribution is approximately symmetric.\n"
    note += (
        f"Most values fall between {Q1:.2f} and {Q3:.2f}, indicating the central spread of the data.\n"
    )
    if not outliers.empty:
        note += (
            f"{len(outliers)} potential outliers were detected outside the typical range.\n"
        )
    else:
        note += "No significant outliers were detected in the data.\n"
    note += (
        "\nThis histogram helps visualize the frequency distribution of the data, "
        "highlighting patterns, spread, and skewness.\n"
    )
    note+="\n"
    return note
def note4scatter(x, y, x_name, y_name):
    note = ""
    if x is None or y is None:
        note="Insufficient data to generate scatter plot insights.\n"
        return note
    df = pd.DataFrame({x_name: x, y_name: y})
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    if df.empty:
        note="Scatter plot cannot be generated due to non-numeric data.\n"
        return note
    corr = df[x_name].corr(df[y_name])
    x_min, x_max = df[x_name].min(), df[x_name].max()
    y_min, y_max = df[y_name].min(), df[y_name].max()
    x_std, y_std = df[x_name].std(), df[y_name].std()
    if corr >= 0.7:
        trend = "a strong positive relationship"
    elif corr >= 0.3:
        trend = "a moderate positive relationship"
    elif corr <= -0.7:
        trend = "a strong negative relationship"
    elif corr <= -0.3:
        trend = "a moderate negative relationship"
    else:
        trend = "little to no clear relationship"
    def find_outliers(series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        return (series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)
    outliers = df[find_outliers(df[x_name]) | find_outliers(df[y_name])]
    note += (
        f"The scatter plot shows {trend} between '{x_name}' and '{y_name}'.\n"
    )
    note += (
        f"The correlation coefficient is {corr:.2f}, indicating the strength of the relationship.\n"
    )
    note += (
        f"'{x_name}' values range from {x_min:.2f} to {x_max:.2f}, "
        f"while '{y_name}' values range from {y_min:.2f} to {y_max:.2f}.\n"
    )
    note += (
        f"The spread of the data suggests variability of approximately "
        f"{x_std:.2f} in '{x_name}' and {y_std:.2f} in '{y_name}'.\n"
    )
    if not outliers.empty:
        note += (
            f"{len(outliers)} potential outliers were identified, "
            f"which may influence the observed relationship.\n"
        )
    else:
        note += "No significant outliers were detected in the data.\n"
    note += (
        "\nThis scatter plot helps identify relationships, trends, and unusual data points "
        "between the two variables.\n"
    )
    note+="\n"
    return note

def note4boxplot(series, col_name):
    if series is None or series.empty:
        return "No data available to generate box plot insights.\n"
    series = pd.to_numeric(series, errors="coerce").dropna()
    if series.empty:
        return "Box plot cannot be generated due to non-numeric data.\n"
    note = ""
    Q1 = series.quantile(0.25)
    Q2 = series.quantile(0.50) 
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    min_val = series.min()
    max_val = series.max()
    outliers = series[
        (series < Q1 - 1.5 * IQR) |
        (series > Q3 + 1.5 * IQR)
    ]
    if Q2 > (Q1 + Q3) / 2:
        skew = "right-skewed"
    elif Q2 < (Q1 + Q3) / 2:
        skew = "left-skewed"
    else:
        skew = "approximately symmetric"
    note += (
        f"The median value of '{col_name}' is {Q2:.2f}.\n"
    )
    note += (
        f"The middle 50% of the data lies between {Q1:.2f} (Q1) and {Q3:.2f} (Q3).\n"
    )
    note += (
        f"The interquartile range (IQR) is {IQR:.2f}, representing the data spread.\n"
    )
    note += (
        f"Values range from {min_val:.2f} to {max_val:.2f} overall.\n"
    )
    note += (
        f"The distribution appears {skew} based on the box plot.\n"
    )
    if not outliers.empty:
        note += (
            f"{len(outliers)} potential outliers were detected outside the whiskers.\n"
        )
    else:
        note += "No significant outliers were detected in the data.\n"
    note += (
        "\nThis box plot provides a compact summary of the data distribution, "
        "making it useful for comparing variability and detecting outliers.\n"
    )
    note+="\n"
    return note

def note4line(series, x_name, y_name):
    if series is None or series.empty:
        return "No data available to generate line chart insights.\n"
    series = pd.to_numeric(series, errors="coerce").dropna()
    if len(series) < 2:
        return "Insufficient data points to analyze line chart trends.\n"
    note = ""
    start_val = series.iloc[0]
    end_val = series.iloc[-1]
    min_val = series.min()
    max_val = series.max()
    mean_val = series.mean()
    delta = end_val - start_val
    pct_change = (delta / abs(start_val)) * 100 if start_val != 0 else None
    if delta > 0:
        trend = "upward"
    elif delta < 0:
        trend = "downward"
    else:
        trend = "flat"
    volatility = series.std()
    peak_idx = series.idxmax()
    trough_idx = series.idxmin()
    diffs = series.diff().dropna()
    spikes = diffs[abs(diffs) > diffs.std() * 2]
    note += (
        f"The line chart shows an overall {trend} trend in '{y_name}'.\n"
    )
    note += (
        f"The values start at {start_val:.2f} and end at {end_val:.2f}.\n"
    )
    if pct_change is not None:
        note += (
            f"This represents a change of {pct_change:.2f}% over the observed period.\n"
        )
    note += (
        f"The highest value ({max_val:.2f}) occurs at {peak_idx}, "
        f"while the lowest value ({min_val:.2f}) occurs at {trough_idx}.\n"
    )
    note += (
        f"The average value across the series is {mean_val:.2f}, "
        f"with a volatility (standard deviation) of {volatility:.2f}.\n"
    )
    if not spikes.empty:
        note += (
            f"{len(spikes)} sudden changes were detected, indicating sharp increases or drops.\n"
        )
    else:
        note += "No significant sudden changes were detected in the series.\n"
    note += (
        "\nThis line chart highlights how values evolve over time or sequence, "
        "making it useful for identifying trends, cycles, and anomalies.\n"
    )
    note+="\n"
    return note

def note4area(series, x_name, y_name):
    if series is None or series.empty:
        return "No data available to generate area chart insights.\n"
    series = pd.to_numeric(series, errors="coerce").dropna()
    if len(series) < 2:
        return "Insufficient data points to analyze area chart trends.\n"
    note = ""
    start_val = series.iloc[0]
    end_val = series.iloc[-1]
    min_val = series.min()
    max_val = series.max()
    mean_val = series.mean()
    delta = end_val - start_val
    pct_change = (delta / abs(start_val)) * 100 if start_val != 0 else None
    if delta > 0:
        trend = "increasing"
    elif delta < 0:
        trend = "decreasing"
    else:
        trend = "stable"
    total_area = series.sum()
    volatility = series.std()
    peak_idx = series.idxmax()
    trough_idx = series.idxmin()
    note += (
        f"The area chart shows an overall {trend} trend in '{y_name}'.\n"
    )
    note += (
        f"The values start at {start_val:.2f} and end at {end_val:.2f}.\n"
    )
    if pct_change is not None:
        note += (
            f"This represents a change of {pct_change:.2f}% over the observed period.\n"
        )
    note += (
        f"The highest value ({max_val:.2f}) occurs at {peak_idx}, "
        f"while the lowest value ({min_val:.2f}) occurs at {trough_idx}.\n"
    )
    note += (
        f"The cumulative total across the chart is {total_area:.2f}, "
        f"highlighting the overall contribution over time.\n"
    )
    note += (
        f"The average value is {mean_val:.2f}, "
        f"with a variability of {volatility:.2f}.\n"
    )
    note += (
        "\nThis area chart emphasizes the magnitude and cumulative behavior of values over time, "
        "making it effective for visualizing growth patterns and overall impact.\n"
    )
    note+="\n"
    return note
def note4bubble(x, y, size, x_name, y_name, size_name):
    if x is None or y is None or size is None:
        return "Insufficient data to generate bubble chart insights.\n"
    df = pd.DataFrame({
        x_name: x,
        y_name: y,
        size_name: size
    })
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    if df.empty:
        return "Bubble chart cannot be generated due to non-numeric data.\n"
    note = ""
    corr = df[x_name].corr(df[y_name])
    x_min, x_max = df[x_name].min(), df[x_name].max()
    y_min, y_max = df[y_name].min(), df[y_name].max()
    size_min, size_max = df[size_name].min(), df[size_name].max()
    largest_idx = df[size_name].idxmax()
    largest_x = df.loc[largest_idx, x_name]
    largest_y = df.loc[largest_idx, y_name]
    largest_size = df.loc[largest_idx, size_name]
    if corr >= 0.7:
        trend = "a strong positive relationship"
    elif corr >= 0.3:
        trend = "a moderate positive relationship"
    elif corr <= -0.7:
        trend = "a strong negative relationship"
    elif corr <= -0.3:
        trend = "a moderate negative relationship"
    else:
        trend = "little to no clear relationship"
    Q1 = df[size_name].quantile(0.25)
    Q3 = df[size_name].quantile(0.75)
    IQR = Q3 - Q1
    size_outliers = df[
        (df[size_name] < Q1 - 1.5 * IQR) |
        (df[size_name] > Q3 + 1.5 * IQR)
    ]
    note += (
        f"The bubble chart shows {trend} between '{x_name}' and '{y_name}'.\n"
    )
    note += (
        f"'{x_name}' ranges from {x_min:.2f} to {x_max:.2f}, "
        f"while '{y_name}' ranges from {y_min:.2f} to {y_max:.2f}.\n"
    )
    note += (
        f"Bubble sizes ('{size_name}') range from {size_min:.2f} to {size_max:.2f}.\n"
    )
    note += (
        f"The largest bubble appears at ({largest_x:.2f}, {largest_y:.2f}) "
        f"with a size value of {largest_size:.2f}, indicating a dominant observation.\n"
    )
    if not size_outliers.empty:
        note += (
            f"{len(size_outliers)} unusually large or small bubbles were detected, "
            f"which may strongly influence interpretation.\n"
        )
    else:
        note += "No significant size-based outliers were detected.\n"
    note += (
        "\nThis bubble chart helps visualize multi-dimensional relationships by combining "
        "position and size, making it effective for identifying dominant and unusual data points.\n"
    )
    note+="\n"
    return note

