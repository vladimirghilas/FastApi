from database import engine

with engine.connect() as connection:
    result = connection.execute("SELECT 1")
    print("Conexiunea funcționează, test:", result.scalar())