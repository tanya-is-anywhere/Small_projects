from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Transaction
from app import db

auth_bp = Blueprint('auth', __name__)
transactions_bp = Blueprint('transactions', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401


@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = int(get_jwt_identity())
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    return jsonify([{
        'id': t.id, 'type': t.type, 'amount': t.amount,
        'category': t.category, 'description': t.description,
        'date': t.date.isoformat()
    } for t in transactions]), 200


@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({'error': 'No JSON data received'}), 422

    if 'type' not in data or 'amount' not in data:
        return jsonify({'error': 'Missing required fields'}), 422

    if data['type'] not in ['income', 'expense']:
        return jsonify({'error': 'Type must be income or expense'}), 422

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 422
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount'}), 422

    transaction = Transaction(
        user_id=user_id,
        type=data['type'],
        amount=amount,
        category=data.get('category', 'Другое'),
        description=data.get('description', '')
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'message': 'Transaction created',
        'id': transaction.id,
        'type': transaction.type,
        'amount': float(transaction.amount),
        'category': transaction.category
    }), 201


@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = int(get_jwt_identity())

    # Находим транзакцию
    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=user_id
    ).first()

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted'}), 200


@transactions_bp.route('/report/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def monthly_report(year, month):
    user_id = int(get_jwt_identity())

    # Получаем все транзакции за указанный месяц
    from datetime import datetime
    start_date = datetime(year, month, 1)
    # Последний день месяца
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).all()

    # Считаем доходы и расходы по категориям
    income_by_category = {}
    expense_by_category = {}
    total_income = 0
    total_expense = 0

    for t in transactions:
        if t.type == 'income':
            total_income += t.amount
            income_by_category[t.category] = income_by_category.get(t.category, 0) + t.amount
        else:
            total_expense += t.amount
            expense_by_category[t.category] = expense_by_category.get(t.category, 0) + t.amount

    return jsonify({
        'year': year,
        'month': month,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'transaction_count': len(transactions),
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category
    }), 200


@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    user_id = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({'error': 'No data provided'}), 422

    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=user_id
    ).first()

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    # Обновляем поля
    if 'type' in data and data['type'] in ['income', 'expense']:
        transaction.type = data['type']
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be positive'}), 422
            transaction.amount = amount
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount'}), 422
    if 'category' in data:
        transaction.category = data['category']
    if 'description' in data:
        transaction.description = data['description']

    db.session.commit()

    return jsonify({
        'message': 'Transaction updated',
        'id': transaction.id,
        'type': transaction.type,
        'amount': float(transaction.amount),
        'category': transaction.category,
        'description': transaction.description
    }), 200
