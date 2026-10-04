import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Veterinary EHR",
    page_icon="🐾",
    layout="wide"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_NAME = "veterinary_ehr.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Owners table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    """)

    # Animals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            animal_name TEXT NOT NULL,
            species TEXT,
            breed TEXT,
            gender TEXT,
            date_of_birth TEXT,
            weight_kg REAL,
            FOREIGN KEY (owner_id)
            REFERENCES owners(owner_id)
        )
    """)

    # Visits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER,
            visit_date TEXT,
            symptoms TEXT,
            diagnosis TEXT,
            notes TEXT,
            FOREIGN KEY (animal_id)
            REFERENCES animals(animal_id)
        )
    """)

    # Vaccinations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER,
            vaccine_name TEXT,
            vaccination_date TEXT,
            next_due_date TEXT,
            FOREIGN KEY (animal_id)
            REFERENCES animals(animal_id)
        )
    """)

    # Medications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_name TEXT,
            description TEXT
        )
    """)

    # Medication history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animal_medications (
            animal_medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER,
            medication_id INTEGER,
            dosage_mg_per_kg REAL,
            frequency TEXT,
            duration_days INTEGER,
            calculated_dose_mg REAL,
            start_date TEXT,
            FOREIGN KEY (animal_id)
            REFERENCES animals(animal_id),
            FOREIGN KEY (medication_id)
            REFERENCES medications(medication_id)
        )
    """)

    connection.commit()
    connection.close()


create_tables()


# ============================================================
# HELPER FUNCTION
# ============================================================

def load_data(query):

    connection = get_connection()

    dataframe = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return dataframe


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🐾 Veterinary EHR")

st.sidebar.write(
    "Animal Clinic Electronic Health Record"
)

page = st.sidebar.selectbox(
    "Select Section",
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

    st.title("🐾 Veterinary Medicine EHR")

    st.subheader(
        "Animal Clinic Electronic Health Record & Medication Tracker"
    )

    st.write(
        "Manage animal owners, animals, visits, vaccinations "
        "and medication records."
    )

    owners = load_data(
        "SELECT * FROM owners"
    )

    animals = load_data(
        "SELECT * FROM animals"
    )

    visits = load_data(
        "SELECT * FROM visits"
    )

    vaccinations = load_data(
        "SELECT * FROM vaccinations"
    )

    medications = load_data(
        "SELECT * FROM medications"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

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

    col5.metric(
        "💊 Medications",
        len(medications)
    )

    st.divider()

    st.subheader("📋 Recent Animals")

    recent_animals = load_data("""
        SELECT
            a.animal_id,
            a.animal_name,
            a.species,
            a.breed,
            a.gender,
            a.weight_kg,
            o.owner_name
        FROM animals a
        LEFT JOIN owners o
        ON a.owner_id = o.owner_id
        ORDER BY a.animal_id DESC
        LIMIT 10
    """)

    if recent_animals.empty:

        st.info(
            "No animals have been added yet."
        )

    else:

        st.dataframe(
            recent_animals,
            use_container_width=True
        )


# ============================================================
# OWNERS
# ============================================================

elif page == "Owners":

    st.title("👤 Owner Management")

    st.subheader("➕ Add New Owner")

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

            if owner_name.strip() == "":

                st.error(
                    "Owner name is required."
                )

            else:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO owners
                    (
                        owner_name,
                        phone,
                        email,
                        address
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        owner_name,
                        phone,
                        email,
                        address
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "✅ Owner added successfully!"
                )

    st.divider()

    st.subheader("📋 Owner Records")

    owners = load_data("""
        SELECT
            owner_id,
            owner_name,
            phone,
            email,
            address
        FROM owners
        ORDER BY owner_id DESC
    """)

    if owners.empty:

        st.info(
            "No owner records found."
        )

    else:

        st.dataframe(
            owners,
            use_container_width=True
        )


# ============================================================
# ANIMALS
# ============================================================

elif page == "Animals":

    st.title("🐾 Animal Management")

    owners = load_data("""
        SELECT
            owner_id,
            owner_name
        FROM owners
        ORDER BY owner_name
    """)

    if owners.empty:

        st.warning(
            "Please add an owner first."
        )

    else:

        owner_options = {
            f"{row.owner_name} (ID: {row.owner_id})":
            row.owner_id
            for row in owners.itertuples()
        }

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
                    "Cow",
                    "Horse",
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
                    "Female",
                    "Unknown"
                ]
            )

            date_of_birth = st.date_input(
                "Date of Birth"
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=0.0,
                step=0.1
            )

            selected_owner = st.selectbox(
                "Owner",
                list(owner_options.keys())
            )

            submit = st.form_submit_button(
                "Add Animal"
            )

            if submit:

                if animal_name.strip() == "":

                    st.error(
                        "Animal name is required."
                    )

                else:

                    owner_id = owner_options[
                        selected_owner
                    ]

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        INSERT INTO animals
                        (
                            owner_id,
                            animal_name,
                            species,
                            breed,
                            gender,
                            date_of_birth,
                            weight_kg
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            owner_id,
                            animal_name,
                            species,
                            breed,
                            gender,
                            str(date_of_birth),
                            weight
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "✅ Animal added successfully!"
                    )

    st.divider()

    st.subheader("📋 Animal Records")

    animals = load_data("""
        SELECT
            a.animal_id,
            a.animal_name,
            a.species,
            a.breed,
            a.gender,
            a.date_of_birth,
            a.weight_kg,
            o.owner_name
        FROM animals a
        LEFT JOIN owners o
        ON a.owner_id = o.owner_id
        ORDER BY a.animal_id DESC
    """)

    if animals.empty:

        st.info(
            "No animal records found."
        )

    else:

        st.dataframe(
            animals,
            use_container_width=True
        )


# ============================================================
# VISITS
# ============================================================

elif page == "Visits":

    st.title("🩺 Veterinary Visits")

    animals = load_data("""
        SELECT
            animal_id,
            animal_name
        FROM animals
        ORDER BY animal_name
    """)

    if animals.empty:

        st.warning(
            "Please add an animal first."
        )

    else:

        animal_options = {
            f"{row.animal_name} (ID: {row.animal_id})":
            row.animal_id
            for row in animals.itertuples()
        }

        with st.form("visit_form"):

            selected_animal = st.selectbox(
                "Animal",
                list(animal_options.keys())
            )

            visit_date = st.date_input(
                "Visit Date",
                value=date.today()
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

                animal_id = animal_options[
                    selected_animal
                ]

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO visits
                    (
                        animal_id,
                        visit_date,
                        symptoms,
                        diagnosis,
                        notes
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        animal_id,
                        str(visit_date),
                        symptoms,
                        diagnosis,
                        notes
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "✅ Visit saved successfully!"
                )

    st.divider()

    st.subheader("📋 Visit History")

    visits = load_data("""
        SELECT
            v.visit_id,
            a.animal_name,
            v.visit_date,
            v.symptoms,
            v.diagnosis,
            v.notes
        FROM visits v
        JOIN animals a
        ON v.animal_id = a.animal_id
        ORDER BY v.visit_id DESC
    """)

    if visits.empty:

        st.info(
            "No visit records found."
        )

    else:

        st.dataframe(
            visits,
            use_container_width=True
        )


# ============================================================
# VACCINATIONS
# ============================================================

elif page == "Vaccinations":

    st.title("💉 Vaccination Records")

    animals = load_data("""
        SELECT
            animal_id,
            animal_name
        FROM animals
        ORDER BY animal_name
    """)

    if animals.empty:

        st.warning(
            "Please add an animal first."
        )

    else:

        animal_options = {
            f"{row.animal_name} (ID: {row.animal_id})":
            row.animal_id
            for row in animals.itertuples()
        }

        with st.form("vaccination_form"):

            selected_animal = st.selectbox(
                "Animal",
                list(animal_options.keys())
            )

            vaccine_name = st.text_input(
                "Vaccine Name"
            )

            vaccination_date = st.date_input(
                "Vaccination Date",
                value=date.today()
            )

            next_due_date = st.date_input(
                "Next Due Date"
            )

            submit = st.form_submit_button(
                "Add Vaccination"
            )

            if submit:

                if vaccine_name.strip() == "":

                    st.error(
                        "Vaccine name is required."
                    )

                else:

                    animal_id = animal_options[
                        selected_animal
                    ]

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        INSERT INTO vaccinations
                        (
                            animal_id,
                            vaccine_name,
                            vaccination_date,
                            next_due_date
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            animal_id,
                            vaccine_name,
                            str(vaccination_date),
                            str(next_due_date)
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "✅ Vaccination added successfully!"
                    )

    st.divider()

    st.subheader("📋 Vaccination History")

    vaccinations = load_data("""
        SELECT
            v.vaccination_id,
            a.animal_name,
            v.vaccine_name,
            v.vaccination_date,
            v.next_due_date
        FROM vaccinations v
        JOIN animals a
        ON v.animal_id = a.animal_id
        ORDER BY v.next_due_date
    """)

    if vaccinations.empty:

        st.info(
            "No vaccination records found."
        )

    else:

        st.dataframe(
            vaccinations,
            use_container_width=True
        )


# ============================================================
# MEDICATIONS
# ============================================================

elif page == "Medications":

    st.title("💊 Medication Management")

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

            if medication_name.strip() == "":

                st.error(
                    "Medication name is required."
                )

            else:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO medications
                    (
                        medication_name,
                        description
                    )
                    VALUES (?, ?)
                    """,
                    (
                        medication_name,
                        description
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "✅ Medication added successfully!"
                )

    st.divider()

    st.subheader("📋 Medication List")

    medications = load_data("""
        SELECT
            medication_id,
            medication_name,
            description
        FROM medications
        ORDER BY medication_id DESC
    """)

    if medications.empty:

        st.info(
            "No medications found."
        )

    else:

        st.dataframe(
            medications,
            use_container_width=True
        )


# ============================================================
# MEDICATION HISTORY
# ============================================================

elif page == "Medication History":

    st.title("📋 Medication History")

    animals = load_data("""
        SELECT
            animal_id,
            animal_name
        FROM animals
        ORDER BY animal_name
    """)

    medications = load_data("""
        SELECT
            medication_id,
            medication_name
        FROM medications
        ORDER BY medication_name
    """)

    if animals.empty:

        st.warning(
            "Please add an animal first."
        )

    elif medications.empty:

        st.warning(
            "Please add a medication first."
        )

    else:

        animal_options = {
            f"{row.animal_name} (ID: {row.animal_id})":
            row.animal_id
            for row in animals.itertuples()
        }

        medication_options = {
            f"{row.medication_name} (ID: {row.medication_id})":
            row.medication_id
            for row in medications.itertuples()
        }

        with st.form("medication_history_form"):

            selected_animal = st.selectbox(
                "Animal",
                list(animal_options.keys())
            )

            selected_medication = st.selectbox(
                "Medication",
                list(medication_options.keys())
            )

            dosage = st.number_input(
                "Veterinarian-prescribed dose (mg/kg)",
                min_value=0.0,
                step=0.1
            )

            frequency = st.text_input(
                "Frequency"
            )

            duration = st.number_input(
                "Duration (days)",
                min_value=1,
                step=1
            )

            start_date = st.date_input(
                "Start Date",
                value=date.today()
            )

            submit = st.form_submit_button(
                "Save Medication History"
            )

            if submit:

                animal_id = animal_options[
                    selected_animal
                ]

                medication_id = medication_options[
                    selected_medication
                ]

                animal_data = animals[
                    animals["animal_id"] == animal_id
                ]

                weight = float(
                    animal_data.iloc[0]["weight_kg"]
                )

                calculated_dose = (
                    weight * dosage
                )

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO animal_medications
                    (
                        animal_id,
                        medication_id,
                        dosage_mg_per_kg,
                        frequency,
                        duration_days,
                        calculated_dose_mg,
                        start_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        animal_id,
                        medication_id,
                        dosage,
                        frequency,
                        duration,
                        calculated_dose,
                        str(start_date)
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "✅ Medication history saved!"
                )

                st.info(
                    f"Calculated dose based on the "
                    f"entered veterinarian-prescribed dose: "
                    f"{calculated_dose:.2f} mg"
                )

    st.divider()

    st.subheader("📋 Medication History Records")

    history = load_data("""
        SELECT
            am.animal_medication_id,
            a.animal_name,
            m.medication_name,
            am.dosage_mg_per_kg,
            am.calculated_dose_mg,
            am.frequency,
            am.duration_days,
            am.start_date
        FROM animal_medications am
        JOIN animals a
        ON am.animal_id = a.animal_id
        JOIN medications m
        ON am.medication_id = m.medication_id
        ORDER BY am.animal_medication_id DESC
    """)

    if history.empty:

        st.info(
            "No medication history found."
        )

    else:

        st.dataframe(
            history,
            use_container_width=True
        )


# ============================================================
# DOSE CALCULATOR
# ============================================================

elif page == "Dose Calculator":

    st.title("🧮 Medication Dose Calculator")

    st.warning(
        "This calculator only calculates a dose already "
        "prescribed by a qualified veterinarian. "
        "It does not prescribe medication."
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

    if st.button(
        "Calculate Dose"
    ):

        if weight <= 0:

            st.error(
                "Please enter a valid animal weight."
            )

        elif prescribed_dose <= 0:

            st.error(
                "Please enter the veterinarian-prescribed dose."
            )

        else:

            total_dose = (
                weight * prescribed_dose
            )

            st.success(
                f"Calculated dose: "
                f"{total_dose:.2f} mg"
            )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("📊 Reports & Analytics")

    animals = load_data("""
        SELECT
            species,
            COUNT(*) AS total
        FROM animals
        GROUP BY species
    """)

    if animals.empty:

        st.info(
            "Add animals to generate reports."
        )

    else:

        st.subheader(
            "🐾 Animals by Species"
        )

        figure = px.bar(
            animals,
            x="species",
            y="total",
            title="Animals by Species"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

    st.divider()

    visits = load_data("""
        SELECT
            visit_date,
            COUNT(*) AS total_visits
        FROM visits
        GROUP BY visit_date
        ORDER BY visit_date
    """)

    if not visits.empty:

        st.subheader(
            "🩺 Veterinary Visits"
        )

        figure = px.line(
            visits,
            x="visit_date",
            y="total_visits",
            markers=True,
            title="Visits Over Time"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.info(
    "🐾 Veterinary Medicine EHR\n\n"
    "SQLite Database\n\n"
    "Built with Streamlit"
)
