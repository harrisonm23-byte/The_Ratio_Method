# The Ratio Method

A framework for characterizing a category of harm (a tort, an activity, a product
class) by breaking it into seven factors. Two of the factors are ratios — how often
the harm occurs relative to the exposed population, and how large the typical harm
is relative to economic output — which is where the method gets its name. The rest
capture the social value of the activity, the mechanism of the harm, and the cost
of litigating it.

## The seven factors

| Factor | Key | What it measures | Type |
|---|---|---|---|
| Frequency | `Frequency` | How often the harm occurs: incidents relative to the exposed population (`incident_count / population`). | ratio (float) |
| Average Damages | `Average_Damages` | The typical size of harm per incident, compared against economic output (`total_damages / gdp_per_capita`). Corresponds to what Gifford refers to as "severity." | ratio (float) |
| Social Value 1  | `SV1` | The economic value that the activity adds — its productive benefit to society. | `int` |
| Social Value 2  | `SV2` | The cultural inclination toward the activity — its value beyond pure economics. | `str` |
| Type of Harm | `Type_Harm` | A classification across the six dimensions in [Type of Harm](#type-of-harm-th) below. Every axis is categorical — none is quantitative. | `str` |
| Litigation Costs 1 | `LC1` | The cost structure of bringing a claim — information costs versus claim costs (Landes & Posner). | `int` |
| Litigation Costs 2 | `LC2` | The difficulty of proving liability (Gifford factor 3). | `int` (see [Notes](#notes--open-questions)) |

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
| `incident_count` | Number of incidents of the harm over the period studied. |
| `population` | Size of the population exposed to the harm over the same period. |
| `total_damages` | Total (or typical per-incident) damages, in the same currency as `gdp_per_capita`. |
| `gdp_per_capita` | GDP per capita, used to normalize damages against economic output. |
| `sv1` | Social Value 1 — economic/productive benefit of the activity. |
| `sv2` | Social Value 2 — cultural inclination toward the activity. |
| `th` | Type of Harm — one value from each of the six `TYPE_OF_HARM` axes. |
| `lc1` | Litigation Costs 1 — information costs versus claim costs. |
| `lc2` | Litigation Costs 2 — difficulty of proving liability. |

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

- **LC2 scale.** LC2 is currently cast to `int`, but it could equally be a string
  (e.g., `"low"`, `"moderate"`, `"high"`) or an integer (e.g., 1–10), depending on
  how it ends up being defined.
- **Encoding `th`.** The function accepts Type of Harm as a single string. The
  `TYPE_OF_HARM` dictionary defines the allowed values for each axis; a harm should
  be described by one value from each of the six axes.

## References

- Gifford — "severity" (Average Damages) and factor 3, difficulty of proving liability (LC2).
- Landes & Posner — information costs versus claim costs (LC1).
