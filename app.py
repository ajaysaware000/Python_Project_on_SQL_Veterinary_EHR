import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Veterinary EHR",
    page_icon="🐾",
    layout="wide"
)


# ============================================================
# SAMPLE DATA
# ============================================================

owners = pd.DataFrame({
    "Owner ID": [1, 2, 3],
    "Owner Name": ["Rahul Kumar", "Priya Sharma", "Amit Patil"],
    "Phone": ["9876543210", "9876543211", "9876543212"],
    "Email": [
        "rahul@example.com",
        "priya@example.com",
        "amit@example.com"
    ]
})


animals = pd.DataFrame({
    "Animal ID": [1, 2, 3, 4],
    "Animal Name": ["Bruno", "Kitty", "Rocky", "Coco"],
    "Species": ["Dog", "Cat", "Dog", "Rabbit"],
    "Breed": ["Labrador", "Persian", "Beagle", "Dutch Rabbit"],
    "Gender": ["Male", "Female", "Male", "Female"],
    "Weight (kg)": [25.5, 4.2, 12.5, 2.3],
    "Owner": [
        "Rahul Kumar",
        "Priya Sharma",
        "Amit Patil",
        "Rahul Kumar"
    ]
})


visits = pd.DataFrame({
    "Visit ID": [1, 2, 3, 4],
    "Animal": ["Bruno", "Kitty", "Rocky", "Coco"],
    "Visit Date": [
        "2026-10-01",
        "2026-10-02",
        "2026-10-03",
        "2026-10-04"
    ],
    "Symptoms": [
        "Fever",
        "Cough",
        "Loss of appetite",
        "Skin irritation"
    ],
    "Diagnosis": [
        "Infection",
        "Respiratory issue",
        "Digestive issue",
        "Skin condition"
    ]
})


vaccinations = pd.DataFrame({
    "Vaccination ID": [1, 2, 3],
    "Animal": ["Bruno", "Kitty", "Rocky"],
    "Vaccine": ["Rabies", "FVRCP", "DHPP"],
    "Vaccination Date": [
        "2026-09-01",
        "2026-08-15",
        "2026-09-20"
    ],
    "Next Due Date": [
        "2027-09-01",
        "2027-08-15",
        "2027-09-20"
    ]
})


medications = pd.DataFrame({
    "Medication ID": [1, 2, 3],
    "Medication Name": [
        "Medication A",
        "Medication B",
        "Medication C"
    ],
    "Description": [
        "Sample medication",
        "Sample medication",
        "Sample medication"
    ]
})


medication_history = pd.DataFrame({
    "Animal": ["Bruno", "Kitty", "Rocky"],
    "Medication": [
        "Medication A",
        "Medication B",
        "Medication C"
    ],
    "Dose (mg/kg)": [10, 5, 8],
    "Calculated Dose (mg)": [255, 21, 100],
    "Frequency": [
        "Twice daily",
        "Once daily",
        "Twice daily"
    ],
    "Duration (days)": [5, 7, 5]
})


# ============================================================
# TITLE
# ============================================================

st.title("🐾 Veterinary Medicine EHR")

st.subheader(
    "Animal Clinic Electronic Health Record & Medication Tracker"
)

st.write(
    "A sample Veterinary EHR application built with Streamlit."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🐾 Navigation")

page = st.sidebar.selectbox(
    "Select a section",
    [
        "Dashboard",
        "Owners",
        "Animals",
        "Visits",
        "Vaccinations",
        "Medications",
        "Medication History",
        "Dose Calculator",
        "Reports"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("🏠 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👤 Owners",
        len(owners)
    )

    col2.metric(
        "🐾 Animals",
        len(animals)
    )

    col3.metric(
        "🩺 Visits",
        len(visits)
    )

    col4.metric(
        "💉 Vaccinations",
        len(vaccinations)
    )

    st.divider()

    st.subheader("🐾 Animals by Species")

    species_count = (
        animals["Species"]
        .value_counts()
        .reset_index()
    )

    species_count.columns = [
        "Species",
        "Number of Animals"
    ]

    fig = px.bar(
        species_count,
        x="Species",
        y="Number of Animals",
        title="Animals by Species"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🩺 Recent Visits")

    st.dataframe(
        visits,
        use_container_width=True
    )


# ============================================================
# OWNERS
# ============================================================

elif page == "Owners":

    st.header("👤 Owner Management")

    st.subheader("➕ Add Owner")

    with st.form("owner_form"):

        owner_name = st.text_input(
            "Owner Name"
        )

        phone = st.text_input(
            "Phone"
        )

        email = st.text_input(
            "Email"
        )

        address = st.text_area(
            "Address"
        )

        submit = st.form_submit_button(
            "Add Owner"
        )

        if submit:

            if owner_name:

                st.success(
                    f"✅ Owner '{owner_name}' added successfully!"
                )

            else:

                st.warning(
                    "Please enter owner name."
                )

    st.divider()

    st.subheader("📋 Owner List")

    st.dataframe(
        owners,
        use_container_width=True
    )


# ============================================================
# ANIMALS
# ============================================================

elif page == "Animals":

    st.header("🐾 Animal Management")

    st.subheader("➕ Add Animal")

    with st.form("animal_form"):

        animal_name = st.text_input(
            "Animal Name"
        )

        species = st.selectbox(
            "Species",
            [
                "Dog",
                "Cat",
                "Rabbit",
                "Bird",
                "Other"
            ]
        )

        breed = st.text_input(
            "Breed"
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            step=0.1
        )

        submit = st.form_submit_button(
            "Add Animal"
        )

        if submit:

            if animal_name:

                st.success(
                    f"✅ {animal_name} added successfully!"
                )

            else:

                st.warning(
                    "Please enter animal name."
                )

    st.divider()

    st.subheader("📋 Animal List")

    st.dataframe(
        animals,
        use_container_width=True
    )


# ============================================================
# VISITS
# ============================================================

elif page == "Visits":

    st.header("🩺 Veterinary Visits")

    st.subheader("➕ Add Veterinary Visit")

    with st.form("visit_form"):

        animal = st.selectbox(
            "Animal",
            animals["Animal Name"].tolist()
        )

        visit_date = st.date_input(
            "Visit Date"
        )

        symptoms = st.text_area(
            "Symptoms"
        )

        diagnosis = st.text_area(
            "Diagnosis"
        )

        notes = st.text_area(
            "Notes"
        )

        submit = st.form_submit_button(
            "Save Visit"
        )

        if submit:

            st.success(
                f"✅ Visit for {animal} saved successfully!"
            )

    st.divider()

    st.subheader("📋 Visit History")

    st.dataframe(
        visits,
        use_container_width=True
    )


# ============================================================
# VACCINATIONS
# ============================================================

elif page == "Vaccinations":

    st.header("💉 Vaccination Records")

    st.subheader("➕ Add Vaccination")

    with st.form("vaccination_form"):

        animal = st.selectbox(
            "Animal",
            animals["Animal Name"].tolist()
        )

        vaccine = st.text_input(
            "Vaccine Name"
        )

        vaccination_date = st.date_input(
            "Vaccination Date"
        )

        next_due_date = st.date_input(
            "Next Due Date"
        )

        submit = st.form_submit_button(
            "Add Vaccination"
        )

        if submit:

            st.success(
                f"✅ {vaccine} vaccination added for {animal}!"
            )

    st.divider()

    st.subheader("📋 Vaccination History")

    st.dataframe(
        vaccinations,
        use_container_width=True
    )


# ============================================================
# MEDICATIONS
# ============================================================

elif page == "Medications":

    st.header("💊 Medication Management")

    st.subheader("➕ Add Medication")

    with st.form("medication_form"):

        medication_name = st.text_input(
            "Medication Name"
        )

        description = st.text_area(
            "Description"
        )

        submit = st.form_submit_button(
            "Add Medication"
        )

        if submit:

            if medication_name:

                st.success(
                    f"✅ {medication_name} added successfully!"
                )

            else:

                st.warning(
                    "Please enter medication name."
                )

    st.divider()

    st.subheader("📋 Medication List")

    st.dataframe(
        medications,
        use_container_width=True
    )


# ============================================================
# MEDICATION HISTORY
# ============================================================

elif page == "Medication History":

    st.header("📋 Medication History")

    st.dataframe(
        medication_history,
        use_container_width=True
    )


# ============================================================
# DOSE CALCULATOR
# ============================================================

elif page == "Dose Calculator":

    st.header("🧮 Medication Dose Calculator")

    st.info(
        "Enter only the dose prescribed by a qualified veterinarian."
    )

    weight = st.number_input(
        "Animal Weight (kg)",
        min_value=0.0,
        step=0.1
    )

    prescribed_dose = st.number_input(
        "Veterinarian-prescribed dose (mg/kg)",
        min_value=0.0,
        step=0.1
    )

    if st.button("Calculate Dose"):

        if weight <= 0:

            st.warning(
                "Please enter a valid weight."
            )

        elif prescribed_dose <= 0:

            st.warning(
                "Please enter the prescribed dose."
            )

        else:

            total_dose = (
                weight * prescribed_dose
            )

            st.success(
                f"Calculated dose: {total_dose:.2f} mg"
            )

            st.write(
                f"Formula: {weight} kg × "
                f"{prescribed_dose} mg/kg"
            )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.header("📊 Reports & Analytics")

    # Animals by species

    species_count = (
        animals["Species"]
        .value_counts()
        .reset_index()
    )

    species_count.columns = [
        "Species",
        "Number of Animals"
    ]

    st.subheader("🐾 Animals by Species")

    fig1 = px.pie(
        species_count,
        names="Species",
        values="Number of Animals",
        title="Animal Distribution"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Animal weight

    st.subheader("⚖️ Animal Weight")

    fig2 = px.bar(
        animals,
        x="Animal Name",
        y="Weight (kg)",
        title="Animal Weight"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Visit information

    st.subheader("🩺 Visit Information")

    st.dataframe(
        visits,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "🐾 Veterinary Medicine EHR"
)

st.sidebar.caption(
    "Sample data version"
)
