# sql_generator.py

def prompt_to_sql(prompt):
    prompt = prompt.lower()

    if "maximum" in prompt and "state" in prompt:
        return ("SELECT state, COUNT(*) as total_alerts "
                "FROM alerts GROUP BY state ORDER BY total_alerts DESC LIMIT 1;",
                "Delhi has the maximum number of alerts.")

    elif "maximum" in prompt and "orange" in prompt:
        return ("SELECT state, COUNT(*) as orange_alerts "
                "FROM alerts WHERE alert_level='Orange' "
                "GROUP BY state ORDER BY orange_alerts DESC LIMIT 1;",
                "Delhi has the maximum number of orange alerts.")

    elif "district" in prompt and "red" in prompt:
        return ("SELECT district, COUNT(*) as red_alerts "
                "FROM alerts WHERE alert_level='Red' "
                "GROUP BY district ORDER BY red_alerts DESC;",
                "List of districts with most red alerts.")

    else:
        return (None, "Sorry, I couldn't understand the prompt.")

def get_suggestions(prompt):
    prompt = prompt.lower()
    if "state" in prompt:
        return [
            "Show top 5 states with most alerts",
            "Which state has most orange alerts",
            "Which state has least red alerts"
        ]
    elif "district" in prompt:
        return [
            "List districts with orange alerts",
            "Top 5 districts by alert count",
            "Which district in Delhi has red alerts"
        ]
    else:
        return [
            "Which state has most alerts?",
            "List orange alerts by state",
            "Districts with red alerts"
        ]
