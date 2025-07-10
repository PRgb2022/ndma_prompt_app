def prompt_to_sql(prompt):
    prompt = prompt.lower().strip()

    # Normalize common phrasing
    prompt = prompt.replace("most", "maximum")

    # Match: state with maximum alerts
    if ("state" in prompt or "states" in prompt) and "maximum" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS total_alerts FROM alerts GROUP BY state_name ORDER BY total_alerts DESC LIMIT 1;",
            "State with the highest number of alerts"
        )

    # Match: orange alerts
    if "orange alerts" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS orange_alerts FROM alerts WHERE severity = 'Orange' GROUP BY state_name ORDER BY orange_alerts DESC;",
            "Orange alerts grouped by state"
        )

    # Match: top 5 districts / areas
    if "top 5 districts" in prompt or "top five districts" in prompt or ("district" in prompt and "top" in prompt) or ("area" in prompt and "top" in prompt):
        return (
            "SELECT area_description, COUNT(*) AS total_alerts FROM alerts GROUP BY area_description ORDER BY total_alerts DESC LIMIT 5;",
            "Top 5 districts or areas with the most alerts"
        )

    # Match: frequent alert types
    if ("event type" in prompt or 
        "alert types" in prompt or 
        "most common alerts" in prompt or 
        "most common alert types" in prompt or 
        "frequent alerts" in prompt or 
        "common alert" in prompt):
        return (
            "SELECT event_type, COUNT(*) AS total FROM alerts GROUP BY event_type ORDER BY total DESC LIMIT 5;",
            "Top 5 most frequent alert event types"
        )

    # Match: flood-related alerts
    if "flood" in prompt:
        return (
            "SELECT * FROM alerts WHERE event_type LIKE '%flood%';",
            "All flood-related alerts"
        )

    # Match: recent or latest alerts
    if "recent" in prompt or "latest" in prompt:
        return (
            "SELECT * FROM alerts ORDER BY effectiveTime DESC LIMIT 10;",
            "Most recent alerts"
        )

    # No match found
    return None, None


def get_suggestions(prompt):
    return [
        "Which district has the most alerts?",
        "Show orange alerts by state",
        "What are the most common alert types?",
        "Recent alerts in the system",
        "How many alerts are flood-related?"
    ]
