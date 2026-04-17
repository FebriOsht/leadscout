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
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        border-color: #1d4ed8;
    }
    .log-box {
        background-color: #0f172a;
        color: #38bdf8;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        height: 250px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# DuckDuckGo Scraping Function (API)
def duckduckgo_search_api(query, max_results=15, target_type='linkedin', log_func=None):
    results = []
    try:
        ddgs = DDGS()
        search_results = ddgs.text(query, max_results=max_results)
        
        if not search_results:
            if log_func: log_func("[!] DDG API returned 0 results (Backend Limit Hit).")
            return []

        for r in search_results:
            href = r.get('href', '')
            title = r.get('title', '')
            
            if target_type == 'linkedin':
                # Strictly filter for LinkedIn Profiles only
                if 'linkedin.com/in/' in href and '/dir/' not in href and '/jobs/' not in href:
                    clean_url = href.split('?')[0] 
                    if clean_url not in [x['url'] for x in results]:
                        results.append({'title': title, 'url': clean_url})
            else:
                # Entire Web mode: accept all relevant URLs
                if href not in [x['url'] for x in results]:
                    results.append({'title': title, 'url': href})
                    
        return results
    except Exception as e:
        if log_func: log_func(f"[!] Internal DDG API error: {str(e)}")
        return []

# App Header
st.title("🎯 LeadScout Pro")
st.markdown("**Premium B2B Executive Profiler & Web Scraper** — Automated prospect searching engine.")
st.divider()

# Sidebar for Information
with st.sidebar:
    st.header("ℹ️ System Info")
    st.markdown("""
        This tool uses the highly stable **DuckDuckGo API Backend** to bypass common bot-protections.
        It does not require normal browser Captcha solving.
        
        **Tips for best results:**
        * Keep keywords specific.
        * When using large search limits, turning on a **VPN** is highly recommended to prevent IP rate-limiting.
    """)

# Main Layout (2 Columns)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("⚙️ Target Configuration")
    
    campaign_name = st.text_input(
        "Campaign Name", 
        placeholder="e.g., Software Engineers in NY"
    )
    
    target_roles = st.text_area(
        "Target Roles / Keywords (Comma-separated)", 
        placeholder="e.g., Software Engineer, CTO, Lead Developer", 
        height=80
    )
    
    target_industries = st.text_area(
        "Industry Keywords (Comma-separated)", 
        placeholder="e.g., Technology, SaaS, Fintech", 
        height=80
    )
    
    target_location = st.text_input(
        "Location (Optional)", 
        placeholder="e.g., United States, London, Singapore"
    )
    
    # Target Source Selection
    target_source = st.radio("Select Target Source", [
        "LinkedIn Profiles Only (Executives)",
        "Entire Web (All Websites, Articles, Companies)"
    ])
    
    # Calculate estimated total leads for UI
    roles_count = len([r for r in target_roles.split(',') if r.strip()])
    max_results = st.slider("Max Searches Per Keyword", min_value=5, max_value=50, value=10, step=5)
    
    if roles_count > 0:
        st.caption(f"💡 **Estimated target:** {roles_count} keywords × {max_results} searches = **Max {roles_count * max_results} total results**.")
    else:
        st.caption(f"💡 **Estimated target:** 0 keywords × {max_results} searches = **Max 0 total results**.")
    
    st.write("") # Spacer
    start_button = st.button("🚀 Start Scraping Now")

with col2:
    st.subheader("💻 Terminal Monitor")
    
    terminal_placeholder = st.empty()
    progress_bar = st.empty()
    result_placeholder = st.empty()
    download_placeholder = st.empty()
    
    if not start_button:
        terminal_placeholder.markdown('<div class="log-box">Waiting for execution command...</div>', unsafe_allow_html=True)

# --- SCRAPING LOGIC ---
if start_button:
    if not target_roles or not target_industries or not campaign_name:
        st.error("Campaign Name, Roles, and Industry cannot be empty!")
    else:
        roles_list = [r.strip() for r in target_roles.split(',')]
        industries_list = [i.strip() for i in target_industries.split(',')]
        
        # Determine targeting mode
        is_linkedin = "LinkedIn" in target_source
        target_mode = 'linkedin' if is_linkedin else 'web'
        
        # Location query preparation
        loc_val = target_location.strip()
        location_dork = f' "{loc_val}"' if loc_val else ""
        
        logs = [f"[*] Starting LeadScout operation..."]
        logs.append(f"[*] Target Campaign: {campaign_name}")
        logs.append(f"[*] Target Source: {'LinkedIn Profiles' if is_linkedin else 'Entire Web'}")
        if loc_val:
            logs.append(f"[*] Target Location: {loc_val}")
        logs.append(f"[*] Engine: DuckDuckGo API (Secure Mode)")
        
        def update_terminal(log_list):
            html_logs = "<br>".join(log_list)
            terminal_placeholder.markdown(f'<div class="log-box">{html_logs}</div>', unsafe_allow_html=True)
            
        update_terminal(logs)
        my_bar = progress_bar.progress(0)
        
        extracted_data = []
        urls_found = set()
        
        try:
            for i, role in enumerate(roles_list):
                logs.append(f"\n[*] Mining data for: {role} ...")
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
                        
                        add_log(f"[+] Found: {url}")
                        count += 1
                        
                current_prog = (i + 1) / len(roles_list)
                my_bar.progress(current_prog)
                
            logs.append("\n[✓] Operation complete!")
            update_terminal(logs)
            my_bar.progress(1.0)
            
        except Exception as e:
            logs.append(f"\n[!] FATAL ERROR: {str(e)}")
            logs.append("System stopped unexpectedly.")
            update_terminal(logs)
            st.error("Failed to run the application perfectly.")
            
        # Display Results Table
        if extracted_data:
            df = pd.DataFrame(extracted_data)
            
            st.success(f"Successfully found a total of {len(extracted_data)} results!")
            result_placeholder.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            download_placeholder.download_button(
                label="📥 Download Data (CSV)",
                data=csv,
                file_name=f"B2B_Leads_{campaign_name.replace(' ', '_')}.csv",
                mime="text/csv",
            )
        else:
            st.warning("Search yielded no results. Try adjusting the keywords or using a broader location.")