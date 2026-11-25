import json
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from agent.prompts import REVIEW_SYSTEM_PROMPT
from agent.schemas import ReviewResult


class AIReviewer:

    def __init__(self):

        llm = ChatGroq(
            model=os.environ.get(
                "LLM_MODEL",
                "openai/gpt-oss-120b"
            ),
            api_key=os.environ["GROQ_API_KEY"],
            temperature=0,
            timeout=120,
            max_retries=2
        )

        self.reviewer = llm.with_structured_output(
            ReviewResult,
            method="json_schema",
            include_raw=True
        )

    def review(self, ticket, pr, commits, files):

        context = {
            "jira_ticket": ticket,
            "pull_request": {
                "title": pr["title"],
                "description": pr.get("body"),
                "branch": pr["head"]["ref"]
            },
            "commits": commits,
            "changed_files": files
        }

        serialized_context = json.dumps(
            context,
            ensure_ascii=False
        )

        if len(serialized_context) > 120_000:
            raise ValueError(
                "PR exceeds review context limit. "
                "Human review required."
            )

        messages = [
            SystemMessage(
                content=REVIEW_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=serialized_context
            )
        ]

        response = self.reviewer.invoke(messages)

        usage = response["raw"].usage_metadata

        print("Token usage:", usage)

        if response["parsing_error"]:
            raise ValueError(
                "LLM returned an invalid review."
            )

        result = response["parsed"]

        if result is None:
            raise ValueError(
                "LLM did not return a valid review."
            )

        return result
