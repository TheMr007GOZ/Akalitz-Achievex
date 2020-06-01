from app import app, db
from app.models import Medalla

m1 = Medalla(nombre="Primer paso", descripcion="Obtén tu primer logro")
m2 = Medalla(nombre="Diez seguidos", descripcion="Obtén 10 logros")
m3 = Medalla(nombre="5 x 5", descripcion="Obtén 25 logros")
m4 = Medalla(nombre="L", descripcion="Obtén 50 logros")

db.session.add(m1)
db.session.add(m2)
db.session.add(m3)
db.session.add(m4)

db.session.commit()
