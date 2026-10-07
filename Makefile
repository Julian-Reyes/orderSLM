# OrderSLM. Targets for later milestones fail loudly until that milestone implements them,
# so nothing silently produces empty results. Planned commands: docs/ARCHITECTURE.md, "Planned commands".
UV ?= uv
RUN := $(UV) run

.PHONY: test lint format check menus annotate teacher-bakeoff synth label student-bakeoff train eval router-bench demo

test:
	$(RUN) pytest

lint:
	$(RUN) ruff check .
	$(RUN) ruff format --check .

format:
	$(RUN) ruff format .
	$(RUN) ruff check . --fix

check: lint test

define not_yet
	@echo "make $@: not implemented yet (milestone $(1)). See PROGRESS.md." >&2; exit 2
endef

menus:
	$(RUN) python -m orderslm.menus
annotate:         ; $(call not_yet,2)
teacher-bakeoff:  ; $(call not_yet,3)
synth:            ; $(call not_yet,4)
label:            ; $(call not_yet,4)
student-bakeoff:  ; $(call not_yet,5)
train:            ; $(call not_yet,6)
eval:             ; $(call not_yet,6)
router-bench:     ; $(call not_yet,7)
demo:             ; $(call not_yet,8)
