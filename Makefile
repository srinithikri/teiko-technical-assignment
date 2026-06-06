setup:
	pip install -r requirements.txt

pipeline:
	python load_data.py
	python analysis.py
	python stats_analysis.py
	python subset_analysis.py

dashboard:
	streamlit run dashboard.py