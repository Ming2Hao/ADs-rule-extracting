#declare the rules for the rule-based approach
rules = [
    {
        "ad":"FAA AD 2025-23-53",
        "aircraft": [
            {
                "MD-11":{

                }

            }, 
            {
                "MD-11F":{

                }
            }, 
            {
                "MD-10-10F":{

                }
            }, 
            {
                "MD-10-30F":{

                }
            }, 
            {
                "DC-10-10":{

                }
            }, 
            {
                "DC-10-10F":{

                }
            }, 
            {
                "DC-10-15":{
                    
                }
            }, 
            {
                "DC-10-30":{
                    
                }
            }, 
            {
                "DC-10-30F":{
                    
                }
            }, 
            {
                "KC-10A":{
                    
                }
            }, 
            {
                "KDC-10":{
                    
                }
            }, 
            {
                "DC-10-40":{
                    
                }
            }, 
            {
                "DC-10-40F":{
                    
                }
            }
        ],
    },
    {
        "ad":"EASA AD 2025-0254",
        "aircraft": [
            {
                "A320-211":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                "a320-212":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                "A320-214":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                
                "A320-215":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                
                "A320-216":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                
                "A320-231":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                
                "A320-232":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
                
                "A320-233":
                    {
                        "exceptions":[
                            "mod 24591 (production)",
                            "SB A320-57-1089 Rev 04"
                        ]
                    },
            },
            {
  
                "A321-111":
                    {
                        "exceptions":[
                            "mod 24977 (production)"
                        ]
                    },
            },
            {

                "A231-112":
                    {
                        "exceptions":[
                            "mod 24977 (production)"
                        ]
                    },
            },
            {

                "A321-131":
                    {
                        "exceptions":[
                            "mod 24977 (production)"
                        ]
                    }
            },
        ],
    }
]

#function to check if an aircraft is affected by any of the rules
def check_rules(aircraft):
    """
    Check if an aircraft is affected by any of the rules.

    Args:
        aircraft (list of dict): A list of dictionaries containing the aircraft model and its modifications.

    Outputs:
        str: A string indicating whether the aircraft is affected by any ADs and the reason.
    """

    model_name = aircraft["aircraft model"]
    current_modifications = aircraft["modifications"]

    for rule in rules:
        ad_name = rule['ad']
        
        # Iterate through each aircraft configuration in the rule
        for aircraft_rule in rule["aircraft"]:
            
            # Skip if the rule does not apply to this specific model
            if model_name not in aircraft_rule:
                continue

            # Get the criteria details for this model
            criteria = aircraft_rule[model_name]
            exceptions = criteria.get("exceptions", [])

            # Check if the aircraft has a modification listed in exceptions
            for modification in exceptions:
                if modification in current_modifications:
                    return f"Aircraft {model_name} with modification {modification} is not affected by {ad_name}"

            # If no exceptions matched (or no exceptions existed), the aircraft is affected
            return f"Aircraft {model_name} is affected by {ad_name}"

    return f"Aircraft {model_name} is not affected by any ADs"           

def main():
    # aircrafts to test the rule checking
    aircrafts = [
        {
            "aircraft model": "MD-11",
            "MSN": "48123",
            "modifications": []
        },
        {
            "aircraft model": "DC-10-30F",
            "MSN": "47890",
            "modifications": []
        },
        {
            "aircraft model": "Boeing 737-800",
            "MSN": "30123",
            "modifications": []
        },
        {
            "aircraft model": "A320-214",
            "MSN": "5234",
            "modifications": []
        },
        {
            "aircraft model": "A320-232",
            "MSN": "6789",
            "modifications": ["mod 24591 (production)"]
        },
        {
            "aircraft model": "A320-214",
            "MSN": "7456",
            "modifications": ["SB A320-57-1089 Rev 04"]
        },
        {
            "aircraft model": "A321-111",
            "MSN": "8123",
            "modifications": []
        },
        {
            "aircraft model": "A321-112",
            "MSN": "364",
            "modifications": ["mod 24977 (production)"]
        },
        {
            "aircraft model": "A319-100",
            "MSN": "9234",
            "modifications": []
        },
        {
            "aircraft model": "MD-10-10F",
            "MSN": "46234",
            "modifications": []
        },

        
    ]

    # Check each aircraft against the rules and print the result
    for aircraft in aircrafts:
        result = check_rules(aircraft)
        print(result)


if __name__ == "__main__":
    main()