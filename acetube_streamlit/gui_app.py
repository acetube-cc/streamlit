from loguru import logger

import streamlit as st
from acetube_streamlit import utils
from acetube_streamlit.models import SummeryTube, configure_prompts_of_fields
from acetube_streamlit.settings import Settings

settings = Settings()  # pyright: ignore


logger.info("Starting Streamlit app iteration")

utils.track_run(
    url=settings.supabase_url, key=settings.supabase_key, env=settings.runtime_env
)

st.sidebar.write(
    """
    # 🚀 AceTube 🚀

    > Quickly generate quality metadata for your content!

    Generate a title, description, and tags for a YouTube video.
    All you need to do is paste the transcript of the video
    (you can find it in the "Studio 🎬")

    * 🔧 Made by Dr. Dror
    * 🧑‍💻 Code available [here](https://github.com/acetube-cc/streamlit)
    * 👊 Use this tool on your own risk! Dr. Dror is not responsible for any damage that
      you may have!
    * 🐞 Bug reports are welcomed [here](https://github.com/acetube-cc/streamlit/issues).
    * 🎙️ Let's discuss [here](https://github.com/acetube-cc/streamlit/discussions)
    * 👋🏻 Say hello over [LinkedIn](https://www.linkedin.com/in/atariah/)
    """
)


def reset_session_state() -> None:
    st.session_state.transcript = None
    st.session_state.summary = None
    st.session_state.transcript_confirmed = False
    st.session_state.prompt_confirmed = False


# Initialize session state for each step
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "transcript_confirmed" not in st.session_state:
    st.session_state.transcript_confirmed = False
if "prompt_confirmed" not in st.session_state:
    st.session_state.prompt_confirmed = False

transcript_input = st.text_area(
    "Paste the transcript here",
    height=200,
    help="Paste here the transcript of the video you want to summarize",
    key="manual_input",
)
st.session_state.transcript = transcript_input

if st.button("🚀 Click here if the transcript is correct"):
    st.session_state.transcript_confirmed = True

# Step 3: Configure prompts of the fields
if st.session_state.transcript_confirmed:

    st.session_state.fields_prompt_dict = (
        SummeryTube.construct_prompt_for_fields_as_dict()
    )
    for k in st.session_state.fields_prompt_dict.keys():
        st.session_state.fields_prompt_dict[k] = st.text_area(
            k.capitalize(),
            st.session_state.fields_prompt_dict[k],
            height=10,
            help=f"Provide a prompt for the {k.capitalize()}",
        )

    configure_prompts_of_fields(**st.session_state.fields_prompt_dict)
    st.table(SummeryTube.construct_prompt_for_fields_as_dict())

    if st.button("🚀 Click here if you are happy with the prompts"):
        st.session_state.prompt_confirmed = True

    if st.session_state.prompt_confirmed:
        st.write("Generating summary...")
        if st.session_state.summary is None and st.session_state.transcript is not None:
            try:
                st.session_state.summary = utils.gen_summary_from_transcript(
                    st.session_state.transcript
                )
            except Exception as e:
                st.error(f"Failed to generate the summary with the error {e}")

        if st.session_state.summary:
            st.write("## Summary:")
            st.session_state.summary = utils.struct_summary(st.session_state.summary)
            for field in st.session_state.summary.model_fields:
                st.write(f"### {field.capitalize()}")
                st.write(getattr(st.session_state.summary, field))
            st.session_state.prompt_confirmed = False
            st.session_state.summary = None
