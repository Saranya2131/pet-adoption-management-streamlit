
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Pet Adoption Management",
    page_icon="🐾",
    layout="wide"
)

st.title("🐾 Pet Adoption Management System")
st.caption("Find your new best friend!")

if "pets" not in st.session_state:
    st.session_state.pets = [
        {"name": "Buddy", "type": "Dog", "age": 2,
         "description": "Friendly and playful."},
        {"name": "Luna", "type": "Cat", "age": 1,
         "description": "Calm, curious, and affectionate."},
        {"name": "Max", "type": "Dog", "age": 3,
         "description": "Loves walks and playing fetch."},
        {"name": "Milo", "type": "Rabbit", "age": 1,
         "description": "Gentle and easygoing."}
    ]

if "requests" not in st.session_state:
    st.session_state.requests = []

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Browse Pets", "Adoption Request", "Admin Dashboard"]
)

if page == "Home":
    st.subheader("Welcome to our Pet Adoption Center ❤️")
    st.write(
        "Give a loving animal a forever home. "
        "Browse available pets and submit an adoption request."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Pets Listed", len(st.session_state.pets))
    col2.metric("Adoption Requests", len(st.session_state.requests))
    col3.metric(
        "Pet Types",
        len(set(p["type"] for p in st.session_state.pets))
    )

    st.info("Visit Browse Pets to meet your new companion!")

elif page == "Browse Pets":
    st.subheader("Meet Our Pets")

    pet_type = st.selectbox(
        "Filter by animal",
        ["All", "Dog", "Cat", "Rabbit", "Bird", "Other"]
    )

    pets = [
        p for p in st.session_state.pets
        if pet_type == "All" or p["type"] == pet_type
    ]

    if not pets:
        st.info("No pets found in this category.")
    else:
        cols = st.columns(2)
        for i, pet in enumerate(pets):
            with cols[i % 2]:
                with st.container(border=True):
                    st.subheader(f"🐾 {pet['name']}")
                    st.write(f"**Animal:** {pet['type']}")
                    st.write(f"**Age:** {pet['age']} year(s)")
                    st.write(pet["description"])
                    st.caption(
                        "To apply, open the Adoption Request page."
                    )

elif page == "Adoption Request":
    st.subheader("Apply to Adopt a Pet")

    if not st.session_state.pets:
        st.info("There are currently no pets listed.")
    else:
        with st.form("adoption_form"):
            applicant = st.text_input("Your full name")
            email = st.text_input("Email address")
            selected_pet = st.selectbox(
                "Choose a pet",
                [p["name"] for p in st.session_state.pets]
            )
            reason = st.text_area(
                "Why would you like to adopt this pet?"
            )
            submitted = st.form_submit_button("Submit Request")

            if submitted:
                if not applicant.strip() or not email.strip():
                    st.error("Please enter your name and email.")
                elif "@" not in email or "." not in email.split("@")[-1]:
                    st.error("Please enter a valid email address.")
                elif not reason.strip():
                    st.error("Please explain why you want to adopt.")
                else:
                    st.session_state.requests.append({
                        "Applicant": applicant.strip(),
                        "Email": email.strip(),
                        "Pet": selected_pet,
                        "Reason": reason.strip(),
                        "Date": date.today().isoformat(),
                        "Status": "Pending"
                    })
                    st.success(
                        f"Your request for {selected_pet} has been submitted!"
                    )

elif page == "Admin Dashboard":
    st.subheader("Adoption Management Dashboard")
    st.warning(
        "Demo only: this dashboard has no administrator login. "
        "Do not enter real applicant information in this public demo."
    )

    if not st.session_state.requests:
        st.info("No adoption requests have been submitted in this session.")
    else:
        st.dataframe(
            st.session_state.requests,
            use_container_width=True
        )

    st.subheader("Add a Pet")

    with st.form("add_pet_form"):
        name = st.text_input("Pet name")
        animal = st.selectbox(
            "Animal type",
            ["Dog", "Cat", "Rabbit", "Bird", "Other"]
        )
        age = st.number_input("Age in years", min_value=0, max_value=50)
        description = st.text_area("Description")
        add = st.form_submit_button("Add Pet")

        if add:
            if not name.strip():
                st.error("Please enter the pet's name.")
            elif any(
                p["name"].lower() == name.strip().lower()
                for p in st.session_state.pets
            ):
                st.error("A pet with this name already exists.")
            else:
                st.session_state.pets.append({
                    "name": name.strip(),
                    "type": animal,
                    "age": int(age),
                    "description": description.strip()
                })
                st.success(f"{name.strip()} added successfully!")
                st.rerun()

st.divider()
st.caption("Pet Adoption Management System | Streamlit Edition")
