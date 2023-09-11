virtualenv .venv
.venv/bin/python -m pip install -r requirements.txt

if [ ! -f ./.streamlit/secrets.toml ]; then
    cp ./.streamlit/secrets_template.toml ./.streamlit/secrets.toml
    read -p  "Please enter your openai api key: " replace
    sed -i "s/your key here/$replace/" ./.streamlit/secrets.toml
fi
.venv/bin/python -m streamlit run source/qualitative_analyse_agent.py