"""The Ratio Method.

A framework for characterizing a category of harm across seven factors:
Frequency, Average Damages, Social Value 1 and 2, Type of Harm, and
Litigation Costs 1 and 2. See README.md for a full description.
"""


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
