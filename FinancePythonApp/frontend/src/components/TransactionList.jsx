import { useState } from 'react'

function TransactionList({ transactions, onDelete, onEdit }) {
  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({})

  const sorted = [...transactions].sort((a, b) => new Date(b.date) - new Date(a.date))

  const CATEGORIES = [
    'Зарплата', 'Подработка', 'Подарок',
    'Еда', 'Транспорт', 'Жильё', 'Развлечения', 'Связь', 'Другое'
  ]

  const startEdit = (t) => {
    setEditingId(t.id)
    setEditForm({
      type: t.type,
      amount: t.amount,
      category: t.category,
      description: t.description || ''
    })
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditForm({})
  }

  const saveEdit = () => {
    if (onEdit && editingId) {
      onEdit(editingId, {
        ...editForm,
        amount: parseFloat(editForm.amount)
      })
      setEditingId(null)
      setEditForm({})
    }
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>📋 История транзакций</h3>

      {sorted.length === 0 ? (
        <p style={styles.empty}>Пока нет транзакций. Добавьте первую!</p>
      ) : (
        <div style={styles.scrollArea}>
          <div style={styles.list}>
            {sorted.map(t => (
              <div key={t.id} style={styles.item}>
                {editingId === t.id ? (
                  /* РЕЖИМ РЕДАКТИРОВАНИЯ */
                  <div style={styles.editForm}>
                    <div style={styles.typeToggle}>
                      <button
                        type="button"
                        onClick={() => setEditForm({ ...editForm, type: 'income' })}
                        style={{
                          ...styles.toggleBtn,
                          background: editForm.type === 'income' ? '#4caf50' : '#e0e0e0',
                          color: editForm.type === 'income' ? 'white' : '#666',
                        }}
                      >
                        💰 Доход
                      </button>
                      <button
                        type="button"
                        onClick={() => setEditForm({ ...editForm, type: 'expense' })}
                        style={{
                          ...styles.toggleBtn,
                          background: editForm.type === 'expense' ? '#f44336' : '#e0e0e0',
                          color: editForm.type === 'expense' ? 'white' : '#666',
                        }}
                      >
                        💸 Расход
                      </button>
                    </div>
                    <input
                      type="number"
                      value={editForm.amount}
                      onChange={(e) => setEditForm({ ...editForm, amount: e.target.value })}
                      style={styles.editInput}
                      placeholder="Сумма"
                    />
                    <select
                      value={editForm.category}
                      onChange={(e) => setEditForm({ ...editForm, category: e.target.value })}
                      style={styles.editInput}
                    >
                      {CATEGORIES.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                    <input
                      type="text"
                      value={editForm.description}
                      onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                      style={styles.editInput}
                      placeholder="Описание"
                    />
                    <div style={styles.editButtons}>
                      <button onClick={saveEdit} style={styles.saveBtn}>💾 Сохранить</button>
                      <button onClick={cancelEdit} style={styles.cancelBtn}>❌ Отмена</button>
                    </div>
                  </div>
                ) : (
                  /* ОБЫЧНЫЙ РЕЖИМ */
                  <>
                    <div style={styles.itemLeft}>
                      <span style={styles.icon}>{t.type === 'income' ? '💰' : '💸'}</span>
                      <div>
                        <p style={styles.category}>{t.category}</p>
                        {t.description && <p style={styles.description}>{t.description}</p>}
                        <p style={styles.date}>
                          {new Date(t.date).toLocaleDateString('ru-RU', {
                            day: '2-digit', month: '2-digit', year: 'numeric',
                            hour: '2-digit', minute: '2-digit'
                          })}
                        </p>
                      </div>
                    </div>
                    <div style={styles.itemRight}>
                      <p style={{
                        ...styles.amount,
                        color: t.type === 'income' ? '#2e7d32' : '#c62828'
                      }}>
                        {t.type === 'income' ? '+' : '-'}{Number(t.amount).toFixed(2)} ₽
                      </p>
                      <button onClick={() => startEdit(t)} style={styles.editBtn} title="Редактировать">✎</button>
                      <button onClick={() => onDelete(t.id)} style={styles.deleteBtn} title="Удалить">✕</button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {sorted.length > 0 && (
        <p style={styles.count}>Всего записей: {sorted.length}</p>
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
    display: 'flex',
    flexDirection: 'column',
    height: '476px',
  },
  title: {
    marginTop: 0,
    marginBottom: 15,
    flexShrink: 0,
  },
  scrollArea: {
    flex: 1,
    overflowY: 'auto',
    overflowX: 'hidden',
    maxHeight: '500px',
    paddingRight: 5,
    scrollbarWidth: 'thin',
    scrollbarColor: '#ccc transparent',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
  },
  empty: {
    color: '#999',
    textAlign: 'center',
    padding: 20,
  },
  count: {
    marginTop: 10,
    fontSize: 13,
    color: '#888',
    flexShrink: 0,
  },
  item: {
    padding: 12,
    background: '#f8f9fa',
    borderRadius: 8,
    transition: 'background 0.2s',
  },
  itemLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    flex: 1,
    minWidth: 0,
  },
  icon: {
    fontSize: 24,
    flexShrink: 0,
  },
  category: {
    margin: 0,
    fontWeight: 'bold',
    fontSize: 15,
  },
  description: {
    margin: '2px 0 0 0',
    fontSize: 13,
    color: '#888',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  date: {
    margin: '2px 0 0 0',
    fontSize: 12,
    color: '#aaa',
  },
  itemRight: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    flexShrink: 0,
    marginTop: 8,
  },
  amount: {
    margin: 0,
    fontSize: 18,
    fontWeight: 'bold',
    whiteSpace: 'nowrap',
  },
  editBtn: {
    background: 'none',
    border: '1px solid transparent',
    color: '#667eea',
    fontSize: 18,
    cursor: 'pointer',
    padding: '4px 8px',
    borderRadius: 4,
    transition: 'all 0.2s',
  },
  deleteBtn: {
    background: 'none',
    border: '1px solid transparent',
    color: '#999',
    fontSize: 18,
    cursor: 'pointer',
    padding: '4px 8px',
    borderRadius: 4,
    transition: 'all 0.2s',
  },
  // Стили для режима редактирования
  editForm: {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
  },
  typeToggle: {
    display: 'flex',
    gap: 8,
  },
  toggleBtn: {
    flex: 1,
    padding: 8,
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: 13,
  },
  editInput: {
    padding: 8,
    border: '2px solid #e0e0e0',
    borderRadius: 6,
    fontSize: 14,
  },
  editButtons: {
    display: 'flex',
    gap: 8,
  },
  saveBtn: {
    flex: 1,
    padding: 8,
    background: '#4caf50',
    color: 'white',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  cancelBtn: {
    flex: 1,
    padding: 8,
    background: '#9e9e9e',
    color: 'white',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
  },
}

export default TransactionList
