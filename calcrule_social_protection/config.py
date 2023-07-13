CLASS_RULE_PARAM_VALIDATION = [
    {
        "class": "PaymentPlan",
        "parameters": [
            {
                "type": "number",
                "name": "fixed_batch",
                "label": {
                    "en": "Fixed batch",
                    "fr": "Fixed batch"
                },
                "rights": {
                },
                "relevance": "True",
                "condition": "INPUT>=0",
                "default": "0"
            }
        ]
    }
]

FROM_TO = None

DESCRIPTION_CONTRIBUTION_VALUATION = F"" \
    F"This is example of calculation rule module," \
    F" skeleton generated automaticallly via command"
