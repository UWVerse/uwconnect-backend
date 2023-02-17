from faker import Faker
fake = Faker()

first_name = fake.first_name_male() if gender =="M" else fake.first_name_female()
last_name = fake.last_name()

output.append(
    {
     "First name": first_name,
     "Last Name": last_name,
     "E-mail": f"{first_name}.{last_name}@{fake.domain_name()}"
    }
)
