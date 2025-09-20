import streamlit as st
import random
import time

# Define housekeeping jobs and dependencies
jobs = [
    {"name": "CMNCLNUP", "desc": "Cleanup"},
    {"name": "CMNBCKUP", "desc": "Backup"},
    {"name": "CMNAUDIT", "desc": "Audit"},
    {"name": "CMNCMPRS", "desc": "Compress"},
    {"name": "CMNRPRT", "desc": "Report"},
]

# Simulated error causes
error_causes = [
    "Missing dataset",
    "Insufficient space",
    "Data error",
    "Previous job abended"
]

def run_job(job_name):
    """Simulate job run with random success/failure"""
    outcome = random.choice(["success", "fail"])
    if outcome == "success":
        return "success", None
    else:
        cause = random.choice(error_causes)
        return "fail", cause

def fix_error(cause, job_name):
    """Simulate auto-fix based on cause"""
    if cause == "Missing dataset":
        return f"Auto-fix: Created dataset for {job_name}"
    elif cause == "Insufficient space":
        return f"Auto-fix: Freed up space for {job_name}"
    elif cause == "Data error":
        return f"Auto-fix: Corrected data for {job_name}"
    elif cause == "Previous job abended":
        return f"Auto-fix: Restarted dependent job before {job_name}"
    return "No fix applied"

# Streamlit UI
st.title("🔄 Housekeeping Job Monitoring & Automation")
st.write("Simulation of housekeeping job chain with monitoring, auto-fix, and retry.")

if st.button("▶ Run Simulation"):
    job_results = []
    all_success = True

    for i, job in enumerate(jobs):
        st.subheader(f"Starting {job['name']} - {job['desc']}")
        time.sleep(1)

        status, cause = run_job(job['name'])

        if status == "success":
            st.success(f"{job['name']} completed successfully ✅")
            job_results.append((job['name'], "Success"))
        else:
            st.error(f"{job['name']} failed ❌ | Cause: {cause}")
            fix_msg = fix_error(cause, job['name'])
            st.info(fix_msg)
            time.sleep(1)

            # Retry after fix
            status2, _ = run_job(job['name'])
            if status2 == "success":
                st.success(f"{job['name']} retried and completed ✅")
                job_results.append((job['name'], "Success (after retry)"))
            else:
                st.error(f"{job['name']} failed again ❌ | Stopping chain.")
                job_results.append((job['name'], f"Failed ({cause})"))
                all_success = False
                break

    st.subheader("📊 Final Summary")
    for name, result in job_results:
        st.write(f"- {name}: {result}")

    if all_success:
        st.success("🎉 All housekeeping jobs completed successfully!")
    else:
        st.warning("⚠ Some jobs failed. Chain stopped.")
