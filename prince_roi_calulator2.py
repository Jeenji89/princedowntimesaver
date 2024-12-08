import streamlit as st

# Display the company logo
st.image("https://princeindustriesinc.com/wp-content/uploads/2018/06/Prince-Logo_120x145.png", use_container_width=150)

def calculate_roi(units_processed_range, cost_per_unit, shifts_per_day, inspection_time, inspections_per_shift):
    # Constants
    operation_days_per_month = 26  # 26 days of operation per month
    hours_per_shift = 9  # Each shift is 9 hours
    total_operational_hours = operation_days_per_month * shifts_per_day * hours_per_shift  # Total operational hours per month

    # Deduct inspection time
    inspection_downtime = (inspection_time * inspections_per_shift * shifts_per_day * operation_days_per_month) / 60  # Convert minutes to hours
    effective_operational_hours = total_operational_hours - inspection_downtime

    # Calculate average units processed per hour
    average_units_processed_per_hour = sum(units_processed_range) / len(units_processed_range)

    # Revenue calculations
    actual_revenue = effective_operational_hours * average_units_processed_per_hour * cost_per_unit

    return effective_operational_hours, actual_revenue

def recommend_machine(average_units_processed_per_hour):
    if average_units_processed_per_hour <= 4000:
        return "221"
    elif 4000 < average_units_processed_per_hour <= 17000:
        if 12000 <= average_units_processed_per_hour <= 17000:
            return "2000C HV-RMJ or 2020 HV-R"
        return "2000C HV-RMJ"
    elif 12000 <= average_units_processed_per_hour <= 30000:
        return "2000C HV-RMJ or 2020 HV-R"
    elif 25000 <= average_units_processed_per_hour <= 40000:
        return "2020 HV-R or Mark III"
    elif average_units_processed_per_hour > 40000:
        return "Mark III"
    else:
        return "No suitable model available for this volume range."

def calculate_savings(user_actual_revenue, prince_actual_revenue):
    # Calculate savings
    savings_per_month = prince_actual_revenue - user_actual_revenue  # Correct difference
    savings_per_day = savings_per_month / 26  # Based on 26 operational days
    savings_per_year = savings_per_month * 12  # Annual savings based on monthly
    return savings_per_day, savings_per_month, savings_per_year

# Streamlit app UI
st.title("Prince Downtime Saver")


# Inputs
st.write("Tell us about your operation.")

# Shift selection
shifts_per_day = st.selectbox("Number of shifts per day", options=[1, 2])

# Inspection inputs
inspection_time = st.number_input("Length of time to inspect machine (minutes)", min_value=0, step=1)
inspections_per_shift = st.number_input("Number of inspections per shift", min_value=0, step=1)

# Volume inputs (500 to 50,000 lbs in increments of 500 lbs)
volume_options = {f"{i}-{i+500} lbs": (i, i+500) for i in range(500, 50001, 500)}
selected_volume_range = st.selectbox("Select your current volume per hour range (lbs)", options=volume_options.keys())
units_processed_range = volume_options[selected_volume_range]

# Cost per unit options (in dollars per pound)
cost_per_unit_options = {
    "Frames (7¢/lb)": 0.07,
    "Fresh (26¢/lb)": 0.26,
    "Frozen (34¢/lb)": 0.34
}
selected_cost_option = st.selectbox("Select your product type (average cents per pound per data from the USDA.)", options=cost_per_unit_options.keys())
cost_per_unit = cost_per_unit_options[selected_cost_option]

# Calculation button
if st.button("Calculate ROI"):
    # Adjust Prince inspection time
    prince_inspection_time = inspection_time if inspection_time <= 10 else 10

    # User results
    user_operational_hours, user_actual_revenue = calculate_roi(
        units_processed_range, cost_per_unit, shifts_per_day, inspection_time, inspections_per_shift
    )

    # Prince results
    prince_operational_hours, prince_actual_revenue = calculate_roi(
        units_processed_range, cost_per_unit, shifts_per_day, prince_inspection_time, inspections_per_shift
    )

    # Calculate savings
    savings_per_day, savings_per_month, savings_per_year = calculate_savings(user_actual_revenue, prince_actual_revenue)

    # Machine recommendation
    average_units_processed_per_hour = sum(units_processed_range) / len(units_processed_range)
    recommended_machine = recommend_machine(average_units_processed_per_hour)

    # Outputs
    st.header("Results Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Results")
        st.write(f"**Operational Time (hours):** {user_operational_hours:,.2f}")
        st.write(f"**Actual Monthly Revenue:** ${user_actual_revenue:,.2f}")

    with col2:
        st.subheader("Prince Results")
        st.write(f"**Operational Time (hours):** {prince_operational_hours:,.2f}")
        st.write(f"**Actual Monthly Revenue:** ${prince_actual_revenue:,.2f}")

    st.subheader("Money Saved Using Prince Machine")
    st.write(f"**Savings Per Day:** ${savings_per_day:,.2f}")
    st.write(f"**Savings Per Month:** ${savings_per_month:,.2f}")
    st.write(f"**Savings Per Year:** ${savings_per_year:,.2f}")

    # Machine Recommendation
    st.header("Your Suggested Model Is The:")
    st.write(f"**{recommended_machine}**")
