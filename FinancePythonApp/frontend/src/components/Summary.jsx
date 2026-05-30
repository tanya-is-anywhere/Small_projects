function Summary({ transactions }) {
  const totalIncome = transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + Number(t.amount), 0)

  const totalExpense = transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + Number(t.amount), 0)

  const balance = totalIncome - totalExpense

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>📊 Сводка</h3>
      <div style={styles.grid}>
        <div style={{ ...styles.card, background: '#e8f5e9' }}>
          <p style={styles.label}>Доходы</p>
          <p style={{ ...styles.amount, color: '#2e7d32' }}>+{totalIncome.toFixed(2)} ₽</p>
        </div>
        <div style={{ ...styles.card, background: '#fce4ec' }}>
          <p style={styles.label}>Расходы</p>
          <p style={{ ...styles.amount, color: '#c62828' }}>-{totalExpense.toFixed(2)} ₽</p>
        </div>
        <div style={{ ...styles.card, background: balance >= 0 ? '#e3f2fd' : '#fff3e0' }}>
          <p style={styles.label}>Баланс</p>
          <p style={{ ...styles.amount, color: balance >= 0 ? '#1565c0' : '#e65100' }}>
            {balance >= 0 ? '+' : ''}{balance.toFixed(2)} ₽
          </p>
        </div>
      </div>
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
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 10,
  },
  card: {
    padding: 15,
    borderRadius: 8,
    textAlign: 'center',
  },
  label: {
    margin: 0,
    fontSize: 14,
    color: '#666',
  },
  amount: {
    margin: '5px 0 0 0',
    fontSize: 20,
    fontWeight: 'bold',
  },
}

export default Summary
