VENV = venv
V_BIN = $(VENV)/bin


all: README.md


$(V_BIN)/python3:
	python3 -m venv $(VENV)
	chmod +x $(V_BIN)/activate
	./$(V_BIN)/activate

	$(V_BIN)/pip install -r requirements.txt


README.md: $(V_BIN)/python3
	$(V_BIN)/python3 -m generate.py


clean:
	rm -f README.md


fclean: clean
	rm -rf venv


.PHONY: clean fclean
