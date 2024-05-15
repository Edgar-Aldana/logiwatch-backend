from sqlalchemy import Column, String, Integer, Date, DateTime, exc
from datetime import datetime
from ...database_connection import session, Base

class Monitoristas(Base):
    
    __tablename__ = "Monitoristas"
    __table_args__ = {"schema": "AUTH"}

    correo = Column(String(255), primary_key=True)
    password = Column(String(255))
    idEmpleado = Column(Integer)

    nombres = Column(String(255))
    apellidoPaterno = Column(String(255))
    apellidoMaterno = Column(String(255))

    telefono = Column(String(20))
    region = Column(String(100))
    fechaRegistro = Column(DateTime, default=datetime.now())


    def find(**kwargs):
        try:
            return session.query(Monitoristas).filter_by(**kwargs).all()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()
            

    def create(**request):
        try:       
            user = Monitoristas(**request)
            session.add(user)
            session.commit()
            return user
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}
        
        
    def updated(**update) -> int:
        try:  
    
            updated = (
                session.query(Monitoristas)
                .filter_by(correo=str(update["correo"]))
                .update(update, synchronize_session="fetch")
            )
            session.commit()
            return updated
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}
    

    def delete(**kwargs) -> int:
        try:        
            updated = (
                session.query(Monitoristas)
                .filter_by(**kwargs)
                .update(
                    {"active": False, "deleteAt": datetime.now()},
                    synchronize_session="fetch",
                )
            )
            session.commit()
            return updated
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}
        


        

class Conductores(Base):
    
    __tablename__ = "Conductores"
    __table_args__ = {"schema": "AUTH"}

    
    idConductor = Column(Integer, primary_key=True)

    nombres = Column(String(255))
    apellidoPaterno = Column(String(255))
    apellidoMaterno = Column(String(255))

    telefono = Column(String(20))
    matricula = Column(String(20))
    region = Column(String(100))
    fechaRegistro = Column(DateTime, default=datetime.now())



