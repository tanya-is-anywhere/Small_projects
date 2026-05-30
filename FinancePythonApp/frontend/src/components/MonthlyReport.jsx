import { useState } from 'react'
import api from '../api/axios.jsx'

function MonthlyReport() {
  const now = new Date()
  const [year, setYear] = useState(now.getFullYear())
  const [month, setMonth] = useState(now.getMonth() + 1)
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ]

  const fetchReport = async () => {
    setLoading(true)
    setError('')
    setReport(null)

    try {
      const response = await api.get(`/transactions/report/${year}/${month}`)
      setReport(response.data)
    } catch (err) {
      setError('Не удалось загрузить отчёт')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Финансовый отчёт</h3>

      <div style={styles.controls}>
        <select value={year} onChange={(e) => setYear(Number(e.target.value))} style={styles.select}>
          {[2024, 2025, 2026, 2027, 2028].map(y => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>

        <select value={month} onChange={(e) => setMonth(Number(e.target.value))} style={styles.select}>
          {months.map((name, i) => (
            <option key={i} value={i + 1}>{name}</option>
          ))}
        </select>

        <button onClick={fetchReport} disabled={loading} style={styles.btn}>
          {loading ? '⏳ Загрузка...' : '📊 Сформировать отчёт'}
        </button>
      </div>

      {error && <p style={styles.error}>{error}</p>}

      {report && (
        <div style={styles.report}>
          <div style={styles.summary}>
            <div style={{ ...styles.card, background: '#e8f5e9' }}>
              <p style={styles.label}>Доходы</p>
              <p style={{ ...styles.amount, color: '#2e7d32' }}>+{report.total_income.toFixed(2)} ₽</p>
            </div>
            <div style={{ ...styles.card, background: '#fce4ec' }}>
              <p style={styles.label}>Расходы</p>
              <p style={{ ...styles.amount, color: '#c62828' }}>-{report.total_expense.toFixed(2)} ₽</p>
            </div>
            <div style={{ ...styles.card, background: report.balance >= 0 ? '#e3f2fd' : '#fff3e0' }}>
              <p style={styles.label}>Баланс</p>
              <p style={{ ...styles.amount, color: report.balance >= 0 ? '#1565c0' : '#e65100' }}>
                {report.balance >= 0 ? '+' : ''}{report.balance.toFixed(2)} ₽
              </p>
            </div>
          </div>

          <p style={styles.count}>Всего операций: {report.transaction_count}</p>

          <div style={styles.categories}>
            <div>
              <h4 style={styles.subtitle}>📈 Доходы по категориям</h4>
              {Object.entries(report.income_by_category).length === 0 ? (
                <p style={styles.empty}>Нет доходов</p>
              ) : (
                Object.entries(report.income_by_category).map(([cat, sum]) => (
                  <div key={cat} style={styles.row}>
                    <span>{cat}</span>
                    <span style={{ color: '#2e7d32', fontWeight: 'bold' }}>+{sum.toFixed(2)} ₽</span>
                  </div>
                ))
              )}
            </div>

            <div>
              <h4 style={styles.subtitle}>📉 Расходы по категориям</h4>
              {Object.entries(report.expense_by_category).length === 0 ? (
                <p style={styles.empty}>Нет расходов</p>
              ) : (
                Object.entries(report.expense_by_category).map(([cat, sum]) => (
                  <div key={cat} style={styles.row}>
                    <span>{cat}</span>
                    <span style={{ color: '#c62828', fontWeight: 'bold' }}>-{sum.toFixed(2)} ₽</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    background: 'white',
    borderRadius: 12,
    padding: 20,
    boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
    marginTop: 20,
  },
  title: {
    marginTop: 0,
    marginBottom: 15,
  },
  controls: {
    display: 'flex',
    gap: 10,
    marginBottom: 15,
    flexWrap: 'wrap',
  },
  select: {
    padding: 8,
    border: '2px solid #e0e0e0',
    borderRadius: 6,
    fontSize: 14,
  },
  btn: {
    padding: '8px 20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  error: {
    color: '#c00',
    textAlign: 'center',
  },
  report: {
    marginTop: 15,
  },
  summary: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 10,
    marginBottom: 15,
  },
  card: {
    padding: 15,
    borderRadius: 8,
    textAlign: 'center',
  },
  label: {
    margin: 0,
    fontSize: 13,
    color: '#666',
  },
  amount: {
    margin: '5px 0 0 0',
    fontSize: 18,
    fontWeight: 'bold',
  },
  count: {
    color: '#666',
    marginBottom: 15,
  },
  categories: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 20,
  },
  subtitle: {
    marginTop: 0,
    marginBottom: 10,
  },
  row: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '5px 0',
    borderBottom: '1px solid #f0f0f0',
  },
  empty: {
    color: '#999',
    fontSize: 14,
  },
}

export default MonthlyReport