def prompt_to_sql(prompt):
    prompt = prompt.lower().strip()

    if "maximum" in prompt and "state" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS total_alerts "
            "FROM alerts GROUP BY state_name ORDER BY total_alerts DESC LIMIT 1;",
            "State with the highest number of alerts"
        )

    if "orange alerts" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS orange_alerts "
            "FROM alerts WHERE severity = 'Orange' "
            "GROUP BY state_name ORDER BY orange_alerts DESC;",
            "Orange alerts by state"
        )

    if "yellow alert" in prompt or "yellow alerts" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS yellow_alerts "
            "FROM alerts WHERE severity = 'Yellow' "
            "GROUP BY state_name ORDER BY yellow_alerts DESC;",
            "States with yellow alerts"
        )

    if "top" in prompt and "district" in prompt:
        return (
            "SELECT area_description AS district, COUNT(*) AS total_alerts "
            "FROM alerts GROUP BY area_description ORDER BY total_alerts DESC LIMIT 5;",
            "Top 5 districts by alert count"
        )

    if "red alerts" in prompt and "district" in prompt and "delhi" in prompt:
        return (
            "SELECT area_description AS district, COUNT(*) AS red_alerts "
            "FROM alerts WHERE severity = 'Red' AND state_name = 'Delhi' "
            "GROUP BY area_description ORDER BY red_alerts DESC;",
            "Districts in Delhi with red alerts"
        )

    if "flood" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS flood_alerts "
            "FROM alerts WHERE event_type LIKE '%flood%' "
            "GROUP BY state_name ORDER BY flood_alerts DESC;",
            "Flood-related alerts by state"
        )

    if "recent" in prompt or "latest" in prompt:
        return (
            "SELECT id, state_name, event_type, effectiveTime "
            "FROM alerts ORDER BY effectiveTime DESC LIMIT 10;",
            "Most recent alerts"
        )

    if "common alert types" in prompt or "event type" in prompt:
        return (
            "SELECT event_type, COUNT(*) AS frequency "
            "FROM alerts GROUP BY event_type ORDER BY frequency DESC LIMIT 5;",
            "Top 5 most frequent alert types"
        )

    if "district" in prompt and "most alerts" in prompt:
        return (
            "SELECT area_description AS district, COUNT(*) AS total_alerts "
            "FROM alerts GROUP BY area_description ORDER BY total_alerts DESC LIMIT 1;",
            "District with the most alerts"
        )

    if "alerts by state" in prompt:
        return (
            "SELECT state_name, COUNT(*) AS total_alerts "
            "FROM alerts GROUP BY state_name ORDER BY total_alerts DESC;",
            "Total alerts by state"
        )

    return None, None


def get_suggestions(prompt):
    return [
        "Top 5 districts by alert count",
        "List states with orange alerts",
        "List states with yellow alerts",
        "Which district in Delhi has red alerts",
        "What are the most common alert types?",
        "Recent alerts in the system",
        "Which state has the most flood alerts?"
    ]
