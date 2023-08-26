from fastapi import APIRouter , status , Depends
from fastapi.exceptions import HTTPException
from database import Session, engine 
from schemas import SignUp , Login
from model import User 
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException 

auth_router = APIRouter(
	prefix='/auth',
	tags=['auth']
)

session = Session(bind=engine)

@auth_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
	try:
		Authorize.jwt_required()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
	
	return {'hello to : ':'world'}

@auth_router.post('/signup', response_model=SignUp, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUp):
	db_email = session.query(User).filter(User.email==user.email).first()

	if db_email is not None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		       detail='User with this email already exists.'
			   ) 
	
	db_username= session.query(User).filter(User.username==user.username).first()

	if db_username is not None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		       detail='User with this username already exists.'
			   ) 
	
	new_user = User(
		username = user.username,
		email = user.email,
		password = generate_password_hash(user.password),
		is_staff = user.is_staff,
		is_active = user.is_active
	)

	session.add(new_user)
	session.commit()

	return new_user

@auth_router.post('/login', status_code=200)
async def login(user:Login, Authorize:AuthJWT=Depends()):
	db_user = session.query(User).filter(User.username==user.username).first()

	if db_user and check_password_hash(db_user.password, user.password):
		access_token = Authorize.create_access_token(subject=db_user.username)
		refresh_token = Authorize.create_refresh_token(subject=db_user.username)

		responses = {
			'access':access_token,
			'refresh':refresh_token
		}	

		return jsonable_encoder(responses)
	
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Username or password is invalid.')

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
	try:
		Authorize.jwt_refresh_token_required()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please provide a valid refresh token')
	
	current_user = Authorize.get_jwt_subject()
	access_token = Authorize.create_access_token(subject=current_user)

	return jsonable_encoder({'access':access_token})