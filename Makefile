ingest:
	python -m src.ingest
index:
	python -m src.embed_index
eval:
	python -m src.evaluate
security:
	pytest -q tests/test_security.py
test:
	pytest -q
app:
	streamlit run app/streamlit_app.py
