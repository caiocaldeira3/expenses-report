from app.parsing.methods import parse_expense
from app.user.methods import ensure_profile

user = ensure_profile()
exp = parse_expense("primeira_conta.jpeg", user)
