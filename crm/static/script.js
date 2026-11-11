document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== toggle && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  document.querySelectorAll('[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      if (!window.confirm(form.getAttribute('data-confirm'))) {
        e.preventDefault();
      }
    });
  });

  const lineItemsWrap = document.getElementById('lineItems');
  const addLineBtn = document.getElementById('addLineItem');
  if (lineItemsWrap && addLineBtn) {
    const products = window.PRODUCTS || [];

    const buildRow = (data) => {
      data = data || {};
      const row = document.createElement('div');
      row.className = 'line-item-row';

      const productOptions = ['<option value="">Custom item</option>']
        .concat(products.map(p => `<option value="${p.id}" data-price="${p.unit_price}"${String(data.product_id) === String(p.id) ? ' selected' : ''}>${p.name}</option>`))
        .join('');

      row.innerHTML = `
        <input type="text" name="line_description[]" placeholder="Description" value="${data.description || ''}" required>
        <select name="line_product_id[]" class="line-product">${productOptions}</select>
        <input type="number" name="line_qty[]" min="0" step="1" placeholder="Qty" value="${data.qty || 1}">
        <input type="number" name="line_price[]" min="0" step="0.01" placeholder="Unit price" value="${data.unit_price || 0}">
        <button type="button" class="btn btn-ghost btn-sm remove-line">&times;</button>
      `;

      row.querySelector('.remove-line').addEventListener('click', () => row.remove());
      row.querySelector('.line-product').addEventListener('change', (e) => {
        const opt = e.target.selectedOptions[0];
        const price = opt ? opt.getAttribute('data-price') : null;
        if (price) row.querySelector('[name="line_price[]"]').value = price;
      });

      return row;
    };

    addLineBtn.addEventListener('click', () => lineItemsWrap.appendChild(buildRow()));

    const existing = window.EXISTING_LINE_ITEMS || [];
    if (existing.length) {
      existing.forEach(item => lineItemsWrap.appendChild(buildRow(item)));
    } else {
      lineItemsWrap.appendChild(buildRow());
    }
  }
});
