import streamlit as st

from benchmark_engine import BenchmarkEngine
from benchmark_engine.adapters.coding import CODING_RULES
from benchmark_engine.extractors.coding import CodingExtractor


st.set_page_config(
    page_title="Benchmark Engine",
    page_icon="📊",
)

st.title("Benchmark Engine")

st.subheader("Coding Benchmark")
st.write(
    "Evaluate a Python implementation against the defined coding benchmark rules."
)

st.caption(
    "Current benchmark profile: Python coding / calculator implementations."
)

uploaded_file = st.file_uploader(
    "Upload a Python implementation",
    type=["py"],
)

if uploaded_file is not None:
    source_code = uploaded_file.getvalue().decode("utf-8")

    if st.button("Run Benchmark"):
        extractor = CodingExtractor()
        engine = BenchmarkEngine(CODING_RULES)

        benchmark_input = extractor.extract(source_code)
        result = engine.evaluate(benchmark_input)

        st.subheader("Benchmark Result")

        st.metric(
            "Overall Score",
            f"{result.score * 100:.1f}%",
        )

        st.subheader("Metric Results")

        for name, metric in result.metrics.items():
            st.write(
                f"**{name}** — "
                f"Score: {metric.score * 100:.1f}% | "
                f"Status: {metric.status}"
            )