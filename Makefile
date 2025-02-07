.PHONY: all check-format commit-check mypy test clean

check-format:
	nix fmt -- --fail-on-change --no-cache

mypy:
	mypy .

pylint:
	pylint .

test:
	pytest --cov-branch --junit-xml=junit.xml --cov=malkoha --cov-report term --cov-report xml:coverage.xml

clean:
	git clean -fXd
