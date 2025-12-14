import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/sweets/api/sweets";

export default function Sweets() {
  const [sweets, setSweets] = useState([]);
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
  });

  const token = localStorage.getItem("token");

  // Load sweets
  useEffect(() => {
    fetch(API_URL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setSweets(data))
      .catch(() => alert("Failed to load sweets"));
  }, []);

  // Add sweet
  const addSweet = async () => {
    if (!form.name || !form.category || !form.price || !form.quantity) {
      alert("Fill all fields");
      return;
    }

    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: form.name,
        category: form.category,
        price: Number(form.price),
        quantity: Number(form.quantity),
      }),
    });

    if (!res.ok) {
      alert("Failed to add sweet");
      return;
    }

    const newSweet = await res.json();
    setSweets([...sweets, newSweet]);

    setForm({ name: "", category: "", price: "", quantity: "" });
  };

  return (
    <div className="page">
      <h2>🍬 Sweet Shop</h2>

      <div className="card">
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          placeholder="Category"
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
        />
        <input
          placeholder="Price"
          type="number"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })}
        />
        <input
          placeholder="Quantity"
          type="number"
          value={form.quantity}
          onChange={(e) => setForm({ ...form, quantity: e.target.value })}
        />
        <button onClick={addSweet}>Add Sweet</button>
      </div>

      <div className="grid">
        {sweets.map((s) => (
          <div className="sweet-card" key={s.id}>
            <h3>{s.name}</h3>
            <p>{s.category}</p>
            <p>₹{s.price}</p>
            <p>Qty: {s.quantity}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

