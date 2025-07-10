def prompt_to_sql(prompt):
    prompt = prompt.lower().strip()

    # 1. Maximum number of alerts by state
    if "maximum" in prompt and "state" in prompt:
        return (
            """
            SELECT state_name, COUNT(*) AS total_alerts
            FROM alerts
            GROUP BY state_name
            ORDER BY total_alerts DESC
            LIMIT 1;
            """,
            "State with the highest number of alerts"
        )

    # 2. Orange alerts by state
    if "orange alerts" in prompt:
        return (
            """
            SELECT state_name, COUNT(*) AS orange_alerts
            FROM alerts
            WHERE severity = 'Orange'
            GROUP BY state_name
            ORDER BY orange_alerts DESC;
            """,
            "Orange alerts grouped by state"
        )

    # 3. Alerts by district or area (area_description)
    if "district" in prompt or "area" in prompt:
        return (
            """
            SELECT area_description, COUNT(*) AS total_alerts
            FROM alerts
            GROUP BY area_description
            ORDER BY total_alerts DESC
            LIMIT 10;
            """,
            "Top districts/areas with most alerts"
        )

    # 4. All flood alerts
    if "flood" in prompt:
        return (
            """
            SELECT *
            FROM alerts
            WHERE event_type LIKE '%flood%';
            """,
            "All flood-related alerts"
        )

    # 5. Top event types
    if "event type" in prompt or "most common alert" in prompt:
        return (
            """
            SELECT event_type, COUNT(*) AS total
            FROM alerts
            GROUP BY event_type
            ORDER BY total DESC
            LIMIT 5;
            """,
            "Top 5 most frequent alert event types"
        )

    # 6. Recent alerts
    if "latest" in prompt or "recent" in prompt:
        return (
            """
            SELECT *
            FROM alerts
            ORDER BY effectiveTime DESC
            LIMIT 10;
            """,
            "Most recent alerts"
        )

    return None, None  # fallback if no match


def get_suggestions(prompt):
    return [
        "Which district has the most alerts?",
        "Show orange alerts by state",
        "What are the most common alert types?",
        "Recent alerts in the system",
        "How many alerts are flood-related?"
    ]
