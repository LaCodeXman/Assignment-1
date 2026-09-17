from .data import COMMITMENTS, CALENDAR

def commitment_state(item):
    """Return a normalized state used by the dashboard and agent."""
    status = item["status"]
    if status == "Completed":
        return "Completed", "green"
    if "Critical" in status or item["owner"] == "Unassigned":
        return "Critical", "red"
    if status == "Unresolved":
        return "Needs confirmation", "yellow"
    if "Scheduled" in status:
        return "Scheduled", "blue"
    return "Confirmed", "blue"


def get_attention_items():
    """Automatically identify open items from normalized commitment state."""
    return [c for c in COMMITMENTS if commitment_state(c)[0] in ["Critical", "Needs confirmation"]]


def executive_brief():
    """Build a short executive brief from the assignment evidence."""
    attention = get_attention_items()
    return {
        "attention_count": len(attention),
        "top_actions": [c["next_action"] for c in attention],
        "completed": [c["title"] for c in COMMITMENTS if commitment_state(c)[0] == "Completed"],
        "confirmed": [c["title"] for c in COMMITMENTS if commitment_state(c)[0] in ["Confirmed", "Scheduled"]],
    }


def _topic_evidence(topic):
    mapping = {
        "vendor": "Vendor List email thread + Leadership Sync + Voice Note 1",
        "lease": "Mumbai Office Lease Renewal email thread + Leadership Sync",
        "expense": "Expense Variance Report email thread + Leadership Sync + Voice Note 2",
        "meridian": "Call Reschedule email thread + Leadership Sync + Voice Note 2",
        "deck": "Q3 Campaign Deck email thread + Leadership Sync + Arjun calendar",
    }
    return mapping.get(topic, "Combined source data pack")


def answer_question(question: str):
    q = question.lower().strip()

    if any(x in q for x in ["what needs my attention", "what do i need", "priorit", "urgent", "important", "action"]):
        return (
            "### Executive focus\n\n"
            "**1. Mumbai office lease renewal — Critical**  \n"
            "Ownership is still unconfirmed and Facilities reported the signature pending Thursday at 4:00 PM. "
            "Raghav followed up at 4:45 PM saying it was still unowned. Deadline: Friday, 25 September, end of day.\n\n"
            "**2. Updated vendor list — Needs confirmation**  \n"
            "Arjun's latest promise was Wednesday morning. Raghav checked at 8:45 AM Wednesday, but the supplied data contains no later delivery confirmation.\n\n"
            "**Completed / confirmed:** the expense variance report is acknowledged, the Meridian call is confirmed, and the campaign deck is ready for the scheduled review."
        )

    if any(x in q for x in ["vendor", "raghav"]):
        return (
            "### Updated vendor list\n\n"
            "**State:** Needs confirmation  \n"
            "**Owner:** Arjun Malhotra  \n"
            "**Latest commitment:** Wednesday morning  \n\n"
            "Raghav checked at 8:45 AM Wednesday asking whether it was still good for that morning. "
            "No later confirmation of delivery appears in the supplied source data.\n\n"
            "**Next action:** Confirm whether the list was sent; if not, send it to Raghav.\n\n"
            f"**Evidence:** {_topic_evidence('vendor')}"
        )

    if any(x in q for x in ["lease", "mumbai", "facilities"]):
        return (
            "### Mumbai office lease renewal\n\n"
            "**State:** Critical / unowned  \n"
            "**Deadline:** Friday, 25 September, end of day  \n\n"
            "Facilities said Thursday at 4:00 PM that the authorized signature was still pending. "
            "At 4:45 PM, Raghav told Arjun the renewal was still unowned and asked who was handling it. "
            "Divya had earlier said it was not on her end and believed Facilities typically handled it.\n\n"
            "**Next action:** Confirm the authorized owner/signatory before the deadline.\n\n"
            f"**Evidence:** {_topic_evidence('lease')}"
        )

    if any(x in q for x in ["expense", "variance", "divya"]):
        return (
            "### July expense variance report\n\n"
            "**State:** Completed  \n"
            "Divya sent the report Wednesday at 6:00 PM and Arjun acknowledged receipt at 6:10 PM. "
            "The supplied source therefore shows the delivery as complete.\n\n"
            f"**Evidence:** {_topic_evidence('expense')}"
        )

    if any(x in q for x in ["meridian", "priya", "client call"]):
        return (
            "### Meridian Logistics client call\n\n"
            "**State:** Confirmed  \n"
            "The call was confirmed for Wednesday, 23 September at 3:00 PM. Priya confirmed Tuesday evening and "
            "Arjun reconfirmed at 2:00 PM Wednesday.\n\n"
            "**Next action:** Attend the confirmed call.\n\n"
            f"**Evidence:** {_topic_evidence('meridian')}"
        )

    if any(x in q for x in ["deck", "campaign", "neha"]):
        return (
            "### Q3 campaign deck\n\n"
            "**State:** Scheduled / ready  \n"
            "The review moved from Wednesday to Thursday at 9:30 AM. Neha sent the ready deck at 8:00 AM Thursday, "
            "ahead of the scheduled review.\n\n"
            "**Next action:** Review the deck at 9:30 AM.\n\n"
            f"**Evidence:** {_topic_evidence('deck')}"
        )

    if any(x in q for x in ["today", "schedule", "calendar", "meeting", "meetings"]):
        arjun_events = [row for row in CALENDAR if row[0] == "Arjun Malhotra"]
        return (
            "### Arjun's supplied calendar\n\n" +
            "\n".join(f"- **{day} {tm}** — {event}" for _, day, tm, event in arjun_events)
            + "\n\nThe agent reports only explicit calendar entries from the source data; it does not infer availability."
        )

    if any(x in q for x in ["who", "person", "owner", "assigned"]):
        return (
            "### Ownership view\n\n"
            "- **Vendor list:** Arjun Malhotra → Raghav Sethi\n"
            "- **Campaign deck review:** Arjun Malhotra → Neha Kapoor\n"
            "- **Expense variance report:** Divya Rao → Arjun Malhotra\n"
            "- **Meridian call:** Arjun Malhotra ↔ Priya Nair\n"
            "- **Mumbai lease renewal:** ownership remains unconfirmed; Facilities is involved but the supplied data does not establish a final owner."
        )

    return (
        "I can answer using only the supplied assignment data. Try questions such as:\n\n"
        "- What needs my attention?\n"
        "- What's the status of the vendor list?\n"
        "- Who owns the Mumbai lease?\n"
        "- What happened with the expense report?\n"
        "- Is the Meridian call confirmed?\n"
        "- Is the campaign deck ready?\n"
        "- Show my calendar."
    )