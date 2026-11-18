import os
from datetime import datetime, timezone
from typing import Generator, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, ForeignKey, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

API_TOKEN = os.getenv("HERMES_API_TOKEN", "")
TENANT_ID = os.getenv("HERMES_TENANT_ID", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hermes-dev.db")
if not API_TOKEN or not TENANT_ID:
    raise RuntimeError("Set HERMES_API_TOKEN and HERMES_TENANT_ID before starting the API.")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(80), index=True)
    company: Mapped[str] = mapped_column(String(180))
    industry: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(254), nullable=True)
    opportunity: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkTask(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(String(240))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(String(240))
    payload: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    decided_by: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    decision_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(80), index=True)
    actor: Mapped[str] = mapped_column(String(120))
    action: Mapped[str] = mapped_column(String(80))
    entity_type: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)
app = FastAPI(title="HERMES Command Center API", version="0.1.0")

allowed_origins = [x.strip() for x in os.getenv("HERMES_ALLOWED_ORIGINS", "").split(",") if x.strip()]
if allowed_origins:
    app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False,
                       allow_methods=["GET", "POST", "PATCH"], allow_headers=["Authorization", "Content-Type"])

def db_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

def authenticate(authorization: str = Header(default="")) -> str:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    import hmac
    if not hmac.compare_digest(token, API_TOKEN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TENANT_ID

class LeadIn(BaseModel):
    company: str = Field(min_length=1, max_length=180)
    industry: Optional[str] = Field(default=None, max_length=120)
    city: Optional[str] = Field(default=None, max_length=120)
    website: Optional[str] = Field(default=None, max_length=500)
    contact_email: Optional[str] = Field(default=None, max_length=254)
    opportunity: Optional[str] = None
    status: str = Field(default="new", pattern="^(new|qualified|contacted|customer|archived)$")

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    description: Optional[str] = None
    status: str = Field(default="open", pattern="^(open|in_progress|done|cancelled)$")

class ApprovalIn(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    payload: str = Field(min_length=1, max_length=20000)

class DecisionIn(BaseModel):
    decision: str = Field(pattern="^(approved|rejected)$")
    actor: str = Field(min_length=1, max_length=120)
    note: Optional[str] = Field(default=None, max_length=4000)

def audit(db: Session, tenant: str, actor: str, action: str, kind: str, entity_id: Optional[int], details: str = "") -> None:
    db.add(AuditLog(tenant_id=tenant, actor=actor, action=action, entity_type=kind,
                    entity_id=str(entity_id) if entity_id is not None else None, details=details[:4000]))

@app.get("/health")
def health():
    return {"status": "ok", "service": "hermes-api"}

@app.get("/api/leads")
def list_leads(tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    return db.scalars(select(Lead).where(Lead.tenant_id == tenant).order_by(Lead.id.desc())).all()

@app.post("/api/leads", status_code=201)
def create_lead(body: LeadIn, tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    item = Lead(tenant_id=tenant, **body.model_dump())
    db.add(item)
    db.flush()
    audit(db, tenant, "api-token", "lead.created", "lead", item.id, item.company)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/tasks")
def list_tasks(tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    return db.scalars(select(WorkTask).where(WorkTask.tenant_id == tenant).order_by(WorkTask.id.desc())).all()

@app.post("/api/tasks", status_code=201)
def create_task(body: TaskIn, tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    item = WorkTask(tenant_id=tenant, **body.model_dump())
    db.add(item)
    db.flush()
    audit(db, tenant, "api-token", "task.created", "task", item.id, item.title)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/approvals")
def list_approvals(tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    return db.scalars(select(Approval).where(Approval.tenant_id == tenant).order_by(Approval.id.desc())).all()

@app.post("/api/approvals", status_code=201)
def create_approval(body: ApprovalIn, tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    item = Approval(tenant_id=tenant, title=body.title, payload=body.payload)
    db.add(item)
    db.flush()
    audit(db, tenant, "api-token", "approval.created", "approval", item.id, item.title)
    db.commit()
    db.refresh(item)
    return item

@app.post("/api/approvals/{approval_id}/decision")
def decide_approval(approval_id: int, body: DecisionIn, tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    item = db.scalar(select(Approval).where(Approval.id == approval_id, Approval.tenant_id == tenant))
    if item is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    if item.status != "pending":
        raise HTTPException(status_code=409, detail="Approval has already been decided")
    item.status = body.decision
    item.decided_by = body.actor
    item.decision_note = body.note
    item.decided_at = datetime.now(timezone.utc)
    audit(db, tenant, body.actor, f"approval.{body.decision}", "approval", item.id, body.note or "")
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/audit")
def list_audit(tenant: str = Depends(authenticate), db: Session = Depends(db_session)):
    return db.scalars(select(AuditLog).where(AuditLog.tenant_id == tenant).order_by(AuditLog.id.desc()).limit(500)).all()
