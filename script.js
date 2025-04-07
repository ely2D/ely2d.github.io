fetch('bills.json')
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector('#bill-table tbody');
    data.forEach(bill => {
      const row = `<tr>
        <td>${bill.date}</td>
        <td>${bill.amount}</td>
        <td>${bill.type}</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  });