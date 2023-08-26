from fastapi import APIRouter , Depends, status 
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT 
from model import User, Order 
from schemas import OrderModel  
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
	prefix='/orders',
	tags=['orders']
)

session = Session(bind=engine)

@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):

	try:
		Authorize.jwt_required()

	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')

	return {'hello':'world'}

# Provide an order
@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel, Authorize:AuthJWT=Depends()):
	try:
		Authorize.jwt_required()

	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
	
	current_user = Authorize.get_jwt_subject()
	user = Session.query(User).filter(User.username==current_user).first() 

	new_order = Order(
		quantity=order.quantity,
		pizza_size=order.pizza_size
	)

	new_order.user = user

	session.add(new_order)
	session.commit()

	response = {
		'quantity' : new_order.quantity,
		'pizza_size': new_order.pizza_size,
		'id':new_order.id ,
		'order_status':new_order.order_status,
	}

	return jsonable_encoder(response)

# Get a list of orders by superusers
@order_router.get('/orders')
async def list_orders(Authorize:AuthJWT=Depends()):

	try:
		Authorize.jwt_required()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
	
	current_user = Authorize.get_jwt_subject()
	user = session.query(User).filter(User.username==current_user).first()

	if user.is_staff:
		orders = session.query(Order).all()
		return jsonable_encoder(orders)
	raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only superusers!.')

#Update an order 
@order_router.put('/order/update/{id}/', status_code=status.HTTP_200_OK)
async def update_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends()):
	try:
		Authorize.jwt_required()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
	
	order_updating = session.query(Order).filter(Order.id==id).first()

	order_updating.quantity = order.quantity 
	order_updating.pizza_size = order.pizza_size 

	session.commit() 

	return jsonable_encoder(order_updating)

# Delete an order 
@order_router.delete('/order/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends()):
	try:
		Authorize.jwt_required()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
	
	order_deleting = session.query(Order).filter(Order.id==id).first()

	session.delete(order_deleting)
	session.commit() 

	return order_deleting

