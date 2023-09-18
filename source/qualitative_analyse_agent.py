import os
from io import StringIO
import time

import streamlit as st

# Setup langsmith variables
os.environ['LANGCHAIN_TRACING_V2'] = st.secrets["langsmith"]["tracing"]
os.environ['LANGCHAIN_ENDPOINT'] = st.secrets["langsmith"]["api_url"]
os.environ['LANGCHAIN_API_KEY'] = st.secrets["langsmith"]["api_key"]
os.environ['LANGCHAIN_PROJECT'] = st.secrets["langsmith"]["project"]

from modules.report import parse_codes  # noqa: E402
from modules.chains import summary_chain, overall_chain  # noqa: E402


st.set_page_config(
    page_title="Qualitative Data Analysis",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:valentin.rudloff.perso@gmail.com',
        'Report a bug': "https://github.com/Gamma-Software/llm_qualitative_data_analysis/issues",
        'About': open("README.md", "r").read()
    }
)

with st.sidebar:
    st.title("Getting started")
    menu = st.selectbox("Select pages", ["Raw data", "Qualitative Analysis", "About"], index=1)

    if ("openai_api_key" not in st.secrets or
        "openai_api_key" in st.secrets and
        st.secrets["openai_api_key"] == "your key here"):
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        if openai_api_key and 'openai_api_key' not in st.session_state:
            st.session_state['openai_api_key'] = openai_api_key
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    else:
        st.session_state['openai_api_key'] = st.secrets["openai_api_key"]

    files = st.file_uploader("Upload your data", accept_multiple_files=True, type=['txt', 'md'])

    options = st.container()
    options.title("Options ⚙️")
    max_limit_summary_words = options.select_slider(
        'Select a limit of words for the summary',
        options=range(100, 2000, 100),
        value=(1000))
    min_limit_codes, max_limit_codes = options.select_slider(
        'Select a range of codes to generate',
        options=range(2, 21, 1),
        value=(14, 20))
    min_limit_theme_words, max_limit_theme_words = options.select_slider(
        'Each themes must between min/max words long',
        options=range(2, 10, 1),
        value=(5, 6))

    st.divider()
    st.markdown("Made with ❤️ by [Valentin Rudloff](https://www.linkedin.com/in/rudloffvalentin/)")

if menu == "About":
    st.markdown(open("README.md", "r").read())
    st.stop()

st.title("Qualitative Analysis 📝 Agent")
st.caption("Using the power of LLMs")

description_container = st.container()
description_container.write(
    """This is a tool to help you do your qualitative data analysis.
    This can for instance take your transcripts and generate codes
    and themes for you""")
description_container.markdown(
    """To perfom the qualitative analysis, you will need to upload
    your transcripts and ask a research question. The tool will
    then generate:\n1. summary of the transcripts \n2. Identify
    excerts and generate codes\n3. Generate themes (by categorizing
    codes) based on the research question you asked.""")
description_container.markdown(
    """Learn more about
    [Qualitative Analysis](https://www.investopedia.com/terms/q/qualitativeanalysis.asp)""")

if not files:
    st.info("Please upload some qualitative data in the sidebar")
    st.stop()

if 'openai_api_key' not in st.session_state:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Fetching Qualitative Data
qualitative_docs = []
if files:
    # Read the qualitative data
    # TODO force a format
    for file in files:
        # To read file as bytes:
        bytes_data = file.getvalue()

        # To convert to a string based IO:
        stringio = StringIO(file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()
        qualitative_docs.append("\n".join([string_data]))
    qualitative_docs_string = "\n\n".join(
        [f"Qualitative Data {files[i].name}:\n{d}" for i, d in enumerate(qualitative_docs)])

    if qualitative_docs and menu == "Raw data":
        st.subheader("Show Raw data")
        tabs = st.tabs([file.name for file in files])
        for i, tab in enumerate(tabs):
            with tab:
                tab.markdown(qualitative_docs[i])

# TODO Add audio transcription to text

# --- Summarizing qualitative data ---
if menu == "Raw data":
    if st.button("Summarize transcripts", key="summarize"):
        with st.spinner("Summarizing..."):
            chain = summary_chain()
            summarize = chain({"max_limit_summary": max_limit_summary_words,
                               "transcript": qualitative_docs_string})
            with st.expander("Summary"):
                st.markdown(summarize["summary"])

# --- Summarizing qualitative data based on a research question ---
# This step should use the RAG method to repond to the user based on the question
if menu == "Qualitative Analysis":
    question = st.text_area("Research question", placeholder="How do students perceive the quality "
                            "and accessibility of food services on campus, and what factors "
                            "influence their dining choices and satisfaction?")

    # --- Summarizing transcripts ---
    # DONE

    # --- Generating initial codes ---
    # DONE

    # --- (Double check) Verify the codes generated ---
    # TODO

    # --- Generating themes ---
    # DONE

    # --- (Double check) Verify the themes generated ---
    # TODO

    # --- Get source of the excerpts ---
    # TODO

    # --- Execute LLM Chain ---
    output = None
    if not question:
        st.info("Please enter a question to continue analysis...")
    elif st.button("🚄 Perform Qualitative Analysis"):
        with st.status("Qualitative Analysis...", expanded=True) as status:
            time_start = time.time()
            status_placeholder = st.container()
            st.toast("Generate Summary/Code/Theme with AI...")
            status_placeholder.write("Generate Summary/Code/Theme with AI...")
            output = overall_chain()({"max_limit_summary": max_limit_summary_words,
                                      "min_limit_codes": min_limit_codes,
                                      "max_limit_codes": max_limit_codes,
                                      "transcript": qualitative_docs_string,
                                      "question": question}, return_only_outputs=True)
            try:
                pass
            except Exception:
                status.update(label="Qualitative Analysis... Failed", state="error")

            st.toast("Generating report 📝...")
            status_placeholder.write("Generating report 📝...")

            st.session_state["generated_themes"] = output["themes"]
            st.session_state["generated_codes"] = output["codes"]
            st.session_state["generated_summary"] = output["summary_qa"]
            st.session_state["table"] = parse_codes(st.session_state["generated_codes"], st.session_state["generated_themes"])
            msg = ""
            for i, row in st.session_state["table"].iterrows():
                msg += "\n## "+row["Theme"]
                sub_code = row["Codes"].split(",")
                sub_exc = row["Excerpts from transcript"].split(",")
                for i, _ in enumerate(sub_code):
                    msg += "\n- "+sub_code[i]+" -> *\""+sub_exc[i]+"\"*"
            st.session_state["report"] = "# Summary\n"+st.session_state["generated_summary"]+f"\n\n# Result of Analysis\n{msg}"

            time_elapsed = time.time() - time_start
            st.caption(f"Generation took: {time_elapsed:.2f}s")

            # --- Generating a report in a table form ---
            status_placeholder = st.empty()
            status.update(label="Qualitative Analysis complete!", state="complete")

if all([key in st.session_state for key in ["report", "generated_summary", "table"]]):
    st.header("Analysis report 📈")
    st.markdown(st.session_state["report"])
    st.download_button(
        label="Download the report",
        data=st.session_state["report"],
        file_name='report.md',
        mime='text/markdown',
    )
