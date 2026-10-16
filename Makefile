PY='python3'
VPY='./.venv/bin/python'

.PHONY: info
info:
	@echo "The following commands should get you started:"
	@echo
	@echo "'make local'	- provisions and runs the local development setup"
	@echo "'make clean'	- clean virtual environment"
.venv:
	$(PY) -m venv ./.venv

freeze.txt: requirements.txt
	$(VPY) -m pip install -r requirements.txt
	$(VPY) -m pip freeze > freeze.txt

freeze.installed: freeze.txt
	FREEZE_INSTALLED=$$($(VPY) -m pip install -r freeze.txt) \
		&& echo "$$FREEZE_INSTALLED" > freeze.installed

local: .venv freeze.installed
	$(VPY) -m fastapi dev app.py

.PHONY: clean
clean:
	@rm -r ./.venv
	@rm -r freeze.installed
