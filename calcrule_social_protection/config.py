CLASS_RULE_PARAM_VALIDATION = [
    {
        "class": "PaymentPlan",
        "parameters": [
            {
                "type": "number",
                "name": "fixed_batch",
                "label": {
                    "en": "Fixed amount",
                    "fr": "Lot fixe"
                },
                "rights": {
                    "read": "157101",
                    "write": "157102",
                    "update": "157103",
                    "replace": "157206"
                },
                "relevance": "True",
                "condition": "INPUT>=0",
                "default": "0"
            },
            {
                "type": "number",
                "name": "limit_per_single_transaction",
                "label": {
                    "en": "Limit Per Single Transaction",
                    "fr": "Limite par transaction unique"
                },
                "rights": {
                    "read": "157101",
                    "write": "157102",
                    "update": "157103",
                    "replace": "157206"
                },
                "relevance": "True",
                "condition": "INPUT>=0",
                "default": ""
            }
        ]
    }
]

FROM_TO = None

DESCRIPTION_CONTRIBUTION_VALUATION = F"" \
    F"This is example of calculation rule module," \
    F" skeleton generated automaticallly via command"
