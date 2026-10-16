# OrderSLM. Targets for later milestones fail loudly until that milestone implements them,
# so nothing silently produces empty results. Planned commands: docs/ARCHITECTURE.md, "Planned commands".
UV ?= uv
RUN := $(UV) run

.PHONY: test lint format check menus annotate annotate-test annotate-api web pizza split-stats lock-test verify-test smoke teacher-bakeoff bakeoff-chart mega-menu label-dev synth label student-bakeoff train eval router-bench demo

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
# Annotation tool on http://127.0.0.1:8765 (local only). annotate-test also opens the sealed test split.
web:
	cd web && npm ci --no-audit --no-fund && npm run build
annotate: web
	$(RUN) uvicorn orderslm.app.main:app --host 127.0.0.1 --port 8765
annotate-test: web
	ORDERSLM_UNSEAL_TEST="annotate test split" $(RUN) uvicorn orderslm.app.main:app --host 127.0.0.1 --port 8765
annotate-api:  # API only, for `cd web && npm run dev` (hot reload on :5173)
	$(RUN) uvicorn orderslm.app.main:app --host 127.0.0.1 --port 8765 --reload

# PIZZA benchmark (docs/PIZZA.md): everything lands in the gitignored data/external/pizza/.
pizza:
	$(RUN) python -m orderslm.data.pizza --download --convert

split-stats:
	$(RUN) python -m orderslm.data.splits stats dev
lock-test:
	ORDERSLM_UNSEAL_TEST="lock M2" $(RUN) python -m orderslm.data.splits lock
verify-test:
	ORDERSLM_UNSEAL_TEST="verify lock" $(RUN) python -m orderslm.data.splits verify
# One tiny live call per model in config/models.json. Without ARGS=--yes it only prints the estimate.
smoke:
	$(RUN) python -m orderslm.llm.smoke $(ARGS)
teacher-bakeoff:
	$(RUN) python -m orderslm.eval.teacher_bakeoff $(ARGS)
# Chart data (before/after views, from saved outputs) + docs/figures SVG for the write-up and case study.
bakeoff-chart:
	$(RUN) python -m orderslm.eval.bakeoff_chart
# Food-court mega-menu from the three training menus (spec §11e): data/menus/mega/food-court.json
mega-menu:
	$(RUN) python -m orderslm.mega
# The M4 label prompt scored on all dev against reviewed gold (orders + intents).
label-dev:
	$(RUN) python -m orderslm.eval.label_dev $(ARGS)
# Synthetic training data (M4): plan / generate / report stages; label is its own target. See synth/run.py.
synth:
	$(RUN) python -m orderslm.synth.run $(ARGS)
label:
	$(RUN) python -m orderslm.synth.run label $(ARGS)
student-bakeoff:  ; $(call not_yet,5)
train:            ; $(call not_yet,6)
eval:             ; $(call not_yet,6)
router-bench:     ; $(call not_yet,7)
demo:             ; $(call not_yet,8)
