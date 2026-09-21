# The Ratio Method

The Ratio Method is a systematic way to design regulation for novel risks posed by AI. The framework profiles an activity, product, or industry by a set of variables. The risk is then matched to a precedent liability regime with similar / matching variables.

The model begins with how much of the population may incur harm (**Frequency**), and how large the harm is on average (**Average Damages**). It then profiles the economic and cultural value of the activity (**Social Value 1 and 2**), the mechanism of the harm (**Type of Harm**), and the cost of potential litigation (**Litigation Costs 1 and 2**).

## [The Ratio Method report: Precedents](https://harrisonm23-byte.github.io/The_Ratio_Method/)

The Precedents report applies the method to the risks named in the International AI Safety Report 2026, and compares each to sixteen existing liability regimes.

## Source

Harrison C. Margolin & Grant H. Frazier, *The Ratio Method: Addressing Complex Tort
Liability in the Fourth Industrial Revolution*, 52 St. Mary's L.J. 679 (2021).  [Article page](https://commons.stmarytx.edu/thestmaryslawjournal/vol52/iss3/4/) · [Full text (PDF)](https://commons.stmarytx.edu/cgi/viewcontent.cgi?article=1115&context=thestmaryslawjournal).

## The Ratio Method variables

<table>
  <thead>
    <tr>
      <th width="16%">Factor</th>
      <th width="14%">Key</th>
      <th width="60%">What it measures</th>
      <th width="10%">Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Frequency</td>
      <td><code>Frequency</code></td>
      <td>How often the harm occurs: <code>incident_count / population</code>.</td>
      <td>ratio</td>
    </tr>
    <tr>
      <td>Average Damages</td>
      <td><code>Average_Damages</code></td>
      <td>The typical size of harm per incident, compared against economic output (<code>total_damages / gdp_per_capita</code>).</td>
      <td>ratio</td>
    </tr>
    <tr>
      <td>Social Value 1</td>
      <td><code>SV1</code></td>
      <td>The economic value that the activity adds — its productive benefit to society.</td>
      <td><code>int</code></td>
    </tr>
    <tr>
      <td>Social Value 2</td>
      <td><code>SV2</code></td>
      <td>The cultural inclination toward the activity — its value beyond pure economics.</td>
      <td><code>str</code></td>
    </tr>
    <tr>
      <td>Type of Harm</td>
      <td><code>Type_Harm</code></td>
      <td>The mechanism of the harm, classified along the six axes in <a href="#type-of-harm-th">Type of Harm</a>.</td>
      <td><code>str</code></td>
    </tr>
    <tr>
      <td>Litigation Costs 1</td>
      <td><code>LC1</code></td>
      <td>The cost structure of bringing a claim — information costs versus claim costs (Landes &amp; Posner).</td>
      <td><code>int</code></td>
    </tr>
    <tr>
      <td>Litigation Costs 2</td>
      <td><code>LC2</code></td>
      <td>The difficulty of proving liability – specifically, breach or causation.</td>
      <td><code>int</code></td>
    </tr>
  </tbody>
</table>

## Implementation

The code below lives in [`ratio_method.py`](ratio_method.py).

```python
def ratio_method(incident_count, population, total_damages, gdp_per_capita,
                 sv1: int, sv2: str, th: str, lc1: int, lc2: int):

    return {
        # Frequency (F): how often the harm occurs, incidents relative to
        # the exposed population.
        "Frequency": incident_count / population,

        # Average Damages (AD): the typical size of harm per incident,
        # compared against economic output (GDP per capita). Corresponds to what
        # Gifford refers to as "severity."
        "Average_Damages": total_damages / gdp_per_capita,

        # Social Value 1 (SV1): the economic value that the activity adds —
        # its productive benefit to society.
        "SV1": int(sv1),

        # Social Value 2 (SV2): the cultural inclination toward the
        # activity — its value beyond pure economics.
        "SV2": str(sv2),

        # Type of Harm (TH): a classification across the six dimensions in
        # TYPE_OF_HARM below (type of injury, defendant's role, physical
        # agent, onset, location, reason). Every axis is categorical — none
        # is quantitative.
        "Type_Harm": str(th),

        # Litigation Costs 1 (LC1): the cost structure of bringing a claim —
        # information costs versus claim costs (Landes & Posner).
        "LC1": int(lc1),

        # Litigation Costs 2 (LC2): the difficulty
        # of proving liability (Gifford factor 3).
        "LC2": int(lc2)
        # LC2 can be a string (e.g., "low", "moderate", "high") or an integer (e.g., 1-10), depending on how we define it.
    }

# Type of Harm (TH): the article's "mechanisms of action" classification.
# Each harm is characterized across SIX dimensions, each with its own set of values.
# A real harm is one value drawn from each axis.
TYPE_OF_HARM = {
    "type_of_injury":     ["Physical/Medical", "Financial", "Environmental", "Rights Violation"],
    "defendants_role":    ["Direct Action", "Product Developer", "Failure of Oversight", "Vicarious/Passive"],
    "physical_agent":     ["Defendant", "Product/Device", "Third-Party(s)", "Non-Product Physical Object"],
    "onset_of_injury":    ["Immediate/Imminent", "Definite Future", "Prolonged", "Uncertain"],
    "location_of_injury": ["Proximate Zone", "Spanning Zone", "Sporadic", "Intangible/Internet"],
    "reason_for_injury":  ["Malice", "Negligence", "Recklessness", "Pure Accident"],
}
```

### Inputs

| Parameter | Description |
|---|---|
| `incident_count` | Number of incidents. |
| `population` | Size of the exposed population. |
| `total_damages` | Damages, in the same currency as GDP per capita. |
| `gdp_per_capita` | GDP per capita. |
| `sv1` | Social Value 1. |
| `sv2` | Social Value 2. |
| `th` | Type of Harm: one value from each of the six axes. |
| `lc1` | Litigation Costs 1. |
| `lc2` | Litigation Costs 2. |

### Example

```python
result = ratio_method(
    incident_count=1_200,
    population=100_000,
    total_damages=250_000,
    gdp_per_capita=65_000,
    sv1=7,
    sv2="widely accepted",
    th="Physical/Medical | Product Developer | Product/Device | Prolonged | Sporadic | Negligence",
    lc1=4,
    lc2=6,
)

# {
#     "Frequency": 0.012,
#     "Average_Damages": 3.846...,
#     "SV1": 7,
#     "SV2": "widely accepted",
#     "Type_Harm": "Physical/Medical | Product Developer | Product/Device | Prolonged | Sporadic | Negligence",
#     "LC1": 4,
#     "LC2": 6,
# }
```

## Type of Harm (TH)

Type of Harm is the article's "mechanisms of action" classification. Each harm is
characterized across **six dimensions**, each with its own set of values. A real harm
is one value drawn from each axis. Every axis is categorical — none is quantitative.

| Dimension | Key | Values |
|---|---|---|
| Type of injury | `type_of_injury` | Physical/Medical · Financial · Environmental · Rights Violation |
| Defendant's role | `defendants_role` | Direct Action · Product Developer · Failure of Oversight · Vicarious/Passive |
| Physical agent | `physical_agent` | Defendant · Product/Device · Third-Party(s) · Non-Product Physical Object |
| Onset of injury | `onset_of_injury` | Immediate/Imminent · Definite Future · Prolonged · Uncertain |
| Location of injury | `location_of_injury` | Proximate Zone · Spanning Zone · Sporadic · Intangible/Internet |
| Reason for injury | `reason_for_injury` | Malice · Negligence · Recklessness · Pure Accident |

## Notes / open questions

- **Societal Cost-Benefit Analysis.** Note that Frequency x Average Damages = Total Cost of Harm / GDP. Compared to Social Value, the initial question is therefore an aggregate societal cost-benefit analysis. The method then inspects the constituents of this inequality to find a match. 
- **LC2 scale.** LC2 is currently cast to `int`, but it could equally be a string
  (e.g., `"low"`, `"moderate"`, `"high"`) or an integer (e.g., 1–10), depending on
  how it ends up being defined.
- **Encoding `th`.** The function accepts Type of Harm as a single string. The
  `TYPE_OF_HARM` dictionary defines the allowed values for each axis; a harm should
  be described by one value from each of the six axes.

## References

- Harrison C. Margolin & Grant H. Frazier, *The Ratio Method: Addressing Complex Tort Liability in the Fourth Industrial Revolution*, 52 St. Mary's L.J. 679 (2021). [Article page](https://commons.stmarytx.edu/thestmaryslawjournal/vol52/iss3/4/) · [Full text (PDF)](https://commons.stmarytx.edu/cgi/viewcontent.cgi?article=1115&context=thestmaryslawjournal). The article this framework and its "mechanisms of action" classification are drawn from.
- Gifford — "severity" (Average Damages) and factor 3, difficulty of proving liability (LC2).
- Landes & Posner — information costs versus claim costs (LC1).
