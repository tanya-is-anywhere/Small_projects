import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios.jsx'
import Summary from '../components/Summary'
import TransactionForm from '../components/TransactionForm'
import TransactionList from '../components/TransactionList'
import MonthlyReport from '../components/MonthlyReport'

function Dashboard() {
  const [transactions, setTransactions] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    fetchTransactions()
  }, [])

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/transactions/')
      setTransactions(response.data)
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('token')
        navigate('/login')
      }
    }
  }

  const handleAdd = async (data) => {
    try {
      await api.post('/transactions/', data)
      fetchTransactions()
    } catch (err) {
      alert('Ошибка при добавлении транзакции')
    }
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/transactions/${id}`)
      fetchTransactions()
    } catch (err) {
      alert('Ошибка при удалении')
    }
  }
  const handleEdit = async (id, data) => {
  try {
    await api.put(`/transactions/${id}`, data)
    fetchTransactions()
  } catch (err) {
    alert('Ошибка при редактировании')
  }
}

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Учёт финансов</h1>
        <button onClick={handleLogout} style={styles.logoutBtn}>Выйти</button>
      </div>

      <div style={styles.content}>
        <div style={styles.leftColumn}>
          <Summary transactions={transactions} />
          <TransactionForm onSubmit={handleAdd} />
        </div>
        <div style={styles.rightColumn}>
          <TransactionList transactions={transactions} onDelete={handleDelete} onEdit={handleEdit} />
        </div>
      </div>
      <MonthlyReport />
    </div>
  )
}

const styles = {
  container: {
    maxWidth: 1200,
    margin: '0 auto',
    padding: 20,
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 30,
    padding: '0 20px',
  },
  title: {
    fontSize: 28,
    margin: 0,
  },
  logoutBtn: {
    padding: '8px 20px',
    background: '#ff4757',
    color: 'white',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  content: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 20,
  },
  leftColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: 20,
  },
  rightColumn: {},
  '@media (maxWidth: 768px)': {
    content: {
      gridTemplateColumns: '1fr',
    },
  },
}

export default Dashboard
