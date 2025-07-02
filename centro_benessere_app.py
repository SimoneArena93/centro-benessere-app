from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date, time
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file db_access.env
load_dotenv()

# Configurazione database PostgreSQL
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionClass = sessionmaker(bind=engine)
Base = declarative_base()

# === DEFINIZIONE MODELLI (TABELLE) ===

class Cliente(Base):
    __tablename__ = 'cliente'
    
    idcliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cognome = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    
    # Relazioni
    prenotazioni = relationship("Prenotazione", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente(id={self.idcliente}, nome='{self.nome}', cognome='{self.cognome}')>"

class Dipendente(Base):
    __tablename__ = 'dipendente'
    
    iddipendente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cognome = Column(String(50), nullable=False)
    ruolo = Column(String(50), nullable=False)
    
    # Relazioni
    prenotazioni = relationship("Prenotazione", back_populates="dipendente")
    
    def __repr__(self):
        return f"<Dipendente(id={self.iddipendente}, nome='{self.nome}', ruolo='{self.ruolo}')>"

class Servizio(Base):
    __tablename__ = 'servizio'
    
    idservizio = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    prezzo = Column(Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f"<Servizio(id={self.idservizio}, nome='{self.nome}', prezzo={self.prezzo})>"

class Prenotazione(Base):
    __tablename__ = 'prenotazione'
    
    idprenotazione = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    ora = Column(Time, nullable=False)
    stato = Column(String(20), nullable=False)
    idcliente = Column(Integer, ForeignKey('cliente.idcliente'), nullable=False)
    iddipendente = Column(Integer, ForeignKey('dipendente.iddipendente'), nullable=False)
    
    # Relazioni
    cliente = relationship("Cliente", back_populates="prenotazioni")
    dipendente = relationship("Dipendente", back_populates="prenotazioni")
    
    def __repr__(self):
        return f"<Prenotazione(id={self.idprenotazione}, data={self.data}, stato='{self.stato}')>"

class Prodotto(Base):
    __tablename__ = 'prodotto'
    
    idprodotto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    prezzo = Column(Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f"<Prodotto(id={self.idprodotto}, nome='{self.nome}', prezzo={self.prezzo})>"

# === CLASSE PRINCIPALE DELL'APPLICAZIONE ===

class CentroBenessereApp:
    def __init__(self):
        self.session = SessionClass()
        print("Applicazione Centro Benessere avviata con PostgreSQL!")
    
    def __del__(self):
        self.session.close()
    
    # === OPERAZIONI CREATE (Inserimento) ===
    
    def crea_cliente(self, nome, cognome, telefono):
        """Crea un nuovo cliente"""
        nuovo_cliente = Cliente(nome=nome, cognome=cognome, telefono=telefono)
        self.session.add(nuovo_cliente)
        self.session.commit()
        print(f"Cliente creato: {nuovo_cliente}")
        return nuovo_cliente
    
    def crea_dipendente(self, nome, cognome, ruolo):
        """Crea un nuovo dipendente"""
        nuovo_dipendente = Dipendente(nome=nome, cognome=cognome, ruolo=ruolo)
        self.session.add(nuovo_dipendente)
        self.session.commit()
        print(f"Dipendente creato: {nuovo_dipendente}")
        return nuovo_dipendente
    
    def crea_servizio(self, nome, prezzo):
        """Crea un nuovo servizio"""
        nuovo_servizio = Servizio(nome=nome, prezzo=prezzo)
        self.session.add(nuovo_servizio)
        self.session.commit()
        print(f"Servizio creato: {nuovo_servizio}")
        return nuovo_servizio
    
    def crea_prenotazione(self, data, ora, stato, idcliente, iddipendente):
        """Crea una nuova prenotazione"""
        nuova_prenotazione = Prenotazione(
            data=data, ora=ora, stato=stato,
            idcliente=idcliente, iddipendente=iddipendente
        )
        self.session.add(nuova_prenotazione)
        self.session.commit()
        print(f"Prenotazione creata: {nuova_prenotazione}")
        return nuova_prenotazione
    
    def crea_prodotto(self, nome, prezzo):
        """Crea un nuovo prodotto"""
        nuovo_prodotto = Prodotto(nome=nome, prezzo=prezzo)
        self.session.add(nuovo_prodotto)
        self.session.commit()
        print(f"Prodotto creato: {nuovo_prodotto}")
        return nuovo_prodotto
    
    # === OPERAZIONI READ (Lettura) ===
    
    def leggi_tutti_clienti(self):
        """Legge tutti i clienti"""
        clienti = self.session.query(Cliente).all()
        print(f"Trovati {len(clienti)} clienti:")
        for cliente in clienti:
            print(f"  {cliente}")
        return clienti
    
    def leggi_cliente_per_id(self, idcliente):
        """Legge un cliente specifico per ID"""
        cliente = self.session.query(Cliente).filter(Cliente.idcliente == idcliente).first()
        if cliente:
            print(f"Cliente trovato: {cliente}")
        else:
            print(f"Cliente con ID {idcliente} non trovato")
        return cliente
    
    def leggi_prenotazioni_cliente(self, idcliente):
        """Legge tutte le prenotazioni di un cliente"""
        prenotazioni = self.session.query(Prenotazione).filter(
            Prenotazione.idcliente == idcliente
        ).all()
        print(f"Prenotazioni per cliente {idcliente}:")
        for prenotazione in prenotazioni:
            print(f"  {prenotazione}")
        return prenotazioni
    
    def leggi_tutti_servizi(self):
        """Legge tutti i servizi"""
        servizi = self.session.query(Servizio).all()
        print(f"Servizi disponibili ({len(servizi)}):")
        for servizio in servizi:
            print(f"  {servizio}")
        return servizi
    
    def leggi_prenotazioni_per_data(self, data):
        """Legge tutte le prenotazioni per una data specifica"""
        prenotazioni = self.session.query(Prenotazione).filter(
            Prenotazione.data == data
        ).all()
        print(f"Prenotazioni per il {data}:")
        for prenotazione in prenotazioni:
            print(f"  {prenotazione}")
        return prenotazioni
    
    # === OPERAZIONI UPDATE (Aggiornamento) ===
    
    def aggiorna_telefono_cliente(self, idcliente, nuovo_telefono):
        """Aggiorna il telefono di un cliente"""
        cliente = self.session.query(Cliente).filter(Cliente.idcliente == idcliente).first()
        if cliente:
            vecchio_telefono = cliente.telefono
            cliente.telefono = nuovo_telefono
            self.session.commit()
            print(f"Telefono cliente {cliente.nome} {cliente.cognome} aggiornato: {vecchio_telefono} -> {nuovo_telefono}")
            return cliente
        else:
            print(f"Cliente con ID {idcliente} non trovato")
            return None
    
    def aggiorna_stato_prenotazione(self, idprenotazione, nuovo_stato):
        """Aggiorna lo stato di una prenotazione"""
        prenotazione = self.session.query(Prenotazione).filter(
            Prenotazione.idprenotazione == idprenotazione
        ).first()
        if prenotazione:
            vecchio_stato = prenotazione.stato
            prenotazione.stato = nuovo_stato
            self.session.commit()
            print(f"Stato prenotazione {idprenotazione} aggiornato: {vecchio_stato} -> {nuovo_stato}")
            return prenotazione
        else:
            print(f"Prenotazione con ID {idprenotazione} non trovata")
            return None
    
    def aggiorna_prezzo_servizio(self, idservizio, nuovo_prezzo):
        """Aggiorna il prezzo di un servizio"""
        servizio = self.session.query(Servizio).filter(Servizio.idservizio == idservizio).first()
        if servizio:
            vecchio_prezzo = servizio.prezzo
            servizio.prezzo = nuovo_prezzo
            self.session.commit()
            print(f"Prezzo servizio '{servizio.nome}' aggiornato: {vecchio_prezzo} -> {nuovo_prezzo}")
            return servizio
        else:
            print(f"Servizio con ID {idservizio} non trovato")
            return None
    
    # === OPERAZIONI DELETE (Cancellazione) ===
    
    def cancella_cliente(self, idcliente):
        """Cancella un cliente (solo se non ha prenotazioni)"""
        cliente = self.session.query(Cliente).filter(Cliente.idcliente == idcliente).first()
        if cliente:
            # Verifica se ha prenotazioni
            num_prenotazioni = self.session.query(Prenotazione).filter(
                Prenotazione.idcliente == idcliente
            ).count()
            
            if num_prenotazioni > 0:
                print(f"Impossibile cancellare cliente {cliente.nome} {cliente.cognome}: ha {num_prenotazioni} prenotazioni")
                return False
            else:
                self.session.delete(cliente)
                self.session.commit()
                print(f"Cliente {cliente.nome} {cliente.cognome} cancellato")
                return True
        else:
            print(f"Cliente con ID {idcliente} non trovato")
            return False
    
    def cancella_prenotazione(self, idprenotazione):
        """Cancella una prenotazione"""
        prenotazione = self.session.query(Prenotazione).filter(
            Prenotazione.idprenotazione == idprenotazione
        ).first()
        if prenotazione:
            self.session.delete(prenotazione)
            self.session.commit()
            print(f"Prenotazione {idprenotazione} cancellata")
            return True
        else:
            print(f"Prenotazione con ID {idprenotazione} non trovata")
            return False
    
    def cancella_servizio(self, idservizio):
        """Cancella un servizio"""
        servizio = self.session.query(Servizio).filter(Servizio.idservizio == idservizio).first()
        if servizio:
            self.session.delete(servizio)
            self.session.commit()
            print(f"Servizio '{servizio.nome}' cancellato")
            return True
        else:
            print(f"Servizio con ID {idservizio} non trovato")
            return False

def test_connessione():
    """Testa la connessione al database"""
    try:
        engine.connect()
        print("✅ Connessione a PostgreSQL riuscita!")
        return True
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return False

# === FUNZIONE PRINCIPALE DI ESEMPIO ===

def crea_tabelle_se_necessario():
    """Crea le tabelle solo se non esistono"""
    try:
        # Verifica e crea solo le tabelle mancanti
        Base.metadata.create_all(engine)
        print("✅ Verifica tabelle completata (create quelle mancanti)")
    except Exception as e:
        print(f"❌ Errore nella creazione tabelle: {e}")
        return False
    return True

def main():
    """Funzione principale che dimostra l'uso dell'applicazione"""
    
    # Testa la connessione
    if not test_connessione():
        print("Impossibile connettersi al database. Controlla le credenziali nel file .env")
        return
    
    # Crea le tabelle se necessario (non sovrascrive quelle esistenti)
    if not crea_tabelle_se_necessario():
        return
    
    # Crea l'istanza dell'applicazione
    app = CentroBenessereApp()
    
    print("\n=== DEMO OPERAZIONI CRUD ===\n")
    
    # === CREATE (Inserimento dati) ===
    print("1. CREAZIONE DATI:")
    
    # Crea clienti
    cliente1 = app.crea_cliente("Mario", "Rossi", "335-1234567")
    cliente2 = app.crea_cliente("Laura", "Bianchi", "338-7654321")
    
    # Crea dipendenti
    dipendente1 = app.crea_dipendente("Anna", "Verdi", "Estetista")
    dipendente2 = app.crea_dipendente("Paolo", "Neri", "Massaggiatore")
    
    # Crea servizi
    servizio1 = app.crea_servizio("Massaggio Rilassante", 60.00)
    servizio2 = app.crea_servizio("Trattamento Viso", 45.00)
    
    # Crea prodotti
    prodotto1 = app.crea_prodotto("Crema Idratante", 29.99)
    
    # Crea prenotazioni
    prenotazione1 = app.crea_prenotazione(
        date(2025, 6, 15), 
        time(14, 30), 
        "Confermata", 
        cliente1.idcliente, 
        dipendente2.iddipendente
    )
    
    print("\n" + "="*50 + "\n")
    
    # === READ (Lettura dati) ===
    print("2. LETTURA DATI:")
    
    # Leggi tutti i clienti
    app.leggi_tutti_clienti()
    print("")
    
    # Leggi servizi
    app.leggi_tutti_servizi()
    print("")
    
    # Leggi prenotazioni di un cliente
    app.leggi_prenotazioni_cliente(cliente1.idcliente)
    print("")
    
    # Leggi prenotazioni per data
    app.leggi_prenotazioni_per_data(date(2025, 6, 15))
    
    print("\n" + "="*50 + "\n")
    
    # === UPDATE (Aggiornamento dati) ===
    print("3. AGGIORNAMENTO DATI:")
    
    # Aggiorna telefono cliente
    app.aggiorna_telefono_cliente(cliente1.idcliente, "335-9999999")
    
    # Aggiorna stato prenotazione
    app.aggiorna_stato_prenotazione(prenotazione1.idprenotazione, "Completata")
    
    # Aggiorna prezzo servizio
    app.aggiorna_prezzo_servizio(servizio1.idservizio, 65.00)
    
    print("\n" + "="*50 + "\n")
    
    # === DELETE (Cancellazione dati) ===
    print("4. CANCELLAZIONE DATI:")
    
    # Crea un altro cliente per testare la cancellazione
    cliente_test = app.crea_cliente("Test", "Cancellazione", "111-1111111")
    
    # Cancella il cliente di test (dovrebbe funzionare perché non ha prenotazioni)
    app.cancella_cliente(cliente_test.idcliente)
    
    # Prova a cancellare un cliente con prenotazioni (dovrebbe fallire)
    app.cancella_cliente(cliente1.idcliente)
    
    print("\n=== DEMO COMPLETATA ===")

if __name__ == "__main__":
    main()