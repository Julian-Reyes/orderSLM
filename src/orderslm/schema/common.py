"""Shared building blocks for every OrderSLM contract.

Language neutrality: every enum value is a language-independent code
(snake_case or UPPER_CASE ASCII). Only customer text, quotes, raw_text fields
and the clarification question are in the conversation's language.
"""

from pydantic import BaseModel, ConfigDict, Field

# Bump a version whenever its contract changes in a way that affects saved data,
# prompts, or grading. Every run logs these (spec §19).
EXTRACTION_SCHEMA_VERSION = "extraction@0.2"  # 0.2: Modification.amount
ROUTER_SCHEMA_VERSION = "router@0.1"
CONVERSATION_SCHEMA_VERSION = "conversation@0.1"
MENU_SCHEMA_VERSION = (
    "menu@0.3"  # 0.2: name_required_for_pickup; 0.3: ingredients/add-ons, aliases, exclusive groups
)
TAXONOMY_VERSION = "taxonomy@0.1"

ID_PATTERN = r"^[a-z0-9][a-z0-9_-]*$"
"""Stable ids: menu items, variants, modifiers, businesses. Language-neutral by construction."""


class Strict(BaseModel):
    """Base for every contract: unknown fields are an error, not silently dropped.

    For model output this matters: a model that invents a `price` or `total`
    field fails validation instead of having it quietly ignored.
    """

    model_config = ConfigDict(extra="forbid", frozen=False, str_strip_whitespace=False)


class Evidence(Strict):
    """Where a value came from: a message index and an exact quote from that message."""

    message_index: int = Field(ge=0)
    quote: str = Field(min_length=1, max_length=300)
