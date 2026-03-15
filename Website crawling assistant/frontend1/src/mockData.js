export function generateMockTests(pageCount) {
  const categories = [
    { label: 'Input Torture',     color: '#f59e0b', bg: 'rgba(245,158,11,0.12)'  },
    { label: 'Boundary Values',   color: '#00cfff', bg: 'rgba(0,207,255,0.12)'   },
    { label: 'State Transitions', color: '#818cf8', bg: 'rgba(129,140,248,0.12)' },
    { label: 'Navigation Chaos',  color: '#22d3a0', bg: 'rgba(34,211,160,0.12)'  },
    { label: 'Mode Switching',    color: '#f43f5e', bg: 'rgba(244,63,94,0.12)'   },
    { label: 'Error Recovery',    color: '#60a5fa', bg: 'rgba(96,165,250,0.12)'  },
  ]
  const goals = [
    'Verify form resets after submission failure',
    'Test XSS injection in search field',
    'Validate max-length boundary on email input',
    'Confirm navigation after session timeout',
    'Verify dropdown resets on page refresh',
    'Test multi-step form abandonment recovery',
    'Validate required fields with whitespace-only input',
    'Confirm proper error on invalid date format',
    'Test tab-order accessibility across form fields',
    'Verify back button preserves form state',
    'Test concurrent form submission',
    'Validate paste handling in number-only fields',
    'Verify autocomplete disabled on password fields',
    'Confirm ARIA labels match visible labels',
    'Test network-error fallback message display',
  ]

  const count = Math.min(Math.max(pageCount * 3, 10), 57)

  return Array.from({ length: count }, (_, i) => {
    const cat      = categories[i % categories.length]
    const stepCount = 3 + (i % 4)
    return {
      id:            `TC-${String(i + 1).padStart(3, '0')}`,
      goal:          goals[i % goals.length],
      category:      cat.label,
      categoryColor: cat.color,
      categoryBg:    cat.bg,
      steps:         stepCount,
      status:        'pending',
    }
  })
}

export function simulateExecution(tests) {
  return tests.map((t, i) => ({
    ...t,
    status:   i % 11 === 0 ? 'failed' : 'passed',
    duration: (1.2 + Math.random() * 3.5).toFixed(1) + 's',
    error:    i % 11 === 0 ? 'Element not found: selector timeout >30s' : null,
  }))
}
