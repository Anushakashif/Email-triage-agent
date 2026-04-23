from typing import TypedDict, Annotated
import operator

class EmailState(TypedDict):
    raw_emails: list[dict]        # fetched from Gmail
    classified: list[dict]        # email + classification
    drafts: list[dict]            # email + draft reply
    digest: str                   # summary for human
    human_approved: bool          # did human approve?
    emails_to_send: list[dict]    # approved emails to send