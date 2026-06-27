import streamlit as st
from PIL import Image
from ai_engine import CellCultureAnalyzer

# Configure page layout and aesthetics
st.set_page_config(page_title="Cell Culture AI AI", page_icon="🔬", layout="wide")

# Header section
st.title("🔬 AI Cell Culture Analyzer")
st.markdown("Upload a brightfield or phase-contrast micrograph to automatically detect contamination, estimate confluency, and assess cellular health.")
st.markdown("---")

# Sidebar for file upload
st.sidebar.header("Input Data")
uploaded_file = st.sidebar.file_uploader("Upload Micrograph", type=["png", "jpg", "jpeg", "tif"])

st.sidebar.info("Supported formats: PNG, JPG, JPEG, TIF. For optimal results, ensure images are in focus and well-lit.")

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    
    # Run Inference
    with st.spinner("Running deep learning models and extracting metrics..."):
        analyzer = CellCultureAnalyzer()
        results = analyzer.analyze(image)
    
    # Layout definition
    col1, col2 = st.columns([2, 1.2])

    with col1:
        st.subheader("Localization & Detection Mapping")
        st.image(results["annotated_image"], use_column_width=True)

    with col2:
        st.subheader("Quantitative Analysis")
        
        # Utilizing Streamlit metrics for a sleek UI
        m1, m2 = st.columns(2)
        m1.metric(label="Cell Count", value=f"{results['cell_count']} cells")
        m2.metric(label="Confluency", value=f"{results['confluency']}%")
        
        m3, m4 = st.columns(2)
        m3.metric(label="Growth Stage", value=results['growth_stage'])
        m4.metric(label="Cell Health", value=results['health_assessment'])
        
        st.markdown("### Contamination Report")
        if results['severity_score'] > 0:
            st.error(f"**Type:** {results['contamination_type']}")
            st.error(f"**Severity Score:** {results['severity_score']} / 10.0")
        else:
            st.success(f"**Type:** {results['contamination_type']}")
            st.success(f"**Severity Score:** {results['severity_score']} / 10.0")

    # Full width recommendation box
    st.markdown("---")
    st.subheader("System Recommendation")
    if results['severity_score'] > 0:
        st.warning(f"⚠️ {results['recommendation']}")
    else:
        st.info(f"✅ {results['recommendation']}")

else:
    # Placeholder when no image is uploaded
    st.info("Awaiting image upload... Please use the sidebar to upload a cell culture micrograph.")
