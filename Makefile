BROWSER ?= xdg-open
PORT    ?= 5173

# ── Local dev ────────────────────────────────────────

install: install-backend install-frontend

install-backend:
	cd backend && npm install

install-frontend:
	cd frontend && npm install

dev: dev-backend dev-frontend

dev-backend:
	cd backend && npm run dev

dev-frontend:
	cd frontend && npm run dev

build: build-frontend

build-frontend:
	cd frontend && npm run build

lint: lint-frontend

lint-frontend:
	cd frontend && npm run lint

check: check-frontend-ts check-backend-ts lint-frontend build-frontend

check-frontend-ts:
	cd frontend && npx tsc --noEmit

check-backend-ts:
	cd backend && npx tsc --noEmit

open:
	$(BROWSER) http://localhost:$(PORT)

# ── Worktree navigation ─────────────────────────────

WORKTREES ?= ../ssht-python ../ssht-rust ../ssht-go

worktree-ls:
	@git worktree list
	@echo ""
	@echo "Convention:"
	@for wt in $(WORKTREES); do \
		if [ -d $$wt ]; then echo "  $$wt  (exists)"; \
		else echo "  $$wt  (not yet created)"; fi; \
	done

worktree-setup:
	@echo "Creating worktrees…"
	@branches="python rust go"; \
	for b in $$branches; do \
		wt="../ssht-$$b"; \
		if [ ! -d "$$wt" ]; then \
			git worktree add "$$wt" "$$b" 2>&1 && echo "  ✔ $$wt ← $$b"; \
		else \
			echo "  – $$wt already exists"; \
		fi; \
	done
	@echo "Done. Use: make worktree-cd-<branch>"

worktree-cd-python:
	@echo "cd ../ssht-python"

worktree-cd-rust:
	@echo "cd ../ssht-rust"

worktree-cd-go:
	@echo "cd ../ssht-go"

# ── Utils ────────────────────────────────────────────

.PHONY: install install-backend install-frontend dev dev-backend dev-frontend
.PHONY: build build-frontend lint lint-frontend check
.PHONY: check-frontend-ts check-backend-ts open
.PHONY: worktree-ls worktree-setup worktree-cd-python worktree-cd-rust worktree-cd-go
