"""Shared building blocks for every OrderSLM contract.

Language neutrality: every enum value is a language-independent code
(snake_case or UPPER_CASE ASCII). Only customer text, quotes, raw_text fields
and the clarification question are in the conversation's language.
"""

from pydantic import BaseModel, ConfigDict, Field

# Bump a version whenever its contract changes in a way that affects saved data,
# prompts, or grading. Every run logs these (spec §19).
# extraction: 0.2 Modification.amount; 0.3 not_on_menu, unmatched_variant_text, agreed_while_incomplete;
# 0.4 Modification.kitchen_note
EXTRACTION_SCHEMA_VERSION = "extraction@0.4"
ROUTER_SCHEMA_VERSION = "router@0.1"
CONVERSATION_SCHEMA_VERSION = (
    "conversation@0.5"  # 0.2: Split.benchmark; 0.3: Source.claude_written, card_id, more Scenario tags;
    # 0.4: Scenario.implicit_category; 0.5: Split.fresh
)
MENU_SCHEMA_VERSION = (
    "menu@0.6"  # 0.2: name_required_for_pickup; 0.3: ingredients/add-ons, aliases, exclusive groups;
    # 0.4: Variant.diameter_cm/slices (reply layer only); 0.5: accepted_kitchen_requests;
    # 0.6: MenuItem.sold_as/pieces_per_order
)
TAXONOMY_VERSION = "taxonomy@0.1"
# Model output for training labels (M4): order facts + ambiguity flags, intents (schema/label.py).
LABEL_SCHEMA_VERSION = "label@0.1"
STUDENT_SCHEMA_VERSION = "student@0.1"
SYNTH_SCHEMA_VERSION = "synth@0.1"  # synthetic chats + their scenario cards (schema/synthetic.py)

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
