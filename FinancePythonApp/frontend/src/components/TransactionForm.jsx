import { useState } from 'react'

const CATEGORIES = [
  'Зарплата', 'Подработка', 'Подарок',
  'Еда', 'Транспорт', 'Жильё', 'Развлечения', 'Связь', 'Другое'
]

function TransactionForm({ onSubmit }) {
  const [form, setForm] = useState({
    type: 'expense',
    amount: '',
    category: 'Еда',
    description: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.amount || form.amount <= 0) return

    onSubmit({ ...form, amount: parseFloat(form.amount) })
    setForm({ type: 'expense', amount: '', category: 'Еда', description: '' })
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Новая транзакция</h3>
      <form onSubmit={handleSubmit}>
        <div style={styles.typeToggle}>
          <button
            type="button"
            onClick={() => setForm({ ...form, type: 'income' })}
            style={{
              ...styles.toggleBtn,
              background: form.type === 'income' ? '#4caf50' : '#e0e0e0',
              color: form.type === 'income' ? 'white' : '#666',
            }}
          >
            💰 Доход
          </button>
          <button
            type="button"
            onClick={() => setForm({ ...form, type: 'expense' })}
            style={{
              ...styles.toggleBtn,
              background: form.type === 'expense' ? '#f44336' : '#e0e0e0',
              color: form.type === 'expense' ? 'white' : '#666',
            }}
          >
            💸 Расход
          </button>
        </div>

        <input
          type="number"
          placeholder="Сумма"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
          required
          min="0.01"
          step="0.01"
          style={styles.input}
        />

        <select
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
          style={styles.input}
        >
          {CATEGORIES.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Описание (необязательно)"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          style={styles.input}
        />

        <button type="submit" style={styles.submitBtn}>
          Добавить
        </button>
      </form>
    </div>
  )
}

const styles = {
  container: {
    background: 'white',
    borderRadius: 12,
    padding: 20,
    boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
  },
  title: {
    marginTop: 0,
    marginBottom: 15,
  },
  typeToggle: {
    display: 'flex',
    gap: 10,
    marginBottom: 15,
  },
  toggleBtn: {
    flex: 1,
    padding: 10,
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: 14,
    transition: 'all 0.2s',
  },
  input: {
    width: '100%',
    padding: 10,
    border: '2px solid #e0e0e0',
    borderRadius: 6,
    fontSize: 14,
    marginBottom: 10,
    boxSizing: 'border-box',
  },
  submitBtn: {
    width: '100%',
    padding: 12,
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: 6,
    fontSize: 16,
    fontWeight: 'bold',
    cursor: 'pointer',
  },
}

export default TransactionForm
