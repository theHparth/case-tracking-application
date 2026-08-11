from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import UserOut, UserCreate, CaseCreate, CaseUpdate, CaseOut
from app.auth import verify_password, create_access_token, get_current_user, require_admin, hash_password
app = FastAPI(title="Case Tracking API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserOut)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin),
):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password),
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




def get_case_or_404(case_id: int, db: Session) -> models.Case:
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return case


def check_owner_or_admin(case: models.Case, current_user: models.User):
    if case.created_by != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to access this case")
    
    
@app.post("/cases", response_model=CaseOut, status_code=status.HTTP_201_CREATED)
def create_case(
    case: CaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_case = models.Case(
        title=case.title,
        description=case.description,
        created_by=current_user.id,
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case


@app.get("/cases", response_model=list[CaseOut])
def list_cases(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Case)
    if current_user.role != models.UserRole.admin:
        query = query.filter(models.Case.created_by == current_user.id)
    return query.all()


@app.get("/cases/{case_id}", response_model=CaseOut)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    case = get_case_or_404(case_id, db)
    check_owner_or_admin(case, current_user)
    return case


@app.put("/cases/{case_id}", response_model=CaseOut)
def update_case(
    case_id: int,
    updates: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    case = get_case_or_404(case_id, db)
    check_owner_or_admin(case, current_user)

    if updates.title is not None:
        case.title = updates.title
    if updates.description is not None:
        case.description = updates.description

    db.commit()
    db.refresh(case)
    return case


@app.patch("/cases/{case_id}/close", response_model=CaseOut)
def close_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    case = get_case_or_404(case_id, db)
    check_owner_or_admin(case, current_user)

    case.status = models.CaseStatus.closed
    db.commit()
    db.refresh(case)
    return case