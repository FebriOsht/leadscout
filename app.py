import streamlit as st
import pandas as pd
import time

# Handle library rename duckduckgo_search to ddgs
try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        st.error("Missing library. Please run: pip install ddgs")

# Web Page Configuration
st.set_page_config(
    page_title="LeadScout Pro | B2B Extractor",
    page_icon="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-mark-night.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (MODERN UI / SILICON VALLEY STYLE) ---
st.markdown("""
    <style>
    /* Global Theme */
    .stApp {
        background-color: #0b0f19; /* Deep modern dark blue/gray */
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Layout Spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Primary Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 0;
        height: 55px;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
        transform: translateY(-2px);
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(30, 41, 59, 0.5);
        color: white;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 1px #38bdf8;
    }

    /* Terminal Log Box */
    .log-box {
        background-color: rgba(15, 23, 42, 0.85);
        color: #38bdf8;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        height: 380px;
        overflow-y: auto;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: inset 0 4px 10px rgba(0, 0, 0, 0.5);
        font-size: 0.9rem;
        line-height: 1.5;
        backdrop-filter: blur(4px);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #0284c7, #38bdf8);
    }

    /* Dataframe Container */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)


# DuckDuckGo search (shared with cli.py, see leadscout_core.py)
from leadscout_core import duckduckgo_search_api

# --- MODERN HEADER DESIGN ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%); padding: 2.5rem 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 2.5rem; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);">
        <h1 style="margin: 0; padding: 0; font-size: 2.8rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #38bdf8, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎯 LeadScout Pro</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; color: #94a3b8; font-weight: 400;">Premium B2B Executive Profiler & Web Scraper <span style="background: rgba(56,189,248,0.2); color: #38bdf8; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; margin-left: 8px;">DuckDuckGo Engine</span></p>
    </div>
""", unsafe_allow_html=True)


# Sidebar for Information
with st.sidebar:
    st.markdown("### ℹ️ System Info")
    st.markdown("---")
    st.info("""
        This tool uses the highly stable **DuckDuckGo API Backend** to bypass common bot-protections.
        It does not require normal browser Captcha solving.
    """)
    st.warning("""
        **Tips for best results:**
        * Keep keywords specific.
        * When using large search limits, turning on a **VPN** is highly recommended to prevent IP rate-limiting.
    """)

# Main Layout (2 Columns)
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### ⚙️ Target Configuration")
    
    campaign_name = st.text_input(
        "📌 Campaign Name", 
        placeholder="e.g., Software Engineers in NY"
    )
    
    target_roles = st.text_area(
        "💼 Target Roles / Keywords (Comma-separated)", 
        placeholder="e.g., Software Engineer, CTO, Lead Developer", 
        height=80
    )
    
    target_industries = st.text_area(
        "🏢 Industry Keywords (Comma-separated)", 
        placeholder="e.g., Technology, SaaS, Fintech", 
        height=80
    )
    
    target_location = st.text_input(
        "📍 Location (Optional)", 
        placeholder="e.g., United States, London, Singapore"
    )
    
    # Target Source Selection
    st.markdown("<br>", unsafe_allow_html=True)
    target_source = st.radio("🌐 Select Target Source", [
        "LinkedIn Profiles Only (Executives)",
        "Entire Web (All Websites, Articles, Companies)"
    ])
    
    # Calculate estimated total leads for UI
    roles_count = len([r for r in target_roles.split(',') if r.strip()])
    
    st.markdown("<br>", unsafe_allow_html=True)
    max_results = st.slider("📊 Max Searches Per Keyword", min_value=5, max_value=50, value=10, step=5)
    
    if roles_count > 0:
        st.caption(f"💡 **Estimated target:** {roles_count} keywords × {max_results} searches = **Max {roles_count * max_results} total results**.")
    else:
        st.caption(f"💡 **Estimated target:** 0 keywords × {max_results} searches = **Max 0 total results**.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    start_button = st.button("🚀 Start Scraping Now")

with col2:
    st.markdown("### 💻 Terminal Monitor")
    
    terminal_placeholder = st.empty()
    st.markdown("<br>", unsafe_allow_html=True)
    progress_bar = st.empty()
    result_placeholder = st.empty()
    download_placeholder = st.empty()
    
    if not start_button:
        terminal_placeholder.markdown('<div class="log-box" style="color:#64748b;">[~] System idle. Waiting for execution command...</div>', unsafe_allow_html=True)

# --- SCRAPING LOGIC ---
if start_button:
    if not target_roles or not target_industries or not campaign_name:
        st.error("⚠️ Campaign Name, Roles, and Industry cannot be empty!")
    else:
        roles_list = [r.strip() for r in target_roles.split(',')]
        industries_list = [i.strip() for i in target_industries.split(',')]
        
        # Determine targeting mode
        is_linkedin = "LinkedIn" in target_source
        target_mode = 'linkedin' if is_linkedin else 'web'
        
        # Location query preparation
        loc_val = target_location.strip()
        location_dork = f' "{loc_val}"' if loc_val else ""
        
        logs = [f"<span style='color:#94a3b8;'>[*]</span> Starting LeadScout operation..."]
        logs.append(f"<span style='color:#94a3b8;'>[*]</span> Target Campaign: <span style='color:#e2e8f0;'>{campaign_name}</span>")
        logs.append(f"<span style='color:#94a3b8;'>[*]</span> Target Source: <span style='color:#e2e8f0;'>{'LinkedIn Profiles' if is_linkedin else 'Entire Web'}</span>")
        if loc_val:
            logs.append(f"<span style='color:#94a3b8;'>[*]</span> Target Location: <span style='color:#e2e8f0;'>{loc_val}</span>")
        logs.append(f"<span style='color:#94a3b8;'>[*]</span> Engine: <span style='color:#e2e8f0;'>DuckDuckGo API (Secure Mode)</span>")
        
        def update_terminal(log_list):
            html_logs = "<br>".join(log_list)
            terminal_placeholder.markdown(f'<div class="log-box">{html_logs}</div>', unsafe_allow_html=True)
            
        update_terminal(logs)
        my_bar = progress_bar.progress(0)
        
        extracted_data = []
        urls_found = set()
        
        try:
            for i, role in enumerate(roles_list):
                logs.append(f"<br><span style='color:#a78bfa;'>[*] Mining data for: <strong>{role}</strong> ...</span>")
                update_terminal(logs)
                
                def add_log(msg):
                    logs.append(msg)
                    update_terminal(logs)
                
                # Build Query based on mode
                if is_linkedin:
                    search_query = f'"{role}" {industries_list[0]}{location_dork} site:linkedin.com/in'
                else:
                    search_query = f'"{role}" {industries_list[0]}{location_dork}'
                
                # Execute Search via API
                results_generator = duckduckgo_search_api(
                    query=search_query, 
                    max_results=max_results, 
                    target_type=target_mode,
                    log_func=add_log
                )
                time.sleep(1.5) # Delay to respect API limits
                
                count = 0
                for item in results_generator:
                    if count >= max_results:
                        break
                    
                    url = item['url']
                    title = item['title']
                    
                    if url not in urls_found:
                        urls_found.add(url)
                        extracted_data.append({
                            "Campaign": campaign_name,
                            "Keyword": role,
                            "Location": loc_val if loc_val else "Global",
                            "Page Title": title,
                            "URL": url
                        })
                        
                        add_log(f"<span style='color:#4ade80;'>[+] Found:</span> {url}")
                        count += 1
                        
                current_prog = (i + 1) / len(roles_list)
                my_bar.progress(current_prog)
                
            logs.append("<br><span style='color:#4ade80; font-weight:bold;'>[✓] Operation complete!</span>")
            update_terminal(logs)
            my_bar.progress(1.0)
            
        except Exception as e:
            logs.append(f"<br><span style='color:#f87171;'>[!] FATAL ERROR: {str(e)}</span>")
            logs.append("<span style='color:#f87171;'>System stopped unexpectedly.</span>")
            update_terminal(logs)
            st.error("Failed to run the application perfectly.")
            
        # Display Results Table
        if extracted_data:
            df = pd.DataFrame(extracted_data)
            
            st.markdown("---")
            st.success(f"✅ Successfully found a total of **{len(extracted_data)}** results!")
            result_placeholder.dataframe(df, use_container_width=True, height=300)
            
            csv = df.to_csv(index=False).encode('utf-8')
            
            col_a, col_b, col_c = st.columns([1,2,1])
            with col_b:
                download_placeholder.download_button(
                    label="📥 DOWNLOAD DATASET (.CSV)",
                    data=csv,
                    file_name=f"B2B_Leads_{campaign_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    type="primary"
                )
        else:
            st.warning("⚠️ Search yielded no results. Try adjusting the keywords or using a broader location.")
